
export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("Nimblox GPT is ready!");
    }

    if (
      request.headers.get("X-Telegram-Bot-Api-Secret-Token") !==
      env.WEBHOOK_SECRET
    ) {
      return new Response("Forbidden", { status: 403 });
    }

    const update = await request.json();
    const message = update.message;

    if (!message || !message.chat) {
      return new Response("OK");
    }

    const chatId = message.chat.id;
    const text = message.text || "";

    let answer;

    if (text === "/start") {
      answer = "Привет! Я Nimblox GPT 🤖 Скоро здесь появится ИИ!";
    } else if (text) {
      answer = "Я получил твоё сообщение: " + text;
    } else {
      answer = "Пока я умею отвечать только на текст.";
    }

    await fetch(
      `https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: chatId,
          text: answer
        })
      }
    );

    return new Response("OK");
  }
};
