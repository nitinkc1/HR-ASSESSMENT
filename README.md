```markdown
# 🤖 HR Resource Query Chatbot

## Overview
An AI-powered HR assistant chatbot that helps HR teams quickly locate suitable employees. The system understands natural language queries about skills, experience, and project history, performs semantic search using a local RAG (Retrieval-Augmentation-Generation) engine, and delivers recommendations in a clean chat interface. All AI processing is handled locally using Llama via Ollama, ensuring privacy and offline usage.

---

## Features
- Search employees by skills, experience, project history, and availability  
- Interactive Streamlit chat interface with styled message bubbles  
- FastAPI backend with semantic search (RAG) for fast retrieval  
- Includes 30+ realistic employee profiles for testing  
- Clear, structured recommendations in natural language  
- Fully local LLM processing with Llama via Ollama (no cloud API)  
- Customizable frontend appearance (colors, layout, and styling)  
- Advanced prompt engineering for detailed and context-aware responses  

---

## Architecture
```

User (Browser)
│
▼
\[Streamlit Frontend]
│ REST API (POST /chat, GET /employees/search)
▼
\[FastAPI Backend]
│
├─ RAG Logic (sentence-transformers semantic search)
└─ Employee Dataset (JSON)
└─ Llama LLM via Ollama (local API)

````

- **Frontend:** Streamlit app for chat with responsive message bubbles  
- **Backend:** FastAPI application with endpoints for chat and employee search  
- **RAG Logic:** Embedding-based retrieval with sentence-transformers + local Llama generation  
- **Data:** JSON dataset containing 30+ employee profiles  

---

## Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/nitinkc1/HR-ASSESSMENT.git
cd HR-ASSESSMENT
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Install Ollama and Llama model**

* Download Ollama: [https://ollama.com/download](https://ollama.com/download)
* Pull a Llama model:

```bash
ollama pull llama2   # or llama3
```

* Start Ollama:

```bash
ollama run llama2
```

4. **Start the backend**

```bash
uvicorn backend.main:app --reload
```

*API available at* `http://localhost:8000`

5. **Start the frontend**

```bash
streamlit run frontend/app.py
```

*UI opens at* `http://localhost:8501`

---

## API Documentation

### POST /chat

**Purpose:** Chat with the HR assistant

**Request Example:**

```json
{ "query": "Find SQL developers with 3+ years experience" }
```

**Response Example:**

```
🤖 Based on your requirements, I found 3 strong candidates:

💼 1. Will Zhang
   - Experience: 7 years
   - Skills: Java, Spring, MySQL
   - Projects: Banking App, Inventory System
   - Availability: ✅ available

💼 2. Priya Desai
   - Experience: 2 years
   - Skills: Python, Flask, SQL
   - Projects: Inventory System, Healthcare Dashboard
   - Availability: ✅ available

💼 3. Genie
   - Experience: 4 years
   - Skills: PyTorch, Azure, C++, DevOps
   - Projects: Fleet Management, Retail Analytics
   - Availability: ✅ available
```

---

## AI Development Process

* **Tools:** ChatGPT, Cursor AI for code assistance
* **AI-assisted work (\~70%):** code generation, boilerplate, debugging, project structure
* **Manual work (\~30%):** UI fine-tuning, session handling, CSS styling, custom logic
* **Challenges solved manually:** Streamlit session state, message bubble rendering, multi-attribute ranking

---

## Technical Decisions

* **Tech Stack:** Python, FastAPI, Streamlit, sentence-transformers, scikit-learn, NumPy, Ollama
* **RAG System:** Local embeddings for fast semantic search + Llama for natural response generation
* **Reason for Local LLM:** Privacy, offline use, zero cloud costs
* **Performance & Privacy:** All data and processing remain local, ensuring security and fast response

---

## Future Improvements

* User authentication and role-based access
* Upload custom employee datasets (CSV/Excel)
* Calendar integration for scheduling
* Advanced LLM responses using multiple models
* Enhanced UI: avatars, mobile-friendly design, chat bubbles
* AI voice response and analytics dashboard

---

## Demo

<img width="1277" height="560" alt="Demo Screenshot" src="https://github.com/user-attachments/assets/bb3f6390-03e6-49d2-be68-1a8dff6d8ec6" />

---

## Troubleshooting

* Ensure both backend and frontend are running
* Ollama must be active and model pulled correctly
* Recommended Python version: 3.10 or 3.11
* Refresh browser or restart Streamlit if UI changes do not apply

---

## Notes

* Backend uses sentence-transformers for semantic search (RAG)
* Frontend is fully Streamlit-based with custom CSS styling for chat interface

```

