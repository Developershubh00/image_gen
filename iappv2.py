import streamlit as st
import openai
from dotenv import load_dotenv
import os
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import requests
import tempfile

load_dotenv()

openai.api_key = "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"

def get_images(prompt_text):
    response = openai.Image.create(
        prompt=prompt_text,
        n=3,
        size="1024x1024"
    )
    return [Image.open(requests.get(img_data['url'], stream=True).raw) for img_data in response['data']]

def generate_solar_points(prompt_text):
    # Use Chat Completion to generate points about solar energy
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Give me some important points about {prompt_text}"}
        ]
    )
    # Extract the content of the assistant's reply and split it into separate points
    points = response['choices'][0]['message']['content'].split("\n")[:3]
    return points

def overlay_text_on_images(images, points):
    positions = [(30, 30), (30, 500), (30, 970)]  # Adjusted positions to fit within the image
    for img, point, pos in zip(images, points, positions):
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", size=30)
        draw.text(pos, point, font=font, fill="white")
    return images

def main():
    st.title('OpenAI Images for Magazine')

    user_prompt = st.text_input('Enter a prompt for image generation:', 'Unveiling the Future of Space Exploration ')
    
    if st.button('Generate Images'):
        images = get_images(user_prompt)
        points = generate_solar_points(user_prompt)
        final_images = overlay_text_on_images(images, points)

        for img, point in zip(final_images, points):
            st.image(img, caption=point, use_column_width=True)

        # Save each image to PDF and provide download links
        for idx, img in enumerate(final_images, start=1):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'_image{idx}.pdf') as tmpfile:
                img.save(tmpfile.name, "PDF", resolution=100.0)
                st.markdown(f'[Download PDF for Image {idx}]({tmpfile.name})')

if __name__ == "__main__":
    main()
