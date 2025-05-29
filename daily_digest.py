import os
import random
import requests
from datetime import datetime

def send_message(text):
    """Sendet die Nachricht an dein Telegram-Chat"""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        print("Fehler beim Senden:", response.text)

# 🗞 Beispiel-Daten (kannst du später ersetzen oder erweitern)

news = [
    "🔬 *OpenAI* veröffentlicht neues GPT-Update.",
    "💼 *Google* investiert 2 Mrd. in KI-Infrastruktur.",
    "🚀 *Anthropic* launcht Claude 3.5 – schneller & genauer.",
]

tools = [
    {"name": "PromptHero Pro", "desc": "Optimiert deine Prompts mit AI-Feedback."},
    {"name": "FlowGPT", "desc": "Teile und entdecke GPT-Prompts von anderen Usern."},
    {"name": "Gamma.app", "desc": "Erstelle automatisch Präsentationen mit AI."},
]

prompts = [
    "Erstelle einen viralen Instagram-Post über AI im Alltag.",
    "Fasse ein YouTube-Video über KI in 5 Bulletpoints zusammen.",
    "Schreibe ein LinkedIn-Update über die Zukunft von KI.",
]

deep_dive_sundays = [
    "🔎 *Deep Dive Sunday: Was ist RAG?*\nRAG (Retrieval-Augmented Generation) verbindet Sprachmodelle mit externem Wissen – perfekt für Chatbots mit Faktenwissen.",
    "🔎 *Deep Dive Sunday: Was sind Transformer?*\nTransformer-Modelle verwenden Self-Attention, um kontextabhängige Texte effizient zu verstehen.",
    "🔎 *Deep Dive Sunday: Vector Databases erklärt*\nSie ermöglichen semantische Suche, ideal für intelligente Systeme mit Gedächtnis.",
]

def build_message():
    today = datetime.now()
    weekday = today.weekday()  # Sonntag = 6
    date_str = today.strftime('%d.%m.%Y')

    message = f"*🧠 AI Daily Digest – {date_str}*\n\n"
    message += f"📰 *News:*\n{random.choice(news)}\n\n"
    
    tool = random.choice(tools)
    message += f"🛠 *Tool-Tipp:*\n{tool['name']}: {tool['desc']}\n\n"
    
    message += f"✍️ *Prompt des Tages:*\n{random.choice(prompts)}\n\n"
    
    if weekday == 6:
        message += f"{random.choice(deep_dive_sundays)}\n\n"
    
    message += "_Tipp: Speichere interessante Inhalte direkt in deinem Telegram!_"

    return message

# Hauptfunktion starten
if __name__ == "__main__":
    msg = build_message()
    send_message(msg)
