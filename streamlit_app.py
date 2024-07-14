import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example scraping logic - customize this based on the article's HTML structure
        title = soup.find('h1').text if soup.find('h1') else 'N/A'
        author = soup.find('span', class_='author').text if soup.find('span', class_='author') else 'N/A'
        category = soup.find('a', class_='category').text if soup.find('a', class_='category') else 'N/A'
        content = ' '.join(p.text for p in soup.find_all('p'))  # Combine all paragraphs
        
        return {
            'title': title,
            'author': author,
            'category': category,
            'content': content,
            'url': url
        }
    except Exception as e:
        st.error(f"Error scraping {url}: {e}")
        return None

# Streamlit app setup
st.title('Article Scraper')

# Add URL input
article_url = st.text_input('Enter the article URL')
if st.button('Scrape Article'):
    if article_url:
        article = scrape_article(article_url)
        if article:
            st.write(f"### {article['title']}")
            st.write(f"**Author:** {article['author']}")
            st.write(f"**Category:** {article['category']}")
            st.write(f"**Content:** {article['content']}")
            st.write(f"[Read more]({article['url']})")
        else:
            st.error("Failed to scrape the article.")
    else:
        st.error("Please enter a valid URL.")
