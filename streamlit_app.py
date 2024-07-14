import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('h1').text if soup.find('h1') else 'N/A'

        # Attempt to find author by various common tags and attributes
        author = None
        
        # Common author class names
        author_tags = soup.find_all(class_='author') + soup.find_all(class_='author-name') + soup.find_all(class_='byline')
        for tag in author_tags:
            if tag.text:
                author = tag.text.strip()
                break
        
        # Meta tags
        if not author:
            meta_author = soup.find('meta', attrs={'name': 'author'})
            if meta_author and meta_author.get('content'):
                author = meta_author['content'].strip()

        # Byline links
        if not author:
            byline_link = soup.find('a', class_='byline')
            if byline_link and byline_link.text:
                author = byline_link.text.strip()

        if not author:
            author = 'N/A'

        # Combine all paragraphs to get content
        content = ' '.join(p.text for p in soup.find_all('p'))

        return {
            'title': title,
            'author': author,
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
            st.write(f"**Content:** {article['content']}")
            st.write(f"[Read more]({article['url']})")
        else:
            st.error("Failed to scrape the article.")
    else:
        st.error("Please enter a valid URL.")
