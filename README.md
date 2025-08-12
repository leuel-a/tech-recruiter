# Tech Recruiter AI Agent

Tech Recruiter is an AI-powered application designed to streamline the technical recruitment process by analyzing GitHub profiles to assess candidate suitability for specific roles.

## 📝 Overview

This project leverages the power of Large Language Models (LLMs) through the LangChain and LangGraph frameworks to create an autonomous agent. The agent can browse a candidate's GitHub profile, analyze their repositories and activities, and provide an informed assessment based on a job description.

The application is served through a web interface built with Streamlit, allowing recruiters to easily input a candidate's GitHub URL and a job description to receive an AI-generated analysis.

## ✨ Key Features

- **AI-Powered Candidate Analysis:** Utilizes an AI agent to perform in-depth analysis of a candidate's GitHub profile.
- **Job Description Matching:** Assesses candidate repositories and contributions against a provided job description.
- **Web-Based UI:** Simple and intuitive interface built with Streamlit for easy interaction.
- **Asynchronous Backend:** Built with FastAPI to handle requests efficiently.
- **Extensible Agent Design:** The agent's capabilities can be expanded with new tools and chains.

## 🛠️ Technology Stack

- **Backend:** FastAPI, Uvicorn
- **AI Agent:** LangChain, LangGraph
- **Frontend:** Streamlit
- **Data Handling:** Pandas
- **Web Scraping:** BeautifulSoup4

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An OpenAI API key (or other compatible LLM provider)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/tech-recruiter.git
    cd tech-recruiter
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root of the project and add your API key:
    ```
    OPENAI_API_KEY="your_openai_api_key"
    ```

### Running the Application

This project consists of a FastAPI backend and a Streamlit frontend.

1.  **Run the FastAPI backend:**
    ```bash
    uvicorn client.main:app --host 0.0.0.0 --port 8000
    ```

2.  **Run the Streamlit frontend in a separate terminal:**
    ```bash
    streamlit run client/main.py
    ```

Once running, open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## 📂 Project Structure

```
/home/leuel/projects/leuela/tech-recuiter/
├───agent/              # Core AI agent logic (LangChain/LangGraph)
├───client/             # Frontend (Streamlit) and API (FastAPI)
├───config/             # Application configuration
├───shared/             # Shared data models
├───tests/              # Tests for the application
├───.gitignore
├───pyproject.toml
├───README.md
└───requirements.txt
```