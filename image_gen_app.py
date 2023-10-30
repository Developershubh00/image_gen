import streamlit as st
import requests
from bs4 import BeautifulSoup

def scrape_ideogram_images(search_query):
    # Construct the search URL
    search_url = f"https://ideogram.ai/t/trending?q={search_query}"

    # Send an HTTP GET request to the search URL
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        image_tags = soup.find_all("img")

        # Extract image URLs
        image_urls = [img["src"] for img in image_tags]

        st.write("Retrieved Images:")
        st.write(image_urls)

        return image_urls
    else:
        st.write("Failed to retrieve images.")
        return []

def main():
    st.title('Ideogram Image Search')

    # User input
    search_query = st.text_input('Enter your search query:')
    
    if st.button('Generate Images'):
        # Perform web scraping to retrieve images
        image_urls = scrape_ideogram_images(search_query)

        if image_urls:
            st.write(f"Found {len(image_urls)} images:")
            for img_url in image_urls:
                st.image(img_url, caption=img_url, use_column_width=True)

                # Provide download link for each image
                st.markdown(f'[Download Image]({img_url})')

if __name__ == "__main__":
    main()
