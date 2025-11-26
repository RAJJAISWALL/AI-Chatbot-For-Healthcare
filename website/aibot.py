import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import google.generativeai as genai

from .models import ChatMessage
from . import db

# Load .env and configure Gemini
ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

aibot = Blueprint("aibot", __name__)

SYSTEM_PROMPT = """
You are a friendly AI assistant for a student project about Artificial Intelligence in Healthcare.

Rules:
- Explain things in clear, simple, conversational language.
- You can talk about AI in medicine, diagnostics, hospitals, healthcare systems, etc.
- YOU ARE NOT A DOCTOR.
- Do NOT give diagnoses, treatment plans, or prescriptions.
- For any serious or personal medical concern, always tell the user to consult a qualified doctor.
- Keep replies concise but helpful.
"""

# Preferred Gemini model; override with GEMINI_MODEL in env if needed.
MODEL_ID = os.getenv("GEMINI_MODEL", "gemini-1.0-pro")


# ------------------------------
# HOME: show chat history
# ------------------------------
@aibot.route("/", methods=["GET"])
@login_required
def home():
    history = []

    msgs = (
        ChatMessage.query
        .filter_by(user_id=current_user.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    for m in msgs:
        history.append(
            {
                "sender": m.sender,
                "text": m.text,
                "time": m.created_at.strftime("%I:%M %p") if m.created_at else "",
            }
        )

    return render_template("index.html", user=current_user, history=history)


# ------------------------------
# Helper: BASIC AI (no history)
# ------------------------------
def generate_ai_reply(user_msg: str) -> str:
    """
    Super simple: send SYSTEM_PROMPT + user message to Gemini
    and return the reply text.
    """
    model = genai.GenerativeModel(MODEL_ID)

    prompt = f"""{SYSTEM_PROMPT}

User: {user_msg}
Assistant:"""

    response = model.generate_content(prompt)

    # Safety: sometimes response.text can be None
    return (response.text or "").strip()


# ------------------------------
# /get endpoint: save + respond
# ------------------------------
@aibot.route("/get", methods=["POST"])
@login_required
def chatbot_response():
    msg = request.form.get("msg", "").strip()
    if not msg:
        return ""

    now = datetime.now()

    # Save user message
    user_msg = ChatMessage(
        user_id=current_user.id,
        sender="user",
        text=msg,
        created_at=now,
    )
    db.session.add(user_msg)
    db.session.commit()

    # Generate reply from Gemini
    try:
        reply = generate_ai_reply(msg)
    except Exception:
        import traceback

        print("------ GEMINI ERROR START ------")
        traceback.print_exc()
        print("------ GEMINI ERROR END ------")
        reply = "Sorry, I'm having some trouble responding right now. Please try again in a bit."

    # Save bot reply
    bot_msg = ChatMessage(
        user_id=current_user.id,
        sender="bot",
        text=reply,
        created_at=now,
    )
    db.session.add(bot_msg)
    db.session.commit()

    return reply
