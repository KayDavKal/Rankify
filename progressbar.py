from PIL import Image, ImageDraw, ImageFont
from user import get_xp

async def create_progress_bar(guild_id, user_id, target_xp):
    current_xp = await get_xp(guild_id, user_id)

    # Calculate percentage completion
    percentage_completion = min(100, (current_xp / target_xp) * 100)

    # Create an image with a blank progress bar
    width, height = 300, 30
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Draw the progress bar
    bar_width = int((width * percentage_completion) / 100)
    draw.rectangle([0, 0, bar_width, height], fill='green')

    # Add text indicating percentage
    font = ImageFont.load_default()
    text = f'{percentage_completion:.2f}%'

    # Get the bounding box of the text
    text_bbox = draw.textbbox((0, 0), text, font=font)

    # Calculate the width and height of the text
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate the position to center the text
    text_position = ((width - text_width) // 2, (height - text_height) // 2)

    # Draw the text
    draw.text(text_position, text, fill='black', font=font)

    # Save or display the image
    img.save('progress_bar.png')
    img.show()