# %%
# %load_ext autoreload
# %autoreload 2
# %%
from pydantic import BaseModel
from langgraph.store.memory import InMemoryStore
from langgraph.prebuilt import create_react_agent
from langmem import create_manage_memory_tool

prompt = "Save all memories to the user profile."


class UserProfile(BaseModel):
    name: str
    age: int | None = None
    recent_memories: list[str] = []
    preferences: dict | None = None


memory_tool = create_manage_memory_tool(
    # All memories saved to this tool will live within this namespace
    # The brackets will be populated at runtime by the configurable values
    namespace=("memories", "user_profile"),
    schema=UserProfile,
    actions_permitted=["create", "update"],
    instructions="Update the existing user profile (or create a new one if it doesn't exist) based on the shared information.",
)
store = InMemoryStore(
    index={
        "dims": 1536,
        "embed": "openai:text-embedding-3-small",
    }
)
agent = create_react_agent(
    "anthropic:claude-3-5-sonnet-latest",
    prompt=prompt,
    tools=[
        memory_tool,
    ],
    store=store,
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "I'm 60 years old and have been programming for 5 days.",
            }
        ]
    },
)
result["messages"][-1].pretty_print()

print(store.search(("memories", "user_profile")))
