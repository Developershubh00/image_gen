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
    url = "https://cloud.leonardo.ai/api/rest/v1/me"
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

# Define a function to handle the webhook call
def handle_webhook_call(image_json):
    # Extract relevant data from the image_json
    image_url = image_json.get("image_url")
    
    # You can then display or use this image_url as needed in your application
    st.image(image_url, use_column_width=True, caption="Generated Image")
    st.success("Image generated successfully.")

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
        # Display a sample image when "Keyword-based" is selected
        st.image("https://example.com/sample_image.jpg", use_column_width=True, caption="Sample Image")
        st.info("This is a sample image for the 'Keyword-based' method.")

if __name__ == "__main__":
    main()
