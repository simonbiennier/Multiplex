from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
headers = {"User-Agent": user_agent}
parser = "html.parser"


def fetch_pages():
    url = "https://buffersports.com/football-games"
    req = Request(url=url, headers=headers)
    res = urlopen(req)
    data = res.read()
    soup = BeautifulSoup(data, parser)

    teams = [item.text.strip() for item in soup.select("a")]
    teams = [
        x for x in teams if ((x != "") and (x != "Link") and (("AM" and "PM") not in x))
    ]
    urls = []
    for i in range(0, len(teams)):
        div = soup.find_all("h6")[i].parent.parent.parent
        urls.append(div.find_all("span")[2].find("a")["href"])
    return urls


def fetch_source(page_url):
    req = Request(url=page_url, headers=headers)
    res = urlopen(req)
    data = res.read()
    soup = BeautifulSoup(data, parser)
    return soup.find("iframe")["src"]


def fetch_server(page_url):
    source_url = fetch_source(page_url)
    req = Request(url=source_url, headers=headers)
    res = urlopen(req)
    data = res.read()
    soup = BeautifulSoup(data, parser)
    return soup.find_all("tr")[2].find("a")["href"]  # mazystreams


servers = []
matches = fetch_pages()
for match in matches:
    servers.append(fetch_server(match))

print(servers)
