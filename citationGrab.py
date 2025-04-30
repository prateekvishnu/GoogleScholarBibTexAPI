import requests
from bs4 import BeautifulSoup
import time

# List of paper titles
paper_titles = [
    "Attention is All You Need",
    "Deep Residual Learning for Image Recognition",
    "AutoML: A Survey of the State-of-the-Art",
    "Some Nonexistent Paper Title That Will Fail"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_latex_citation(paper):
    try:
        query = requests.utils.quote(paper)
        search_url = f"https://scholar.google.de/scholar?hl=de&as_sdt=0%2C5&q={query}"
        search_response = requests.get(search_url, headers=headers)
        bs_page = BeautifulSoup(search_response.content, "html.parser")

        block = bs_page.find("div", {"class": "gs_ri"})
        if not block:
            return None
        title = block.find("h3")
        link = title.find("a")
        if not link or "id" not in link.attrs:
            return None
        citation_id = link["id"]

        cite_url = f"https://scholar.google.de/scholar?q=info:{citation_id}:scholar.google.com/&output=cite"
        cite_response = requests.get(cite_url, headers=headers)
        citation_view = BeautifulSoup(cite_response.content, "html.parser")
        latex_link = citation_view.find("div", {"id": "gs_citi"}).find_all("a")[0]["href"]

        latex_response = requests.get(latex_link, headers=headers)
        return latex_response.text.strip()

    except Exception:
        return None


# Output file
output_file = "citations.bib"
errors = []

with open(output_file, "w", encoding="utf-8") as f:
    for title in paper_titles:
        print(f"Processing: {title}")
        citation = get_latex_citation(title)
        if citation:
            f.write(citation + "\n\n")
        else:
            errors.append(title)
        time.sleep(3)  # rate limit

# Print summary
if errors:
    print("\nCould not retrieve citations for the following papers:")
    for err_title in errors:
        print(f" - {err_title}")
else:
    print("\nAll citations retrieved successfully!")

print(f"\nSaved results to '{output_file}'")
