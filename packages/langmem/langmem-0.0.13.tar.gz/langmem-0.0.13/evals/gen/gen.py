import asyncio
import json
import os
import random
import typing
import uuid
from contextlib import AsyncExitStack
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List

from langchain.chat_models import init_chat_model
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.func import entrypoint, task
from pydantic import BaseModel, Field
from tqdm import tqdm

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
    "support": {
        "service_role": "Technical Support Engineer",
        "user_role": "Customer",
        "verifiable_attributes": {
            "subscription_tier": ["free", "pro", "enterprise"],
            "technical_level": ["novice", "intermediate", "expert"],
            "common_issues": [
                "API errors",
                "configuration issues",
                "performance problems",
            ],
        },
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
    "tutor": {
        "service_role": "Academic Tutor",
        "user_role": "Student",
        "verifiable_attributes": {
            "education_level": ["high school", "undergraduate", "graduate"],
            "learning_style": ["visual", "auditory", "kinesthetic", "reading/writing"],
            "subject_gpa": {"min": 2.0, "max": 4.0},
        },
        "key_attributes": [
            "education_level",
            "learning_style",
            "academic_goals",
            "subject_focus",
            "study_environment",
        ],
        "change_types": [
            "academic_progress",
            "learning_preferences",
            "schedule_changes",
            "goal_updates",
        ],
        "relationship_types": ["teacher", "parent", "peer_student", "tutor"],
        "memory_importance": {
            "learning_style": 0.85,
            "academic_weaknesses": 0.9,
            "schedule_constraints": 0.75,
            "goal_changes": 0.8,
        },
    },
    "real_estate": {
        "service_role": "Realtor",
        "user_role": "Client",
        "verifiable_attributes": {
            "property_budget": {"min": 200000, "max": 2000000, "unit": "USD"},
            "preferred_locations": ["urban", "suburban", "rural"],
            "transaction_type": ["buy", "sell", "rent"],
        },
        "key_attributes": [
            "property_types",
            "client_demographics",
            "market_knowledge",
            "transaction_style",
            "geographic_focus",
        ],
        "change_types": [
            "client_needs",
            "market_conditions",
            "financial_situation",
            "timeline_changes",
        ],
        "relationship_types": ["buyer", "seller", "lender", "home_inspector"],
        "memory_importance": {
            "client_preferences": 0.95,
            "budget_changes": 0.9,
            "property_requirements": 0.85,
            "timeline_updates": 0.8,
        },
    },
    "general_chat": {
        "service_role": "Conversational Companion",
        "user_role": "User",
        "verifiable_attributes": {
            "communication_frequency": ["daily", "weekly", "monthly"],
            "shared_interests": ["sports", "technology", "cooking", "travel"],
            "last_interaction": {"format": "days_ago"},
        },
        "key_attributes": [
            "communication_style",
            "personal_interests",
            "cultural_background",
            "life_events",
            "hobbies",
        ],
        "change_types": [
            "interest_shifts",
            "life_circumstances",
            "relationship_status",
            "opinion_changes",
        ],
        "relationship_types": ["family_member", "friend", "colleague", "acquaintance"],
        "memory_importance": {
            "recurring_topics": 0.7,
            "personal_values": 0.8,
            "recent_events": 0.75,
            "preference_changes": 0.65,
        },
    },
}

# Define real-world company/organization contexts
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
    "support": [
        {
            "name": "DataViz Pro",
            "description": "Data visualization and analytics platform",
            "product": "DataViz Studio",
            "support_tiers": ["Basic", "Premium", "Enterprise"],
            "common_issues": ["API integration", "Custom visualization", "Data import"],
            "documentation": "docs.dataviz.pro",
            "support_channels": ["Email", "Live Chat", "Phone (Enterprise only)"],
        },
        {
            "name": "CloudScale",
            "description": "Cloud infrastructure management platform",
            "product": "CloudScale Manager",
            "support_tiers": ["Developer", "Team", "Business", "Enterprise"],
            "common_issues": [
                "Resource provisioning",
                "Cost optimization",
                "Security configuration",
            ],
            "documentation": "help.cloudscale.com",
            "support_channels": [
                "Community forum",
                "Ticket system",
                "24/7 phone support",
            ],
        },
    ],
    "tutor": [
        {
            "name": "BrightMinds Academy",
            "description": "Online tutoring platform specializing in STEM subjects",
            "subjects": ["Mathematics", "Physics", "Computer Science", "Chemistry"],
            "levels": ["High School", "AP", "Undergraduate"],
            "teaching_approach": "Personalized learning paths with interactive content",
            "platform_features": [
                "Virtual whiteboard",
                "Practice problems",
                "Video sessions",
            ],
        },
        {
            "name": "Global Language Institute",
            "description": "Language learning center with online and in-person tutoring",
            "subjects": ["English", "Spanish", "Mandarin", "French"],
            "levels": ["Beginner", "Intermediate", "Advanced", "Business"],
            "teaching_approach": "Immersive learning with native speakers",
            "platform_features": [
                "Language exchange",
                "Cultural workshops",
                "Business communication",
            ],
        },
    ],
    "real_estate": [
        {
            "name": "Urban Living Realty",
            "description": "Boutique real estate agency specializing in urban properties",
            "market_focus": [
                "Luxury condos",
                "Historic properties",
                "Urban developments",
            ],
            "service_area": "Greater San Francisco Bay Area",
            "specialties": [
                "First-time buyers",
                "Property investment",
                "Urban renovation",
            ],
            "unique_approach": "3D virtual tours and sustainable living focus",
        },
        {
            "name": "Suburban Homes & Properties",
            "description": "Family-focused real estate agency",
            "market_focus": [
                "Single-family homes",
                "New developments",
                "School districts",
            ],
            "service_area": "Seattle Metropolitan Area",
            "specialties": ["Family homes", "Relocation services", "New construction"],
            "unique_approach": "Family-first approach with school district expertise",
        },
    ],
}


def generate_persona_profile(domain: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a detailed persona profile based on domain and attributes"""

    # Select a random company context
    company = random.choice(COMPANY_CONTEXTS.get(domain, [{"name": "Generic Company"}]))

    # Generate basic demographic info
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

    # Add domain-specific details
    if domain == "sdr":
        profile.update(
            {
                "company_name": company["name"],
                "product": company["product"],
                "target_market": company["target_market"],
                "unique_value": company["unique_value"],
                "role": "Sales Development Representative",
                "background": f"Previously worked in {random.choice(['software sales', 'consulting', 'account management'])}",
                "goals": "Build strong pipeline and exceed quarterly targets",
            }
        )

    elif domain == "support":
        profile.update(
            {
                "company_name": company["name"],
                "product": company["product"],
                "support_level": company["support_tiers"][-1],  # Highest tier
                "expertise": random.choice(
                    ["Technical", "Customer Success", "Product Specialist"]
                ),
                "background": f"Has {profile['years_experience']} years of technical support experience",
                "specialties": random.sample(company["common_issues"], 2),
            }
        )

    elif domain == "tutor":
        profile.update(
            {
                "institution": company["name"],
                "subjects": random.sample(company["subjects"], 2),
                "teaching_level": random.choice(company["levels"]),
                "teaching_style": company["teaching_approach"],
                "credentials": f"{'PhD' if random.random() < 0.3 else 'Masters'} in {random.choice(company['subjects'])}",
                "specialization": f"Specializes in {random.choice(company['subjects'])}",
            }
        )

    elif domain == "real_estate":
        profile.update(
            {
                "agency": company["name"],
                "market_area": company["service_area"],
                "specialties": random.sample(company["specialties"], 2),
                "certifications": random.sample(["CRS", "ABR", "SRS", "GRI"], 2),
                "transaction_volume": f"${random.randint(5, 20)}M+ annually",
                "focus_areas": random.sample(company["market_focus"], 2),
            }
        )

    return profile


# Domain-specific noise snippets for more realistic conversations
DOMAIN_NOISE = {
    "sdr": [
        "Our office just got new standing desks installed.",
        "The commute to client meetings has been brutal lately.",
        "Have you tried that new CRM software everyone's talking about?",
        "The coffee machine in our break room is acting up again.",
        "Our team building event last week was interesting.",
    ],
    "support": [
        "The new IDE update is taking some getting used to.",
        "My second monitor just died on me.",
        "The dev team's been talking about that new framework.",
        "Our slack channels are getting pretty chaotic.",
        "Had to restart my laptop three times today.",
    ],
    "tutor": [
        "The campus library just got renovated.",
        "My study group meets in that new coffee shop now.",
        "The wifi in the dorm has been spotty lately.",
        "They changed the parking situation on campus.",
        "The weather's making it hard to focus on studying.",
    ],
    "real_estate": [
        "The construction on Main Street is affecting showings.",
        "Have you seen the new development downtown?",
        "The market reports this morning were interesting.",
        "My car's GPS took me to the wrong property yesterday.",
        "The weather's been perfect for open houses.",
    ],
    "general_chat": [
        "Just got back from walking my dog.",
        "My phone's been acting up all morning.",
        "The new coffee shop downtown is amazing.",
        "Can't believe how fast this year is going by.",
        "Finally got around to organizing my desk.",
    ],
}

# General noise snippets as fallback
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

# Fireworks.ai API configuration
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
if not FIREWORKS_API_KEY:
    raise ValueError("Please set FIREWORKS_API_KEY environment variable")


user_model = init_chat_model("accounts/fireworks/models/deepseek-v3")
assistant_model = init_chat_model("openai:o3-mini")


class conversation_status(BaseModel):
    reasoning: str = Field(
        description="Reasoning for why you classify the conversatino as still in-progress."
    )
    status: typing.Literal["in_progress", "completed"] = "in_progress"


did_complete_model = init_chat_model("openai:gpt-4o-mini").with_structured_output(
    conversation_status
)


def format_convo(messages: List[Dict[str, str]]) -> str:
    return "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])


@task
async def generate_chat_completion(
    messages: List[Dict[str, str]], temperature: float = 0.6, which_model: str = "user"
) -> str:
    """Generate chat completion using Fireworks.ai DeepSeek R1 model"""
    if which_model == "user":
        model = user_model
    elif which_model == "assistant":
        model = assistant_model
    else:
        raise ValueError("which_model must be either 'user' or 'assistant'")

    response = str((await model.ainvoke(messages)).content).strip('"')
    return response


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


@dataclass
class ConversationState:
    """State for conversation generation"""

    persona: Dict[str, Any]
    conv_idx: int
    active_memories: List[Memory]
    messages: List[Dict[str, str]]
    info_leakage: Dict[str, bool]
    noise_ratio: float = 0.2
    current_turn: int = 0


@task
async def generate_user_message(
    state: ConversationState, num_turns: int
) -> ConversationState:
    """Generate a user message as part of the conversation"""
    domain_config = DOMAINS[state.persona["domain"]]
    profile = state.persona["profile"]
    company = next(
        c
        for c in COMPANY_CONTEXTS[state.persona["domain"]]
        if c["name"] == profile["company_name"]
    )

    # Format verifiable attributes nicely
    formatted_attributes = {}
    for attr, value in state.persona["attributes"].items():
        if attr in domain_config["verifiable_attributes"]:
            if isinstance(value, (int, float)) and attr.endswith("budget"):
                formatted_attributes[attr] = f"${value:,}"
            else:
                formatted_attributes[attr] = str(value)
        else:
            formatted_attributes[attr] = value

    # Gradually reveal information in early turns
    early_turn = len(state.messages) < 3
    reveal_probs = (
        {"name": 0.2, "age": 0.1, "location": 0.3, "attributes": 0.4}
        if early_turn
        else {"name": 1.0, "age": 1.0, "location": 1.0, "attributes": 1.0}
    )

    # Build background section based on what we want to reveal
    background_items = []
    if random.random() < reveal_probs["name"]:
        name_context = f"You are {profile['name']}"
    else:
        name_context = f"You are a {domain_config['user_role']}"

    (
        background_items.append(f"- Age: {profile['age']}")
        if random.random() < reveal_probs["age"]
        else None
    )
    (
        background_items.append(f"- Location: {profile['location']}")
        if random.random() < reveal_probs["location"]
        else None
    )

    if random.random() < reveal_probs["attributes"]:
        background_items.extend(
            f"- {attr.replace('_', ' ').title()}: {value}"
            for attr, value in formatted_attributes.items()
        )

    background_section = (
        "\n".join(background_items)
        if background_items
        else "Share information about yourself naturally as the conversation progresses."
    )

    user_context = f"""{name_context}, having a conversation with a {domain_config["service_role"]} from {company["name"]}.

Your background and context:
{background_section}

Company context ({company["name"]}):
{company["description"]}
Product: {company["product"]}
Target Market: {company["target_market"]}

Conversation guidelines:
1. This is conversation #{state.conv_idx + 1}
2. Be natural and conversational, speaking as your role
3. Express your genuine needs and challenges
4. React authentically to suggestions
5. Share relevant details about your situation only when appropriate
6. Feel free to ask questions about {company["product"]}
7. Take time to explore topics fully - don't rush to conclusions
8. Spread the conversation over at least {num_turns // 2} turns by:
   - Asking follow-up questions
   - Sharing concerns gradually
   - Discussing different aspects of your needs
   - Taking time to consider suggestions
   - Bringing up related points naturally
   - Avoid dumping everything at once. No need for efficiency :)
   - You are only on turn {state.current_turn} of {state.num_turns}.
9. Format your response as regualr text. Do NOT include things like "**Prospect:**" or "**Sales Development Representative:**" in your response. Just respond with the text the recipient should see.


Important: Keep the conversation flowing naturally and reveal information organically.
Just respond with your next message in the conversation.
"""

    current_messages = [
        {"role": "system", "content": user_context},
        *state.messages,
    ]

    response = await generate_chat_completion(
        current_messages, temperature=0.7, which_model="user"
    )

    if not response:
        raise ValueError(
            f"Failed to generate user message at turn {state.current_turn}"
        )

    should_add_noise = random.random() < state.noise_ratio
    if len(state.messages) > 3 and should_add_noise:
        # Get domain-specific noise snippets if available
        domain_snippets = DOMAIN_NOISE.get(state.persona["domain"], NOISE_SNIPPETS)

        # 70% chance to use domain-specific noise if available
        noise = random.choice(
            domain_snippets if random.random() < 0.7 else NOISE_SNIPPETS
        )

        # Vary noise placement more naturally
        if random.random() < 0.3:  # 30% chance to insert in middle
            words = response.split()
            insert_point = len(words) // 2
            content = " ".join(words[:insert_point] + [noise] + words[insert_point:])
        elif random.random() < 0.5:  # 35% chance at start
            content = f"{noise} {response}"
        else:  # 35% chance at end
            content = f"{response} {noise}"
    else:
        content = response

    message = {
        "role": "user",
        "content": content,
        "turn": state.current_turn,
        "has_noise": should_add_noise,
    }

    # Check for information leakage
    for memory in state.active_memories:
        if memory.content.lower() in content.lower():
            state.info_leakage[memory.content] = True

    state.messages.append(message)
    state.current_turn += 1
    return state


@task
async def generate_assistant_message(state: ConversationState) -> ConversationState:
    """Generate an assistant message as part of the conversation"""
    domain_config = DOMAINS[state.persona["domain"]]
    profile = state.persona["profile"]
    company = next(
        c
        for c in COMPANY_CONTEXTS[state.persona["domain"]]
        if c["name"] == profile["company_name"]
    )

    if state.persona["domain"] == "sdr":
        role_context = f"""
Product details:
- Product: {company["product"]}
- Target market: {company["target_market"]}
- Pricing: {company["pricing_model"]}
- Key differentiator: {company["unique_value"]}
- Main competitors: {", ".join(company["competitors"])}"""

    elif state.persona["domain"] == "support":
        role_context = f"""
Support context:
- Product: {company["product"]}
- Support channels: {", ".join(company["support_channels"])}
- Documentation: {company["documentation"]}
- Common issues: {", ".join(company["common_issues"])}"""

    elif state.persona["domain"] == "tutor":
        role_context = f"""
Teaching context:
- Institution: {company["name"]}
- Subjects: {", ".join(company["subjects"])}
- Levels: {", ".join(company["levels"])}
- Approach: {company["teaching_approach"]}
- Features: {", ".join(company["platform_features"])}"""

    elif state.persona["domain"] == "real_estate":
        role_context = f"""
Agency details:
- Focus: {", ".join(company["market_focus"])}
- Service area: {company["service_area"]}
- Specialties: {", ".join(company["specialties"])}
- Approach: {company["unique_approach"]}"""
    else:
        role_context = ""

    assistant_context = f"""You are a {domain_config["service_role"]} representing {company["name"]}.

{role_context}

Your approach:
1. Listen actively and show genuine interest
2. Provide specific, actionable advice based on {company["name"]}'s offerings
3. Ask clarifying questions when needed
4. Share relevant examples and insights about {company["product"]}
5. Be encouraging but professional
6. Address their specific needs and challenges
7. Guide the conversation naturally toward solutions

Remember: Focus on building rapport while highlighting how {company["name"]} can help.
Just respond with your next message in the conversation.
"""

    current_messages = [
        {"role": "system", "content": assistant_context},
        *state.messages,
    ]

    response = await generate_chat_completion(
        current_messages, temperature=0.7, which_model="assistant"
    )

    if not response:
        raise ValueError(
            f"Failed to generate assistant message at turn {state.current_turn}"
        )

    message = {
        "role": "assistant",
        "content": response,
        "turn": state.current_turn,
    }

    state.messages.append(message)
    state.current_turn += 1
    return state


# Set up checkpointer for persistence


@task
async def generate_conversation_durable(
    state: ConversationState,
    *,
    num_turns: int = 10,
    noise_ratio: float = 0.2,
) -> Dict[str, Any]:
    """Generate a single conversation with the persona using durable execution"""
    persona = state.persona
    conv_idx = state.conv_idx
    active_memories = state.active_memories
    noise_ratio = state.noise_ratio
    num_turns = state.num_turns

    while state.current_turn < num_turns:
        if state.current_turn % 2 == 0:
            state = await generate_user_message(state, num_turns)
        else:
            state = await generate_assistant_message(state)
        state.messages[-1].pretty_print()
        if state.current_turn >= 6:
            convo = format_convo(state.messages)

            status = await did_complete_model.ainvoke(
                "Classify the status of the folloing conversation."
                f" Is it still in-progress? Explain your reasoning:\n\n{convo}"
            )
            if status.status != "in_progress":
                print(f"Stopping early! Final status: {status}")
                break

    # Check if all information was leaked
    unleaked_info = [
        content for content, leaked in state.info_leakage.items() if not leaked
    ]
    if unleaked_info:
        print(f"Warning: Failed to leak information: {unleaked_info}")
        print("Regenerating conversation...")
        return await generate_conversation_durable(
            state=state,
            num_turns=num_turns,
            noise_ratio=noise_ratio,
        )

    return {
        "conversation_id": f"{persona['id']}_conv_{conv_idx}",
        "messages": state.messages,
        "metadata": {
            "conv_index": conv_idx,
            "active_memories": [asdict(m) for m in active_memories],
            "timestamp": (datetime.now() + timedelta(days=conv_idx)).isoformat(),
            "noise_stats": {
                "noise_ratio": noise_ratio,
                "noisy_turns": sum(
                    1 for m in state.messages if m.get("has_noise", False)
                ),
                "clean_turns": sum(
                    1 for m in state.messages if not m.get("has_noise", False)
                ),
            },
            "verified_leaks": dict(state.info_leakage),
        },
    }


async def generate_conversation(
    state: ConversationState, *, previous_state=None
) -> Dict[str, Any]:
    """Generate a conversation given a state"""
    if previous_state:
        return entrypoint.final(value=previous_state, save=previous_state)
    result = await generate_conversation_durable(state=state)
    return entrypoint.final(value=result, save=state)


def generate_change_details(domain_config: Dict[str, Any], change_type: str) -> str:
    """Generate realistic change details based on domain configuration"""

    if change_type == "buying_stage":
        stages = ["awareness", "consideration", "evaluation", "decision"]
        return f"Moved to {random.choice(stages)} stage"

    elif change_type == "priorities":
        return f"New priority: {random.choice(['cost reduction', 'efficiency', 'scalability', 'security'])}"

    elif change_type == "technical_sophistication":
        levels = domain_config["verifiable_attributes"]["technical_level"]
        return f"Technical proficiency increased to {random.choice(levels)}"

    elif change_type == "academic_progress":
        subjects = ["math", "science", "history", "literature"]
        improvements = [
            "significant improvement",
            "steady progress",
            "breakthrough",
            "mastery",
        ]
        return f"{random.choice(improvements)} in {random.choice(subjects)}"

    elif change_type == "learning_preferences":
        styles = domain_config["verifiable_attributes"]["learning_style"]
        return f"Prefers {random.choice(styles)} learning methods"

    elif change_type == "client_needs":
        if "property_budget" in domain_config["verifiable_attributes"]:
            budget_spec = domain_config["verifiable_attributes"]["property_budget"]
            new_budget = (
                round(random.uniform(budget_spec["min"], budget_spec["max"]) / 1000)
                * 1000
            )
            return f"Updated budget to ${new_budget:,}"
        return "Changed property requirements"

    elif change_type == "market_conditions":
        conditions = [
            "buyer's market",
            "seller's market",
            "competitive",
            "cooling down",
        ]
        return f"Market shifted to {random.choice(conditions)}"

    elif change_type == "interest_shifts":
        if "shared_interests" in domain_config["verifiable_attributes"]:
            interests = domain_config["verifiable_attributes"]["shared_interests"]
            return f"New interest in {random.choice(interests)}"
        return "Developed new interests"

    return f"Change in {change_type}"


async def generate_test_case(
    domain: str,
    persona_idx: int,
    convs_per_phase: int = 3,
    num_changes: int = None,
) -> TestCase:
    """Generate a complete test case (persona with multiple conversations)

    Args:
        domain: Domain to generate test case for
        persona_idx: Index of this persona in the dataset
        convs_per_phase: Number of conversations per phase (initial/change)
        num_changes: Optional number of changes to generate. If None, randomly chosen.
    """
    # Create initial persona
    AsyncSqliteSaver.from_conn_string("checkpoints.db")
    persona_id = f"{domain}_persona_{persona_idx}"

    # Generate base attributes
    attributes = {}
    domain_config = DOMAINS[domain]
    for attr in domain_config["key_attributes"]:
        if attr in domain_config["verifiable_attributes"]:
            attr_spec = domain_config["verifiable_attributes"][attr]
            if isinstance(attr_spec, list):
                attributes[attr] = random.choice(attr_spec)
            elif isinstance(attr_spec, dict):
                if "min" in attr_spec and "max" in attr_spec:
                    value = random.uniform(attr_spec["min"], attr_spec["max"])
                    if attr_spec.get("unit") == "USD":
                        value = round(value / 1000) * 1000
                    attributes[attr] = value
                elif attr_spec.get("format") == "days_ago":
                    attributes[attr] = random.randint(1, 30)
        else:
            attributes[attr] = f"placeholder_{attr} (ignore this; don't mention)"

    # Generate detailed profile
    profile = generate_persona_profile(domain, attributes)

    persona = {
        "id": persona_id,
        "domain": domain,
        "attributes": attributes,
        "profile": profile,
        "relationships": {},
        "timeline": [],
    }

    # Plan changes over time
    changes = []
    if num_changes is None:
        num_changes = random.randint(2, 4)

    # Calculate total number of conversations needed
    total_phases = 1 + num_changes  # Initial persona + each change
    total_convs = total_phases * convs_per_phase

    # Assign changes to conversation indices, ensuring each change starts a new phase
    for i in range(num_changes):
        change_type = random.choice(domain_config["change_types"])
        # Place change at start of its phase (after initial phase)
        conv_idx = (i + 1) * convs_per_phase
        changes.append(
            {
                "type": change_type,
                "conversation_index": conv_idx,
                "details": generate_change_details(domain_config, change_type),
            }
        )

    # Generate conversations
    conversations = []
    expected_memories = {}
    active_memories = []

    # Initial phase: leak base persona attributes
    initial_memories = []
    for attr, value in persona["attributes"].items():
        if attr in domain_config["verifiable_attributes"]:
            # Format the value nicely if it's a verifiable attribute
            if isinstance(value, (int, float)) and attr.endswith("budget"):
                formatted_value = f"${value:,}"
            else:
                formatted_value = str(value)

            content = f"{attr}: {formatted_value}"
        else:
            content = f"{attr}: {value}"

        memory = Memory(
            content=content,
            importance=domain_config["memory_importance"].get(attr, 0.5),
            first_seen=0,
            last_updated=0,
            is_active=True,
            category="attribute",
            source_type="explicit",
        )
        initial_memories.append(memory)

    # Generate all conversations across phases
    for conv_idx in range(total_convs):
        # Update active memories when hitting a change boundary
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

        # For initial phase, use initial memories
        if conv_idx < convs_per_phase:
            memories_to_leak = initial_memories
        else:
            # For change phases, use active memories
            memories_to_leak = active_memories

        thread_id = uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"{domain}:{persona}:{conv_idx}",
        )
        config = {"configurable": {"thread_id": str(thread_id)}}
        conv = await generate_conversation.ainvoke(
            ConversationState(
                persona=persona,
                conv_idx=conv_idx,
                active_memories=memories_to_leak,
                messages=[],
                info_leakage={},
            ),
            config=config,
        )

        conversations.append(conv)

        expected_memories[conv_idx] = memories_to_leak.copy()

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
    domain: str,
    num_personas: int = 100,
    output_file: str | None = None,
    append: bool = True,
) -> Dict[str, Any]:
    """Generate a complete dataset for a domain

    Args:
        domain: Domain to generate test cases for
        num_personas: Number of personas to generate
        output_file: Optional output file path. If None, uses default naming
        append: If True and output file exists, append to it. If False, overwrite.
    """
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

    # Generate and write test cases one at a time
    with open(output_file, mode) as f:
        for i in tqdm(range(num_personas)):
            test_case = await generate_test_case(domain, i)
            test_case_dict = {"type": "test_case", "data": asdict(test_case)}
            f.write(json.dumps(test_case_dict) + "\n")
            f.flush()  # Ensure each line is written immediately

    print(f"Generated {num_personas} test cases")
    print(f"Saved to {output_file}")

    return {"file": output_file, "num_cases": num_personas}


async def main(args):
    """Generate datasets based on command line arguments"""
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

            await generate_domain_dataset(
                domain=domain,
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
        help="Output file path. Default: [domain]_dataset.jsonl",
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
