# 🧠  Sahaara — Mental Health Support Assistant

Sahaara is a conversational AI system designed to provide emotional support, detect signs of distress, and escalate help when necessary.

It combines natural conversation with safety-aware actions such as therapist recommendations and emergency call triggers.

---

## ✨ Features

* 💬 **Natural Conversations**
  Users can chat normally with the assistant for emotional support or general conversation.

* 🧠 **Emotional State Analysis**
  The system analyzes user messages to detect signs of distress, depression, or crisis.

* 🤖 **Therapeutic Response Generation**
  Uses the **MedGemma model** to generate empathetic and supportive responses.

* 📍 **Local Therapist Recommendations**
  Integrates **Google Places API** to suggest nearby therapists and provide contact details.

* 🚨 **Emergency Escalation**
  If a high-risk situation is detected, the system triggers a **Twilio call** to provide immediate support.

* 🛠️ **Tool-Oriented AI Architecture**
  Uses LangChain + LangGraph for intelligent decision-making and action routing.

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **LLM Orchestration:** LangChain, LangGraph
* **Model Integration:** MedGemma via Ollama
* **Location Services:** Google Places API
* **Communication:** Twilio
* **Frontend (optional):** Streamlit

---

## 📦 Dependencies

```
fastapi>=0.133.1
langchain>=1.2.10
langchain-groq>=1.1.2
langgraph>=1.0.9
ollama>=0.6.1
pydantic>=2.12.5
requests>=2.32.5
streamlit>=1.54.0
uvicorn>=0.41.0
```

---

## ⚙️ How It Works

1. User sends a message.
2. The AI analyzes emotional intent.
3. Based on the analysis:

   * Provides empathetic support via MedGemma
   * Suggests nearby therapists if needed
   * Triggers an emergency call if crisis is detected
4. The system ensures the user always receives a response or support pathway.

---

## 📞 About Emergency Calls

When a high-risk situation is detected, Twilio initiates a call to the user.
Currently, the call plays an automated support message.
This can be extended to forward calls to a real helpline or counselor.

---

## ⚠️ Disclaimer

Sahaara is not a medical or diagnostic tool.
It is intended for emotional support and guidance only and does not replace professional mental health care.

---

## 🚀 Future Improvements

* Real-time voice AI support
* Conversation memory
* Crisis risk classifier
* Integration with verified mental health resources
* Multi-language support

---

## 📌 Project Goal

The goal of Sahaara is to bridge the gap between immediate emotional support and professional help by providing a safety-aware conversational companion.

---
