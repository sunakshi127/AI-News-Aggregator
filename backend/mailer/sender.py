import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv(r"C:\AI news aggregator\.env")

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")


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
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Daily AI News Digest"
    msg["From"] = EMAIL
    msg["To"] = to_email

    html_content = build_email_html(news)
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print("Email sent to:", to_email)
        return True

    except Exception as e:
        print("EMAIL ERROR:", repr(e))
        return False