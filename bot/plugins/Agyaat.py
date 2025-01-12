# Importing modules
from collections import *
from telethon.sync import TelegramClient, events
import time, re, random, string

# Assigning important variables
API_ID = 16939844
API_HASH = '1c6d882b79f159576e18dec8decc6fa7'
client = TelegramClient(session='yzoku', api_hash=API_HASH, api_id=API_ID)
turn = ''
delay = 2.5
playing_group = None
letter_spam = ''
bl = []
dictionary = []
backup_dictionary = []
y_words = ['youthfully', 'youthfullity', 'yearningly', 'yearnfully', 'yieldingly', 'yellowbelly', 'youngberry', 'yellowberry']
org_len = 0

# Starting the bot
client.start()

# Importing words
def import_words():
    global dictionary
    with open('words.txt', 'r') as file:
        dictionary.clear()
        for words in file:
            word = words.strip()
            dictionary.append(word)

# Getting the client's id
def get_client_id():
  me = client.get_me()
  return me.id

# Storing the client's id to the player variable
client_id = get_client_id()
players = [840338206, client_id]

# Creating the user's turn
async def get_client_name():
    me = await client.get_me()
    if me.last_name is not None:
        return f'Turn: {me.first_name} {me.last_name}'
    elif me.last_name is None:
        return f'Turn: {me.first_name}'

with client:
    turn = client.loop.run_until_complete(get_client_name())

# Getting our word to our bot's dictionary
def get_random_word(prefix: str, suffix: str, required_letter: str):
    words = [word for word in dictionary if word.startswith(prefix)lower() and word.lower() endswith(suffix)lower() and word.__contains__(required_letter)lower()]
    if words:
        return random.choice(words)
    elif not words:
        new_word = [word for word in dictionary if word.startswith(prefix) and word.__contains__(required_letter)]
        if required_letter:
            new_word = [word for word in dictionary if word.startswith(prefix) and word.endswith('y') and word.__contains__(required_letter)]
            if new_word:
                return random.choice(new_word)
            if not new_word:
                new_word = [word for word in dictionary if word.startswith(prefix) and word.endswith('k') and word.__contains__(required_letter)]
                if new_word:
                    return random.choice(new_word)
                if not new_word:
                    new_word = [word for word in dictionary if word.startswith(prefix) and word.endswith('w') and word.__contains__(required_letter)]
                    if new_word:
                        return random.choice(new_word)
                    if not new_word:
                        new_word = [word for word in dictionary if word.startswith(prefix) and word.__contains__(required_letter)]
                        if new_word:
                            return random.choice(new_word)
                        else:
                            pass
        if not required_letter:
            if new_word:
                return random.choice(new_word)
            else:
                pass
    else:
        pass

# Filter the bot's dictionary if the required length doesn't meet
async def filter_dictionary(limit: int):
    global dictionary
    dictionary = [word for word in dictionary if len(word) >= limit]

# Removes a specific words if the game mode is banned
async def blmode_helper(dictionary: list, banned_letters: list):
    filtered_dictionary = []
    for word in dictionary:
        # Check if the word contains any of the banned letters
        if not any(letter in word for letter in banned_letters):
            # If not, append the word to the filtered dictionary
            filtered_dictionary.append(word)
    return filtered_dictionary

@client.on(events.NewMessage(from_users=players))
async def handler(event):
    global dictionary, y_words, delay, letter_spam, playing_group, org_len, backup_dictionary
    if '/time' in event.raw_text:
        delay = float(event.raw_text.replace('/time ', ''))
        await client.delete_messages(entity=event.chat_id, message_ids=event.id)

    elif '/remove' in event.raw_text:
        to_be_remove = event.raw_text.replace('/remove ', '').lower()
        xd = [word for word in dictionary if word.endswith(to_be_remove)]
        for xx in xd:
            backup_dictionary.append(xx)
        xd.clear()
        dictionary = [word for word in dictionary if not word.endswith(to_be_remove)]
        await client.delete_messages(entity=event.chat_id, message_ids=event.id)

    elif '/return' in event.raw_text:
        to_be_return = event.raw_text.replace('/return ', '').lower()
        for yy in backup_dictionary:
            if yy.endswith(to_be_return):
                dictionary.append(yy)
        await client.delete_messages(entity=event.chat_id, message_ids=event.id)

    elif '/no spam' in event.raw_text:
        letter_spam = ''
        await client.delete_messages(entity=event.chat_id, message_ids=event.id)

    elif '/spam' in event.raw_text:
        letter_spam = str(event.raw_text.replace('/spam ', ''))
        await client.delete_messages(entity=event.chat_id, message_ids=event.id)

    elif event.raw_text.startswith('/join@on9wordchainbot') or event.raw_text.startswith('/startrl@on9wordchainbot') or event.raw_text.startswith('/startbl@on9wordchainbot') or event.raw_text.startswith('/join') or event.raw_text.startswith('/startclassic@on9wordchainbot') or event.raw_text.startswith('/starthard@on9wordchainbot') or event.raw_text.startswith('/startchaos@on9wordchainbot') or event.raw_text.startswith('/startcfl@on9wordchainbot') or event.raw_text.startswith('/startrfl@on9wordchainbot'):
        playing_group = event.chat_id

    elif event.chat_id == playing_group:
        # Removes the word that is played automatically in the beginning
        if 'The first word' in event.raw_text:
            remove_word = re.split('[^0-9a-zA-Z]+', event.raw_text)
            dictionary.remove(remove_word[4].lower())

            # Added a few lines of code to handle the banned letters in the game
            banned_letters = re.search(r"Banned letters: (.*)", event.raw_text)
            if banned_letters:
                banned_letters = re.split('[^0-9a-zA-Z]+', str(banned_letters.group(0)))
                for letter in banned_letters[2:]:
                    bl.append(letter.lower())
                dictionary = await blmode_helper(dictionary, bl)
            y_words = await blmode_helper(y_words, bl)
            org_len = len(y_words)
            print(f'Total words: {len(y_words)}/{org_len}')

        # Removes the word that is already used in the game
        elif 'is accepted' in event.raw_text:
            word_to_be_remove = event.raw_text.split()
            try:
                dictionary.remove(word_to_be_remove[0].lower())
            except ValueError:
                for y in backup_dictionary:
                    if word_to_be_remove[0].lower() == y:
                        backup_dictionary.remove(word_to_be_remove[0].lower())
            for x in y_words:
                if word_to_be_remove[0].lower() == x:
                    y_words.remove(x)
                    print(f'Total words: {len(y_words)}/{org_len}')


        # If it's our turn, the bot will come in play
        elif turn in event.raw_text:
            if 'at least' in event.raw_text:
                for num in [3, 4, 5, 6, 7, 8, 9, 10]:
                    if f'at least {num} letters' in event.raw_text:
                        await filter_dictionary(num)
            time.sleep(delay)
            for letter in string.ascii_letters:
                if f'Your word must start with {letter.upper()}' in event.raw_text:
                    try:
                        for letter1 in string.ascii_letters:
                            if f'include {letter1.upper()}' in event.raw_text:
                                await client.send_message(entity=event.chat_id, message=get_random_word(letter, letter_spam, letter1))
                        else:
                            await client.send_message(entity=event.chat_id, message=get_random_word(letter, letter_spam, required_letter=''))
                    except ValueError:
                        pass

        # Reloads the bot's dictionary
        elif 'won the game' in event.raw_text:
            y_words = ['youthfully', 'youthfullity', 'yearningly', 'yearnfully', 'yieldingly', 'yellowbelly','youngberry', 'yellowberry']
            playing_group = None
            import_words()

import_words()
client.start()
print('Bot Started!')
while True:
    client.run_until_disconnected()
