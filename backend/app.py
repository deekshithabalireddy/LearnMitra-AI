
import requests
import json
import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

from backend.database import history_collection


# Load environment variables
load_dotenv()

# n8n Production Webhook
N8N_WEBHOOK_URL = "https://learnmitra-ai.app.n8n.cloud/webhook/learnmitra-activity"


# Send activity details to n8n
def notify_n8n(activity_type, topic, language):

    try:
        requests.post(
            N8N_WEBHOOK_URL,
            json={
                "userId": "student-101",
                "activityType": activity_type,
                "topic": topic,
                "language": language,
                "timestamp": datetime.now().isoformat()
            },
            timeout=5
        )

    except requests.RequestException as error:
        print("n8n notification failed:", error)


# Create FastAPI application
app = FastAPI(
    title="LearnMitra-AI",
    description="AI-powered Vernacular Education and Translation Platform",
    version="1.0.0"
)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Request Models
class TranslateRequest(BaseModel):
    text: str
    source_language: str
    target_language: str


class ExplainRequest(BaseModel):
    topic: str
    language: str


class QuizRequest(BaseModel):
    topic: str
    language: str


class ChatRequest(BaseModel):
    message: str
    language: str


class AgentRequest(BaseModel):
    message: str
    language: str = "English"


# Home Route
@app.get("/")
def home():
    return {
        "message": "Welcome to LearnMitra-AI",
        "status": "Backend is running successfully"
    }


# Health Check
@app.get("/health")
def health():
    return {"status": "healthy"}


# AI Translation
@app.post("/translate")
def translate(request: TranslateRequest):

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Please enter some text.")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is not configured."
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        Translate the following text from
        {request.source_language} to {request.target_language}.

        Use simple and natural language.

        Text: {request.text}

        Return only the translated text.
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        history_collection.insert_one({
            "activity_type": "translation",
            "input": request.text,
            "source_language": request.source_language,
            "target_language": request.target_language,
            "result": response.text,
            "created_at": datetime.now()
        })

        notify_n8n(
            "translation",
            request.text,
            request.target_language
        )

        return {
            "translation": response.text
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(error)}"
        )


# AI Learning Assistant
@app.post("/explain")
def explain_topic(request: ExplainRequest):

    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Please enter a topic.")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is not configured."
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        Explain the topic '{request.topic}'
        in {request.language}.

        Use simple words and student-friendly examples.
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        history_collection.insert_one({
            "activity_type": "explanation",
            "input": request.topic,
            "language": request.language,
            "result": response.text,
            "created_at": datetime.now()
        })

        notify_n8n(
            "explanation",
            request.topic,
            request.language
        )

        return {
            "topic": request.topic,
            "explanation": response.text
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Explanation failed: {str(error)}"
        )


# AI Quiz Generation
@app.post("/generate-quiz")
def generate_quiz(request: QuizRequest):

    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Please enter a topic.")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is not configured."
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        Generate 5 multiple-choice questions about
        {request.topic} in {request.language}.

        Return only valid JSON in this format:
        {{
            "questions": [
                {{
                    "question": "Question text",
                    "options": ["A", "B", "C", "D"],
                    "answer": "Correct option"
                }}
            ]
        }}
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        quiz_text = response.text.strip()
        quiz_text = quiz_text.replace("```json", "")
        quiz_text = quiz_text.replace("```", "").strip()

        quiz_data = json.loads(quiz_text)

        history_collection.insert_one({
            "activity_type": "quiz",
            "input": request.topic,
            "language": request.language,
            "result": quiz_data,
            "created_at": datetime.now()
        })

        notify_n8n(
            "quiz",
            request.topic,
            request.language
        )

        return quiz_data

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Quiz generation failed: {str(error)}"
        )


# AI Chatbot
@app.post("/chat")
def chat_with_ai(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Please enter your question.")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is not configured."
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are LearnMitra-AI, a friendly educational assistant.

        Answer in {request.language}.
        Use simple words and student-friendly examples.

        Question: {request.message}
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        history_collection.insert_one({
            "activity_type": "chat",
            "input": request.message,
            "language": request.language,
            "result": response.text,
            "created_at": datetime.now()
        })

        notify_n8n(
            "chat",
            request.message,
            request.language
        )

        return {
            "question": request.message,
            "answer": response.text
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(error)}"
        )


# Get Learning History
@app.get("/history")
def get_learning_history():

    try:
        history = list(
            history_collection.find(
                {},
                {"_id": 0}
            ).sort("created_at", -1)
        )

        return {
            "total_records": len(history),
            "history": history
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to fetch learning history: {str(error)}"
        )


# Agentic AI Router
@app.post("/agent")
def learning_agent(request: AgentRequest):

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Please enter your request.")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is not configured."
        )

    try:
        client = genai.Client(api_key=api_key)

        # Step 1: Identify user's intention
        classify_prompt = f"""
        You are the task-routing agent for LearnMitra-AI.

        Select exactly one action:
        translate, explain, quiz, chat.

        Extract the relevant topic or text.

        For translation, identify source and target languages.
        If source language is not specified, use English.
        If target language is unclear, use {request.language}.

        User request: {request.message}

        Return ONLY valid JSON:
        {{
            "action": "explain",
            "content": "photosynthesis",
            "source_language": "English",
            "target_language": "Telugu"
        }}
        """

        classification = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=classify_prompt
        )

        classification_text = classification.text.strip()
        classification_text = classification_text.replace("```json", "")
        classification_text = classification_text.replace("```", "").strip()

        action_data = json.loads(classification_text)

        action = action_data.get("action", "").lower()
        content = action_data.get("content", request.message)

        # Step 2: Execute the selected function
        if action == "translate":

            source_language = action_data.get(
                "source_language", "English"
            )

            target_language = action_data.get(
                "target_language", request.language
            )

            result = translate(
                TranslateRequest(
                    text=content,
                    source_language=source_language,
                    target_language=target_language
                )
            )

            output = result["translation"]

        elif action == "explain":

            result = explain_topic(
                ExplainRequest(
                    topic=content,
                    language=request.language
                )
            )

            output = result["explanation"]

        elif action == "quiz":

            result = generate_quiz(
                QuizRequest(
                    topic=content,
                    language=request.language
                )
            )

            output = result

        elif action == "chat":

            result = chat_with_ai(
                ChatRequest(
                    message=request.message,
                    language=request.language
                )
            )

            output = result["answer"]

        else:
            raise HTTPException(
                status_code=400,
                detail="Agent could not identify a valid task."
            )

        # Existing functions save the activity in MongoDB
        # and send the activity notification to n8n.

        return {
            "agent": "LearnMitra-AI Agent",
            "selected_action": action,
            "response": output,
            "message": "Task completed successfully."
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Agent failed: {str(error)}"
        )
