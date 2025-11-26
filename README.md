# AI Chatbot for Healthcare (Flask + Gemini)

A simple Flask web app that provides a healthcare-focused chatbot using Google's Gemini API. It handles authentication, stores chat history per user, and formats model replies into friendly HTML (lists, bold text, headings).

## Demo
Add a short GIF or screenshot of the chat UI here:
```
docs/demo.gif   # create this file and update the link below
```
![Chat demo](docs/demo.gif)

## Features
- Gemini-powered chatbot with safety prompt (not a doctor, avoids diagnoses).
- Auth flows (login/signup) with per-user chat history.
- Minimal markdown-to-HTML rendering for bot replies (bold, lists, headings).
- Light/dark UI toggle; chat bubble layout.

## Quick Start
1) Clone and install deps:
```bash
python -m venv venv
.\venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

2) Configure environment: copy the example and add your values (do NOT commit real secrets).
```bash
copy website\.env.example website\.env
# edit website\.env
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=models/gemini-2.5-pro   # or another supported model
```

3) Run the app:
```bash
flask --app main run --debug
```
Open http://127.0.0.1:5000.

## Usage Example
- Log in or sign up, then ask: “Explain how AI helps in early diabetes detection.”
- The bot responds with concise, safe guidance and will remind you it is not a doctor.
- Model replies support basic formatting (bold, lists, headings) so bullets render cleanly.

## Gemini Model Notes
- The app reads `GEMINI_MODEL` from `website/.env`. Use a model that supports `generateContent`, e.g. `models/gemini-2.5-pro` or `models/gemini-2.5-flash`.
- If you change models, restart the app.

## Safety Prompt (bot constraints)
- Friendly, simple language; focused on AI in healthcare.
- Not a doctor; no diagnoses, treatments, or prescriptions.
- For serious/personal issues, directs users to a qualified clinician.

## Repo Hygiene
- Secrets are ignored via `.gitignore`; keep your API key only in `website/.env`.
- A sample file `website/.env.example` is provided for local setup.

## Project Structure (high level)
- `main.py` – Flask entrypoint.
- `website/__init__.py` – app factory, login manager, DB init.
- `website/aibot.py` – routes, Gemini calls, reply formatting.
- `website/auth.py` – auth routes.
- `website/models.py` – SQLAlchemy models (`User`, `ChatMessage`).
- `website/templates/` – HTML templates (`index.html`, `base.html`, auth pages).
- `website/static/` – styles and assets.

## Troubleshooting
| Issue | Fix |
| --- | --- |
| 404 model not found | Set `GEMINI_MODEL` to a model from `genai.list_models()` that supports `generateContent` (e.g., `models/gemini-2.5-pro`). |
| Missing API key | Ensure `GOOGLE_API_KEY` is in `website/.env`; reload the app. |
| Env not loading | Verify `ENV_PATH` in `website/aibot.py` points to `website/.env`. |
| Still seeing raw `*` or `#` | The formatter supports bold, lists, and headings; ensure the model response uses those patterns. |

## License
MIT
