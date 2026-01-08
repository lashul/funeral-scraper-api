from fastapi import FastAPI
from fun_orgs_n8n import scrape_rifda_members

app = FastAPI()

@app.get("/scrape")
async def get_members():
    """
    Trigger the scraper and return the results as JSON for n8n.
    """
    data = scrape_rifda_members()
    return {"count": len(data), "members": data}

@app.get("/")
def home():
    return {"status": "Scraper API is running"}
