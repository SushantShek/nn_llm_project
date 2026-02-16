# AI Person Finder

A premium web application that discovers influential leaders from **Forbes**, **Time**, and **Gartner** using AI-powered analysis.

## Features
- **Curated Intelligence**: Pulls randomly from high-profile lists of global leaders.
- **AI-Powered Insights**: Uses OpenAI (GPT-4o-mini) to generate creative descriptions and unique abilities.
- **Premium Web UI**: Modern glassmorphic interface with real-time analysis status.
- **Production Ready**: Optimized multi-stage Docker builds and FastAPI backend.

---

## 🛠 Running with Docker (Recommended)

The easiest way to run the application is using Docker Compose.

### 1. Run with a Real API Key
To see the full power of the AI, you should provide a real OpenAI API key:

```bash
env OPENAI_API_KEY="your_actual_key_here" docker-compose up --build
```

### 2. Access the Application
Once the containers are running, open your browser and navigate to:
**[http://localhost:8000](http://localhost:8000)**

---

## 💻 Local Development Setup

If you prefer to run the application outside of Docker:

### 1. Prerequisites
- Python 3.10+
- A valid OpenAI API Key

### 2. Installation
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Execution

You can run the web server directly:
```bash
export OPENAI_API_KEY="your_actual_key_here"
export PYTHONPATH=$PYTHONPATH:.
python3 -m src.api
```

Alternatively, use the provided `Makefile`:
```bash
# Setup venv and install dependencies
make build

# Run the web application (Recommended)
make run-web

# Run the backend (CLI version)
make run
```

---

## 📁 Project Structure
- `src/api.py`: FastAPI server and endpoints.
- `src/curated_data.py`: Curated data sources for Forbes, Time, and Gartner.
- `src/llm.py`: Interaction layer with OpenAI.
- `static/`: Frontend assets (HTML/CSS).
- `Dockerfile`: Multi-stage production image build.
- `docker-compose.yml`: Local orchestration and networking.
