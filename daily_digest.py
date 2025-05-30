import os
import random
import datetime
import requests
from bs4 import BeautifulSoup

# ==== Telegram Setup ====
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ==== Tool & Prompt Datenbasis (groß & zufällig) ====
TOOLS = [
    {"name": "Gamma.app", "desc": "Erstelle schöne, interaktive Präsentationen mit KI."},
    {"name": "Perplexity.ai", "desc": "KI-gestützte Suche mit Quellenangaben."},
    {"name": "Krea.ai", "desc": "Live-Bildgenerierung mit KI-Steuerung in Echtzeit."},
    {"name": "Rewind.ai", "desc": "Erinnere dich an alles, was du je am PC getan hast – 100% lokal."},
    {"name": "Adept.ai", "desc": "Steuere jede Software nur mit Spracheingabe."},
    {"name": "LeiaPix", "desc": "Verwandle 2D-Bilder in 3D-Animationen."},
    {"name": "Notion AI", "desc": "Verfasse & überarbeite Inhalte direkt in Notion per KI."},
    {"name": "Synthesia", "desc": "Erstelle KI-Videos mit Avataren – perfekt für Schulungen."},
    {"name": "Runway ML", "desc": "Next-Level KI-Video-Editing mit Gen-2 Tools."},
    {"name": "Leonardo AI", "desc": "Erstelle schnell professionelle Illustrationen und Assets."}
]

PROMPTS = [
    "Erstelle mir eine Content-Strategie für TikTok rund um ein Nischenprodukt deiner Wahl.",
    "Fasse mir ein komplexes Forschungspapier in 5 Sätzen für LinkedIn zusammen.",
    "Erkläre mir den Unterschied zwischen Retrieval-Augmented Generation und Fine-Tuning.",
    "Generiere 5 Produktnamen für ein KI-gestütztes Meditations-Tool.",
    "Simuliere ein Interview mit Elon Musk über die Zukunft von AI.",
    "Gib mir 3 Content-Ideen für einen YouTube-Kanal über Tech & Tools.",
    "Wie würde Steve Jobs GPT-4 im Jahr 2025 verwenden? Spekuliere in einem fiktiven Zitat.",
    "Gib mir einen Prompt, mit dem ich Midjourney einen Manga-Stil generieren lassen kann.",
    "Formuliere einen LinkedIn-Post über ethische Herausforderungen von Deepfakes.",
    "Schreibe eine Schritt-für-Schritt-Anleitung zur Automatisierung meines Wochenplans mit AI."
]

# ==== AI-News aus 3 Top-Newslettern (Scraping) ====
def get_ai_news():
    news = []

    # Ben's Bites
    try:
        res = requests.get("https://bensbites.co")
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.find_all("a", class_="no-underline group", limit=2)
        for a in articles:
            title = a.find("h2").text.strip()
            summary = a.find("p").text.strip()
            link = "https://bensbites.co" + a.get("href")
            news.append({"title": title, "summary": summary, "link": link})
    except:
        pass

    # The Rundown AI
    try:
        res = requests.get("https://www.therundown.ai/")
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("a.text-xl.font-bold", limit=2)
        for a in items:
            title = a.text.strip()
            link = a["href"]
            summary = "Neuer Beitrag auf The Rundown AI."
            news.append({"title": title, "summary": summary, "link": link})
    except:
        pass

    # Superhuman
    try:
        res = requests.get("https://www.superhuman.ai/newsletter")
        soup = BeautifulSoup(res.text, "html.parser")
        block = soup.find("div", class_="max-w-xl").find_all("a", limit=1)
        for a in block:
            title = a.text.strip()
            link = "https://www.superhuman.ai" + a["href"]
            news.append({"title": title, "summary": "Top-News von Superhuman", "link": link})
    except:
        pass

    return news[:5]  # Top 5 News

# ==== Deep Dive für Sonntag ====
def get_deep_dive():
    return (
        "*Deep Dive Sunday*\n"
        "🧠 Heute erfährst du:\n"
        "- Wie Retrieval-Augmented Generation (RAG) funktioniert\n"
        "- Warum Agenten die Zukunft von KI sind\n"
        "- Welche Prompts besonders effektiv sind\n\n"
        "Mehr dazu hier: [Deep Dive PDF](https://example.com/deep-dive)"
    )

# ==== Nachricht formatieren & senden ====
def send_message(msg):
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    requests.post(TELEGRAM_URL, data=payload)

# ==== Bot-Ablauf starten ====
def main():
    today = datetime.datetime.now().strftime("%A")

    # News
    news_items = get_ai_news()
    news_text = "*📰 Top AI-News des Tages:*\n\n" + "\n\n".join(
        [f"*{n['title']}*\n{n['summary']}\n[Mehr lesen]({n['link']})" for n in news_items]
    )

    # Tool-Tipp
    tool = random.choice(TOOLS)
    tool_text = f"*🛠️ Tool-Tipp: {tool['name']}*\n{tool['desc']}"

    # Prompt des Tages
    prompt = random.choice(PROMPTS)
    prompt_text = f"*💬 Prompt des Tages:*\n`{prompt}`"

    # Deep Dive nur sonntags
    deep_dive = get_deep_dive() if today == "Sunday" else ""

    # Finaler Text
    full_message = f"{news_text}\n\n{tool_text}\n\n{prompt_text}"
    if deep_dive:
        full_message += f"\n\n{deep_dive}"

    send_message(full_message)

if __name__ == "__main__":
    main()
