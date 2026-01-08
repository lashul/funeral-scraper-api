import httpx
from bs4 import BeautifulSoup
import re
import json

def scrape_rifda_members():
    url = "https://rifda.org/rifda-members/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = httpx.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content_div = soup.find('div', class_='entry-content') or soup.find('main')
        if not content_div:
            return [] # Return empty list if no data found

        lines = [line.strip() for line in content_div.get_text(separator="\n").splitlines() if line.strip()]
        members = []
        city_state_zip_re = re.compile(r'^(.+),\s+([A-Z]{2})\s+(\d{5}-?\d*)$')
        phone_re = re.compile(r'^(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})$')

        start_index = 0
        for i, line in enumerate(lines):
            if "RIFDA Members" in line and i > 5:
                start_index = i + 1
                break

        current_member = {}
        buffer = []

        for line in lines[start_index:]:
            csz_match = city_state_zip_re.match(line)
            phone_match = phone_re.match(line)

            if csz_match:
                current_member['city'] = csz_match.group(1).strip()
                current_member['state'] = csz_match.group(2).strip()
                current_member['zip'] = csz_match.group(3).strip()
                if buffer:
                    current_member['address'] = buffer.pop()
                if buffer:
                    current_member['name'] = " ".join(buffer)
                buffer = []
            elif phone_match:
                current_member['phone_number'] = phone_match.group(1).strip()
                if 'name' in current_member:
                    members.append(current_member)
                current_member = {}
                buffer = []
            else:
                buffer.append(line)

        return members # Return the list directly

    except Exception as e:
        print(f"Error during scrape: {e}")
        return []

if __name__ == "__main__":
    # Keeping CLI functionality for local testing
    data = scrape_rifda_members()
    print(json.dumps(data, indent=4))
