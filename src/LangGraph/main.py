import streamlit as st
from src.LangGraph.ui.streamlitui.loadui import LoadStreamlitUI

def load_langgraph_agenticai_app():
    """Load the LangGraph Agentic AI app with Streamlit UI."""
    UI = LoadStreamlitUI()
    user_inputs = UI.load_streamlit_ui()

    if not user_inputs:
        st.error("Failed to load user inputs. Please check your configuration.")
        return
    
    user_messages = st.chat_input("Enter your message: ")

    