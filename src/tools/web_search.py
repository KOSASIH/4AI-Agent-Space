"""
🌐 Advanced Web Search & Research Tools
"""

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import asyncio

@tool
async def advanced_web_search(query: str, max_results: int = 5) -> str:
    """Perform advanced web search with result summarization"""
    search = DuckDuckGoSearchRun()
    
    results = await asyncio.to_thread(search.run, query)
    
    # Extract top results and summarize
    summary = f"🔍 Search Results for '{query}':\n\n"
    for i, result in enumerate(results.split('\n')[:max_results*2], 1):
        if i > max_results:
            break
        summary += f"{i}. {result.strip()}\n"
    
    return summary

@tool
async def scrape_website(url: str, max_content: int = 2000) -> str:
    """Scrape and extract clean content from website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script/style
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        domain = urlparse(url).netloc
        return f"📄 {domain}:\n{text[:max_content]}..."
        
    except Exception as e:
        return f"❌ Error scraping {url}: {str(e)}"
