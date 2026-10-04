"""Agent 2: finds delays, waste and risks in the mapped process."""
from crewai import Agent, Task


def create_agent(llm) -> Agent:
    return Agent(
        role="Bottleneck and Waste Analyst",
        goal="Find delays, manual handoffs, rework, and risks in the mapped process",
        backstory=(
            "A Lean Six Sigma black belt who spots waste (waiting, rework, manual effort, "
            "errors) and explains its business impact."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def create_task(agent, goal, context, callback=None) -> Task:
    return Task(
        description=(
            f"Primary goal: {goal}.\n"
            "Using the process map, identify the top 5 bottlenecks or wastes. For each give: "
            "where it happens, why it hurts, and a rough quantified impact "
            "(state assumptions clearly). Add a short list of risks."
        ),
        expected_output=(
            "A markdown table of bottlenecks (Issue, Step, Impact, Severity High/Med/Low) "
            "and a short risks list."
        ),
        agent=agent,
        context=context,
        callback=callback,
    )
