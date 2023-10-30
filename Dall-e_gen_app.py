import streamlit as st
import requests
import os

# Replace with your DALL·E API key
API_KEY = "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"

# DALL·E endpoint
DALLE_ENDPOINT = "https://api.openai.com/v1/dalle-generate"

def generate_images(prompt_text):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "text": prompt_text
    }

    try:
        response = requests.post(DALLE_ENDPOINT, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            image_url = result.get("image_url")
            return image_url
        else:
            st.error("Error generating image.")
            st.error(f"API Response Content: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error(f"API Response Content: {response.text}")
        return None


def main():
    st.title('Image Generator for Magzine')

    st.header('Generate Images from Text')
    user_prompt = st.text_input('Enter a prompt for image generation:')
    
    if st.button('Generate Image'):
        image_url = generate_images(user_prompt)

        if image_url:
            st.image(image_url, caption='Generated Image', use_column_width=True)

            # Provide a download link for the image
            st.markdown(f'[Download Image](image_url)')

if __name__ == "__main__":
    main()
