import google.generativeai as genai
from pyrogram import Client, filters
from info import GENAI_API_KEY, PREFIX

genai.configure(api_key=GENAI_API_KEY)

def gemini(text):
    try:
        generation_config = {
            "temperature": 0.6,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
          {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_ONLY_HIGH"
          },
          {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_ONLY_HIGH"
          },
          {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_ONLY_HIGH"
          },
          {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_ONLY_HIGH"
          },
        ]
        model = genai.GenerativeModel(model_name="gemini-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        convo = model.start_chat()
        convo.send_message(text)
        return f"{convo.last.text}"
    except Exception as e:
        print(f"Error generating text: {str(e)}")
        return f"Error generating text: {str(e)}"


@Client.on_message(filters.command(["ask", "a"], PREFIX) & filters.me)
async def ask(client, message):
    try:
        text = message.text.split(None, 1)[1]
    except IndexError:
        await message.edit(f"Use `{PREFIX}ask <your questions>`")
        return

    if not text:
        await message.edit(f"Use `{PREFIX}ask <your questions>`")
    else:
        await message.edit(gemini(text))
