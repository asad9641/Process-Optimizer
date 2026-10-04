"""Connects the four agents into one sequential CrewAI workflow."""
from crewai import Crew, Process

from crew_agents import process_mapper, bottleneck_analyst, automation_scorer, roadmap_writer
from llm import get_llm


def run_optimization(process_text, industry, goal, model_id, api_key, on_task_done=None):
    """Runs all agents in order and returns their outputs as a dict."""
    llm = get_llm(model_id, api_key)

    # 1) Create the agents
    a1 = process_mapper.create_agent(llm)
    a2 = bottleneck_analyst.create_agent(llm)
    a3 = automation_scorer.create_agent(llm)
    a4 = roadmap_writer.create_agent(llm)

    # 2) Create the tasks; each one receives the earlier tasks' results as context
    t1 = process_mapper.create_task(a1, process_text, industry, goal, on_task_done)
    t2 = bottleneck_analyst.create_task(a2, goal, [t1], on_task_done)
    t3 = automation_scorer.create_task(a3, [t1, t2], on_task_done)
    t4 = roadmap_writer.create_task(a4, goal, [t1, t2, t3], on_task_done)

    # 3) Run the crew
    crew = Crew(
        agents=[a1, a2, a3, a4],
        tasks=[t1, t2, t3, t4],
        process=Process.sequential,
        verbose=False,
    )
    crew.kickoff()

    return {
        "process_map": t1.output.raw,
        "bottlenecks": t2.output.raw,
        "opportunities": t3.output.raw,
        "roadmap": t4.output.raw,
    }
