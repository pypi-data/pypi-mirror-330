"""
Generates large-scale synthetic datasets for memory system evaluation.
Each dataset represents a domain with 100 test cases (personas).
"""

import json
import random
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import openai
from datetime import datetime, timedelta
import asyncio
from tqdm import tqdm

from langgraph.checkpoint.sqlite import SQLiteSaver

# Noise snippets for more realistic conversations
NOISE_SNIPPETS = [
    "Unrelated, but I've been meaning to organize my closet.",
    "On another note, the traffic was terrible this morning.",
    "Random thought: I need to schedule a dentist appointment soon.",
    "By the way, my phone battery dies so quickly these days.",
    "Off-topic, but I'm thinking about trying that new restaurant downtown.",
    "Changing subjects, the neighbor's dog barks a lot at night.",
    "On a different note, I should probably start exercising more regularly.",
    "Unrelated, but my favorite mug broke yesterday.",
    "Random thing: I keep forgetting to water my plants.",
    "Switching gears, the Wi-Fi has been acting up lately.",
    "Just remembered I need to call my mom later.",
    "Speaking of random things, I saw a rainbow this morning.",
    "Not related, but I'm thinking of repainting my room.",
    "By the way, have you ever tried meditation?",
    "Random question: do you prefer sunrise or sunset?",
]

DOMAINS = {
    "sdr": {
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
    "support": {
        "key_attributes": [
            "product_usage",
            "technical_level",
            "subscription_tier",
            "integration_setup",
        ],
        "change_types": ["issue_patterns", "feature_usage", "technical_sophistication"],
        "relationship_types": ["admin_user", "end_user", "technical_contact"],
        "memory_importance": {
            "technical_level": 0.8,
            "recurring_issues": 0.9,
            "preferences": 0.7,
            "workarounds": 0.8,
        },
    },
    # Add other domains similarly
}


@dataclass
class Memory:
    """A specific piece of information to be remembered"""

    content: Any
    importance: float  # 0-1 scale
    first_seen: int  # Conversation number
    last_updated: int  # Conversation number
    is_active: bool  # Whether this is still current
    category: str  # Type of memory (fact, preference, relationship, etc)
    source_type: str  # How it was revealed (explicit, implicit, derived)


@dataclass
class TestCase:
    """A single persona test case"""

    persona_id: str
    domain: str
    conversations: List[Dict[str, Any]]
    expected_memories: Dict[int, List[Memory]]  # Key: conversation_index
    metrics: Dict[str, float]  # Aggregated metrics for this test case


async def generate_conversation(
    persona: Dict[str, Any],
    conv_idx: int,
    active_memories: List[Memory],
    num_turns: int = 30,
    noise_ratio: float = 0.3,  # 30% of turns will include noise
) -> Dict[str, Any]:
    """Generate a single conversation with the persona"""

    # Generate noise snippets
    noise_snippets = NOISE_SNIPPETS

    # Track what information has been leaked
    info_leakage = {memory.content: False for memory in active_memories}

    # Build context for the LLMs
    user_context = f"""
You are roleplaying as a person with these characteristics:
{json.dumps(persona, indent=2)}

Current context:
- This is conversation #{conv_idx + 1} with the AI
- You should reference and build upon previous information naturally
- Express your thoughts, needs, and situation changes organically

Start the conversation in a natural way that makes sense for your role and context.
"""

    assistant_context = """
You are an AI assistant. Engage naturally while staying aware of the user's context.
Remember previous interactions (if any) and maintain consistent understanding.
"""

    messages = []
    conversation = []

    # Generate the conversation turn by turn
    for turn in range(num_turns):
        if turn % 2 == 0:
            # User turn
            current_messages = [
                {"role": "system", "content": user_context},
                *conversation,
            ]
            response = await openai.ChatCompletion.acreate(
                model="gpt-4", messages=current_messages, temperature=0.7
            )
            # Decide if this turn should include noise
            should_add_noise = random.random() < noise_ratio

            base_content = response.choices[0].message.content

            # Add random noise if selected
            if should_add_noise:
                noise = random.choice(noise_snippets)
                # Randomly place noise at start or end of message
                if random.random() < 0.5:
                    content = f"{noise} {base_content}"
                else:
                    content = f"{base_content} {noise}"
            else:
                content = base_content

            message = {
                "role": "user",
                "content": content,
                "turn": turn,
                "has_noise": should_add_noise,
            }

            # Check if this message leaked any expected info
            for memory in active_memories:
                # Use semantic similarity or keyword matching to check if memory was leaked
                if memory.content.lower() in content.lower():
                    info_leakage[memory.content] = True
        else:
            # Assistant turn
            current_messages = [
                {"role": "system", "content": assistant_context},
                *conversation,
            ]
            response = await openai.ChatCompletion.acreate(
                model="gpt-4", messages=current_messages, temperature=0.7
            )
            message = {
                "role": "assistant",
                "content": response.choices[0].message.content,
                "turn": turn,
            }

        conversation.append(message)
        messages.append(message)

    # Verify all required information was leaked
    unleaked_info = [content for content, leaked in info_leakage.items() if not leaked]

    # If some info wasn't leaked, regenerate the conversation
    if unleaked_info:
        print(f"Warning: Failed to leak information: {unleaked_info}")
        print("Regenerating conversation...")
        return await generate_conversation(
            persona, conv_idx, active_memories, num_turns, noise_ratio
        )

    return {
        "conversation_id": f"{persona['id']}_conv_{conv_idx}",
        "messages": messages,
        "metadata": {
            "conv_index": conv_idx,
            "active_memories": [asdict(m) for m in active_memories],
            "timestamp": (datetime.now() + timedelta(days=conv_idx)).isoformat(),
            "noise_stats": {
                "noise_ratio": noise_ratio,
                "noisy_turns": sum(1 for m in messages if m.get("has_noise", False)),
                "clean_turns": sum(
                    1 for m in messages if not m.get("has_noise", False)
                ),
            },
            "verified_leaks": dict(info_leakage),
        },
    }


async def generate_test_case(domain: str, persona_idx: int) -> TestCase:
    """Generate a complete test case (persona with multiple conversations)"""

    # Create initial persona
    persona_id = f"{domain}_persona_{persona_idx}"
    persona = {
        "id": persona_id,
        "domain": domain,
        "attributes": {},  # Will be filled based on domain
        "relationships": {},
        "timeline": [],
    }

    # Fill in domain-specific attributes
    domain_config = DOMAINS[domain]
    for attr in domain_config["key_attributes"]:
        # (You'd have specific value generators for each attribute)
        persona["attributes"][attr] = f"placeholder_{attr}"

    # Plan changes over time
    changes = []
    num_changes = random.randint(2, 4)
    for _ in range(num_changes):
        change_type = random.choice(domain_config["change_types"])
        conv_idx = random.randint(1, 6)  # When it happens
        changes.append(
            {
                "type": change_type,
                "conversation_index": conv_idx,
                "details": f"placeholder_change_{change_type}",
            }
        )

    # Generate conversations
    conversations = []
    expected_memories = {}
    active_memories = []

    for conv_idx in range(7):  # 7 conversations per persona
        # Update active memories based on changes
        for change in changes:
            if change["conversation_index"] == conv_idx:
                memory = Memory(
                    content=change["details"],
                    importance=domain_config["memory_importance"].get(
                        change["type"], 0.5
                    ),
                    first_seen=conv_idx,
                    last_updated=conv_idx,
                    is_active=True,
                    category=change["type"],
                    source_type="explicit",
                )
                active_memories.append(memory)

        # Generate conversation
        conv = await generate_conversation(persona, conv_idx, active_memories)
        conversations.append(conv)

        # Record expected memories for this point
        expected_memories[conv_idx] = active_memories.copy()

    # Initialize metrics (will be filled during evaluation)
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
        metrics=metrics,
    )


async def generate_domain_dataset(
    domain: str, num_personas: int = 100
) -> Dict[str, Any]:
    """Generate a complete dataset for a domain"""

    print(f"Generating {domain} dataset with {num_personas} personas...")

    test_cases = []
    for i in tqdm(range(num_personas)):
        test_case = await generate_test_case(domain, i)
        test_cases.append(asdict(test_case))

    dataset = {
        "domain": domain,
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "num_personas": num_personas,
        },
        "test_cases": test_cases,
        "aggregated_metrics": {},  # Will be filled during evaluation
    }

    return dataset


async def main():
    """Generate all domain datasets"""
    for domain in DOMAINS.keys():
        dataset = await generate_domain_dataset(domain)

        # Save dataset
        with open(f"{domain}_dataset.json", "w") as f:
            json.dump(dataset, f, indent=2)

        print(
            f"Generated {domain} dataset with {len(dataset['test_cases'])} test cases"
        )


if __name__ == "__main__":
    asyncio.run(main())

            num_personas=args.num_personas,
            output_file=args.output_file,
            append=not args.no_append,
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
        help="Number of personas to generate per domain. Default: 100",
    )
    
    parser.add_argument(
        "--output-file",
        type=str,
        help="Output file path. Default: [domain]_dataset.json",
    )
    
    parser.add_argument(
        "--no-append",
        action="store_true",
        help="If set, overwrite output file instead of appending",
    )
    
    parser.add_argument(
        "--noise-ratio",
        type=float,
        default=0.2,
        help="Ratio of conversation turns that should include noise. Default: 0.2",
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
        help="Number of conversations per phase (initial/change). Default: 3",
    )
    
    args = parser.parse_args()
    asyncio.run(main(args))
