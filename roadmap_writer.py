"""Agent 4: writes the executive improvement roadmap."""
from crewai import Agent, Task


def create_agent(llm) -> Agent:
    return Agent(
        role="Transformation Roadmap Writer",
        goal="Create a practical, executive-ready improvement roadmap",
        backstory=(
            "A senior consultant who writes concise, decision-oriented plans that leaders "
            "can approve quickly."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def create_task(agent, goal, context, callback=None) -> Task:
    return Task(
        description=(
            f"Write an executive roadmap to achieve the goal '{goal}'. Include: "
            "1) a 3-sentence executive summary, 2) Quick wins (0-30 days), "
            "3) Medium term (1-3 months), 4) Long term (3-6 months), "
            "5) expected benefits with stated assumptions, "
            "6) key risks and how to manage them. Be concise and specific."
        ),
        expected_output="A concise markdown roadmap with the 6 sections above.",
        agent=agent,
        context=context,
        callback=callback,
    )
