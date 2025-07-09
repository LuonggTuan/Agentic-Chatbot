from langgraph.graph import StateGraph
from src.LangGraph.state.state import State
from langgraph.graph import START,END
from src.LangGraph.nodes.basic_chatbot_node import BasicChatbotNode
from src.LangGraph.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition,ToolNode
from src.LangGraph.nodes.chatbot_with_Tool_node import ChatbotWithToolNode

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """

        self.basic_chatbot_node=BasicChatbotNode(self.llm)

        # Add the basic chatbot node to the graph
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_build_graph(self):
        """
        Placeholder for building a chatbot graph with tools.
        This method can be expanded to include additional nodes and edges
        for a more complex chatbot setup.
        """
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # Define the LLM
        llm = self.llm

        # Define the chatbot node
        obj_chatbot_with_tool_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_tool_node.create_chatbot(tools)

        # Add nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        # Add edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot With WebTool":
            self.chatbot_with_tools_build_graph()

        return self.graph_builder.compile()
