import base64
import json
import os
import streamlit as st
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
import io

# Function to copy text to clipboard using JavaScript
def copy_to_clipboard(text: str, button_text: str = "Copy to clipboard"):
    """
    Creates a button that copies the provided text to clipboard when clicked.
    
    Args:
        text: The text to copy to clipboard
        button_text: The text to display on the button
    """
    if text:
        # Create a unique key for this button
        unique_key = f"copy_btn_{abs(hash(text)) % 10000}"
        
        # JavaScript to copy text to clipboard
        js_code = f"""
        <script>
        function copyToClipboard{unique_key}() {{
            const el = document.createElement('textarea');
            el.value = `{text.replace('`', '\\`')}`;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
            
            // Show a toast notification
            const toast = document.createElement('div');
            toast.style.position = 'fixed';
            toast.style.bottom = '20px';
            toast.style.left = '50%';
            toast.style.transform = 'translateX(-50%)';
            toast.style.backgroundColor = '#4CAF50';
            toast.style.color = 'white';
            toast.style.padding = '16px';
            toast.style.borderRadius = '4px';
            toast.style.zIndex = '1000';
            toast.innerHTML = 'Copied to clipboard!';
            document.body.appendChild(toast);
            
            // Remove the toast after 2 seconds
            setTimeout(() => {{
                toast.style.opacity = '0';
                toast.style.transition = 'opacity 0.5s';
                setTimeout(() => document.body.removeChild(toast), 500);
            }}, 2000);
        }}
        </script>
        <button 
            onclick="copyToClipboard{unique_key}()" 
            style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 4px;"
        >
            {button_text}
        </button>
        """
        st.components.v1.html(js_code, height=50)

# Function to create a download button for text content
def download_button(content: str, file_name: str, button_text: str):
    """
    Creates a download button for the provided content
    
    Args:
        content: The content to download
        file_name: The name of the file to download
        button_text: The text to display on the button
    """
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{file_name}" style="background-color: #008CBA; color: white; border: none; padding: 8px 16px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">{button_text}</a>'
    st.markdown(href, unsafe_allow_html=True)

# Function to download images
def download_image_button(image_data, file_name, button_text="Download Image"):
    """
    Creates a download button for image data
    
    Args:
        image_data: The image data as bytes or PIL Image
        file_name: The name of the file to download
        button_text: The text to display on the button
    """
    if isinstance(image_data, Image.Image):
        buf = io.BytesIO()
        image_data.save(buf, format='PNG')
        image_bytes = buf.getvalue()
    else:
        image_bytes = image_data
        
    b64 = base64.b64encode(image_bytes).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{file_name}" style="background-color: #008CBA; color: white; border: none; padding: 8px 16px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">{button_text}</a>'
    st.markdown(href, unsafe_allow_html=True)

# Custom styling for chat messages
def message_styling(is_user: bool):
    """Returns the styling for a chat message based on whether it's from the user or the AI"""
    if is_user:
        return {
            "background-color": "#F0F2F6",
            "border-radius": "10px",
            "padding": "10px",
            "margin": "5px 0",
            "max-width": "80%",
            "align-self": "flex-end",
            "font-family": "Arial, sans-serif"
        }
    else:
        return {
            "background-color": "#E1F5FE",
            "border-radius": "10px",
            "padding": "10px",
            "margin": "5px 0",
            "max-width": "80%",
            "align-self": "flex-start",
            "font-family": "Arial, sans-serif"
        }

# Function to display chat messages
def display_chat_message(message, is_user: bool, with_copy_button: bool = True):
    """
    Displays a chat message with proper styling
    
    Args:
        message: The message content (can be a string or other object)
        is_user: Whether the message is from the user (True) or AI (False)
        with_copy_button: Whether to include a copy button (default: True)
    """
    style = message_styling(is_user)
    
    # Convert the style dict to inline CSS
    style_str = "; ".join([f"{k}: {v}" for k, v in style.items()])
    
    # Ensure message is a string
    if not isinstance(message, str):
        try:
            # Try to convert to string if it's not already
            message_str = str(message)
        except Exception:
            message_str = "[Content cannot be displayed as text]"
    else:
        message_str = message
    
    # Create the HTML for the message container
    msg_html = f'<div style="{style_str}">{message_str}</div>'
    st.markdown(msg_html, unsafe_allow_html=True)
    
    # Add copy and download buttons for AI messages
    if not is_user and with_copy_button and isinstance(message, str) and message.strip():
        col1, col2 = st.columns(2)
        with col1:
            # Use a safe text value for copy operations
            copy_to_clipboard(message_str, "Copy Response")
        with col2:
            download_button(message_str, "response.txt", "Download Response")

# Helper function to create styled expanders
def styled_expander(title, expanded=False):
    """
    Creates a styled expander with custom CSS
    
    Args:
        title: The title of the expander
        expanded: Whether the expander is expanded by default
    """
    # Custom CSS for the expander
    st.markdown("""
    <style>
    .styled-expander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .styled-expander-header {
        font-weight: bold;
        cursor: pointer;
        padding: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    return st.expander(title, expanded=expanded)

# Initialize session state variables if they don't exist
def init_session_state():
    """Initialize all session state variables if they don't exist"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "Home"
    
    if 'code_interpreter_history' not in st.session_state:
        st.session_state.code_interpreter_history = []
    
    if 'image_generation_history' not in st.session_state:
        st.session_state.image_generation_history = []
    
    if 'web_search_history' not in st.session_state:
        st.session_state.web_search_history = []
    
    if 'orchestration_history' not in st.session_state:
        st.session_state.orchestration_history = []
    
    if 'function_calls_history' not in st.session_state:
        st.session_state.function_calls_history = []
    
    if 'api_key' not in st.session_state:
        # Try to load from .env file
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("MISTRAL_API_KEY", "")
            st.session_state.api_key = api_key
        except:
            st.session_state.api_key = ""
