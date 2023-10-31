import streamlit as st
import requests
import tempfile
import base64
import json  # Add this import for handling JSONDecodeError

# Set the Leonardo.ai API key
LEONARDO_API_KEY = "1573513a-5c1c-4746-bacb-dc686eb51372"

# Set the webhook call URL
WEBHOOK_CALL_URL = "http://localhost:8501/webhook"

# Define a function to call the Leonardo.ai API
def call_leonardo_api(prompt):
    url = "https://api.leonardo.ai/generate"
    params = {
        "prompt": prompt,
        "api_key": LEONARDO_API_KEY,
    }
    response = requests.post(url, params=params)

    if response.status_code == 200:
        try:
            return response.json()  # Try to parse JSON response
        except json.JSONDecodeError as e:
            st.error(f"API Error: JSON Parsing Error - {e}")
            return None  # Return None when JSON decoding fails
    else:
        st.error(f"API Error: Status Code {response.status_code}")
        return None  # Return None when the status code is not 200

# Function to handle the webhook call
def handle_webhook_call(image_json):
    payload = {
        "height": 512,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
        "prompt": "An oil painting of a cat",
        "width": 512
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": LEONARDO_API_KEY
    }
    response = requests.post(WEBHOOK_CALL_URL, json=payload, headers=headers)
    st.text(response.text)  # Print the response

# ... (other functions remain the same)

# Streamlit app
def main():
    st.title('Leonardo AI Images for Magazine')

    user_prompt = st.text_input('Enter a prompt for image generation:', 'A hyper-realistic image with a beautiful landscape')

    # Choose the image generation method
    method = st.radio("Select Image Generation Method", ("Leonardo.ai API", "Keyword-based"))

    if method == "Leonardo.ai API":
        if st.button('Generate Images'):
            with st.spinner('Generating Images...'):
                image_json = call_leonardo_api(user_prompt)

            if image_json and image_json.get("status") == "success":  # Check for "status" field
                handle_webhook_call(image_json)
                st.success("Image generated successfully.")
            else:
                st.warning("No image was returned by the API.")
    else:
        if st.button('Generate Images'):
            with st.spinner('Generating Images...'):
                image_urls = generate_images(user_prompt)

            if image_urls:
                for idx, img_url in enumerate(image_urls, start=1):
                    st.image(img_url, use_column_width=True, caption=f'Image {idx}')
                    image_data = requests.get(img_url).content
                    b64 = base64.b64encode(image_data).decode()
                    st.markdown(f'[Download Image {idx}](data:image/png;base64,{b64})')
                st.success("Images generated successfully.")
            else:
                st.warning("No images were returned by the API.")

if __name__ == "__main__":
    main()
