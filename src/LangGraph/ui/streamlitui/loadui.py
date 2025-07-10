import streamlit as st
import os

from src.LangGraph.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            # User choose Groq LLM 
            if self.user_controls["selected_llm"] == "Groq":
                groq_model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", groq_model_options)
                self.user_controls["API_KEY"] = st.session_state["API_KEY"] = st.text_input("API Key", type="password")
                # Validate API key
                if not self.user_controls["API_KEY"]:
                    st.warning("Please enter your API key to proceed.")
            elif self.user_controls["selected_llm"] == "OpenAI":
                openai_model_options = self.config.get_openai_model_options()
                self.user_controls["selected_openai_model"] = st.selectbox("Select Model", openai_model_options)
                self.user_controls["API_KEY"] = st.session_state["API_KEY"] = st.text_input("API Key", type="password")
                # Validate API key
                if not self.user_controls["API_KEY"]:
                    st.warning("Please enter your API key to proceed.")
            # Usecase selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)

            if self.user_controls["selected_usecase"] == "Chatbot With WebTool" or self.user_controls["selected_usecase"] == "AI News":
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API Key", type="password")
                # Validate TAVILY API key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY API key to proceed.")

            if self.user_controls["selected_usecase"] == "AI News":
                st.subheader("AI News Explorer ")

                with st.sidebar:
                    time_frame = st.selectbox(
                        "Select Time Frame", 
                        ["Daily", "Weekly", "Monthly", "Yearly"],
                        index=0
                    )
                if st.button("Fetch AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.time_frame = time_frame
                
        return self.user_controls