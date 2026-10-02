import os
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = "sunakshi1207@gmail.com"
SENDER_NAME = "AI News Aggregator"


def build_email_html(news):
    html = "<h2>🗞️ Your AI News Digest</h2>"

    for article in news[:15]:
        html += f"""
        <div style="margin-bottom:16px; padding-bottom:12px; border-bottom:1px solid #ddd;">
            <p style="color:#7c3aed; font-size:12px; text-transform:uppercase;">{article.get('source', '')}</p>
            <a href="{article.get('url', '#')}" style="font-size:16px; font-weight:bold; color:#111; text-decoration:none;">
                {article.get('title', '')}
            </a>
        </div>
        """

    return html


def send_news_email(to_email, news):
    html_content = build_email_html(news)

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": to_email}],
        "subject": "Your Daily AI News Digest",
        "htmlContent": html_content,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)

        if response.status_code in (200, 201):
            print("Email sent to:", to_email)
            return True
        else:
            print("EMAIL ERROR:", response.status_code, response.text)
            return False

    except Exception as e:
        print("EMAIL ERROR:", repr(e))
        return False