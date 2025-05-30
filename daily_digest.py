import os
import random
import requests
import feedparser
from datetime import datetime

def send_message(text):
    """Sendet Nachricht an Telegram"""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        print("Fehler beim Senden:", response.text)

def get_ai_news():
    """Holt aktuelle KI-News von The Decoder (RSS Feed)"""
    feed_url = "https://the-decoder.com/feed/"
    feed = feedparser.parse(feed_url)
    articles = feed.entries[:3]  # Nehme die 3 neuesten Artikel
    headlines = [f"• [{entry.title}]({entry.link})" for entry in articles]
    return "\n".join(headlines)

tools = [
    {"name": "PromptHero Pro", "desc": "Optimiert deine Prompts mit AI-Feedback."},
    {"name": "FlowGPT", "desc": "Teile und entdecke GPT-Prompts von anderen Usern."},
    {"name": "Gamma.app", "desc": "Erstelle automatisch Präsentationen mit AI."},
    {"name": "Ideogram", "desc": "Bilder mit Text-Logo-Fokus – stark für Branding."},
    {"name": "Perplexity", "desc": "Die bessere Google-Suche, KI-basiert."},
]

deep_dive_sundays = [
    "🔎 *Deep Dive Sunday: Was ist RAG?*\nRAG (Retrieval-Augmented Generation) verbindet Sprachmodelle mit externem Wissen – perfekt für Chatbots mit Faktenwissen.",
    "🔎 *Deep Dive Sunday: Was sind Transformer?*\nTransformer-Modelle verwenden Self-Attention, um kontextabhängige Texte effizient zu verstehen.",
    "🔎 *Deep Dive Sunday: Vector Databases erklärt*\nSie ermöglichen semantische Suche, ideal für intelligente Systeme mit Gedächtnis.",
    "🔎 *Deep Dive Sunday: Agents erklärt*\nAI-Agents führen autonome Aktionen aus – mit Plan, Tools und Gedächtnis.",
]

def get_random_prompt():
    """Liest zufälligen Prompt aus prompts.txt (falls vorhanden)"""
    try:
        with open("prompts.txt", "r", encoding="utf-8") as f:
            prompts = [line.strip() for line in f if line.strip()]
            return random.choice(prompts)
    except FileNotFoundError:
        return "Wie kann ich GPT heute sinnvoll im Alltag einsetzen?"

def build_message():
    today = datetime.now()
    weekday = today.weekday()  # Sonntag = 6
    date_str = today.strftime('%d.%m.%Y')

    message = f"*🧠 AI Daily Digest – {date_str}*\n\n"
    message += f"📰 *News:*\n{get_ai_news()}\n\n"

    tool = random.choice(tools)
    message += f"🛠 *Tool-Tipp:*\n{tool['name']}: {tool['desc']}\n\n"

    message += f"✍️ *Prompt des Tages:*\n{get_random_prompt()}\n\n"

    if weekday == 6:
        message += f"{random.choice(deep_dive_sundays)}\n\n"

    message += "_Tipp: Speichere interessante Inhalte direkt in deinem Telegram!_"
    return message

# Hauptfunktion starten
if __name__ == "__main__":
    msg = build_message()
    send_message(msg)
