# 🧠 AI-Powered CRM (HCP Interaction Assistant)

## 📌 Overview

This project is an AI-powered CRM system designed to log, manage, and analyze interactions with healthcare professionals (HCPs).
It combines a chat-based assistant with structured form input, enabling efficient tracking of doctor interactions.

---

## 🚀 Features

* 💬 Chat-based AI assistant (like ChatGPT)
* 📝 Form-based interaction logging
* 🧠 AI-powered summarization & suggestions
* 🔀 Smart tool routing using LangGraph
* 📊 Interaction history tracking
* 💾 SQL database (SQLite)
* 🎨 Modern React dashboard UI

---

## 🏗️ Tech Stack

### 🔹 Frontend

* React.js
* Axios
* CSS (custom dashboard UI)

### 🔹 Backend

* FastAPI
* LangGraph (multi-tool agent)
* Groq LLM (Mixtral model)
* SQLAlchemy ORM
* SQLite database

---

## 🧠 AI Capabilities

The system uses an LLM to:

* Summarize interactions
* Suggest next actions
* Respond conversationally
* Assist with CRM workflows

---

## ⚙️ Project Structure

```
MediConnect-AI-CRM/
│
├── backend/
│   ├── main.py
│   ├── crm.db
│   ├── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│
├── README.md
```

---

## ⚙️ Setup Instructions

### 🔹 1. Clone Repository

```
git clone <your-repo-url>
cd MediConnect-AI-CRM
```

---

### 🔹 2. Backend Setup

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy python-dotenv langchain-groq langgraph
```

Create `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

Run backend:

```
python -m uvicorn main:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### 🔹 3. Frontend Setup

```
cd frontend
npm install
npm start
```

Frontend runs on:

```
http://localhost:3000
```

---

## 🔄 How It Works

1. User sends message via chat or form
2. Frontend sends request to backend
3. LangGraph routes request to correct tool
4. LLM generates response
5. Data is stored in database
6. Response is returned to UI

---

## 🗄️ Database Design

Table: `interactions`

| Column   | Description |
| -------- | ----------- |
| id       | Primary key |
| message  | User input  |
| response | AI output   |

---

## 🧪 Sample Inputs

* "I met Dr Rao and discussed diabetes treatment"
* "suggest next action"
* "show history"
* "summarize this conversation"

---

## 🎯 Use Case

Designed for:

* Pharma representatives
* Healthcare CRM systems
* Medical interaction tracking

---

## 🔥 Future Improvements

* User authentication (login system)
* Cloud deployment (AWS/Render)
* PostgreSQL integration
* Better UI/UX enhancements
* Real-time analytics dashboard

---

## 🎤 Demo Explanation

This project demonstrates:

* AI integration in real-world CRM
* Multi-tool orchestration using LangGraph
* Full-stack development (React + FastAPI)
* Database integration

---

## 👨‍💻 Author

Your Name
Final Year Student / Fresher

---

## ⭐ Conclusion

This project showcases how AI can enhance CRM systems by automating interaction logging, generating insights, and improving workflow efficiency.
