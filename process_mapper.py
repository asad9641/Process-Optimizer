"""Agent 1: turns a messy description into a structured process map."""
from crewai import Agent, Task


def create_agent(llm) -> Agent:
    return Agent(
        role="Process Mapping Specialist",
        goal="Turn a messy process description into a clear, structured step-by-step map",
        backstory=(
            "A veteran business process analyst who documents workflows precisely "
            "and never invents steps that were not described."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )


def create_task(agent, process_text, industry, goal, callback=None) -> Task:
    return Task(
        description=(
            f"Industry/department: {industry}\n"
            f"Primary goal: {goal}\n\n"
            f"Process description:\n{process_text}\n\n"
            "Map this process. Output a numbered list of steps with: actor/role, action, "
            "system or tool used, and whether the step is manual or automated. "
            "Then list the inputs and outputs of the process. "
            "Use only facts from the description."
        ),
        expected_output=(
            "A markdown table of process steps (Step, Actor, Action, Tool, Manual/Automated) "
            "plus inputs and outputs."
        ),
        agent=agent,
        callback=callback,
    )
