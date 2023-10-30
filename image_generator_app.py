import streamlit as st
import openai

# Load your OpenAI API key from environment variables
openai.api_key = "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"  # Replace with your actual API key

def generate_images(prompt_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_text}
        ]
    )
    image_urls = response['choices'][0]['message']['content']
    return image_urls

def main():
    st.title('Image and Magazine Generator')

    st.header('Generate Images from Text')
    user_prompt = st.text_input('Enter a prompt for image generation:')
    
    if st.button('Generate Images'):
        image_urls = generate_images(user_prompt)
        
        for idx, img_url in enumerate(image_urls.split("\n"), start=1):
            st.image(img_url, caption=f'Image {idx}', use_column_width=True)
            
            # Provide a download link for each image
            st.markdown(f'[Download Image {idx}]({img_url})')

if __name__ == "__main__":
    main()
