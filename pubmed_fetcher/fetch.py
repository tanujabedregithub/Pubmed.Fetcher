import requests
import re
from typing import List, Dict, Optional

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_ids(query: str) -> List[str]:
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": 50}
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_id: str) -> Dict[str, Optional[str]]:
    params = {"db": "pubmed", "id": pubmed_id, "retmode": "xml"}
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    text = response.text

    title = re.search(r'<ArticleTitle>(.*?)</ArticleTitle>', text)
    pub_date = re.search(r'<PubDate>(.*?)</PubDate>', text)
    email_match = re.search(r'([\w\.-]+@[\w\.-]+)', text)

    return {
        "PubmedID": pubmed_id,
        "Title": title.group(1) if title else None,
        "Publication Date": pub_date.group(1) if pub_date else None,
        "Corresponding Author Email": email_match.group(1) if email_match else None
    }
