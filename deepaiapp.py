import streamlit as st
import requests
import io
from PIL import Image

# Define your DeepAI API key
DEEPAI_API_KEY = 'QUdJIGlzIGNvbWluZy4uLi4K'

# Streamlit app title and description
st.title("Text to Image Generator")
st.write("Generate images from text prompts using DeepAI")

# Input field for the text prompt
text_prompt = st.text_area("Enter your text prompt:")

# Generate images when the user provides a text prompt
if st.button("Generate Images") and text_prompt:
    # Send a POST request to DeepAI's text2img API
    r = requests.post(
        "https://api.deepai.org/api/text2img",
        data={'text': text_prompt},
        headers={'api-key': DEEPAI_API_KEY}
    )

    # Check if the request was successful
    if r.status_code == 200:
        response = r.json()
        image_urls = response.get('output_images', [])

        if image_urls:
            st.subheader("Generated Images:")
            for i, image_url in enumerate(image_urls):
                image_data = requests.get(image_url).content
                image = Image.open(io.BytesIO(image_data))
                st.image(image, caption=f"Image {i+1}", use_column_width=True)

            # Offer the option to download the images
            st.subheader("Download Images:")
            for i, image_url in enumerate(image_urls):
                st.markdown(f"Download Image {i+1}: [Image {i+1}.jpg]({image_url})")
        else:
            st.error("No images were generated. Please try a different text prompt.")
    else:
        st.error("Failed to generate images. Please check your API key and try again.")
