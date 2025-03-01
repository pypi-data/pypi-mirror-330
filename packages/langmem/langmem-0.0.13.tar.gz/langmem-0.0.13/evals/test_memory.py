import json
from pathlib import Path

import langsmith as ls
import pytest
from langchain.chat_models import init_chat_model
from langgraph.func import entrypoint
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langsmith import testing as t
from pydantic import BaseModel, Field

from langmem import create_memory_store_manager, create_search_memory_tool
from langmem.knowledge.tools import create_manage_memory_tool

HERE = Path(__file__).parent

pytestmark = pytest.mark.anyio


def get_conversations():
    for file in (HERE / "gen" / "data").glob("*.jsonl"):
        all_lines = []
        with open(file) as f:
            for line in f:
                data = json.loads(line)
                if data:
                    all_lines.append(data)
        yield all_lines


class Correctness(BaseModel):
    """Respond with whether the response is correct or incorrect."""

    test_case_index: int
    reasoning: str = Field(description="The reasoning behind the decision.")
    is_correct: bool


class Judgement(BaseModel):
    """Grade the correctness of each response."""

    results: list[Correctness]


@pytest.mark.parametrize("series", get_conversations())
@pytest.mark.parametrize("which", ["manager"])  # , "agent"])
@pytest.mark.langsmith
async def test_extraction(series: list[dict], which: str):
    judge = init_chat_model("openai:o3-mini").with_structured_output(Judgement)
    store = InMemoryStore(
        index={
            "dims": 1536,
            "embed": "openai:text-embedding-3-small",
        }
    )
    if which == "manager":
        manager = create_memory_store_manager("openai:o3-mini", namespace=("memories"))

        @entrypoint(store=store)
        async def manage_memory(state):
            await manager.ainvoke(state)

    elif which == "agent":
        manage_memory = create_react_agent(
            "openai:o3-mini",
            prompt="Save all information from the following conversation worth remembering for later use."
            " Search for similar memories to reconcile and update your memory state. Continue until the the memory state is fully updated.",
            tools=[
                create_search_memory_tool(("memories",)),
                create_manage_memory_tool(("memories",)),
            ],
            store=store,
        )
    else:
        raise ValueError(f"Unsupported memory agent type: {which}")

    responder = create_react_agent(
        "openai:o3-mini",
        prompt="Search your memories to answer the user's questions. Respond with all information you remember relevant to the answer (for high recall).",
        tools=[create_search_memory_tool(("memories",))],
        store=store,
    )

    all_scores = []
    for i, convo in enumerate(series):
        with ls.trace("Convo_" + str(i)):
            await manage_memory.ainvoke({"messages": convo["messages"]})
            final_state = convo["metadata"]["final_state"]["final_attributes"]
            # Soon-to-be-planned because the generator script tends to have some whiplash that translates
            # to narratives like "We plan to grow to xyz in the next Y time" instead of saying that they actually did it already
            questions = [
                f"What's the user's current or soon-to-be-planned {key}?"
                for key in final_state
            ]
            with ls.trace("Evaluate", inputs=final_state) as rt:
                expected = [final_state[key] for key in final_state]
                all_results = await responder.abatch(
                    [{"messages": [{"role": "user", "content": q}]} for q in questions]
                )
                response_values = [
                    str(result["messages"][-1].content) for result in all_results
                ]
                formatted = "\n\n".join(
                    f"""<test_case index={i}>\n\n{q}\n\nExpected: {expected[i]}\n\nResponse: {response_values[i]}\n\n</test_case>"""
                    for i, q in enumerate(questions)
                )
                formatted = f"""Grade the following test cases. Assume the "expected" value is correct.

        {formatted}

        Reason over each result and justify your response. Return a correctness score for all {len(questions)} test cases.
        """
                results = await judge.ainvoke(formatted)
                assert len(results.results) == len(questions)
                round_results = []
                for result in results.results:
                    t.log_feedback(
                        key="correctness",
                        score=result.is_correct,
                        comment=result.reasoning,
                    )
                    round_results.append(result.is_correct)

                all_scores.extend(round_results)
                if round_results:
                    rt.add_outputs({"avg": sum(round_results) / len(round_results)})
    average_score = sum(all_scores) / len(all_scores)
    assert all(all_scores), f"Average score: {average_score}"
