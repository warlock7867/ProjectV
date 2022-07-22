from bs4 import BeautifulSoup
import re
import requests 
import concurrent.futures as cf
from time import sleep
from os.path import basename

def urlGetter(url):

    showList = []
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    rows = soup.find_all("tr", class_ = "ranking-list")
    for row in rows:
        title = row.find("td", class_ = "title al va-t word-break")
        url = title.find("a", class_ = "hoverinfo_trigger fl-l ml12 mr8", href = True)
        showList.append(url['href'])
    return showList

def listOfShows(baseURL, noOfShows = 50):
    allURLs = []
    for i in range(0, noOfShows, 50):
        if i == 0:
            allURLs.append(baseURL)
        else:
            allURLs.append("%s?limit=%s"%(baseURL, i))        
    shows = []
    with cf.ProcessPoolExecutor() as executor:
            futures = [executor.submit(urlGetter, a) for a in allURLs]
            for f in cf.as_completed(futures):
                show = f.result()
                shows += show  
    return shows

def listOfShowsV2(baseURL, start = 0, noOfShows = 50):
    end = start + noOfShows
    allURLS = []

    for i in range(start, end, 50):
        if i == 0:
            allURLS.append(baseURL)
        else:
            allURLS.append(f'{baseURL}?limit={i}')

    shows = []
    with cf.ProcessPoolExecutor() as executor:
            futures = [executor.submit(urlGetter, a) for a in allURLS]
            for f in cf.as_completed(futures):
                show = f.result()
                shows += show  
    return shows

def animeExtractor(soup):
    synonymsPattern = re.compile(r"Synonyms:(.+)", re.IGNORECASE)
    typePattern = re.compile(r"Type:(.+)", re.IGNORECASE)
    episodePattern = re.compile(r"Episodes:(.+)")
    statusPattern = re.compile(r"Status:(.+)", re.IGNORECASE)
    airedPattern = re.compile(r"Aired:(.+)", re.IGNORECASE)
    premieredPattern = re.compile(r"Premiered:(.+)", re.IGNORECASE)
    producersPatern = re.compile(r"Producer(s)?:(.+)", re.IGNORECASE)
    licensorsPattern = re.compile(r"Licensor(s)?:(.+)", re.IGNORECASE)
    studioPattern = re.compile(r"Studio(s)?:(.+)", re.IGNORECASE)
    sourcePattern = re.compile(r"Source:(.+)", re.IGNORECASE)
    genrePattern = re.compile(r"Genre(s)?:(.+)", re.IGNORECASE)
    themePattern = re.compile(r"Theme(s)?:(.+)", re.IGNORECASE)
    demoPattern = re.compile(r"Demographic(s)?:(.+)", re.IGNORECASE)
    ratingPattern = re.compile(r"Rating:(.+)", re.IGNORECASE)
    scorePattern = re.compile(r"Score:\s*(\d{1}\.\d{2})+", re.IGNORECASE)
    rankedPattern = re.compile(r"Ranked:\s*#(\d+)", re.IGNORECASE)
    popularityPattern = re.compile(r"Popularity:\s*#(\d+)", re.IGNORECASE)
    memberPattern = re.compile(r"Members:(.+)", re.IGNORECASE)
    favouritePattern = re.compile(r"Favorites:(.+)", re.IGNORECASE)
    anime = dict()
    japaneseName = soup.find('h1', class_ = "title-name h1_bold_none")
    anime["japaneseName"] = japaneseName.text
    try:
        englishName = soup.find('p', class_ = "title-english title-inherit")
        anime["englishName"] = englishName.text
    except:
        anime["englishName"] = anime["japaneseName"]

    details = soup.find('td', class_ = "borderClass")
    moreDetails = details.find_all('div', class_ = "spaceit_pad")
    details = soup.find('td', class_ = "borderClass")
    
    moreDetails = details.find_all('div', class_ = "spaceit_pad")   

    for finerDetail in moreDetails:
        text = finerDetail.text.strip()
        text = text.replace("\n", " ")
        for m in synonymsPattern.finditer(text):
            anime["synonyms"] = m.group(1).strip()

        for m in typePattern.finditer(text):
            anime["type"] = m.group(1).strip()

        for m in episodePattern.finditer(text):
            anime["episodes"] = m.group(1).strip()

        for m in statusPattern.finditer(text):
            anime["status"] = m.group(1).strip()

        for m in airedPattern.finditer(text):
            anime["aired"] = m.group(1).strip()

        for m in premieredPattern.finditer(text):
            anime["premiered"] = m.group(1).strip()

        for m in producersPatern.finditer(text):
            producers = m.group(2).strip()
            producers = producers.split(",")
            newProducers = []
            for prod in producers:
                newProducers.append(prod.strip())
            anime["producers"] = newProducers

        for m in licensorsPattern.finditer(text):
            licensors = m.group(2).strip().split(",")
            newLicensors = []
            for l in licensors:
                newLicensors.append(l.strip())
            anime["licensors"] = newLicensors

        for m in studioPattern.finditer(text):
            anime["studio"] = m.group(2).strip()
            
        for m in genrePattern.finditer(text):
            genre = m.group(2).strip()
            genre = genre.split(",")
            newGenre = []
            for g in genre:
                g = g.strip()
                n = int(len(g) / 2)
                newGenre.append(g[0:n])
            anime["genres"] = newGenre

        for m in themePattern.finditer(text):
            theme = m.group(2).strip()
            theme = theme.split(",")
            newTheme = []
            for g in theme:
                g = g.strip()
                n = int(len(g) / 2)
                newTheme.append(g[0:n])
            anime["themes"] = newTheme

        for m in demoPattern.finditer(text):
            demo = m.group(2).strip()
            n = int(len(demo) / 2)
            demo = demo[0:n]
            anime["demographic"] = demo

        for m in ratingPattern.finditer(text):
            anime["rating"] = m.group(1).strip()

        for m in scorePattern.finditer(text):
            anime["score"] = m.group(1).strip()

        for m in rankedPattern.finditer(text):
            ranked = m.group(1).strip()
            ranked = ranked[:-1]
            anime["ranked"] = ranked

        for m in popularityPattern.finditer(text):
            anime["popularity"] = m.group(1).strip()

        for m in memberPattern.finditer(text):
            anime["members"] = m.group(1).strip()
            
        for m in favouritePattern.finditer(text):
            anime["favourites"] = m.group(1).strip()

        for m in sourcePattern.finditer(text):
            anime["source"] = m.group(1).strip()

    description = soup.find('p', itemprop = 'description').text
    anime['description'] = description
    return anime

def APICaller(url):
    url = url.strip()
    print(f'requesting...{basename(url)}')
    with open('errors.txt', 'a', encoding='utf-8') as error:
        data = dict()
        try:
            html = requests.get(url)
            text = html.text
            soup = BeautifulSoup(text, 'lxml')
            data = animeExtractor(soup)
        except:
                error.writelines(f'{url}')
        print(f'request complete for {basename(url)}...')
        sleep(5)
        return data