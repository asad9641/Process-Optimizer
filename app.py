"""Streamlit UI only. All AI logic lives in orchestrator.py and agents/."""
# --- SQLite fix for Streamlit Cloud (must run before crewai is imported) ---
import sys
try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import os
import streamlit as st

from config import MODELS, GOALS, AGENT_STEPS, SAMPLE_PROCESS
from orchestrator import run_optimization

st.set_page_config(page_title="AI Process Optimizer", page_icon="⚙️", layout="wide")


def get_secret_key():
    try:
        return st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        return os.getenv("GROQ_API_KEY", "")


st.title("⚙️ AI Process Optimizer")
st.caption("A team of 4 AI agents that maps your process, finds bottlenecks, "
           "scores automation opportunities, and writes an improvement roadmap.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Groq API key", value=get_secret_key(), type="password",
                            help="Get a free key at console.groq.com")
    model_label = st.selectbox("Model", list(MODELS.keys()))
    st.markdown("---")
    st.markdown("**Agent team**")
    for i, name in enumerate(AGENT_STEPS, 1):
        st.markdown(f"{i}. {name}")

col1, col2 = st.columns([2, 1])
with col2:
    industry = st.text_input("Industry / department", "Human Resources")
    goal = st.selectbox("Primary goal", GOALS)
    if st.button("Load sample process"):
        st.session_state["process_text"] = SAMPLE_PROCESS
with col1:
    process_text = st.text_area(
        "Describe your business process in plain words",
        value=st.session_state.get("process_text", ""),
        height=280,
        placeholder="Describe the steps, who does them, tools used, delays, volumes...",
    )

if st.button("🚀 Optimize my process", type="primary"):
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar.")
    elif len(process_text.strip()) < 40:
        st.warning("Please describe the process in a bit more detail (or load the sample).")
    else:
        progress = st.progress(0, text="Starting agents...")
        done = {"n": 0}

        def on_task_done(_output):
            done["n"] += 1
            n = done["n"]
            nxt = AGENT_STEPS[n] if n < len(AGENT_STEPS) else "Finalizing"
            progress.progress(n / len(AGENT_STEPS),
                              text=f"✅ {AGENT_STEPS[n-1]} finished → next: {nxt}")

        try:
            st.session_state["results"] = run_optimization(
                process_text, industry, goal, MODELS[model_label], api_key, on_task_done
            )
            progress.progress(1.0, text="All agents finished ✅")
        except Exception as e:
            progress.empty()
            st.error(f"Something went wrong: {e}")
            st.info("If you see a rate-limit error, wait a minute or switch to the 8B model.")

if "results" in st.session_state:
    r = st.session_state["results"]
    tabs = st.tabs(["🗺️ Process Map", "🔍 Bottlenecks", "🤖 Automation Opportunities", "📋 Roadmap"])
    for tab, key in zip(tabs, ["process_map", "bottlenecks", "opportunities", "roadmap"]):
        with tab:
            st.markdown(r[key])

    report = (
        "# AI Process Optimization Report\n\n"
        f"**Industry:** {industry}  \n**Goal:** {goal}\n\n"
        "## 1. Process Map\n" + r["process_map"] +
        "\n\n## 2. Bottlenecks\n" + r["bottlenecks"] +
        "\n\n## 3. Automation Opportunities\n" + r["opportunities"] +
        "\n\n## 4. Roadmap\n" + r["roadmap"]
    )
    st.download_button("⬇️ Download full report (.md)", report,
                       file_name="process_optimization_report.md", mime="text/markdown")
