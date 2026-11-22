CHABBY 2.0 - LOCAL SETUP
========================

IMPORTANT
---------
1. Work only inside your "chabby v2" folder.
2. Do not replace your original deployed project yet.
3. Keep your existing .env file private. Never paste your API key into chat.
4. This package does not include your .env file.

FILES
-----
app.py             Main Streamlit app
model_router.py    OpenRouter model selection and fallback
rag_engine.py      PDF extraction, chunking, embeddings and retrieval
requirements.txt   Python dependencies

BEFORE RUNNING
--------------
Make sure your .env file is in the same folder as app.py and contains:

OPENROUTER_API_KEY=your_actual_key_here

Do not include quotation marks unless your key itself requires them.
Do not share this file.

RUN
---
Open Command Prompt in the chabby v2 folder.

Activate the environment:
.venv\Scripts\activate.bat

Start Chabby:
python -m streamlit run app.py

You can also use your existing runthis.py after the environment is activated:
python runthis.py

FEATURES AND LIMITATIONS
------------------------
- Text chat through OpenRouter.
- NVIDIA Nemotron model IDs selected in model_router.py.
- Image understanding through the vision model.
- PDF text extraction and RAG using a local multilingual embedding model.
- Voice input through SpeechRecognition's online Google recognizer.
- Voice output through gTTS.
- Language selection for replies and speech.
- Chat conversations are saved locally in chabby_chats.json and remain available after restarting.
- PDF vector memory is in RAM for the current app session. Re-add PDFs after restarting.
- Scanned/image-only PDFs are not OCR processed in this version.
- Uploaded images are sent to the vision provider and their image data is saved in the
  local chat-history JSON so the conversation can be reopened. This can make that file large.
- Free model availability, rate limits, supported image formats, and language speech
  support depend on the external providers and can change.
- Voice features send audio/text to online services. Do not use them for sensitive audio.

FIRST TEST
----------
1. Start the app and send: "Hi, who are you?"
2. Upload a small text-based PDF and wait for "Ready".
3. Ask a question whose answer is in that PDF.
4. Upload an image and ask what is visible.
5. Test voice input and then the read-aloud button.

If a model provider is busy or rate-limited, wait and retry. Free providers do not
guarantee uninterrupted availability.
