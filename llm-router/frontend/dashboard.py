from __future__ import annotations

import os

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = os.getenv("LLM_ROUTER_API_URL", "http://127.0.0.1:8000")


st.set_page_config(page_title="LLM Router Dashboard", layout="wide")
st.title("LLM Router Dashboard")
st.caption(
    "This dashboard lets us test prompt routing, inspect classifier confidence, "
    "and review recent routing history."
)

with st.sidebar:
    st.header("Why this page exists")
    st.write(
        "Week 1 is about proving the routing loop works end to end. "
        "We send a prompt, classify it, choose a model, and log the result."
    )
    st.write(f"API target: `{API_BASE_URL}`")


sample_prompt = st.text_area(
    "Prompt",
    height=180,
    placeholder="Example: Explain this SQL join issue and suggest how to debug it.",
)

if st.button("Route Prompt", type="primary"):
    if not sample_prompt.strip():
        st.warning("Enter a prompt first.")
    else:
        with st.spinner("Routing prompt..."):
            response = requests.post(
                f"{API_BASE_URL}/route",
                json={"prompt": sample_prompt},
                timeout=90,
            )

        if response.ok:
            result = response.json()
            left, right = st.columns(2)

            with left:
                st.subheader("Routing Result")
                st.json(result)

            with right:
                st.subheader("What happened")
                st.write(f"Predicted class: `{result['predicted_class']}`")
                st.write(f"Confidence: `{result['confidence']}`")
                st.write(f"Route: `{result['route_name']}`")
                st.write(f"Model used: `{result['model_used']}`")
                st.write(f"Fallback triggered: `{result['fallback_triggered']}`")
                st.write(
                    "Why this matters: the router can choose a cheaper local model "
                    "for simple prompts and escalate to a stronger model when needed."
                )

            st.subheader("Model Response")
            st.write(result["response"])
        else:
            st.error(response.text)


st.divider()
st.subheader("Recent Request History")
try:
    history_response = requests.get(f"{API_BASE_URL}/history", timeout=30)
    if history_response.ok:
        history = history_response.json()
        if history:
            frame = pd.DataFrame(history)
            st.dataframe(frame, use_container_width=True)
        else:
            st.info("No requests logged yet. Send a prompt to create the first record.")
    else:
        st.warning("The API returned an error while loading history.")
except requests.RequestException:
    st.warning("Could not load history yet. Make sure the FastAPI server is running.")
