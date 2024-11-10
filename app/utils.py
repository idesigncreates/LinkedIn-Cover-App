from PIL import Image, ImageDraw, ImageFont
import os

def add_text_behind_image(image_path, text, font_path="arial.ttf", font_size=40):
    # Open the image and convert to RGBA for transparency support
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    
    # Create a transparent text layer
    text_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)
    
    # Load the font and get the text's bounding box
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        # If the font is not found, fall back to a default font
        font = ImageFont.load_default()
    
    # Calculate the bounding box for the text
    text_bbox = draw.textbbox((0, 0), text, font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    
    # Calculate the position for the text to be centered
    text_position = ((width - text_width) // 2, (height - text_height) // 2)
    
    # Draw the text onto the text layer with semi-transparent black color
    draw.text(text_position, text, font=font, fill=(0, 0, 0, 150))
    
    # Combine the text layer with the original image
    combined = Image.alpha_composite(image, text_layer)
    
    # Ensure the final image is saved in the correct path
    processed_filename = "processed_image.png"
    processed_path = os.path.join("app", "static", "uploads", processed_filename)
    
    # Save the final image with text added
    combined.save(processed_path, "PNG")
    
    return processed_path
