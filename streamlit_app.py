import requests
from bs4 import BeautifulSoup
import streamlit as st

# List of domains to scrape
domains = [
    "https://edition.cnn.com/politics/live-news/election-biden-trump-07-13-24/index.html",
    "https://www.cnn.com"
]

def scrape_from_domain(domain):
    try:
        response = requests.get(domain)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example scraping logic - this will need to be customized for each site
        item = soup.find('div', class_='gs-c-promo')  # Update this based on actual HTML structure of the site
        if item:
            title = item.find('h3').text if item.find('h3') else 'N/A'
            category = 'News'  # Example static category, customize as needed
            author = 'N/A'  # Author is often not available on main pages, customize as needed
            content = item.find('p').text if item.find('p') else 'N/A'
            link = item.find('a')['href'] if item.find('a') else 'N/A'
            
            if not link.startswith('http'):
                link = domain + link  # Handle relative URLs
            
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
