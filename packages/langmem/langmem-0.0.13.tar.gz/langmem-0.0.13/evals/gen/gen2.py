#!/usr/bin/env python3
"""
Synthetic Data Generator for Memory Benchmarking with A Priori Trajectory

This script generates a persona and then pre-computes a “memory trajectory”
(i.e. planned key changes/deltas over conversations and turns). When rolling out
the conversation, at the appropriate conversation and turn the system prompt is
augmented with a subtle hint about what has changed. The LLM is expected to
naturally leak the updated fact; we then confirm leakage using a structured call.

Updates can occur mid‐conversation or between conversations, and their severity
may vary.
"""

import asyncio
import json
import os
import random
import typing
from contextlib import AsyncExitStack
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from langchain.chat_models import init_chat_model
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.func import entrypoint, task
from pydantic import BaseModel, Field
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Configuration, Domains, and Company Contexts
# ---------------------------------------------------------------------------
DOMAINS = {
    "sdr": {
        "service_role": "Sales Development Representative",
        "user_role": "Prospect",
        "verifiable_attributes": {
            "company_size": ["1-10", "11-50", "51-200", "201-500", "501+"],
            "pain_points": [
                "budget constraints",
                "long sales cycles",
                "decision maker access",
                "technical integration",
            ],
            "budget": {"min": 5000, "max": 100000, "unit": "USD"},
        },
        "key_attributes": [
            "company_size",
            "industry",
            "pain_points",
            "budget",
            "timeline",
        ],
        "change_types": ["buying_stage", "priorities", "objections", "team_structure"],
        "relationship_types": ["decision_maker", "champion", "blocker", "influencer"],
        "memory_importance": {
            "buying_stage": 0.9,
            "objections": 0.8,
            "relationships": 0.9,
            "preferences": 0.7,
        },
    },
    # (Other domains omitted for brevity.)
}

COMPANY_CONTEXTS = {
    "sdr": [
        {
            "name": "TechFlow Solutions",
            "description": "B2B SaaS company providing workflow automation software",
            "product": "TechFlow Automation Platform",
            "target_market": "Mid-sized enterprises looking to automate business processes",
            "pricing_model": "Per-user subscription with tiered features",
            "competitors": ["Automation Anywhere", "UiPath", "Blue Prism"],
            "unique_value": "Industry-specific automation templates and no-code workflow builder",
        },
        {
            "name": "SecureStack",
            "description": "Cloud security and compliance platform",
            "product": "SecureStack Enterprise",
            "target_market": "Enterprise companies with complex cloud infrastructure",
            "pricing_model": "Usage-based pricing with annual contracts",
            "competitors": ["Prisma Cloud", "Wiz", "Orca Security"],
            "unique_value": "Real-time threat detection with automated remediation",
        },
    ],
    # (Other domains omitted for brevity.)
}

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
if not FIREWORKS_API_KEY:
    raise ValueError("Please set FIREWORKS_API_KEY environment variable")

# ---------------------------------------------------------------------------
# Model Initialization
# ---------------------------------------------------------------------------
user_model = init_chat_model("accounts/fireworks/models/deepseek-v3")
assistant_model = init_chat_model("openai:o3-mini")


class ConversationStatus(BaseModel):
    reasoning: str = Field(description="Reasoning for conversation progress.")
    status: typing.Literal["in_progress", "completed"] = "in_progress"


did_complete_model = init_chat_model("openai:gpt-4o-mini").with_structured_output(
    ConversationStatus
)


class MemoryConfirmation(BaseModel):
    confirmed: bool = Field(
        ..., description="Whether the memory was confirmed in the output."
    )


did_confirm_model = init_chat_model("openai:gpt-4o-mini").with_structured_output(
    MemoryConfirmation
)


def format_convo(messages: List[Dict[str, str]]) -> str:
    return "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])


# ---------------------------------------------------------------------------
# Data Classes for Memory, Conversation State, and Memory Events
# ---------------------------------------------------------------------------
@dataclass
class Memory:
    content: Any
    importance: float
    first_seen: int
    last_updated: int
    is_active: bool
    category: str
    source_type: str


@dataclass
class ConversationState:
    persona: Dict[str, Any]
    conv_idx: int
    active_memories: List[Memory]
    messages: List[Dict[str, Any]]
    info_leakage: Dict[str, bool]
    noise_ratio: float = 0.2
    current_turn: int = 0
    num_turns: int = 30


@dataclass
class MemoryEvent:
    conv_idx: int
    turn: int
    event_type: str  # "update", "conflict", "delete", "insert"
    attribute: str  # which attribute or category is affected
    old_value: Optional[str]
    new_value: Optional[str]
    severity: float  # 0.0 (slight) to 1.0 (significant)
    reason: str


# ---------------------------------------------------------------------------
# A Priori Memory Trajectory Generation
# ---------------------------------------------------------------------------
def generate_memory_trajectory(
    domain_config: Dict[str, Any],
    base_memories: List[Memory],
    total_convs: int,
    turns_per_conv: int,
    event_probability: float = 0.1,
) -> List[MemoryEvent]:
    """
    Pre-compute a list of memory events (deltas) that will occur over the course
    of total_convs x turns_per_conv. The events are keyed by conversation index and turn.
    """
    trajectory = []
    for conv in range(total_convs):
        for turn in range(1, turns_per_conv):  # skip turn 0 (initial)
            if random.random() < event_probability:
                event_type = random.choices(
                    ["update", "conflict", "delete", "insert"],
                    weights=[0.4, 0.3, 0.15, 0.15],
                )[0]
                # For update/conflict, pick an existing base memory
                if event_type in ("update", "conflict") and base_memories:
                    mem = random.choice(base_memories)
                    attr = mem.content.split(":")[0]  # assume format "attr: value"
                    old_val = mem.content.split(":", 1)[1].strip()
                    if event_type == "update":
                        # For budget, scale it; otherwise, append a suffix.
                        if attr == "budget":
                            try:
                                num = float(old_val.replace("$", "").replace(",", ""))
                                factor = random.uniform(0.9, 1.2)
                                new_val = f"${int(num * factor):,}"
                            except Exception:
                                new_val = old_val + " (upd)"
                        else:
                            new_val = old_val + " (upd)"
                        reason = (
                            f"{attr} updated subtly"
                            if random.random() < 0.5
                            else f"{attr} updated significantly"
                        )
                    else:  # conflict
                        new_val = old_val + "_v2"
                        reason = f"Conflicting info for {attr}"
                    trajectory.append(
                        MemoryEvent(
                            conv_idx=conv,
                            turn=turn,
                            event_type=event_type,
                            attribute=attr,
                            old_value=old_val,
                            new_value=new_val,
                            severity=random.random(),
                            reason=reason,
                        )
                    )
                elif event_type == "delete" and base_memories:
                    mem = random.choice(base_memories)
                    attr = mem.content.split(":")[0]
                    trajectory.append(
                        MemoryEvent(
                            conv_idx=conv,
                            turn=turn,
                            event_type="delete",
                            attribute=attr,
                            old_value=mem.content.split(":", 1)[1].strip(),
                            new_value=None,
                            severity=random.random(),
                            reason=f"{attr} is no longer relevant",
                        )
                    )
                elif event_type == "insert":
                    # For insertion, choose an attribute from a set of possible extras.
                    extras = {
                        "phone": f"+1-555-{random.randint(1000, 9999)}",
                        "email": f"user{random.randint(1, 100)}@example.com",
                        "address": f"{random.randint(100, 999)} Main St",
                        "preference": random.choice(["casual", "formal", "sporty"]),
                    }
                    attr = random.choice(list(extras.keys()))
                    trajectory.append(
                        MemoryEvent(
                            conv_idx=conv,
                            turn=turn,
                            event_type="insert",
                            attribute=attr,
                            old_value=None,
                            new_value=extras[attr],
                            severity=random.random(),
                            reason=f"New info: {attr} added",
                        )
                    )
    return trajectory


# ---------------------------------------------------------------------------
# Dynamic System Prompt Builder
# ---------------------------------------------------------------------------
def build_system_prompt(turn: int, pending_updates: List[str]) -> str:
    prompt = f"Turn {turn}: Continue the conversation naturally."
    if pending_updates:
        prompt += (
            " Note: Since the last message, the following has changed: "
            + "; ".join(pending_updates)
        )
        prompt += ". Please work these details into your response subtly."
    return prompt


# ---------------------------------------------------------------------------
# Memory Confirmation Detection
# ---------------------------------------------------------------------------
async def detect_memory_confirmation(memory: Memory, message: str) -> bool:
    prompt = (
        f"Does the following message naturally confirm that the memory '{memory.content}' "
        f"was mentioned (even implicitly)?\n\nMessage:\n{message}\n\n"
        'Respond with a JSON object: {"confirmed": true} or {"confirmed": false}.'
    )
    try:
        result = await did_confirm_model.ainvoke(prompt, config={"configurable": {}})
        return result.confirmed
    except Exception:
        return memory.content.lower() in message.lower()


# ---------------------------------------------------------------------------
# Conversation Generation: User and Assistant Messages
# ---------------------------------------------------------------------------
@task
async def generate_chat_completion(
    messages: List[Dict[str, str]], temperature: float = 0.6, which_model: str = "user"
) -> str:
    model = user_model if which_model == "user" else assistant_model
    response = str((await model.ainvoke(messages)).content).strip('"')
    return response


@task
async def generate_user_message(state: ConversationState) -> ConversationState:
    domain_config = DOMAINS[state.persona["domain"]]
    profile = state.persona["profile"]
    company = random.choice(
        COMPANY_CONTEXTS.get(state.persona["domain"], [{"name": "Generic Company"}])
    )
    reveal = " ".join([f"{k}: {v}" for k, v in state.persona["attributes"].items()])
    user_context = (
        f"You are {profile['name']}, a {domain_config['user_role']} speaking with a {domain_config['service_role']} "
        f"from {company['name']}. Background: {reveal}. Be natural. (Turn {state.current_turn} of {state.num_turns})"
    )
    system_prompt = build_system_prompt(
        state.current_turn, state.persona.get("pending_updates", [])
    )
    current_messages = [
        {"role": "system", "content": user_context + "\n" + system_prompt}
    ] + state.messages
    response = await generate_chat_completion(
        current_messages, temperature=0.7, which_model="user"
    )
    if state.current_turn > 3 and random.random() < state.noise_ratio:
        noise = random.choice(DOMAIN_NOISE.get(state.persona["domain"], NOISE_SNIPPETS))
        response = (
            f"{noise} {response}" if random.random() < 0.5 else f"{response} {noise}"
        )
    message = {"role": "user", "content": response, "turn": state.current_turn}
    state.messages.append(message)
    # Check confirmation for each pending update (if not yet confirmed)
    for mem in state.active_memories:
        conf = await detect_memory_confirmation(mem, response)
        state.info_leakage[mem.content] = conf
    state.current_turn += 1
    return state


@task
async def generate_assistant_message(state: ConversationState) -> ConversationState:
    domain_config = DOMAINS[state.persona["domain"]]
    profile = state.persona["profile"]
    company = random.choice(
        COMPANY_CONTEXTS.get(state.persona["domain"], [{"name": "Generic Company"}])
    )
    assistant_context = (
        f"You are a {domain_config['service_role']} representing {company['name']}. "
        f"Listen actively and respond with actionable advice. (Turn {state.current_turn})"
    )
    system_prompt = build_system_prompt(
        state.current_turn, state.persona.get("pending_updates", [])
    )
    current_messages = [
        {"role": "system", "content": assistant_context + "\n" + system_prompt}
    ] + state.messages
    response = await generate_chat_completion(
        current_messages, temperature=0.7, which_model="assistant"
    )
    message = {"role": "assistant", "content": response, "turn": state.current_turn}
    state.messages.append(message)
    for mem in state.active_memories:
        conf = await detect_memory_confirmation(mem, response)
        state.info_leakage[mem.content] = conf
    state.current_turn += 1
    return state


# ---------------------------------------------------------------------------
# Conversation Durable Generation with Pre-Computed Trajectory
# ---------------------------------------------------------------------------
@task
async def generate_conversation_durable(
    state: ConversationState,
    conv_trajectory: List[MemoryEvent],
    noise_ratio: float = 0.2,
) -> Dict[str, Any]:
    """
    Generate a conversation. At each turn, if a memory event is scheduled in conv_trajectory,
    update the active memories and add a subtle hint into the pending_updates buffer.
    """
    domain_config = DOMAINS[state.persona["domain"]]
    # Filter trajectory for the current conversation.
    events_this_conv = [e for e in conv_trajectory if e.conv_idx == state.conv_idx]
    # Ensure pending_updates buffer exists.
    state.persona.setdefault("pending_updates", [])

    while state.current_turn < state.num_turns:
        # Check for any event scheduled at this turn.
        for event in events_this_conv:
            if event.turn == state.current_turn:
                # Process event according to type.
                if event.event_type in ("update", "conflict"):
                    # For update/conflict, find a matching memory to update.
                    for mem in state.active_memories:
                        if mem.content.startswith(event.attribute + ":"):
                            mem.content = f"{event.attribute}: {event.new_value}"
                            mem.last_updated = state.current_turn
                            state.persona["pending_updates"].append(event.reason)
                elif event.event_type == "delete":
                    for mem in state.active_memories:
                        if mem.content.startswith(event.attribute + ":"):
                            mem.is_active = False
                            state.persona["pending_updates"].append(event.reason)
                elif event.event_type == "insert":
                    new_mem = Memory(
                        content=f"{event.attribute}: {event.new_value}",
                        importance=domain_config["memory_importance"].get(
                            event.attribute, 0.5
                        ),
                        first_seen=state.current_turn,
                        last_updated=state.current_turn,
                        is_active=True,
                        category=event.attribute,
                        source_type="explicit",
                    )
                    state.active_memories.append(new_mem)
                    state.info_leakage[new_mem.content] = False
                    state.persona["pending_updates"].append(event.reason)
        # (Optionally, one might remove confirmed updates from pending_updates here.)

        # Alternate user/assistant turns.
        if state.current_turn % 2 == 0:
            state = await generate_user_message(state)
        else:
            state = await generate_assistant_message(state)

        # Ask conversation completion model (optional).
        if state.current_turn >= 6:
            convo_text = format_convo(state.messages)
            status = await did_complete_model.ainvoke(
                "Based on the conversation below, "
                "has it reached a natural conclusion?\n\n" + convo_text
            )
            if status.status != "in_progress":
                print(f"Conversation ended early: {status.reasoning}")
                break
    # Final check: if any pending_updates remain unconfirmed, we might choose to regenerate.
    unconfirmed = [upd for upd in state.persona.get("pending_updates", [])]
    if unconfirmed:
        print(f"Warning: Some planned updates were not confirmed: {unconfirmed}")
        print("Regenerating conversation to enforce natural leakage...")
        return await generate_conversation_durable.ainvoke(
            state, conv_trajectory, noise_ratio
        )

    return {
        "conversation_id": f"{state.persona['id']}_conv_{state.conv_idx}",
        "messages": state.messages,
        "metadata": {
            "conv_index": state.conv_idx,
            "active_memories": [asdict(m) for m in state.active_memories],
            "timestamp": (datetime.now() + timedelta(days=state.conv_idx)).isoformat(),
        },
    }


# ---------------------------------------------------------------------------
# Test Case and Domain Dataset Generation
# ---------------------------------------------------------------------------
@dataclass
class TestCase:
    persona_id: str
    domain: str
    conversations: List[Dict[str, Any]]
    expected_memories: Dict[int, List[Memory]]
    memory_trajectory: List[MemoryEvent]
    metrics: Dict[str, float]


def generate_persona_profile(domain: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
    # (Simplified version; similar to previous implementations.)
    first_names = ["Alex", "Jordan", "Morgan", "Taylor", "Sam", "Chris", "Pat", "Jamie"]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
    ]
    profile = {
        "name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "age": random.randint(25, 55),
        "location": random.choice(
            ["San Francisco", "Seattle", "Austin", "Boston", "Chicago"]
        ),
        "years_experience": random.randint(1, 15),
    }
    # Domain-specific additions.
    if domain == "sdr":
        company = random.choice(COMPANY_CONTEXTS[domain])
        profile.update(
            {
                "company_name": company["name"],
                "product": company["product"],
                "target_market": company["target_market"],
                "unique_value": company["unique_value"],
                "role": "Sales Development Representative",
                "background": f"Worked previously in {random.choice(['software sales', 'consulting', 'account management'])}",
                "goals": "Build a strong sales pipeline",
            }
        )
    return profile


async def generate_test_case(
    domain: str,
    persona_idx: int,
    convs_per_phase: int = 3,
    num_changes: Optional[int] = None,
) -> TestCase:
    AsyncSqliteSaver.from_conn_string("checkpoints.db")
    persona_id = f"{domain}_persona_{persona_idx}"
    attributes = {}
    domain_config = DOMAINS[domain]
    for attr in domain_config["key_attributes"]:
        spec = domain_config["verifiable_attributes"].get(attr)
        if spec:
            if isinstance(spec, list):
                attributes[attr] = random.choice(spec)
            elif isinstance(spec, dict) and "min" in spec and "max" in spec:
                value = random.uniform(spec["min"], spec["max"])
                if spec.get("unit") == "USD":
                    value = round(value / 1000) * 1000
                attributes[attr] = value
        else:
            attributes[attr] = f"placeholder_{attr}"
    profile = generate_persona_profile(domain, attributes)
    persona = {
        "id": persona_id,
        "domain": domain,
        "attributes": attributes,
        "profile": profile,
        "relationships": {},
        "timeline": [],
    }
    # Plan changes (not used directly here, as our trajectory covers many events).
    num_changes = num_changes or random.randint(2, 4)
    total_phases = 1 + num_changes
    total_convs = total_phases * convs_per_phase

    # Base memories from persona attributes.
    base_memories = []
    for attr, value in persona["attributes"].items():
        if attr in domain_config["verifiable_attributes"]:
            formatted = f"{attr}: {f'${value:,}' if isinstance(value, (int, float)) and attr.endswith('budget') else value}"
            mem = Memory(
                content=formatted,
                importance=domain_config["memory_importance"].get(attr, 0.5),
                first_seen=0,
                last_updated=0,
                is_active=True,
                category="attribute",
                source_type="explicit",
            )
            base_memories.append(mem)
    # Pre-generate the memory trajectory.
    memory_trajectory = generate_memory_trajectory(
        domain_config,
        base_memories,
        total_convs,
        convs_per_phase * 30,
        event_probability=0.1,
    )
    print("Pre-generated Memory Trajectory:")
    for ev in memory_trajectory:
        print(asdict(ev))

    conversations = []
    expected_memories = {}
    active_memories = base_memories.copy()
    for conv_idx in range(total_convs):
        # (Optionally, insert phase-level changes here.)
        state = ConversationState(
            persona=persona,
            conv_idx=conv_idx,
            active_memories=active_memories.copy(),
            messages=[],
            info_leakage={},
            noise_ratio=0.2,
            current_turn=0,
            num_turns=30,
        )
        conv = await generate_conversation_durable(
            state, memory_trajectory, noise_ratio=0.2
        )
        conversations.append(conv)
        expected_memories[conv_idx] = active_memories.copy()
    metrics = {
        "fact_retention": 0.0,
        "change_detection": 0.0,
        "relationship_tracking": 0.0,
        "temporal_relevance": 0.0,
    }
    return TestCase(
        persona_id=persona_id,
        domain=domain,
        conversations=conversations,
        expected_memories=expected_memories,
        memory_trajectory=memory_trajectory,
        metrics=metrics,
    )


async def generate_domain_dataset(
    domain: str,
    num_personas: int = 100,
    output_file: Optional[str] = None,
    append: bool = True,
) -> Dict[str, Any]:
    print(f"Generating {domain} dataset with {num_personas} personas...")
    if output_file is None:
        output_file = f"{domain}_dataset.jsonl"
    mode = "a" if append and os.path.exists(output_file) else "w"
    if mode == "w":
        metadata = {
            "type": "metadata",
            "domain": domain,
            "generated_at": datetime.now().isoformat(),
            "num_personas": num_personas,
        }
        with open(output_file, "w") as f:
            f.write(json.dumps(metadata) + "\n")
        mode = "a"
    with open(output_file, mode) as f:
        for i in tqdm(range(num_personas)):
            test_case = await generate_test_case(domain, i)
            test_case_dict = {"type": "test_case", "data": asdict(test_case)}
            f.write(json.dumps(test_case_dict) + "\n")
            f.flush()
    print(f"Generated {num_personas} test cases and saved to {output_file}")
    return {"file": output_file, "num_cases": num_personas}


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------
async def generate_conversation(
    state: ConversationState, *, previous_state=None
) -> Dict[str, Any]:
    """Generate a conversation given a state"""
    if previous_state:
        return entrypoint.final(value=previous_state, save=previous_state)
    result = await generate_conversation_durable(state=state)
    return entrypoint.final(value=result, save=state)


async def main(args):
    domains = args.domains if args.domains else DOMAINS.keys()
    exit_stack = AsyncExitStack()
    checkpointer = await exit_stack.enter_async_context(
        AsyncSqliteSaver.from_conn_string("checkpoints.db")
    )
    global generate_conversation
    generate_conversation = entrypoint(checkpointer=checkpointer)(generate_conversation)
    async with exit_stack:
        for domain in domains:
            if domain not in DOMAINS:
                print(f"Warning: Unknown domain {domain}, skipping")
                continue
            await generate_conversation.ainvoke(
                dict(
                    domain=domain,
                    num_personas=args.num_personas,
                    output_file=args.output_file,
                    append=not args.no_append,
                )
            )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate conversation datasets for memory evaluation"
    )
    parser.add_argument(
        "--domains",
        nargs="+",
        choices=list(DOMAINS.keys()),
        help="Domains to generate datasets for. Default: all domains",
    )
    parser.add_argument(
        "--num-personas",
        type=int,
        default=100,
        help="Number of personas per domain. Default: 100",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="Output file path. Default: [domain]_dataset.jsonl",
    )
    parser.add_argument(
        "--no-append",
        action="store_true",
        help="Overwrite output file instead of appending",
    )
    parser.add_argument(
        "--noise-ratio",
        type=float,
        default=0.2,
        help="Ratio of turns with noise. Default: 0.2",
    )
    parser.add_argument(
        "--turns-per-conv",
        type=int,
        default=30,
        help="Number of turns per conversation. Default: 30",
    )
    parser.add_argument(
        "--convs-per-phase",
        type=int,
        default=3,
        help="Conversations per phase. Default: 3",
    )

    args = parser.parse_args()
    asyncio.run(main(args))
