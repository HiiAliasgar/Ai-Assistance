<h1 align="center">AI Assistant</h1>

<p align="center">
  <b>Simple AI assistant using LangChain with tool-use capabilities</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge" alt="LangChain" />
  <img src="https://img.shields.io/badge/Groq-FF6B6B?style=for-the-badge" alt="Groq" />
</p>

---

## Overview

A Python script that creates a simple AI assistant using LangChain's Groq chat model and a React agent. It includes tool functions for calculation and greeting, then runs a loop to take user input and call the agent to respond.

### Features

| Feature | Description |
|---------|-------------|
| 🧠 AI Chat | Natural language conversation |
| 🔧 Tool Use | Calculator and greeting tools |
| ⚡ Fast inference | Powered by Groq's fast inference |
| 🔄 React Agent | Multi-step reasoning capability |

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/HiiAliasgar/Ai-Assistance.git
cd Ai-Assistance
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install langchain langchain-groq python-dotenv
```

### 4. Set up API key

```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 5. Run the assistant

```bash
python main.py
```

---

## How It Works

1. **Initialize** the Groq chat model via LangChain
2. **Define tools** (calculator, greeting)
3. **Create React agent** that can use tools
4. **Chat loop** takes user input and responds

---

## Project Structure

```
Ai-Assistance/
├── main.py           # Main application
├── .env              # Environment variables (not committed)
├── .gitignore        # Git ignore rules
├── .python-version   # Python version
├── pyproject.toml    # Project configuration
└── uv.lock          # Dependency lock file
```

---

## Author

**Aliasgar Lohawala** - [@HiiAliasgar](https://github.com/HiiAliasgar)

---

<p align="center">
  Made with ❤️ and LangChain
</p>
