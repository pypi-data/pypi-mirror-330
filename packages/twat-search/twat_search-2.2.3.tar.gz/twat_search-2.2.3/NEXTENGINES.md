# Next backends and engines to implement

## https://github.com/Sanix-Darker/falla

Implement all engines as `*-falla` from this. 

Token Usage:
GitHub Tokens: 7766
LLM Input Tokens: 0
LLM Output Tokens: 0
Total Tokens: 7766

FileTree:
.gitignore
README.md
app/__init__.py
app/core/Aol.py
app/core/Ask.py
app/core/Bing.py
app/core/DogPile.py
app/core/DuckDuckGo.py
app/core/Falla.py
app/core/Gibiru.py
app/core/Google.py
app/core/Mojeek.py
app/core/Qwant.py
app/core/SearchEncrypt.py
app/core/StartPage.py
app/core/Yahoo.py
app/core/Yandex.py
app/core/__init__.py
app/main.py
app/settings.py
app/utils.py
example.config.txt
requirements.txt
tests/test.py

Analysis:
.gitignore
```.gitignore
config.txt
*__pycache__
.idea
.vscode
.history
*.json
*.log
*.pyc
```
README.md
# FAllA

A search-engine-cli-scraper for more than 15 search engines, including Google. duckduckgo, Bing, Ask, etc...
<br>
**NOTE:** For educationnal purpose, am not responsible of the bad use of this tool !

## Requirements
- Python (3.x)
- Docker-CE (Not required for all search-engine, just few of them)

## How to install

- You need to install all requirements :
```shell-script
pip3 install -r requirements.txt
```
- Install geckodriver :
```shell-script
# For linux users
sudo apt install firefox-geckodriver

# For other OS's users, please check releases on https://github.com/mozilla/geckodriver/releases
```

- Pull and run the splash-scrap module from docker-hub (Some of search engine need this):
```shell-script
docker run -p 8050:8050 scrapinghub/splash
```

- Replace `example.config.txt` by `config.txt` and provide the running IP for the splash-scrap

## How to launch

How to use Falla:
```shell-script
usage: main.py [-h] [-e ENGINE] [-q QUERY]

optional arguments:
  -h, --help            show this help message and exit
  -e ENGINE, --engine ENGINE
                        The search engine
  -q QUERY, --query QUERY
                        The query text
```

- To list all search-engine:
```shell-script
$ python3 -m app.main
# output
[+] Falla [the search-engine-scraper]
[+] Listing search-Engines
[+] > google
[+] > bing
[+] > aol
[+] > dogpile
[+] > falla
[+] > ask
[+] > qwant
[+] > duckduckgo
[+] > mojeek
[+] > gibiru
[+] > yandex
[+] > yahoo
[+] > searchencrypt
[+] > iem
[+] > kallasearch
[+] > wosx
```

- To search something:
```shell-script
$ python3 -m app.main -e google -q "sanix darker"
# output
```
<img src="./images/falla.png">
## Author

- Sanix-darker
app/__init__.py
```.py

```
app/core/Aol.py
```.py
# Falla-Aol
# -*- encoding: utf-8 -*-
# Sanix-darker

from app.core.Falla import Falla


class Aol(Falla):
    def __init__(self):
        self.try_it = 0
        self.max_retry = 3
        self.source = "Aol"
        self.mode = "requests"
        self.results_box = "//div[@id='web']"
        self.each_element = {
            "tag": "li"
        }
        self.href = {
            "tag": "a",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "a",
            "type": "text"
        }
        self.cite = {
            "tag": "div:compText",
            "child": {
                "tag": "p",
                "type": "text"
            }
        }

    def search(self, search_text, pages=""):
        url = "https://search.aol.com/aol/search?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# a = Aol()
# print(a.search("un avion"))

```
app/core/Ask.py
```.py
# Falla-Ask
# -*- encoding: utf-8 -*-
# Sanix-darker

from app.core.Falla import Falla


class Ask(Falla):
    def __init__(self):
        self.try_it = 0
        self.max_retry = 3
        self.source = "Ask"
        self.mode = "requests"
        self.results_box = "//div[@class='l-mid-content']"
        self.each_element = {
            "tag": "div",
            "attr": {"class": "PartialSearchResults-item"}
        }
        self.href = {
            "tag": "a:PartialSearchResults-item-title-link",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "a:PartialSearchResults-item-title-link",
            "type": "text"
        }
        self.cite = {
            "tag": "p:PartialSearchResults-item-abstract",
            "type": "text"
        }

    def search(self, search_text, pages=""):
        url = "https://www.ask.com/web?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# ak = Ask()
# print(ak.search("un avion"))

```
app/core/Bing.py
```.py
# Falla-Bing
# -*- encoding: utf-8 -*-
# Sanix-darker

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from app.core.Falla import Falla


class Bing(Falla):
    def __init__(self):
        self.source = "Bing"
        self.mode = "splash_scrap"
        self.try_it = 0
        self.max_retry = 3
        self.results_box = "//ol[@id='b_results']"
        self.each_element = {
            "tag": "li",
            "attr": {"class": "b_algo"}
        }
        self.href = {
            "tag": "a",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "h2",
            "type": "text",
            "child": {}
        }
        self.cite = {
            "tag": "div:b_caption",
            "child": {
                "tag": "p",
                "type": "text"
            }
        }

    def search(self, search_text, pages=""):
        url = "https://www.bing.com/search?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# b = Bing()
# print(b.search("un avion"))

```
app/core/DogPile.py
```.py
# Falla-DogPile
# -*- encoding: utf-8 -*-
# Sanix-darker

from app.core.Falla import Falla


class DogPile(Falla):
    def __init__(self):
        self.try_it = 0
        self.max_retry = 3
        self.source = "DogPile"
        self.mode = "requests"
        self.results_box = "//div[@class='mainline-results']"
        self.each_element = {
            "tag": "div",
            "attr": {"class": "web-bing__result"}
        }
        self.href = {
            "tag": "a:web-bing__title",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "a:web-bing__title",
            "type": "text"
        }
        self.cite = {
            "tag": "span:web-bing__description",
            "type": "text"
        }

    def search(self, search_text, pages=""):
        url = "https://www.dogpile.com/serp?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# dp = DogPile()
# print(dp.search("un avion"))

```
app/core/DuckDuckGo.py
```.py
# Falla-DuckDuckGo
# -*- encoding: utf-8 -*-
# Sanix-darker

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from app.core.Falla import Falla


class DuckDuckGo(Falla):
    def __init__(self):
        self.option = Options()
        self.option.headless = True
        self.driver = webdriver.Firefox(options=self.option)

        self.source = "DuckDuckGo"
        self.mode = "selenium"
        self.try_it = 0
        self.max_retry = 3
        self.results_box = "//div[@id='links']"
        self.each_element = {
            "tag": "div",
            "attr": {"class": "result__body"}
        }
        self.href = {
            "tag": "a:result__a",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "a:result__a",
            "type": "text",
            "child": {}
        }
        self.cite = {
            "tag": "div:result__snippet",
            "type": "text",
            "child": {}
        }

    def search(self, search_text, pages=""):
        url = "https://duckduckgo.com/?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# d = DuckDuckGo()
# print(d.search("un avion"))

```
app/core/Falla.py
```.py
# Falla
# -*- encoding: utf-8 -*-
# Sanix-darker

import json
import sys
import time
import traceback
import requests
from bs4 import BeautifulSoup

from app.settings import *


class Falla:
    def __init__(self, results_box, each_element, href, title, cite):
        self.driver = None
        self.results_box = results_box
        self.each_element = each_element
        self.href = href
        self.title = title
        self.cite = cite
        self.try_it = 0
        self.max_retry = 4
        self.source = "Falla"
        self.mode = "requests"

        self.option = None
        self.option.headless = None
        self.driver = None

    def get_trace(self):
        """
        This method will just print the Traceback after an error occur
        """
        print("Exception in code:")
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)

    def get_element_from_type(self, to_return, the_filter=None):
        """
        A parse-method to extract from parse_entry_point an element as attribute or text

        to_return: The BeautifulSoup object
        the_filter: The Json-Filter
        """
        if the_filter["type"] == "text":
            to_return = to_return.getText()
        elif the_filter["type"] == "attribute":
            try:
                to_return = to_return[the_filter["key"]]
            except Exception:
                self.get_trace()
                to_return = ""
        else:
            print("[x] Error, specify a valid type !")

        return to_return

    def get_tag(self, element, tag):
        """
        This method will extract the tag having a attriute or not

        element: The Beautifull-Soup object
        tag: The Json tag (can be a class or other)
        """
        if ":" in tag:
            return element.find(tag.split(":")[0], {"class": tag.split(":")[1]})
        else:
            return element.find(tag)

    def parse_entry_point(self, element, the_filter):
        """
        This method will extract the href, the title and the cite in result

        element: The Beautifull-Soup Object
        the_filter: The JSON object for the Filter
        """
        to_return = self.get_tag(element, the_filter["tag"])

        if "type" in the_filter:
            to_return = self.get_element_from_type(to_return, the_filter)
        else:
            if bool(the_filter["child"]):  # There are some child
                to_return = self.get_tag(to_return, the_filter["child"]["tag"])

                to_return = self.get_element_from_type(to_return, the_filter["child"])
            else:
                print("[x] Malformed filter !")

        return ' '.join(str(to_return).split())

    def get_each_elements(self, soup):
        """
        Get all elements list from Beautifull-Soup object

        soup: The Beautiful-Soup object
        """
        fetchs = []
        if "attr" in self.each_element:
            if self.each_element["attr"] is not None:
                fetchs = soup.findAll(self.each_element["tag"], self.each_element["attr"])
            else:
                fetchs = soup.findAll(self.each_element["tag"])
        else:
            fetchs = soup.findAll(self.each_element["tag"])

        return fetchs

    def scrapy_splash_request(self, to_fetch_url):
        """
        This method is responsible for scrapping a html_content from a url using splash-scrap

        to_fetch_url: The url of the website
        """
        json_data = {
            "response_body": False,
            "lua_source": "function main(splash, args)\r\n  assert(splash:go(args.url))\r\n  assert(splash:wait("
                          "0.5))\r\n  return {\r\n    html = splash:html(),\r\n    png = splash:png(),\r\n    har = "
                          "splash:har(),\r\n  }\r\nend",
            "url": to_fetch_url,
            "html5_media": False,
            "save_args": [],
            "viewport": "1024x768",
            "http_method": "GET",
            "resource_timeout": 0,
            "render_all": False,
            "png": 1,
            "har": 1,
            "timeout": 90,
            "request_body": False,
            "load_args": {},
            "html": 1,
            "images": 1,
            "wait": 0.7
        }

        r = requests.post(SPLASH_SCRAP_URL + "/execute", json=json_data)
        html_string = json.loads(r.content.decode())["html"]

        return html_string

    def get_html_content(self, url):
        """
        This method will check the mode of fetching and proceed

        url: The url of the target
        """
        html_content = ""
        if self.mode == "selenium":
            self.driver.get(url)
            self.driver.implicitly_wait(10)  # in seconds

            element = self.driver.find_element_by_xpath(self.results_box)
            html_content = element.get_attribute('outerHTML')
        elif self.mode == "splash_scrap":
            html_content = self.scrapy_splash_request(url)

        elif self.mode == "requests":
            r = requests.get(url, headers={"Upgrade-Insecure-Requests": "1",
                                           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
                                                         "like Gecko) Chrome/80.0.3987.100 Safari/537.36",
                                           "Sec-Fetch-Dest": "document",
                                           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                                                     "image/webp,image/apng,*/*;q=0.8,"
                                                     "application/signed-exchange;v=b3;q=0.9 "
                                           })
            html_content = r.content.decode()

        return html_content

    def fetch(self, url):
        """
        The main method for fetching results from url

        url: The url of the target
        """
        html_content = self.get_html_content(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        fetchs = self.get_each_elements(soup)

        results = []
        # print("fetchs: ", fetchs)
        # print("self.parse_entry_point(elt, self.href): ", self.parse_entry_point(fetchs[0], self.href))
        for elt in fetchs:
            try:
                element = {
                    "source": self.source,
                    "href": self.parse_entry_point(elt, self.href),  # elt.find("a")["href"]
                    "title": self.parse_entry_point(elt, self.title),  # str(elt.find("a").find("h3").getText())
                    "cite": self.parse_entry_point(elt, self.cite)  # str(elt.find("a").find("cite").getText())
                }
                results.append(element)
            except Exception:
                self.get_trace()

        if len(results) == 0 and self.try_it < self.max_retry:
            self.try_it += 1
            time.sleep(0.5)
            print("[+] try: ", self.try_it)
            self.fetch(url)

        if self.mode == "selenium":
            self.driver.quit()

        return json.dumps(results, ensure_ascii=False)

```
app/core/Gibiru.py
```.py
# Falla-Gibiru
# -*- encoding: utf-8 -*-
# Sanix-darker

from app.core.Falla import Falla


class Gibiru(Falla):
    def __init__(self):
        self.source = "Gibiru"
        self.mode = "splash_scrap"
        self.try_it = 0
        self.max_retry = 3
        self.results_box = "//div[@class='gsc-resultsRoot']"
        self.each_element = {
            "tag": "div",
            "attr": {"class": "gs-webResult"}
        }
        self.href = {
            "tag": "a:gs-title",
            "type": "attribute",
            "key": "data-ctorig",
            "child": {}
        }
        self.title = {
            "tag": "a:gs-title",
            "type": "text",
            "child": {}
        }
        self.cite = {
            "tag": "div:gs-snippet",
            "type": "text",
            "child": {}
        }

    def search(self, search_text, pages=""):
        url = "https://gibiru.com/results.html?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# gi = Gibiru()
# print(gi.search("un avion"))

```
app/core/Google.py
```.py
# Falla-Google
# -*- encoding: utf-8 -*-
# Sanix-darker

import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from app.core.Falla import Falla


class Google(Falla):
    def __init__(self):
        self.option = Options()
        self.option.headless = True
        self.driver = webdriver.Firefox(options=self.option)

        self.try_it = 0
        self.max_retry = 3
        self.source = "Google"
        self.mode = "selenium"
        self.results_box = "//div[@id='search']"
        self.each_element = {
            "tag": "div",
            "attr": {"class": "g"}
        }
        self.href = {
            "tag": "a",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "a",
            "child": {
                "tag": "h3",
                "type": "text"
            }
        }
        self.cite = {
            "tag": "a",
            "child": {
                "tag": "cite",
                "type": "text"
            }
        }

    def search(self, search_text, pages=""):

        base_url = "https://www.google.com/search?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + base_url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        # results = json.loads(self.fetch(base_url))
        #
        # if pages > 1:
        #     for nb_page in range(pages):
        #         url = base_url + "&start=" + str(nb_page + 1) + "0"
        #         time.sleep(1)
        #         results = results + self.fetch(url)
        #
        # results = json.dumps(results)

        return self.fetch(base_url)


# g = Google()
# print(g.search("un avion"))

```
app/core/Mojeek.py
```.py
# Falla-Mojeek
# -*- encoding: utf-8 -*-
# Sanix-darker

from app.core.Falla import Falla


class Mojeek(Falla):
    def __init__(self):
        self.try_it = 0
        self.max_retry = 3
        self.source = "Mojeek"
        self.mode = "requests"
        self.results_box = "//ul[@class='results-standard']"
        self.each_element = {
            "tag": "li"
        }
        self.href = {
            "tag": "a:ob",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "a:ob",
            "type": "text"
        }
        self.cite = {
            "tag": "p:s",
            "type": "text"
        }

    def search(self, search_text, pages=""):
        url = "https://www.mojeek.com/search?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# mk = Mojeek()
# print(mk.search("un avion"))

```
app/core/Qwant.py
```.py
# Falla-Qwant
# -*- encoding: utf-8 -*-
# Sanix-darker

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from app.core.Falla import Falla


class Qwant(Falla):
    def __init__(self):
        self.option = Options()
        self.option.headless = True
        self.driver = webdriver.Firefox(options=self.option)

        self.try_it = 0
        self.max_retry = 3
        self.source = "Qwant"
        self.mode = "selenium"
        self.results_box = "//div[@class='result_fragment']"
        self.each_element = {
            "tag": "div",
            "attr": {"class": "result--web"}
        }
        self.href = {
            "tag": "a:result--web--link",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "span:result--web--title",
            "type": "text",
            "child": {}
        }
        self.cite = {
            "tag": "div:result--web",
            "child": {
                "tag": "p",
                "type": "text"
            }
        }

    def search(self, search_text, pages=""):
        url = "https://www.qwant.com/?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# qw = Qwant()
# print(qw.search("un avion"))

```
app/core/SearchEncrypt.py
```.py
# Falla-SearchEncrypt
# -*- encoding: utf-8 -*-
# Sanix-darker

from app.core.Falla import Falla


class SearchEncrypt(Falla):
    def __init__(self):
        self.try_it = 0
        self.max_retry = 3
        self.source = "SearchEncrypt"
        self.mode = "requests"
        self.results_box = "//section[@class='serp__results']"
        self.each_element = {
            "tag": "div",
            "attr": {"class": "web-result"}
        }
        self.href = {
            "tag": "a:web-result__link",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "a:web-result__link",
            "type": "text",
            "child": {}
        }
        self.cite = {
            "tag": "p:web-result__description",
            "child": {
                "tag": "span",
                "type": "text"
            }
        }

    def search(self, search_text, pages=""):
        url = "https://www.searchencrypt.com/search/?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# se = SearchEncrypt()
# print(se.search("un avion"))

```
app/core/StartPage.py
```.py
# Falla-StartPage
# -*- encoding: utf-8 -*-
# Sanix-darker

from app.core.Falla import Falla


class StartPage(Falla):
    def __init__(self):
        self.try_it = 0
        self.max_retry = 3
        self.source = "StartPage"
        self.mode = "requests"
        self.results_box = "//section[@id='w-gl--default']"
        self.each_element = {
            "tag": "div",
            "attr": {"class": "w-gl__result"}
        }
        self.href = {
            "tag": "a:w-gl__result-title",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "a:w-gl__result-title",
            "child": {
                "tag": "h3",
                "type": "text"
            }
        }
        self.cite = {
            "tag": "p:w-gl__description",
            "type": "text",
            "child": {}
        }

    def search(self, search_text, pages=""):
        url = "https://www.startpage.com/sp/search?q=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# sp = StartPage()
# print(sp.search("un avion"))

```
app/core/Yahoo.py
```.py
# Falla-Yahoo
# -*- encoding: utf-8 -*-
# Sanix-darker

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from app.core.Falla import Falla


class Yahoo(Falla):
    def __init__(self):
        self.option = Options()
        self.option.headless = True
        self.driver = webdriver.Firefox(options=self.option)

        self.try_it = 0
        self.max_retry = 3
        self.source = "Yahoo"
        self.mode = "selenium"
        self.results_box = "//div[@id='web']"
        self.each_element = {
            "tag": "li"
        }
        self.href = {
            "tag": "a",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "a",
            "type": "text"
        }
        self.cite = {
            "tag": "div:compText",
            "child": {
                "tag": "p",
                "type": "text"
            }
        }

    def search(self, search_text, pages=""):
        url = "https://search.yahoo.com/search?p=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# y = Yahoo()
# print(y.search("un avion"))

```
app/core/Yandex.py
```.py
# Falla-Yandex
# -*- encoding: utf-8 -*-
# Sanix-darker

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from app.core.Falla import Falla


class Yandex(Falla):
    def __init__(self):
        self.option = Options()
        self.option.headless = True
        self.driver = webdriver.Firefox(options=self.option)

        self.try_it = 0
        self.max_retry = 3
        self.source = "Yandex"
        self.mode = "selenium"
        self.results_box = "//div[@class='content__left']"
        self.each_element = {
            "tag": "li",
            "attr": {"class": "serp-item"}
        }
        self.href = {
            "tag": "a:link",
            "type": "attribute",
            "key": "href",
            "child": {}
        }
        self.title = {
            "tag": "div:organic__url-text",
            "type": "text"
        }
        self.cite = {
            "tag": "div:organic__content-wrapper",
            "child": {
                "tag": "div:text-container",
                "type": "text"
            }
        }

    def search(self, search_text, pages=""):
        url = "https://yandex.com/search/?text=" + search_text.replace(" ", "+") + pages
        print("[+] Searching results for '" + url.split("=")[1].replace("+", " ") +
              "' on '" + self.source + "' :\n")

        return self.fetch(url)

# y = Yandex()
# print(y.search("un avion"))

```
app/core/__init__.py
```.py
from app.core.Aol import Aol
from app.core.Ask import Ask
from app.core.Bing import Bing
from app.core.DogPile import DogPile
from app.core.DuckDuckGo import DuckDuckGo
from app.core.Gibiru import Gibiru
from app.core.Mojeek import Mojeek
from app.core.Google import Google
from app.core.Qwant import Qwant
from app.core.SearchEncrypt import SearchEncrypt
from app.core.StartPage import StartPage
from app.core.Yahoo import Yahoo
from app.core.Yandex import Yandex

```
app/main.py
```.py
# main-script
# -*- encoding: utf-8 -*-
#  _____ _    _     _        _    
# |  ___/ \  | |   | |      / \   
# | |_ / _ \ | |   | |     / _ \  
# |  _/ ___ \| |___| |___ / ___ \ 
# |_|/_/   \_\_____|_____/_/   \_\
#
# By Sanix-darker
__version__ = 0.1
__author__ = "Sanix-darker"

import argparse
from app.utils import *

if __name__ == "__main__":
    # Initialize the arguments
    # python3 -m app.main # Search-Engine list
    # python3 -m app.main -e aol -q "sanix darker"
    #
    # python3 -m app.main -e google -q "sanix darker" -p "&start=10"
    prs = argparse.ArgumentParser()
    prs.add_argument('-e', '--engine', help='The search engine', type=str, default="google")
    prs.add_argument('-q', '--query', help='The query text', type=str)
    prs.add_argument('-p', '--page', help='Number of pages to fetch', type=str, default="")
    prs = prs.parse_args()

    print("[+] Falla [the search-engine-scraper]")
    if prs.engine is not None and prs.query is not None:
        get_results(engine=prs.engine.lower(), query=prs.query.lower(), pages=prs.page)
    else:
        list_engines()

```
app/settings.py
```.py
import configparser as ConfigParser

# Configs parameters configParser.get('your-config', 'path1')
configParser = ConfigParser.RawConfigParser()
configFilePath = r'config.txt'
configParser.read(configFilePath)

# Filling parameters
SPLASH_SCRAP_URL = configParser.get('falla-config', 'SPLASH_SCRAP_URL')

```
app/utils.py
```.py
from os import listdir as ls
from app.core import *
import json


class Bcolors:
    """[summary]
    """
    AUTRE = '\033[96m'  # rose
    HEADER = '\033[95m'  # rose
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'  # jaune
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def list_engines():
    print(Bcolors().OKBLUE + "[+] Listing search-Engines" + Bcolors().ENDC)
    engines = [elt.replace(".py", "").lower() for elt in ls("./app/core/") if
               ".py" in elt and "__" not in elt and "falla" not in elt]
    for e in engines:
        print("[+] > " + Bcolors().AUTRE + e + Bcolors().ENDC)


def get_results(engine, query, pages):
    if engine == "aol" or engine == "al":
        f = Aol()
    elif engine == "ask" or engine == "ak":
        f = Ask()
    elif engine == "bing" or engine == "b":
        f = Bing()
    elif engine == "dogpile" or engine == "dp":
        f = DogPile()
    elif engine == "duckduckgo" or engine == "dd":
        f = DuckDuckGo()
    elif engine == "gibiru" or engine == "gu":
        f = Gibiru()
    elif engine == "mojeek" or engine == "m":
        f = Mojeek()
    elif engine == "qwant" or engine == "q":
        f = Qwant()
    elif engine == "searchencrypt" or engine == "se":
        f = SearchEncrypt()
    elif engine == "startpage" or engine == "sp":
        f = StartPage()
    elif engine == "yahoo" or engine == "y":
        f = Yahoo()
    elif engine == "google" or engine == "g":
        f = Google()
    else:
        f = Google()

    results = json.loads(f.search(query, pages))
    bcolors = Bcolors()

    for elt in results:
        print("|> " + bcolors.OKBLUE + elt["title"] + bcolors.ENDC)
        print("|- " + bcolors.WARNING + elt["href"] + bcolors.ENDC)
        print("|| " + elt["cite"])
        print("")

```
example.config.txt
```.txt
[falla-config]
SPLASH_SCRAP_URL = http://127.0.0.1:8050

```
requirements.txt
```.txt
requests==2.31.0
pandas==1.0.1
lxml==4.9.1
beautifulsoup4==4.8.2
selenium==3.141.0
configparser

```
tests/test.py
```.py

```


