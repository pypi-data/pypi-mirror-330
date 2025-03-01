#!/usr/bin/env python3
"""
Synthetic Data Generator for Memory Benchmarking

This script generates a single conversation between a persona and an assistant,
with planned memory updates that get subtly incorporated during the conversation.
"""

import asyncio
import json
import os
import random
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Annotated

from langchain.chat_models import init_chat_model
import langsmith as ls
from pydantic import BaseModel, Field, AfterValidator
from trustcall import create_extractor
from copy import deepcopy


# ---------------------------------------------------------------------------
# Configuration and Domain Context
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
        "memory_importance": {
            "buying_stage": 0.9,
            "objections": 0.8,
            "relationships": 0.9,
            "preferences": 0.7,
        },
    },
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
chat_model = init_chat_model("accounts/fireworks/models/deepseek-v3", max_tokens=8000)


class ChapterSummary(BaseModel):
    before: str = Field(
        description="What happed before this chapter (and after the previous one, if applicable)."
        " That may have motivated the next chapter's motive and changes. If it's the first chapter, can just be some background you can make up."
        " Should be worded like 'Since the last time the user spoke, ...'"
    )
    motive: str = Field(
        description="The main purpose / thing that is addressed in this chapter."
    )


@dataclass
class MemoryUpdate:
    turn: int
    attribute: str
    old_value: Optional[str]
    new_value: Optional[str]
    reason: str
    severity: float = 1.0  # 0.0 (slight) to 1.0 (significant)


@dataclass
class ConversationState:
    persona: Dict[str, Any]
    messages: List[Dict[str, Any]]
    memory_updates: List[MemoryUpdate]
    current_turn: int = 0
    num_turns: int = 30
    temperature: float = 0.7


def build_system_prompt(turn: int, pending_updates: List[str]) -> str:
    prompt = f"Turn {turn}: Continue the conversation naturally."
    if pending_updates:
        prompt += (
            " Note: Since the last message, the following has changed: "
            + "; ".join(pending_updates)
        )
        prompt += ". Please work these details into your response subtly."
    return prompt


def build_conversation_prompt(
    persona: Dict[str, Any],
    num_turns: int,
    memory_updates: List[MemoryUpdate],
    previous_context: str = "",
    chapter_context: Optional[Dict[str, Any]] = None,
) -> str:
    domain_config = DOMAINS[persona["domain"]]
    profile = persona["profile"]
    company = COMPANY_CONTEXTS[persona["domain"]][0]

    # Sort memory updates by turn
    updates_by_turn = {}
    for update in memory_updates:
        if update.turn not in updates_by_turn:
            updates_by_turn[update.turn] = []
        updates_by_turn[update.turn].append(update)

    chapter_info = ""
    if chapter_context:
        chapter_info = f"""
        
Chapter Context (Chapter {chapter_context['chapter_number']} of {chapter_context['total_chapters']}):
- Goal: {chapter_context['chapter_motive']}
"""
        if chapter_context["previous_context"]:
            chapter_info += f"- Previous Context: {chapter_context['previous_context']}"

    prompt = f"""
Generate a {num_turns}-turn conversation between a {domain_config['user_role']} and a {domain_config['service_role']}, with anywhere from 1-30 sentences per response.{chapter_info}

User Profile:
- Name: {profile['name']}
- Role: {domain_config['user_role']}
- Background: {', '.join(f'{k}: {v}' for k, v in persona['attributes'].items())}

Assistant Profile:
- Role: {domain_config['service_role']} at {company['name']}
- Company: {company['description']}
- Product: {company['product']}
- Value Proposition: {company['unique_value']}

Memory Updates:

The following updates occur while the conversation is in progress. They actually occur, rather than being planned for the future.
Incorporate them into your response subtly at the prescribed turn in the conversation.
"""

    for turn, updates in sorted(updates_by_turn.items()):
        prompt += f"\nTurn {turn}:\n"
        for update in updates:
            prompt += f"- {update.reason}\n"

    prompt += f"""
Format each turn in XML, like:
<turn n="1">
<user>
[user's message]
</user>
<assistant>
[assistant's message]
</assistant>
</turn>
<thinking>
[Plan out the next turn to ensure it's natural, sufficiently high-variance, and consistent with the personality.]
</thinking>
<turn n="2">
...
</turn>

Guidelines:
1. Keep responses natural and conversational. Incorporate spelling mistakes and colloquialisms. 
    These must pass an AI-text classifier, so it must be indistinguishable from humans.
2. Subtly incorporate memory updates in the turn they occur. Make them hard to detect if possible, though ensure they are incorporated eventually and organically.
3. Maintain consistent personality and knowledge throughout
4. Include relevant background information naturally
5. Each response should be anywhere from 1-50 sentences. Include some variety.

Generate the complete conversation:{previous_context}

Remember, try to spread the conversation realistically over {num_turns} turns.
"""

    return prompt


async def generate_chat_completion(messages, temperature: float = 0.7) -> str:
    response = str(
        (await chat_model.bind(temperature=temperature).ainvoke(messages)).content
    ).strip('"')
    return response


class InformationAnalysis(BaseModel):
    """Analyze the conversation to check that all the expected information was incorporated."""

    reasoning: str = Field(description="Reason over what was said or hinted at.")
    included: list[str] = Field(
        default_factory=list,
        description="State the line in which each expected piece of information is leaked.",
    )
    missing: list[str] = Field(
        default_factory=list,
        description="List all articles of information from the memory updates that"
        " are not yet included. If all content is included, then keep this list empty.",
    )
    instructions: str = Field(
        ...,
        description="If there is information that was omitted, instruct the AI to continue the dialog from the point it stopped at,"
        " ensuring it naturally includes the missing information."
        " Explicitly state what informaiton to be sure to include organically in tne remaining turns."
        " Like 'You failed to mention X and Y. Starting from turn T, continue the conversation. Be sure to keep it organic,"
        " undedectable from a real dialog you may overhear in the wild, incorporating personality, humor, etc....'",
    )


analyzer = init_chat_model("openai:o3-mini").with_structured_output(InformationAnalysis)


async def generate_verified_conversation(
    prompt: str,
    temperature: float = 0.7,
    updates: list = [],
) -> str:
    state = [
        {
            "role": "system",
            "content": "You are writing a dialog with the expected style and parameters.",
        },
        {"role": "user", "content": prompt},
    ]
    dialog = []

    while True:
        response = await generate_chat_completion(state, temperature)
        dialog.append(response)
        state.append({"role": "assistant", "content": response})
        current_dialog = "\n".join(dialog)
        to_analyze = f"""You're checked with checking that all the user's information is organically included in the dialog.
Review all the following information. Evaluate whether there is any missing content that ought to be woven in.

## Information:
{updates}

## Dialog:
{current_dialog}

Reminder, everything mentioned within Information should be mentioned or at least subtly alluded to in the dialog. Ideally it's very subtle."""
        analysis = await analyzer.ainvoke(to_analyze)
        if analysis.missing:
            state.append({"role": "user", "content": analysis.instructions})
        else:
            break
    return "\n".join(dialog)


@ls.traceable
def parse_conversation(raw_conversation: str) -> List[Dict[str, Any]]:
    import xml.etree.ElementTree as ET
    from io import StringIO

    # Ensure we have a root element for valid XML
    xml_str = f"<conversation>\n{raw_conversation}\n</conversation>"

    try:
        # Parse XML string
        root = ET.parse(StringIO(xml_str)).getroot()
        messages = []

        # Process each turn
        for turn in root.findall(".//turn"):
            turn_num = int(turn.get("n"))

            # Extract user message
            user = turn.find("user")
            if user is not None and user.text:
                messages.append(
                    {"role": "user", "content": user.text.strip(), "turn": turn_num}
                )

            # Extract assistant message
            assistant = turn.find("assistant")
            if assistant is not None and assistant.text:
                messages.append(
                    {
                        "role": "assistant",
                        "content": assistant.text.strip(),
                        "turn": turn_num,
                    }
                )

        return messages
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        print("Raw conversation:")
        print(raw_conversation)
        raise


@ls.traceable
async def generate_conversation(
    domain: str,
    persona: Dict[str, Any],
    num_turns: int = 30,
    temperature: float = 0.7,
    memory_updates: Optional[List[MemoryUpdate]] = None,
    last_conversation: Optional[Dict[str, Any]] = None,
    conversation_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Generate a single conversation with planned memory updates.

    Args:
        domain: The conversation domain (e.g. 'sdr')
        persona: The persona dictionary containing the current state of the user
                This should include any updates from previous conversations
        num_turns: Maximum number of conversation turns
        temperature: Temperature for generation
        memory_updates: List of planned memory updates for this conversation
        last_conversation: Previous conversation for context
        conversation_context: Additional context about this conversation's place in the series
    """
    domain_config = DOMAINS[domain]

    # Use provided persona instead of generating a new one
    if not persona:
        raise ValueError("A persona must be provided")

    # Validate persona has required fields
    required_fields = ["id", "domain", "attributes", "profile"]
    missing_fields = [f for f in required_fields if f not in persona]
    if missing_fields:
        raise ValueError(f"Persona missing required fields: {missing_fields}")

    # Generate memory updates if none provided
    if memory_updates is None:
        attrs_updated = set()
        memory_updates = []
        num_updates = random.randint(2, 4)
        for _ in range(num_updates):
            turn = random.randint(3, num_turns - 3)
            attr = random.choice(
                list(domain_config["verifiable_attributes"] - attrs_updated)
            )
            attrs_updated.add(attr)
            if attr == "budget":
                old_val = persona["attributes"][attr]
                new_val = int(float(old_val) * random.uniform(0.6, 1.4))
                reason = f"Budget updated from ${old_val:,} to ${new_val:,}"
            else:
                spec = domain_config["verifiable_attributes"][attr]
                old_val = persona["attributes"].get(attr)
                new_val = (
                    random.choice([x for x in spec if str(x) != str(old_val)])
                    if isinstance(spec, list)
                    else None
                )
                reason = f"{attr.replace('_', ' ').title()} changed to {new_val}"

            memory_updates.append(
                MemoryUpdate(
                    turn=turn,
                    attribute=attr,
                    old_value=str(old_val) if old_val else None,
                    new_value=str(new_val),
                    reason=reason,
                    severity=random.random(),
                )
            )
        memory_updates.sort(key=lambda x: x.turn)

    # Generate the complete conversation in one shot
    # Build context from last conversation if available
    previous_context = ""
    if last_conversation:
        last_messages = last_conversation.get("messages", [])
        if last_messages:
            previous_context = (
                "\nContext from the previous conversation:\n<transcript>\n"
            )
            for msg in last_messages[-30:]:
                previous_context += f"- {msg['role'].title()}: {msg['content']}\n"
            previous_context += "</transcript>\n"

    prompt = build_conversation_prompt(
        persona=persona,
        num_turns=num_turns,
        memory_updates=memory_updates,
        previous_context=previous_context,
        chapter_context=conversation_context,
    )

    @ls.traceable
    def calculate_final_state(
        initial_attributes: Dict[str, Any], updates: List[MemoryUpdate]
    ) -> Dict[str, Any]:
        """Calculate the final state after applying all memory updates."""
        final_state = deepcopy(initial_attributes)
        update_history = {}

        for update in sorted(updates, key=lambda x: x.turn):
            if update.new_value is not None:
                # Track when this attribute was last updated
                update_history[update.attribute] = update.turn
                # Update the value
                final_state[update.attribute] = update.new_value

        return {
            "final_attributes": final_state,
            "last_update_turn": update_history,
            "unchanged_attributes": [
                attr for attr in initial_attributes if attr not in update_history
            ],
        }

    final_state = calculate_final_state(persona["attributes"], memory_updates)
    if last_conversation:
        updates = memory_updates
    else:
        updates = [final_state["final_attributes"]]
    raw_conversation = await generate_verified_conversation(
        prompt, temperature, updates
    )
    messages = parse_conversation(raw_conversation)

    return {
        "conversation_id": f"{persona['id']}_single",
        "messages": messages,
        "metadata": {
            "persona": persona,
            "memory_updates": [asdict(u) for u in memory_updates],
            "domain": domain,
            "num_turns": num_turns,
            "temperature": temperature,
            "final_state": final_state,
        },
    }


@dataclass
class ConversationHistory:
    persona_id: str
    conversations: List[Dict[str, Any]]
    current_attributes: Dict[str, Any]
    domain: str
    last_conversation_time: float

    @classmethod
    def create_new(cls, domain: str, persona: Dict[str, Any]) -> "ConversationHistory":
        return cls(
            persona_id=persona["id"],
            conversations=[],
            current_attributes=deepcopy(persona["attributes"]),
            domain=domain,
            last_conversation_time=time.time(),
        )

    def add_conversation(self, conversation: Dict[str, Any]):
        self.conversations.append(conversation)
        self.current_attributes = conversation["metadata"]["final_state"][
            "final_attributes"
        ]
        self.last_conversation_time = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationHistory":
        return cls(**data)


def generate_memory_update_plan(
    domain: str,
    num_conversations: int,
    initial_persona: Dict[str, Any],
    num_turns_per_conversation: int = 10,
    min_updates_per_conv: int = 1,
    max_updates_per_conv: int = 3,
) -> List[List[MemoryUpdate]]:
    """Generate a complete plan of memory updates for all conversations in a series.

    Args:
        domain: The conversation domain
        num_conversations: Number of conversations in the series
        initial_persona: Initial persona state
        num_turns_per_conversation: Number of turns per conversation
        min_updates_per_conv: Minimum number of updates per conversation
        max_updates_per_conv: Maximum number of updates per conversation

    Returns:
        List of lists of MemoryUpdate objects, one list per conversation
    """
    domain_config = DOMAINS[domain]
    current_persona = deepcopy(initial_persona)
    all_updates = []

    for conv_idx in range(num_conversations):
        conv_updates = []
        num_updates = random.randint(min_updates_per_conv, max_updates_per_conv)

        # Generate updates for this conversation
        for _ in range(num_updates):
            turn = random.randint(3, num_turns_per_conversation - 3)
            attr = random.choice(list(domain_config["verifiable_attributes"].keys()))
            old_val = current_persona["attributes"].get(attr)

            if attr == "budget":
                new_val = int(float(old_val) * random.uniform(0.8, 1.2))
                reason = f"Budget updated from ${old_val:,} to ${new_val:,}"
            else:
                spec = domain_config["verifiable_attributes"][attr]
                new_val = (
                    random.choice([x for x in spec if str(x) != str(old_val)])
                    if isinstance(spec, list)
                    else None
                )
                reason = f"{attr.replace('_', ' ').title()} changed to {new_val}"

            update = MemoryUpdate(
                turn=turn,
                attribute=attr,
                old_value=str(old_val) if old_val else None,
                new_value=str(new_val),
                reason=reason,
                severity=random.random(),
            )
            conv_updates.append(update)

            # Update current persona state
            if new_val is not None:
                current_persona["attributes"][attr] = new_val

        # Sort updates by turn
        conv_updates.sort(key=lambda x: x.turn)
        all_updates.append(conv_updates)

    return all_updates


@ls.traceable
async def project_conversation_trajectory(
    domain: str,
    num_conversations: int,
    initial_persona: Dict[str, Any],
    memory_updates: List[List[MemoryUpdate]],
) -> "Chapters":
    """Project the trajectory of conversations to ensure a coherent narrative arc."""
    domain_config = DOMAINS[domain]

    # Build update summary for each conversation
    update_summaries = []
    current_persona = deepcopy(initial_persona)

    for conv_idx, conv_updates in enumerate(memory_updates):
        summary = []
        for update in conv_updates:
            summary.append(update.reason)
            if update.new_value:
                current_persona["attributes"][update.attribute] = update.new_value
        update_summaries.append(summary)

    prompt = f"""
    Given a {domain_config['user_role']}'s profile and {num_conversations} planned conversations,
    project how their journey should evolve across these conversations.
    Each conversation should have a clear purpose and advance the overall narrative.
    
    User Profile:
    - Role: {domain_config['user_role']}
    - Background: {', '.join(f'{k}: {v}' for k, v in initial_persona['attributes'].items())}
    - Name: {initial_persona['profile']['name']}
    
    Company Context:
    - Company: {COMPANY_CONTEXTS[domain][0]['name']}
    - Product: {COMPANY_CONTEXTS[domain][0]['product']}
    - Value Prop: {COMPANY_CONTEXTS[domain][0]['unique_value']}
    
    Planned Changes:
"""

    for i, updates in enumerate(update_summaries):
        prompt += f"""
    
Conversation {i+1}:
{chr(10).join(f'- {update}' for update in updates)}
"""

    prompt += """
    
    Plan these conversations/chapters to tell a complete story that incorporates these changes,
    with realistic challenges, setbacks, and progress. Don't make it too easy - include realistic
    friction points and obstacles that align with the planned changes. Add extra changes as well, being creative but realistic.
    """

    def correct_number(end_states: list):
        if not len(end_states) == num_conversations:
            raise ValueError(
                f"Expected {num_conversations} end states, but got {len(end_states)}"
            )
        return end_states

    class Chapters(BaseModel):
        """Propose what the "end state" of each chapter should be in a multi-chapter series of dialogs/interactions."""

        chapter_end_states: Annotated[
            list[ChapterSummary], AfterValidator(correct_number)
        ] = Field(
            description="The motives/end state of the conversation / motive of each chapter."
        )

    trajectory_projector = create_extractor(
        init_chat_model("openai:o3-mini"), tools=[Chapters], tool_choice="Chapters"
    )
    result = await trajectory_projector.ainvoke(
        {"messages": [{"role": "user", "content": prompt}]}
    )
    return result["responses"][0]


@ls.traceable
async def generate_conversation_series(
    domain: str,
    num_conversations: int,
    min_time_delta_hours: float = 24,
    max_time_delta_hours: float = 168,  # 1 week
    num_turns_per_conversation: int = 10,
    temperature: float = 0.7,
    initial_persona: Optional[Dict[str, Any]] = None,
    history: Optional[ConversationHistory] = None,
) -> ConversationHistory:
    """Generate a series of conversations with an evolving persona."""

    # Create or use existing history
    if history is None:
        # Generate initial persona if not provided
        if initial_persona is None:
            domain_config = DOMAINS[domain]
            attributes = {}
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

            first_names = [
                "Alex",
                "Jordan",
                "Morgan",
                "Taylor",
                "Sam",
                "Chris",
                "Pat",
                "Jamie",
            ]
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
            initial_persona = {
                "id": f"{domain}_persona_{random.randint(1000, 9999)}",
                "domain": domain,
                "attributes": attributes,
                "profile": {
                    "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                    "age": random.randint(25, 55),
                    "location": random.choice(
                        ["San Francisco", "Seattle", "Austin", "Boston", "Chicago"]
                    ),
                    "years_experience": random.randint(1, 15),
                },
            }

        history = ConversationHistory.create_new(domain, initial_persona)

    # Generate complete memory update plan
    all_memory_updates = generate_memory_update_plan(
        domain=domain,
        num_conversations=num_conversations,
        initial_persona=initial_persona,
        num_turns_per_conversation=num_turns_per_conversation,
    )

    # Project the conversation trajectory with planned updates
    current_persona = deepcopy(initial_persona)
    trajectory = await project_conversation_trajectory(
        domain, num_conversations, current_persona, all_memory_updates
    )

    # Generate conversations using pre-planned updates
    for i in range(num_conversations):
        chapter = trajectory.chapter_end_states[i]
        memory_updates = all_memory_updates[i]

        # Add chapter info to conversation context
        conversation_context = {
            "chapter_number": i + 1,
            "total_chapters": num_conversations,
            "chapter_motive": chapter.motive,
            "previous_context": chapter.before if i > 0 else None,
        }

        # Add time delay between conversations
        if i > 0:
            time_delta = (
                random.uniform(min_time_delta_hours, max_time_delta_hours) * 3600
            )
            history.last_conversation_time += time_delta

        # Generate conversation with current state and previous context
        last_conv = history.conversations[-1] if history.conversations else None
        conversation = await generate_conversation(
            domain=domain,
            persona=current_persona,  # Pass the current persona state
            num_turns=num_turns_per_conversation,
            temperature=temperature,
            memory_updates=memory_updates,
            last_conversation=last_conv,
            conversation_context=conversation_context,
        )

        # Update conversation timestamp
        conversation["metadata"]["timestamp"] = history.last_conversation_time

        # Update persona with memory updates from this conversation
        for update in memory_updates:
            if update.new_value:
                current_persona["attributes"][update.attribute] = update.new_value

        # Add to history
        history.add_conversation(conversation)

    return history


def get_next_series_index(data_dir: str, domain: str) -> int:
    """Get the next available series index for a domain."""
    import glob
    import os

    os.makedirs(data_dir, exist_ok=True)
    pattern = os.path.join(data_dir, f"{domain}-*.jsonl")
    existing_files = glob.glob(pattern)
    if not existing_files:
        return 0

    indices = [int(f.split("-")[-1].split(".")[0]) for f in existing_files]
    return max(indices) + 1


async def main(
    domain: str,
    num_turns: int,
    num_conversations: int,
    num_series: int = 1,
    temperature: float = 0.7,
    data_dir: str = "data",
) -> None:
    """Generate multiple conversation series and save them as JSONL files."""
    os.makedirs(data_dir, exist_ok=True)

    for _ in range(num_series):
        # Get next series index
        series_idx = get_next_series_index(data_dir, domain)
        output_file = os.path.join(data_dir, f"{domain}-{series_idx}.jsonl")

        # Generate the conversation series
        history = await generate_conversation_series(
            domain=domain,
            num_conversations=num_conversations,
            num_turns_per_conversation=num_turns,
            temperature=temperature,
        )

        # Write each conversation as a separate line in JSONL
        with open(output_file, "w") as f:
            for conv in history.conversations:
                f.write(json.dumps(conv) + "\n")

        print(f"Generated conversation series saved to {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a single conversation with memory updates"
    )
    parser.add_argument(
        "--domain",
        choices=list(DOMAINS.keys()),
        default="sdr",
        help="Domain for conversation generation",
    )
    parser.add_argument(
        "--num-turns",
        type=int,
        default=30,
        help="Number of turns in conversation",
    )
    parser.add_argument(
        "--num-conversations",
        type=int,
        default=3,
        help="Number of conversations to generate",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for generation",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="evals/gen/data",
        help="Directory to store conversation series JSONL files",
    )
    parser.add_argument(
        "--num-series",
        type=int,
        default=1,
        help="Number of conversation series to generate",
    )

    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
