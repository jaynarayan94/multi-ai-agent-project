import streamlit as st
import requests
import json

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi-AI Agent", layout="centered")
st.title("Multi-AI Agent Interface using Groq and Travily Search: V1.0")

system_prompt = st.text_area("Define your AI agent:", height=70)
selected_model = st.selectbox("Select AI Model:", settings.ALLOWED_MODEL_NAMES)

allow_web_search = st.checkbox("Allow Web Search", value=False)
user_query = st.text_area("Enter your query :", height=200)


API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask AI Agent") and user_query.strip():

    payload = {
            "model_name": selected_model,
            "system_prompt": system_prompt or "You are a helpful AI assistant.",
            "messages": [user_query],
            "allow_search": allow_web_search
    }       

    try:
        logger.info(f"Sending request to API with payload: {payload}")
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            agent_response = response.json().get("response", "No response from AI agent.")
            logger.info("Received response from API successfully.")
            st.subheader("AI Agent Response:")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
            # st.write(agent_response)
        else:
            error_detail = response.json().get("detail", "Unknown error occurred.")
            logger.error(f"API Error {response.status_code}: {error_detail}")
            st.error(f"Error {response.status_code}: {error_detail}")

    except Exception as e:
        custom_error = CustomException("Failed to get response from API", e)
        logger.error(f"Exception occurred: {custom_error}")
        st.error(f"An error occurred: {custom_error}")
