# Mistral AI Agents Explorer

A comprehensive Streamlit application that showcases the capabilities of Mistral AI Agents API.

## Features

The application demonstrates the following capabilities of Mistral AI Agents:

1. **Code Interpreter** - Execute Python code in a secure sandbox for computation, data manipulation, and visualization
2. **Image Generation** - Generate diverse images based on text prompts using advanced image models
3. **Web Search** - Access the latest information from the internet, overcoming LLM knowledge cut-off limitations
4. **Agent Orchestration** - Coordinate multiple agents to solve complex, multi-faceted problems collaboratively
5. **Function Calls** - Define custom functions allowing agents to interact with external APIs or proprietary systems

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Mistral AI API Key (obtain from [Mistral AI's website](https://mistral.ai))

### Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure your `.env` file contains your Mistral API key:
   ```
   MISTRAL_API_KEY=your_api_key_here
   ```

### Running the Application

Run the Streamlit app with:

```
streamlit run app.py
```

This will start the local server and open the application in your web browser.

## Usage Guide

1. **Home Page**: Overview of Mistral AI Agents capabilities
2. **Code Interpreter**: Try running Python code examples
3. **Image Generation**: Generate images from text prompts
4. **Web Search**: Get up-to-date information from the web
5. **Agent Orchestration**: See how multiple agents can collaborate
6. **Function Calls**: Experience how agents can interact with custom functions

## Features

- Modern, responsive UI with a clean design
- Copy-to-clipboard functionality for easy code and text sharing
- Download options for responses and generated images
- Persistent conversation history maintained with Streamlit session state
- Comprehensive examples for each agent capability

## Notes

- All agent interactions require a valid Mistral AI API key
- API calls may take some time to process, especially for complex tasks
- The application is for demonstration purposes and may have limitations in production environments

## Credits

Created by AI Anytime

Powered by Mistral AI Agents API
