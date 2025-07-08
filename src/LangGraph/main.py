import streamlit as st
from src.LangGraph.ui.streamlitui.loadui import LoadStreamlitUI
from src.LangGraph.LLMs.groqllm import GroqLLM
from src.LangGraph.graph.graph_builder import GraphBuilder
from src.LangGraph.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """Load the LangGraph Agentic AI app with Streamlit UI."""
    UI = LoadStreamlitUI()
    user_input = UI.load_streamlit_ui()

    if not user_input:
        st.error("Failed to load user inputs. Please check your configuration.")
        return
    
    user_message = st.chat_input("Enter your message: ")

    if user_message:
        try:
            ## Configure The LLM's
            obj_llm_config=GroqLLM(user_contols_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            # Initialize and set up the graph based on use case
            usecase=user_input.get("selected_usecase")

            if not usecase:
                    st.error("Error: No use case selected.")
                    return
            
            ## Graph Builder

            graph_builder=GraphBuilder(model)
            try:
                 graph=graph_builder.setup_graph(usecase)
                 print(user_message)
                 DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                 st.error(f"Error: Graph set up failed- {e}")
                 return

        except Exception as e:
             st.error(f"Error: Graph set up failed- {e}")
             return   

    