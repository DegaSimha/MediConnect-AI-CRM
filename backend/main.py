from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# ---------------- INIT ---------------- #
load_dotenv()
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DATABASE ---------------- #
engine = create_engine("sqlite:///./crm.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    response = Column(Text)

Base.metadata.create_all(bind=engine)

# ---------------- LLM ---------------- #
llm = ChatGroq(
    model="mixtral-8x7b-32768",   # stable working model
    api_key=os.getenv("GROQ_API_KEY")
)

class ChatRequest(BaseModel):
    message: str

# ---------------- TOOLS ---------------- #

def safe_llm_call(prompt):
    try:
        res = llm.invoke(prompt)
        return res.content
    except Exception as e:
        return f"LLM Error: {str(e)}"


# 1. Chat + Log
def chat_tool(state):
    db = SessionLocal()
    try:
        text = state.get("message", "")

        if not text:
            return {"response": "Please enter a message"}

        reply = safe_llm_call(text)

        db.add(Interaction(message=text, response=reply))
        db.commit()

        return {"response": reply}

    finally:
        db.close()


# 2. History
def get_history(state):
    db = SessionLocal()
    try:
        data = db.query(Interaction).all()

        if not data:
            return {"response": "No history found"}

        result = "\n".join(
            [f"{i.id}. {i.message} → {i.response}" for i in data]
        )

        return {"response": result}

    finally:
        db.close()


# 3. Suggest
def suggest(state):
    text = state.get("message", "")
    return {"response": safe_llm_call(f"Suggest next action: {text}")}


# 4. Summarize
def summarize(state):
    text = state.get("message", "")
    return {"response": safe_llm_call(f"Summarize: {text}")}


# 5. Edit
def edit(state):
    return {"response": "Edit feature coming soon"}


# ---------------- ROUTER ---------------- #

def router(state):
    text = state.get("message", "").lower()

    if "history" in text:
        return {"next": "history"}
    elif "suggest" in text:
        return {"next": "suggest"}
    elif "summarize" in text:
        return {"next": "summarize"}
    elif "edit" in text:
        return {"next": "edit"}
    else:
        return {"next": "chat"}


# ---------------- LANGGRAPH ---------------- #

graph = StateGraph(dict)

graph.add_node("router", router)
graph.add_node("chat", chat_tool)
graph.add_node("history", get_history)
graph.add_node("suggest", suggest)
graph.add_node("summarize", summarize)
graph.add_node("edit", edit)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    lambda state: state["next"],
    {
        "chat": "chat",
        "history": "history",
        "suggest": "suggest",
        "summarize": "summarize",
        "edit": "edit",
    }
)

for node in ["chat", "history", "suggest", "summarize", "edit"]:
    graph.add_edge(node, END)

app_graph = graph.compile()

# ---------------- ROUTES ---------------- #

@app.get("/")
def home():
    return {"message": "AI Chat Assistant Running"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        return app_graph.invoke({"message": req.message})
    except Exception as e:
        return {"response": f"Server Error: {str(e)}"}