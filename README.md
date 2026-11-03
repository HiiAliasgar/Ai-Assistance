# AI Assistant

A small Python command-line assistant built with LangChain and Groq. It demonstrates connecting a chat model to a set of application-defined tools and running an interactive conversation loop.

## What it demonstrates

- Initializing a Groq chat model through LangChain.
- Defining simple tools such as calculation and greeting.
- Connecting tools to a ReAct-style agent.
- Accepting user input in a command-line loop.

## Technology

- Python
- LangChain
- langchain-groq
- Groq API
- python-dotenv

## Setup

```bash
git clone https://github.com/HiiAliasgar/Ai-Assistance.git
cd Ai-Assistance

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install langchain langchain-groq python-dotenv
```

Create a local `.env` file and add:

```env
GROQ_API_KEY=your_groq_api_key
```

Run:

```bash
python main.py
```

## Learning scope

This is an introductory tool-calling example, not a production conversational platform. Tool coverage, error handling, persistence and evaluation should be expanded before using it in a real workflow.

[Source code](https://github.com/HiiAliasgar/Ai-Assistance)
