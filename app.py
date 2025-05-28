import streamlit as st
import os
import json
import base64
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    copy_to_clipboard, 
    download_button, 
    download_image_button,
    display_chat_message,
    styled_expander,
    init_session_state
)

# Import feature modules
from code_interpreter import display_code_interpreter_page
from image_generation import display_image_generation_page
from web_search import display_web_search_page
from agent_orchestration import display_agent_orchestration_page
from function_calls import display_function_calls_page

# Set page configuration
st.set_page_config(
    page_title="Mistral AI Agents Explorer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 6px 6px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #e1f5fe;
        border-radius: 6px 6px 0px 0px;
    }
    
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 60vh;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: white;
    }
    
    .title-container {
        border-radius: 10px;
        padding: 20px;
        background: linear-gradient(90deg, #1E3B70 0%, #29539B 100%);
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .card {
        border-radius: 10px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .agent-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        color: white;
        background-color: #1E3B70;
        border: none;
        padding: 10px 15px;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #29539B;
        transform: scale(1.02);
    }
    
    .api-key-input input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 10px;
    }
    
    /* Custom styling for the sidebar */
    .sidebar .sidebar-content {
        background-color: #f9f9f9;
        padding: 20px;
    }
    
    /* Styling for code blocks */
    pre {
        background-color: #f7f7f7;
        border-radius: 5px;
        padding: 10px;
        overflow-x: auto;
    }
    
    code {
        font-family: monospace;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for API key configuration and navigation
with st.sidebar:
    st.image("logo-1.png", width=200)
    st.title("Mistral AI Agents Explorer")
    
    # API Key input
    st.subheader("API Configuration")
    api_key = st.text_input(
        "Enter your Mistral API Key",
        value=st.session_state.api_key,
        type="password",
        key="api_key_input",
        help="Your Mistral API key will be securely stored in session state",
        placeholder="Enter your API key here...",
    )
    
    # Update session state when API key changes
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
    
    # Navigation
    st.subheader("Navigation")
    pages = {
        "Home": "🏠",
        "Code Interpreter": "💻",
        "Image Generation": "🖼️",
        "Web Search": "🔍",
        "Agent Orchestration": "🔄",
        "Function Calls": "📞"
    }
    
    for page, icon in pages.items():
        if st.button(f"{icon} {page}", key=f"nav_{page}"):
            st.session_state.current_tab = page
            st.rerun()
    
    st.markdown("---")
    st.markdown("Made with ❤️ by AI Anytime")
    st.markdown("Powered by Mistral AI Agents API")

# Main content area
def main():
    if st.session_state.current_tab == "Home":
        display_home_page()
    elif st.session_state.current_tab == "Code Interpreter":
        display_code_interpreter_page()
    elif st.session_state.current_tab == "Image Generation":
        display_image_generation_page()
    elif st.session_state.current_tab == "Web Search":
        display_web_search_page()
    elif st.session_state.current_tab == "Agent Orchestration":
        display_agent_orchestration_page()
    elif st.session_state.current_tab == "Function Calls":
        display_function_calls_page()

# Home page function
def display_home_page():
    # Title container with gradient background
    st.markdown("""
    <div class="title-container">
        <h1>Welcome to Mistral AI Agents Explorer</h1>
        <p>A comprehensive showcase of Mistral's Agents API capabilities</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    ## About Mistral AI Agents
    
    Mistral AI's Agents API represents a significant evolution in AI technology, transforming 
    AI from a passive text generator to an active problem-solving partner. The API is built 
    around three main pillars:
    """)
    
    # Three columns for the main pillars
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="agent-icon">🔌</div>
            <h3>Built-in Connectors</h3>
            <p>Pre-built tools for code execution, web search, image generation, and more, plus MCP tool integration.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <div class="agent-icon">🧠</div>
            <h3>Persistent Memory</h3>
            <p>Maintain context and history across conversations for more consistent, meaningful interactions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <div class="agent-icon">🔄</div>
            <h3>Agent Orchestration</h3>
            <p>Coordinate multiple specialized agents to collaborate on complex multi-step tasks.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features showcase
    st.header("Features Showcase")
    st.markdown("Explore the powerful capabilities of Mistral AI Agents through our interactive demos:")
    
    # Two rows of feature cards
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    
    with row1_col1:
        st.markdown("""
        <div class="card">
            <h3>💻 Code Interpreter</h3>
            <p>Execute Python code in a secure sandbox for computation, data manipulation, and visualization.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Code Interpreter", key="try_code"):
            st.session_state.current_tab = "Code Interpreter"
            st.rerun()
    
    with row1_col2:
        st.markdown("""
        <div class="card">
            <h3>🖼️ Image Generation</h3>
            <p>Generate diverse images based on text prompts using advanced image models.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Image Generation", key="try_image"):
            st.session_state.current_tab = "Image Generation"
            st.rerun()
    
    with row1_col3:
        st.markdown("""
        <div class="card">
            <h3>🔍 Web Search</h3>
            <p>Access the latest information from the internet, overcoming LLM knowledge cut-off limitations.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Web Search", key="try_web"):
            st.session_state.current_tab = "Web Search"
            st.rerun()
    
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.markdown("""
        <div class="card">
            <h3>🔄 Agent Orchestration</h3>
            <p>Coordinate multiple agents to solve complex, multi-faceted problems collaboratively.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Agent Orchestration", key="try_orchestration"):
            st.session_state.current_tab = "Agent Orchestration"
            st.rerun()
    
    with row2_col2:
        st.markdown("""
        <div class="card">
            <h3>📞 Function Calls</h3>
            <p>Define custom functions allowing agents to interact with external APIs or proprietary systems.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Try Function Calls", key="try_function"):
            st.session_state.current_tab = "Function Calls"
            st.rerun()
    
    st.markdown("---")
    
    # Getting Started Section
    with styled_expander("Getting Started with Mistral AI Agents", expanded=False):
        st.markdown("""
        ### Prerequisites
        
        To use this application, you'll need:
        
        1. A Mistral AI API key (can be obtained from [Mistral AI's website](https://mistral.ai))
        2. Basic understanding of the different agent capabilities
        
        ### How to Use
        
        1. Enter your Mistral AI API key in the sidebar
        2. Navigate to the feature you want to explore
        3. Follow the instructions on each page to interact with the agents
        4. Enjoy the power of AI agents working for you!
        """)

# Import and execute the main function
if __name__ == "__main__":
    main()
