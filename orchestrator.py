"""Connects the four agents into one sequential CrewAI workflow."""
import time

from crewai import Crew, Process

from crew_agents import process_mapper, bottleneck_analyst, automation_scorer, roadmap_writer
from llm import get_llm

# Groq's free tier limits tokens per minute, so we pause between agents.
PAUSE_SECONDS = 30
TOTAL_AGENTS = 4


def run_optimization(process_text, industry, goal, model_id, api_key, on_task_done=None):
    """Runs all agents in order and returns their outputs as a dict."""
    llm = get_llm(model_id, api_key)

    state = {"done": 0}

    def paced_callback(output):
        state["done"] += 1
        if on_task_done:
            on_task_done(output)          # update the progress bar first
        if state["done"] < TOTAL_AGENTS:
            time.sleep(PAUSE_SECONDS)     # let the token budget refill

    # 1) Create the agents
    a1 = process_mapper.create_agent(llm)
    a2 = bottleneck_analyst.create_agent(llm)
    a3 = automation_scorer.create_agent(llm)
    a4 = roadmap_writer.create_agent(llm)

    # 2) Create the tasks; each one receives the earlier tasks' results as context
    t1 = process_mapper.create_task(a1, process_text, industry, goal, paced_callback)
    t2 = bottleneck_analyst.create_task(a2, goal, [t1], paced_callback)
    t3 = automation_scorer.create_task(a3, [t1, t2], paced_callback)
    t4 = roadmap_writer.create_task(a4, goal, [t1, t2, t3], paced_callback)

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
