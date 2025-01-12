import asyncio
from pyrogram import Client, filters, enums
from info import PREFIX
import aiohttp


@Client.on_message(filters.command(["facts", "f"], PREFIX) & filters.me)
async def facts(client, message):
    data = await get_json(f"https://nekos.life/api/v2/fact")
    fact = data.get('fact')
    if not fact:
        await message.edit(f"Something went wrong!")
    await message.edit(f"{fact}")

@Client.on_message(filters.command(["urban", "ud"], PREFIX) & filters.me)
async def urban(client, message):
    word = message.text.split(maxsplit=1)[1]
    m = await message.edit(f"**Searching for** `{word}`")
    try:
        response =  await get_json(
            f"http://api.urbandictionary.com/v0/define?term={word}",
        )
        word = response["list"][0]["word"]
        definition = response["list"][0]["definition"]
        example = response["list"][0]["example"]
        result = f"**Text: {replacetext(word)}**\n**Meaning:**\n`{replacetext(definition)}`\n\n**Example:**\n`{replacetext(example)}`"
        await m.edit(result)
    except IndexError:
        await m.edit(
            text="`Sorry pal, we couldn't find meaning for the word you were looking for.`",
        )
    except Exception as e:
        await m.edit(text="`The Urban Dictionary API could not be reached`")


@Client.on_message(filters.command(["meaning", "m"], PREFIX) & filters.me)
async def meaning(client, message):
    word = message.text.split(maxsplit=1)[1]
    m = await message.edit(f"**Searching for** `{word}`")
    await asyncio.sleep(2)
    try:
        ft = f"<b>Search Query: </b><code>{word}</code>\n\n"
        response = await get_json(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
        )
        if "word" in response[0]:
            result = response[0]
            if "phonetics" in result:
                for phonetic in result["phonetics"]:
                    if phonetic.get("text"):
                        ft += f"<b>Phonetic: </b>\n<code>{phonetic['text']}</code>\n\n"
                        if phonetic.get("audio"):
                            ft += f"<b>Audio: </b>\n<code>{phonetic['audio']}</code>\n\n"
            if "meanings" in result:
                for meaning in result["meanings"]:
                    ft += f"<u><b>Meaning ({meaning['partOfSpeech']}):</b></u>\n"
                    for count, definition in enumerate(meaning["definitions"], 1):
                        ft += f"<b>{count}.</b> {definition['definition']}\n"
                        if definition.get("synonyms"):
                            ft += f"<b>Synonyms: </b><code>{', '.join(definition['synonyms'])}</code>\n"
                        if definition.get("antonyms"):
                            ft += f"<b>Antonyms: </b><code>{', '.join(definition['antonyms'])}</code>\n"
                    ft += "\n"
        else:
            ft += "`Sorry, we couldn't find Meaning for the word you were looking for.`"
        await m.edit(ft, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        await m.edit(text=f"{e}")

def replacetext(text):
    return (
        text.replace(
            '"',
            "",
        )
        .replace(
            "\\r",
            "",
        )
        .replace(
            "\\n",
            "",
        )
        .replace(
            "\\",
            "",
        )
    )

async def get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()