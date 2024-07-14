import streamlit as st
from newspaper3k import Article

def scrape_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        # Extract title
        title = article.title

        # Extract author
        authors = ', '.join(article.authors) if article.authors else 'N/A'

        # Extract content
        content = article.text

        return {
            'title': title,
            'author': authors,
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
