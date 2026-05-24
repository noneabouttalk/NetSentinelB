# NetSentinelB 🛡️

NetSentinelB is a lightweight, Python-based network monitoring tool designed to audit traffic and detect anomalies using local Artificial Intelligence. By leveraging local LLMs, it provides privacy-focused security insights without sending sensitive network data to external cloud services.


## Key Features
- **Real-time Monitoring:** Continuous tracking of network traffic.
- **AI-Powered Analysis:** Integrates with local LLMs via `llama.cpp` to analyze and interpret potential security threats.
- **Privacy-First:** All processing happens locally. No data leaves your machine.
- **Audit-Ready:** Automated logging of network events for security auditing.

## Tech Stack
- **Language:** Python 3
- **AI Engine:** [llama.cpp](https://github.com/ggerganov/llama.cpp)
- **Libraries:** `streamlit`, `subprocess`, `json`, `os`, `requests`, `time`

## Prerequisites
1. **Python 3.13** installed.
2. **Docker Desktop (Windows)** Installed.
3. **llama.cpp**: Must be compiled and configured on your system.
4. **AI Model**: A GGUF-formatted model (e.g., Llama 3, Mistral) compatible with `llama.cpp`.
5. **Model Server**: The model must be running and accessible as an API server at:
   `http://localhost:8080/v1/chat/completions`

## Configuration
Before starting the tool, ensure your settings are configured:
- **Model Path & Server:** Ensure the `llama.cpp` server is active and pointing to your model.
- **Credentials:** Store your sensitive API keys and database passwords in an environment file (`.env`) or local `config.json`. 

> **⚠️ SECURITY WARNING:** Never commit your `.env` or `config.json` files to version control. Add them to your `.gitignore` file.

## 📥 Installation
1. Clone the repository:
   git clone https://github.com/noneabouttalk/NetSentinelB.git
   cd NetSentinelB



## Usage
1. Start your llama.cpp server (ensuring it listens on localhost:8080).
2. Run the docker compose and ensure that the main.py is on the same folder where are the docker-compose.yml
   docker compose up -d --build to create the entire enviroment
3. Access the streamlit interface:
   http://localhost:8501


## ⚠️ Compatibility Warning
**NetSentinelB v1.0** is currently optimized for **Windows environments**. 
- If you are running this on Linux or macOS, please note that the file paths (specifically in `app.py`) and the network bridge configurations (in `docker-compose.yml`) may require adjustments to match your operating system's specific environment.




   
