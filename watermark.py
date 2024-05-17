from io import BytesIO
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from fonts import available_fonts


# Function to add watermark to an image
def add_watermark(input_image, watermark_text, position, opacity, font_path, font_size, text_color, angle):
    original = Image.open(input_image).convert("RGBA")

    # Create watermark image
    watermark = Image.new("RGBA", original.size)
    draw = ImageDraw.Draw(watermark)

    # Load a font
    font = ImageFont.truetype(font_path, font_size)

    # Determine text width and position
    text_width = draw.textlength(watermark_text, font)
    if position == 'top-left':
        text_position = (10, 10)
    elif position == 'top-right':
        text_position = (original.size[0] - text_width - 10, 10)
    elif position == 'bottom-left':
        text_position = (10, original.size[1] - font_size - 10)
    elif position == 'bottom-right':
        text_position = (original.size[0] - text_width - 10, original.size[1] - font_size - 10)
    else:
        text_position = ((original.size[0] - text_width) // 2, (original.size[1] - font_size) // 2)
    # Convert text_color from hex to RGB
    text_color = tuple(int(text_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))

    # Apply the text to the watermark image
    draw.text(text_position, watermark_text, fill=(*text_color, opacity), font=font)

    # Rotate the watermark if an angle is set
    if angle != 0:
        watermark = watermark.rotate(angle, expand=1)

    # Crop the watermark to the size of the original image
    watermark = watermark.crop((0, 0, original.size[0], original.size[1]))

    # Combine the original image with watermark
    watermarked = Image.alpha_composite(original, watermark)

    # Convert to RGB and save the image
    watermarked = watermarked.convert("RGB")

    return watermarked


# Streamlit web interface
def main():
    st.title("Image Watermarking Application")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    watermark_text = st.text_input("Enter watermark text:", "Sample Watermark")
    position = st.selectbox("Select watermark position:",
                            ["top-left", "top-right", "bottom-left", "bottom-right", "center"])
    opacity = st.slider("Select watermark opacity (0-255):", 0, 255, 128)
    font_size = st.slider("Select font size:", 10, 455, 50)
    font_choice = st.selectbox("Select font:", list(available_fonts.keys()))
    font_path = available_fonts[font_choice]
    text_color = st.color_picker("Pick a text color:", "#FFFFFF")
    angle = st.slider("Select text rotation angle:", 0, 360, 0)

    if uploaded_file is not None:
        # Process the image and add watermark
        watermarked_image = add_watermark(uploaded_file, watermark_text, position, opacity, font_path, font_size,
                                          text_color, angle)

        # Display the watermarked image
        st.image(watermarked_image, caption="Watermarked Image", use_column_width=True)
        st.success("Watermark applied successfully!")

        # Provide a download button
        buffer = BytesIO()
        watermarked_image.save(buffer, format="JPEG")
        buffer.seek(0)
        st.download_button(
            label="Download watermarked image",
            data=buffer,
            file_name="watermarked_image.jpg",
            mime="image/jpeg"
        )


if __name__ == "__main__":
    main()
