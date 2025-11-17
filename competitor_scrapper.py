import requests
from bs4 import BeautifulSoup

def analyze_competitors(urls):
    analysis = []
    for url in urls:
        try:
            r = requests.get(url, timeout=6)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else "No title"
            meta_desc = soup.find("meta", attrs={"name": "description"})
            analysis.append({
                "url": url,
                "title": title,
                "meta_description": meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else "None"
            })
        except Exception as e:
            analysis.append({"url": url, "error": str(e)})
    return analysis
