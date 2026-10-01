"""Agent 3: proposes and ranks automation / AI opportunities."""
from crewai import Agent, Task


def create_agent(llm) -> Agent:
    return Agent(
        role="Automation Opportunity Scorer",
        goal="Rank where AI, workflow tools and automation will give the highest return",
        backstory=(
            "An automation architect who knows RPA, workflow engines, GenAI and AI agents, "
            "and scores ideas on impact versus effort realistically."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def create_task(agent, context, callback=None) -> Task:
    return Task(
        description=(
            "For each bottleneck, propose an improvement using AI, workflow automation, or "
            "simple process redesign. Score each 1-5 for Business Impact and 1-5 for Ease of "
            "Implementation, compute Priority = Impact x Ease, and sort by priority. "
            "Name the technology type (e.g. workflow engine, document AI, GenAI assistant, "
            "AI agent)."
        ),
        expected_output=(
            "A markdown table sorted by priority: Opportunity, Technology, Impact, Ease, "
            "Priority, Estimated time saved."
        ),
        agent=agent,
        context=context,
        callback=callback,
    )
