from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
total = 0
articlesData = []

while total < 15:
    references = []
    headlines = []
    driver.get("https://en.wikipedia.org/wiki/Special:Random")
    articleUrl = driver.current_url

    try:
        title = driver.find_element(by=By.CLASS_NAME, value='mw-page-title-main').text
    except NoSuchElementException:
        continue

    articleHeadlines = driver.find_elements(by=By.CLASS_NAME, value='mw-headline')

    if len(articleHeadlines) == 0:
        continue

    for headline in articleHeadlines:
        if headline.text == 'References':
            try:
                referencesSection = driver.find_element(by=By.CLASS_NAME, value='references')
            except NoSuchElementException:
                break
            allReferences = referencesSection.find_elements(by=By.TAG_NAME, value='li')
            for reference in allReferences:
                try:
                    references.append(reference.find_elements(by=By.CLASS_NAME, value='reference-text')[-1].find_element(by=By.TAG_NAME, value='a').get_attribute('href'))
                except:
                    try:
                        refs = reference.find_elements(by=By.CLASS_NAME, value='mw-cite-backlink')[0].find_elements(by=By.TAG_NAME, value='a')
                        for ref in refs:
                            references.append(ref.get_attribute('href'))
                    except:
                        continue
        elif headline.text == "See also":
            continue
        else:
            headlines.append(headline.text)

    articlesData.append({"title": title, "link": articleUrl,"headlines": headlines, "references": references})
    total += 1

print(articlesData)