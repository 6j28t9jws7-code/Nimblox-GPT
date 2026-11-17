
import os
import json
import time
import urllib.request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Не задан токен Telegram")

API = f"https://api.telegram.org/bot{TOKEN}/"


def telegram(method, data):
    request = urllib.request.Request(
        API + method,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    offset = 0
    print("Nimblox GPT запущен!")

    while True:
        try:
            updates = telegram("getUpdates", {
                "offset": offset,
                "timeout": 30
            })

            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                text = message.get("text", "")

                if not chat_id:
                    continue

                if text == "/start":
                    answer = (
                        "Привет! Я Nimblox GPT 🤖\n"
                        "Скоро здесь появится искусственный интеллект!"
                    )
                elif text:
                    answer = (
                        "Я получил твоё сообщение! 💚\n"
                        "Скоро научусь отвечать с помощью ИИ."
                    )
                else:
                    answer = "Пока я умею принимать только текстовые сообщения."

                telegram("sendMessage", {
                    "chat_id": chat_id,
                    "text": answer
                })

        except Exception as error:
            print("Ошибка:", error)
            time.sleep(5)


if __name__ == "__main__":
    main()
