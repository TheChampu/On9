from PIL import Image, ImageDraw, ImageFont
import requests, textwrap, aiohttp, logging, asyncio
from io import BytesIO
from pyrogram import Client, filters
from info import PREFIX
import random


def add_quote_to_image(image_url, quote, output_path='output_image.jpg'):
    try:
        # Download the image from the URL
        response = requests.get(image_url)
        # If the request was not successful, use a random fallback URL
        if response.status_code != 200:
            fallback_urls = [
                'https://telegra.ph/file/8aa8b5ed1fba1f81bfbc8.jpg'
            ]
            response = requests.get(random.choice(fallback_urls))

        img = Image.open(BytesIO(response.content))
        # Create a drawing object
        draw = ImageDraw.Draw(img)
        
        # Define the font and size
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Change to an available font path on your system
        font_size = 40  # Initial font size
        min_font_size = 20  # Minimum font size
        margin = 110  # Margin from the edges
        
        # Load font
        font = ImageFont.truetype(font_path, font_size)
        
        # Calculate the maximum width for the text
        max_text_width = img.width - 2 * margin
        
        # Adjust font size and wrap text
        while font_size >= min_font_size:
            wrapped_text = textwrap.fill(quote, width=40)
            lines = wrapped_text.split('\n')
            text_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines])
            text_width = max([draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0] for line in lines])
            if text_height + 2 * margin > img.height or text_width + 2 * margin > img.width:
                font_size -= 2
                font = ImageFont.truetype(font_path, font_size)
            else:
                break
        
        if font_size < min_font_size:
            print("The quote is too long to fit in the image even with the minimum font size.")
            return None
        
        # Calculate position and draw text line by line
        y = (img.height - text_height) / 2
        shadow_offset = 2  # Adjust the shadow offset as needed
        shadow_color = "black"  # Adjust the shadow color as needed
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (img.width - text_width) / 2
            # Draw shadow
            draw.text((x + shadow_offset, y + shadow_offset), line, font=font, fill=shadow_color)
            # Draw text
            draw.text((x, y), line, font=font, fill="white")
            y += bbox[3] - bbox[1]
        
        # Save the edited image
        img.save(output_path)
        
        return output_path
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None 


# Function to set profile photo
async def set_profile_photo(client):
    IMAGE_URL = "https://source.unsplash.com/random/800x600"
    try:
        quotes = await get_quotes()
        if not quotes:
            logging.error("No quotes found")
            return False
        
        photo_path = add_quote_to_image(IMAGE_URL, quotes)
        if photo_path:
            await client.set_profile_photo(photo=photo_path)
            return True
        
        logging.error("No photo path found")
        return False
    except Exception as e:
        await client.send_message("me", f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")
        return False

# Command to change profile picture
@Client.on_message(filters.command("pfq", PREFIX) & filters.me)
async def change_pfp(client, message):
    try:
        m = await message.edit("Changing profile pic...")
        success = await set_profile_photo(client)
        if success:
            await m.edit_text("Profile picture has been changed successfully")
        else:
            await m.edit_text("Failed to change profile picture")
        await asyncio.sleep(30)
        await m.delete()
    except Exception as e:
        await message.edit(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

        
@Client.on_message(filters.command("imgq", PREFIX) & filters.me)
async def image_quote(client, message):
    try:
        m = await message.edit("Fetching image quote...")
        quotes = await get_quotes()
        if quotes:
            IMAGE_URL = "https://source.unsplash.com/random/800x600"
            photo_path = add_quote_to_image(IMAGE_URL, quotes)
            if photo_path:
                await client.send_photo(message.chat.id, photo=photo_path)
                await m.delete()
                return
    except Exception as e:
        await message.edit(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

@Client.on_message(filters.command(["quotes", "q", "quote"], PREFIX) & filters.me)
async def get_quote(client, message):
    quotes = await get_quotes()
    await message.edit(f"{quotes}")

@Client.on_message(filters.command("bio", PREFIX) & filters.me)
async def change_bio(client, message):
    try:
        msg = await message.edit("Changing bio...")
        while True:
            quote = await get_quotes()
            if len(quote) <= 70:
                await client.update_profile(bio=quote)
                await msg.edit(f"**Bio has been changed to:** {quote}")
                break    
    except Exception as e:
        await message.edit(f"An error occurred: {e}")

async def get_quotes():
    url = "https://api.quotable.io/quotes/random"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                quote_data = await response.json()
                
                # Check if the response is a list of quotes
                if isinstance(quote_data, list) and len(quote_data) > 0:
                    quote = quote_data[0]
                    return quote.get("content", None)
                
                # If not a list, assume it's a single quote
                return quote_data.get("content", None)
            else:
                return None        