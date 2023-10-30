import streamlit as st
import requests
import tempfile
import base64  # Import base64 for encoding files to enable download links

# Replace 'YOUR_LEONARDO_API_KEY' with your actual Leonardo AI API key
api_key = 'c3c2d72b-7f30-443a-ae0f-7f3168aa3e2f'  # Replace with your actual API key
api_url = 'https://app.leonardo.ai/api/v1/images'

# Function to extract keywords from the prompt
def extract_keywords(prompt_text):
    # Split the prompt text into words and consider each word as a keyword
    keywords = prompt_text.split()
    return keywords

# Function to generate images based on keywords
def generate_images(prompt_text):
    keywords = extract_keywords(prompt_text)
    params = {
        'api_key': api_key,
        'keywords': keywords,
        # Add other parameters like aspect ratio, etc. based on the user's input
    }
    
    response = requests.get(api_url, params=params)
    
    # Check the HTTP status code
    if response.status_code == 200:
        try:
            image_urls = response.json()
        except ValueError as e:
            st.error(f"API Error: JSON Parsing Error - {e}")
            image_urls = []
    else:
        st.error(f"API Error: Status Code {response.status_code}")
        image_urls = []

    return image_urls

# Streamlit app
def main():
    st.title('Leonardo AI Images for Magazine')

    user_prompt = st.text_input('Enter a prompt for image generation:', 'A hyper-realistic image with a beautiful landscape')

    if st.button('Generate Images'):
        with st.spinner('Generating Images...'):
            image_urls = generate_images(user_prompt)

        if image_urls:
            for idx, img_url in enumerate(image_urls, start=1):
                st.image(img_url, use_column_width=True, caption=f'Image {idx}')

                # Provide download links for generated images (if applicable)
                image_data = requests.get(img_url).content
                b64 = base64.b64encode(image_data).decode()
                st.markdown(f'[Download Image {idx}](data:image/png;base64,{b64})')

            st.success("Images generated successfully.")
        else:
            st.warning("No images were returned by the API.")

if __name__ == "__main__":
    main()
