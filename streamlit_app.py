import requests
from bs4 import BeautifulSoup
import streamlit as st

# List of domains to scrape
domains = [
    "https://example-news-site1.com",
    "https://example-news-site2.com"
]

def scrape_from_domain(domain):
    try:
        response = requests.get(domain)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the first news item
        item = soup.find('div', class_='news-item')  # Update this based on actual HTML structure
        if item:
            title = item.find('h2').text
            category = item.find('span', class_='category').text if item.find('span', class_='category') else 'N/A'
            author = item.find('span', class_='author').text if item.find('span', 'author') else 'N/A'
            content = item.find('p', class_='content').text if item.find('p', class_='content') else 'N/A'
            link = item.find('a')['href']
            
            return {
                'title': title,
                'category': category,
                'author': author,
                'content': content,
                'link': link,
                'domain': domain
            }
        return None
    except Exception as e:
        st.error(f"Error scraping {domain}: {e}")
        return None

def scrape_all_domains():
    articles = []
    for domain in domains:
        article = scrape_from_domain(domain)
        if article:
            articles.append(article)
    
    return articles

# Streamlit app setup
st.title('News Scraper')

# Add domain input
new_domain = st.text_input('Add a new domain')
if st.button('Add Domain'):
    if new_domain:
        domains.append(new_domain)
        st.success(f"Added domain: {new_domain}")
    else:
        st.error("Please enter a valid domain")

# Scrape and display articles
if st.button('Scrape News'):
    articles = scrape_all_domains()
    if articles:
        st.write(f"Scraped {len(articles)} articles.")
        for article in articles:
            st.write(f"### {article['title']}")
            st.write(f"**Category:** {article['category']}")
            st.write(f"**Author:** {article['author']}")
            st.write(f"**Content:** {article['content']}")
            st.write(f"[Read more]({article['link']})")
            st.write(f"**Domain:** {article['domain']}")
            st.write("---")
    else:
        st.write("No articles found.")
