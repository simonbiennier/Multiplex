from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

url = "https://buffersports.com/football-games"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
headers = {"User-Agent": user_agent}

req = Request(url=url, headers=headers)
res = urlopen(req)
data = res.read()

soup = BeautifulSoup(data, "html.parser")


def find_urls():
    teams = [item.text.strip() for item in soup.select("a")]
    teams = [
        x for x in teams if ((x != "") and (x != "Link") and (("AM" and "PM") not in x))
    ]
    urls = []
    for i in range(0, len(teams)):
        div = soup.find_all("h6")[i].parent.parent.parent
        urls.append(div.find_all("span")[2].find("a")["href"])
    return urls


matches = find_urls()
print(matches)
