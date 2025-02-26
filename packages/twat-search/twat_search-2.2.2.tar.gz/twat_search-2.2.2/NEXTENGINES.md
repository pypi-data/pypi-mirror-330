# Next backends and engines to implement

## Python googlesearch-python 

- [ ] Implement the `googlesearch-python` backend with the exposed engine `google-scraper` in `google_scraper.py`

Info: 

Token Usage:
GitHub Tokens: 3102
LLM Input Tokens: 0
LLM Output Tokens: 0
Total Tokens: 3102

FileTree:
.gitignore
README.md
googlesearch/__init__.py
googlesearch/user_agents.py
requirements.txt
setup.cfg
setup.py

Analysis:
.gitignore
```.gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/
```
README.md
# googlesearch
googlesearch is a Python library for searching Google, easily. googlesearch uses requests and BeautifulSoup4 to scrape Google. 

## Installation
To install, run the following command:
```bash
python3 -m pip install googlesearch-python
```

## Usage
To get results for a search term, simply use the search function in googlesearch. For example, to get results for "Google" in Google, just run the following program:
```python
from googlesearch import search
search("Google")
```

## Additional options
googlesearch supports a few additional options. By default, googlesearch returns 10 results. This can be changed. To get a 100 results on Google for example, run the following program.
```python
from googlesearch import search
search("Google", num_results=100)
```
If you want to have unique links in your search result, you can use the `unique` option as in the following program.
```python
from googlesearch import search
search("Google", num_results=100, unique=True)
```
In addition, you can change the language google searches in. For example, to get results in French run the following program:
```python
from googlesearch import search
search("Google", lang="fr")
```
You can also specify the region ([Country Codes](https://developers.google.com/custom-search/docs/json_api_reference#countryCodes)) for your search results. For example, to get results specifically from the US run the following program:
```python
from googlesearch import search
search("Google", region="us")
```
If you want to turn off the safe search function (this function is on by default), you can do this:
```python
from googlesearch import search
search("Google", safe=None)
```
To extract more information, such as the description or the result URL, use an advanced search:
```python
from googlesearch import search
search("Google", advanced=True)
# Returns a list of SearchResult
# Properties:
# - title
# - url
# - description
```
If requesting more than 100 results, googlesearch will send multiple requests to go through the pages. To increase the time between these requests, use `sleep_interval`:
```python
from googlesearch import search
search("Google", sleep_interval=5, num_results=200)
```

```
If requesting more than 10 results, but want to manage the batching yourself? 
Use `start_num` to specify the start number of the results you want to get:
```python
from googlesearch import search
search("Google", sleep_interval=5, num_results=200, start_result=10)
```

If you are using a HTTP Rotating Proxy which requires you to install their CA Certificate, you can simply add `ssl_verify=False` in the `search()` method to avoid SSL Verification.
```python
from googlesearch import search


proxy = 'http://username:password@proxy.host.com:8080/'
# or for socks5
# proxy = 'socks5://username:password@proxy.host.com:1080/'

j = search("proxy test", num_results=100, lang="en", proxy=proxy, ssl_verify=False)
for i in j:
    print(i)
```

googlesearch/__init__.py
```.py
"""googlesearch is a Python library for searching Google, easily."""
from time import sleep
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import unquote # to decode the url
from .user_agents import get_useragent


def _req(term, results, lang, start, proxies, timeout, safe, ssl_verify, region):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": get_useragent(),
            "Accept": "*/*"
        },
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests
            "hl": lang,
            "start": start,
            "safe": safe,
            "gl": region,
        },
        proxies=proxies,
        timeout=timeout,
        verify=ssl_verify,
        cookies = {
            'CONSENT': 'PENDING+987', # Bypasses the consent page
            'SOCS': 'CAESHAgBEhIaAB',
        }
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5, safe="active", ssl_verify=None, region=None, start_num=0, unique=False):
    """Search the Google search engine"""

    # Proxy setup
    proxies = {"https": proxy, "http": proxy} if proxy and (proxy.startswith("https") or proxy.startswith("http") or proxy.startswith("socks5")) else None

    start = start_num
    fetched_results = 0  # Keep track of the total fetched results
    fetched_links = set() # to keep track of links that are already seen previously

    while fetched_results < num_results:
        # Send request
        resp = _req(term, num_results - start,
                    lang, start, proxies, timeout, safe, ssl_verify, region)
        
        # put in file - comment for debugging purpose
        # with open('google.html', 'w') as f:
        #     f.write(resp.text)
        
        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", class_="ezO2md")
        new_results = 0  # Keep track of new results in this iteration

        for result in result_block:
            # Find the link tag within the result block
            link_tag = result.find("a", href=True)
            # Find the title tag within the link tag
            title_tag = link_tag.find("span", class_="CVA68e") if link_tag else None
            # Find the description tag within the result block
            description_tag = result.find("span", class_="FrIlee")

            # Check if all necessary tags are found
            if link_tag and title_tag and description_tag:
                # Extract and decode the link URL
                link = unquote(link_tag["href"].split("&")[0].replace("/url?q=", "")) if link_tag else ""
            # Extract and decode the link URL
            link = unquote(link_tag["href"].split("&")[0].replace("/url?q=", "")) if link_tag else ""
            # Check if the link has already been fetched and if unique results are required
            if link in fetched_links and unique:
                continue  # Skip this result if the link is not unique
            # Add the link to the set of fetched links
            fetched_links.add(link)
            # Extract the title text
            title = title_tag.text if title_tag else ""
            # Extract the description text
            description = description_tag.text if description_tag else ""
            # Increment the count of fetched results
            fetched_results += 1
            # Increment the count of new results in this iteration
            new_results += 1
            # Yield the result based on the advanced flag
            if advanced:
                yield SearchResult(link, title, description)  # Yield a SearchResult object
            else:
                yield link  # Yield only the link

            if fetched_results >= num_results:
                break  # Stop if we have fetched the desired number of results

        if new_results == 0:
            #If you want to have printed to your screen that the desired amount of queries can not been fulfilled, uncomment the line below:
            #print(f"Only {fetched_results} results found for query requiring {num_results} results. Moving on to the next query.")
            break  # Break the loop if no new results were found in this iteration

        start += 10  # Prepare for the next set of results
        sleep(sleep_interval)

```
googlesearch/user_agents.py
```.py
import random

def get_useragent():
    """
    Generates a random user agent string mimicking the format of various software versions.

    The user agent string is composed of:
    - Lynx version: Lynx/x.y.z where x is 2-3, y is 8-9, and z is 0-2
    - libwww version: libwww-FM/x.y where x is 2-3 and y is 13-15
    - SSL-MM version: SSL-MM/x.y where x is 1-2 and y is 3-5
    - OpenSSL version: OpenSSL/x.y.z where x is 1-3, y is 0-4, and z is 0-9

    Returns:
        str: A randomly generated user agent string.
    """
    lynx_version = f"Lynx/{random.randint(2, 3)}.{random.randint(8, 9)}.{random.randint(0, 2)}"
    libwww_version = f"libwww-FM/{random.randint(2, 3)}.{random.randint(13, 15)}"
    ssl_mm_version = f"SSL-MM/{random.randint(1, 2)}.{random.randint(3, 5)}"
    openssl_version = f"OpenSSL/{random.randint(1, 3)}.{random.randint(0, 4)}.{random.randint(0, 9)}"
    return f"{lynx_version} {libwww_version} {ssl_mm_version} {openssl_version}"
```
requirements.txt
```.txt
beautifulsoup4>=4.9
requests>=2.20

```
setup.cfg
```.cfg
[metadata]
description-file=README.md
license_files=LICENSE
```
setup.py
```.py
from setuptools import setup

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding='UTF-8') as fh:
    requirements = fh.read().split("\n")

setup(
    name="googlesearch-python",
    version="1.3.0",
    author="Nishant Vikramaditya",
    author_email="junk4Nv7@gmail.com",
    description="A Python library for scraping the Google search engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nv7-GitHub/googlesearch",
    packages=["googlesearch"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[requirements],
    include_package_data=True,
)

```


---

## searchit

- [ ] Implement the `searchit` backend with the exposed engines `google-searchit`, `yandex-searchit`, `qwant-searchit`, `bing-searchit` in `searchit.py`

Info

Token Usage:
GitHub Tokens: 7754
LLM Input Tokens: 0
LLM Output Tokens: 0
Total Tokens: 7754

FileTree:
.gitignore
CODE_OF_CONDUCT.md
README.md
requirements.txt
searchit/__init__.py
searchit/exceptions/__init__.py
searchit/scrapers/__init__.py
searchit/scrapers/bing.py
searchit/scrapers/google.py
searchit/scrapers/qwant.py
searchit/scrapers/scraper.py
searchit/scrapers/yandex.py
setup.py
test.py
tests/files/qwant.json
tests/test_qwant.py
tests/test_yandex.py

Analysis:
.gitignore
```.gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
```
CODE_OF_CONDUCT.md
# Contributor Covenant Code of Conduct

## Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, sex characteristics, gender identity and expression,
level of experience, education, socio-economic status, nationality, personal
appearance, race, religion, or sexual identity and orientation.

## Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
 advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
 address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
 professional setting

## Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

## Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at edmartin101@googlemail.com. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at https://www.contributor-covenant.org/version/1/4/code-of-conduct.html

[homepage]: https://www.contributor-covenant.org

For answers to common questions about this code of conduct, see
https://www.contributor-covenant.org/faq

README.md
# searchit
Searchit is a library for async scraping of search engines. The library supports multiple search engines 
(currently Google, Yandex, Qwant and Bing) with support for other search engines to come.

# Install
```
pip install searchit
```
Can be installed using pip, by running the above command.

# Using Searchit
```python
import asyncio

from searchit import GoogleScraper, YandexScraper, BingScraper
from searchit import ScrapeRequest

request = ScrapeRequest("watch movies online", 30)
google = GoogleScraper(max_results_per_page=10) # max_results = Number of results per page
yandex = YandexScraper(max_results_per_page=10)

loop = asyncio.get_event_loop()

results = loop.run_until_complete(google.scrape(request))
results = loop.run_until_complete(yandex.scrape(request))
```
To use Searchit users first create a ScrapeRequest object, with term and number of results as required fields. 
This object can then be passed to multiple different search engines and scraped asynchronously.

## Scrape Request - Object
```
term - Required str - the term to be searched for
count - Required int - the total number of results
domain - Optional[str] - the domain to search i.e. .com or .com
sleep - Optional[int] - time to wait betweeen paginating pages - important to prevent getting blocked
proxy - Optional[str] - proxy to be used to make request - default none
language - Optional[str] - language to conduct search in (only Google atm)
geo - Optional[str] - Geo location to conduct search from Yandex, and Qwant
```

## Roadmap
* Add additional search engines
* Tests
* Blocking non-async scrape method
* Add support for page rendering (Selenium and Puppeteer)
requirements.txt
```.txt
aiohttp>=3.6.2
beautifulsoup4>=4.8.2
black==24.3.0
pytest==5.3.2
```
searchit/__init__.py
```.py
from searchit.scrapers.google import GoogleScraper
from searchit.scrapers.yandex import YandexScraper
from searchit.scrapers.bing import BingScraper
from searchit.scrapers.scraper import ScrapeRequest
from searchit.scrapers.qwant import QwantScraper


__all__ = [
    "GoogleScraper",
    "YandexScraper",
    "BingScraper",
    "ScrapeRequest",
    "QwantScraper",
]

```
searchit/exceptions/__init__.py
```.py
class BlockedException(Exception):
    pass


class ConfigException(Exception):
    pass

```
searchit/scrapers/__init__.py
```.py
from searchit.scrapers.scraper import (
    SearchScraper,
    ScrapeRequest,
    ScrapeResponse,
    SearchResult,
)

```
searchit/scrapers/bing.py
```.py
import asyncio
from typing import List

import bs4

from searchit.scrapers import SearchScraper, ScrapeRequest, SearchResult, ScrapeResponse
from searchit.exceptions import BlockedException, ConfigException


def _check_config(max_results: int):
    if max_results > 30:
        raise ConfigException("Bing max results per page cannot be larger than 30")
    return max_results


class BingScraper(SearchScraper):

    BASE_URL = "https://www.bing.com/search?q={}&first={}&count={}"

    def __init__(self, max_results_per_page: int = 10):
        self.max_results = _check_config(max_results_per_page)

    def _parse_page(self, results: List[SearchResult], resp: ScrapeResponse) -> None:
        rank = len(results) + 1
        soup = bs4.BeautifulSoup(resp.html, "html.parser")
        for block in soup.find_all("li", attrs={"class": "b_algo"}):
            link = block.find("a", href=True)
            if link:
                link = link["href"]

            if not link:
                continue

            title = block.find("h2")
            if title:
                title = title.get_text()

            description = block.find("div", {"class": "b_caption"})
            if description:
                description = description.find("p")
                if description:
                    description = description.get_text()
            results.append(SearchResult(rank, link, title, description))
            rank += 1

    def _paginate(self, term: str, domain: str, language: str, count: int):
        urls: List[str] = []
        first = 1
        num = 0
        while num < count:
            urls.append(self.BASE_URL.format(term, first, self.max_results))
            num += self.max_results
        return urls

    def _check_exceptions(self, res: ScrapeResponse) -> None:
        if res.status >= 400:
            raise BlockedException("Blocked by Bing")
        return

    async def scrape(self, req: ScrapeRequest) -> List[SearchResult]:
        domain = req.domain if req.domain else ".com"
        language = req.language if req.language else "en"
        urls = self._paginate(req.term, domain, language, req.count)
        headers = self.user_agent()
        results = []
        for idx, uri in enumerate(urls):
            response = await self._scrape_one(uri, headers, req.proxy)
            self._check_exceptions(response)
            self._parse_page(results, response)
            if not idx == len(urls) - 1:
                await asyncio.sleep(req.sleep)
        return results

```
searchit/scrapers/google.py
```.py
import asyncio
from typing import List

import bs4

from searchit.scrapers import SearchScraper, ScrapeRequest, SearchResult, ScrapeResponse
from searchit.exceptions import BlockedException


class GoogleScraper(SearchScraper):

    BASE_URL = "https://www.google{}/search?q={}&num={}&hl={}&start={}&filter=0"

    def __init__(self, max_results_per_page: int = 100):
        self.max_results = max_results_per_page

    def _parse_page(self, results: List[SearchResult], res: ScrapeResponse) -> None:
        rank = len(results) + 1
        soup = bs4.BeautifulSoup(res.html, features="html.parser")
        for block in soup.find_all("div", attrs={"class": "g"}):
            link = block.find("a", href=True)
            if link:
                link = link["href"]

            if link.startswith("/") or link.startswith("#"):
                continue

            title = block.find("h3")
            if title:
                title = title.get_text()

            description = block.find("div", {"data-content-feature": "1"})
            if description:
                description = description.get_text()
            results.append(SearchResult(rank, link, title, description))
            rank += 1

    def _check_exceptions(self, res: ScrapeResponse):
        if res.status >= 400:
            raise BlockedException("Google has rate limited this IP address")

    def _paginate(self, term: str, domain: str, language: str, count: int) -> List[str]:
        urls = []
        start = 0
        term = term.replace(" ", "+")
        while start < count:
            num = min(self.max_results, count - start)
            urls.append(self.BASE_URL.format(domain, term, num, language, start))
            start += self.max_results
        return urls

    async def scrape(self, req: ScrapeRequest) -> List[SearchResult]:
        domain = req.domain if req.domain else ".com"
        language = req.language if req.language else "en"
        urls = self._paginate(req.term, domain, language, req.count)
        headers = self.user_agent()
        results = []
        for idx, uri in enumerate(urls):
            response = await self._scrape_one(uri, headers, req.proxy)
            self._check_exceptions(response)
            self._parse_page(results, response)
            if not idx == len(urls) - 1:
                await asyncio.sleep(req.sleep)
        return results

```
searchit/scrapers/qwant.py
```.py
import asyncio
from typing import Dict, List, Optional

from aiohttp import ClientSession, ClientError

from searchit.scrapers import SearchScraper, ScrapeRequest, SearchResult, ScrapeResponse
from searchit.exceptions import BlockedException, ConfigException


def _check_config(max_results: int):
    if max_results > 10:
        raise ConfigException("Qwant max results per page cannot be larger than 10")
    return max_results


class QwantScraper(SearchScraper):

    BASE_URL = (
        "https://api.qwant.com/v3/search/web?count={}&offset={}"
        "&q={}&t=web&device=desktop&extensionDisabled=true&safesearch=0&locale={}&uiv=4"
    )

    def __init__(self, max_results_per_page: int = 10):
        self.max_results = _check_config(max_results_per_page)

    async def _scrape_one(
        self, url: str, headers: Dict[str, str], proxy: Optional[str]
    ) -> ScrapeResponse:
        async with ClientSession() as client:
            try:
                async with client.get(
                    url, headers=headers, proxy=proxy, timeout=60
                ) as response:
                    json = await response.json()
                    return ScrapeResponse("", response.status, json=json)
            except ClientError as err:
                raise err

    def _parse_json(self, results: List[SearchResult], resp: ScrapeResponse) -> None:
        data = resp.json['data']['result']['items']["mainline"]
        items: List[Dict] = []
        for listing in data:
            context = listing.get('items')
            if context:
                for c in context:
                    items.append(c)
        for search_result in items:
            title = search_result.get("title")
            url = search_result.get("url")
            if url is None:
                continue
            description = search_result.get("description")
            position = len(results) + 1
            results.append(SearchResult(position, url, title, description))

    def _paginate(self, term: str, _: str, geo: str, count: int):
        urls: List[str] = []
        offset = 0
        term = term.replace(" ", "%20")
        while offset < count:
            urls.append(self.BASE_URL.format(self.max_results, offset, term, geo))
            offset += self.max_results
        return urls

    def _check_exceptions(self, res: ScrapeResponse) -> None:
        if res.json["status"] != "success":
            raise BlockedException("Qwant request was not successful")
        return

    async def scrape(self, req: ScrapeRequest) -> List[SearchResult]:
        geo = req.geo if req.geo else "en_GB"
        urls = self._paginate(req.term, "", geo, req.count)
        headers = self.user_agent()
        results = []
        for idx, uri in enumerate(urls):
            response = await self._scrape_one(uri, headers, req.proxy)
            self._check_exceptions(response)
            self._parse_json(results, response)
            if not idx == len(urls) - 1:
                await asyncio.sleep(req.sleep)
        return results

```
searchit/scrapers/scraper.py
```.py
from abc import ABCMeta, abstractmethod
from random import choice
from typing import Dict, List, Optional

from aiohttp import ClientSession, ClientError


_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
]


class ScrapeRequest:
    def __init__(
        self,
        term: str,
        count: int,
        domain: Optional[str] = None,
        sleep: int = 0,
        proxy: Optional[str] = None,
        language: Optional[str] = None,
        geo: Optional[str] = None,
    ):
        self.term = term
        self.count = count
        self.domain = domain
        self.sleep = sleep
        self.proxy = proxy
        self.language = language
        self.geo = geo


class ScrapeResponse:
    def __init__(self, html: str, status: int, json: Optional[Dict] = None):
        self.html = html
        self.json = json
        self.status = status

    def __repr__(self):
        return "<ScrapeResponse: html:{}, status:{}>".format(
            self.html[:10], self.status,
        )


class SearchResult:
    def __init__(
        self, rank: int, url: int, title: str, description: str,
    ):
        self.rank = rank
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return "<SearchResult: Rank:{}, URL: {}>".format(self.rank, self.url)


class SearchScraper(metaclass=ABCMeta):
    @staticmethod
    def user_agent() -> Dict[str, str]:
        return {
            "User-Agent": choice(_USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    async def _scrape_one(
        self, url: str, headers: Dict[str, str], proxy: Optional[str]
    ) -> ScrapeResponse:
        async with ClientSession() as client:
            try:
                async with client.get(
                    url, headers=headers, proxy=proxy, timeout=60
                ) as response:
                    html = await response.text()
                    return ScrapeResponse(html, response.status)
            except ClientError as err:
                raise err

    @abstractmethod
    def _check_exceptions(self, res: ScrapeResponse) -> None:
        pass

    @abstractmethod
    def _paginate(self, term: str, domain: str, language: str, count: int) -> List[str]:
        pass

    @abstractmethod
    async def scrape(self, request: ScrapeRequest):
        pass

```
searchit/scrapers/yandex.py
```.py
import asyncio
from typing import List, Dict

import bs4

from searchit.scrapers.scraper import (
    SearchScraper,
    ScrapeResponse,
    ScrapeRequest,
    SearchResult,
)
from searchit.exceptions import BlockedException, ConfigException


def _clean_yandex_url(url: str) -> str:
    if url.startswith("//"):
        return f"https:{url}"
    return url


def _check_config(max_results: int):
    if max_results > 10:
        raise ConfigException("Yandex max results per page cannot be larger than 10")
    return max_results


class YandexScraper(SearchScraper):

    BASE_URL = "https://yandex{}/search/?text={}&lr={}&p={}"
    DEFAULT_GEO = "10394"

    def __init__(self, max_results_per_page: int = 10):

        self.max_results = _check_config(max_results_per_page)

    def _parse_page(self, results: List[SearchResult], res: ScrapeResponse):
        rank = len(results) + 1
        soup = bs4.BeautifulSoup(res.html, "html.parser")
        for block in soup.find_all("li", attrs={"class": "serp-item"}):
            title_block = block.find("h2", attrs={"class": "organic__title-wrapper"})
            if not title_block:
                continue
            title_text = title_block.get_text()
            url = title_block.find("a", href=True)
            if url:
                url = _clean_yandex_url(url["href"])
            description = block.find("div", attrs={"class": "text-container"})
            if description:
                description = description.get_text()

            results.append(SearchResult(rank, url, title_text, description))
            rank += 1

    def _paginate(self, term: str, domain: str, location: str, count: int) -> List[str]:
        urls = []
        done = 0
        pg = 0
        while done < count:
            term = term.replace(" ", "%20")
            num_doc = min(self.max_results, count - done)
            urls.append(self.BASE_URL.format(domain, term, location, num_doc, pg))
            done += num_doc
            pg += 1
        return urls

    def _check_exceptions(self, res: ScrapeResponse):
        if res.status >= 400:
            raise BlockedException("Yandex has blocked this request")

    @staticmethod
    def user_agent() -> Dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-ch-ua": """Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109""",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }

    async def scrape(self, request: ScrapeRequest) -> List[SearchResult]:
        domain = request.domain if request.domain else ".ru"
        location = request.geo if request.geo else self.DEFAULT_GEO
        urls = self._paginate(request.term, domain, location, request.count)
        headers = self.user_agent()
        results = []
        for idx, uri in enumerate(urls):
            response = await self._scrape_one(uri, headers, request.proxy)
            self._check_exceptions(response)
            self._parse_page(results, response)
            if not idx == len(urls) - 1:
                await asyncio.sleep(request.sleep)
        return results



```
setup.py
```.py
import sys
import pathlib
from setuptools import find_packages
from distutils.core import setup


if sys.version_info <= (3, 5, 3):
    raise RuntimeError("aiohttp 3.x requires Python 3.5.3+")


here = pathlib.Path(__file__).parent


install_requires = [
    'aiohttp>=3.6.2',
    'beautifulsoup4>=4.8.2',
]


def read(f):
    return (here / f).read_text('utf-8').strip()


args = dict(
    name='searchit',
    version='2023.02.05.1',
    description='Aysncio search engine scraping package',
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    author='Edmund Martin',
    maintainer='Edmund Martin <edmartin101@gmail.com>',
    maintainer_email='edmartin101@gmail.com',
    url='https://github.com/EdmundMartin/search_it',
    packages=find_packages(exclude=('tests', '*.tests', '*.tests.*')),
    python_requires='>=3.6',
    install_requires=install_requires,
    include_package_data=True,
)

setup(**args)

```
test.py
```.py

```
tests/files/qwant.json
```.json
{"status":"success","data":{"query":{"locale":"en_gb","query":"watch movies online","offset":0},"cache":{"key":"f2dd7315213bb685f12aff0410af4e66","created":1577667568,"expiration":604800,"status":"hits","age":61168,"version":1,"system":"R","mode":3},"result":{"total":49,"items":[{"title":"<b>Watch Movies Online<\/b> For Free | Zmovies","favicon":"\/\/s.qwant.com\/fav\/z\/m\/zmovies_me.ico","url":"https:\/\/zmovies.me\/","source":"https:\/\/zmovies.me","desc":"<b>Watch movies online<\/b> for free on zmovie, putlocker,vodlocker, sockshare, download full movie for free in high quality for free.","_id":"e46c71e5884261b8ff7696dac37af3d9","score":0,"position":1},{"title":"123movies: <b>Watch Movies Online<\/b>","favicon":"\/\/s.qwant.com\/fav\/1\/2\/123moviespower_com.ico","url":"https:\/\/123moviespower.com\/","source":"https:\/\/123moviespower.com","desc":"<b>Watch<\/b> HD <b>Movies Online<\/b> For Free and Download the latest <b>movies<\/b> without Registration at 123movies","_id":"c0f85aa3fb5dcdadd4432f33f26514eb","score":0,"position":2},{"title":"GoStream | 123movies | <b>Watch Movies Online<\/b>","favicon":"\/\/s.qwant.com\/fav\/g\/o\/gostream_site.ico","url":"https:\/\/gostream.site\/","source":"https:\/\/gostream.site","desc":"No video file is hosted on Gostream, all the files are uploaded by non affiliated uploaders on file-sharing hosts. FREE <b>MOVIES<\/b> <b>WATCH MOVIES ONLINE<\/b> FREE FREE <b>MOVIES ONLINE<\/b> <b>WATCH<\/b> FULL <b>MOVIES ONLINE<\/b> FREE <b>ONLINE<\/b> <b>MOVIES<\/b> FULL <b>WATCH MOVIES<\/b> 123Movies","_id":"623920cbaa439ef7f3eb6c4a71863da7","score":0,"position":3},{"title":"StreamDor \u2013 <b>watch movies online<\/b> for free","favicon":"\/\/s.qwant.com\/fav\/s\/t\/www_streamdor_com.ico","url":"https:\/\/www.streamdor.com\/","source":"https:\/\/www.streamdor.com","desc":"Web\u2019s largest catalog of free movies. <b>Watch movies online<\/b> for free. Just click and watch! No registration, no fees.","_id":"e93c7599ab1db3b376f3b85dd8188ec8","score":0,"position":4},{"title":"<b>Watch Movies Online<\/b> | Free Full Movie","favicon":"\/\/s.qwant.com\/fav\/v\/e\/vexmovies_org.ico","url":"http:\/\/vexmovies.org\/","source":"vexmovies.org","desc":"<b>Watch<\/b> Full <b>Movies<\/b> Free - Stream <b>Online<\/b> <b>Movies<\/b> in HD. Better than 123movies, Putlocker - No popups, no registration. 12000+ <b>Movies<\/b>.","_id":"2b97df5c198dc23cc684c844b5e0d533","score":0,"position":5},{"title":"<b>Movies<\/b> | <b>Watch<\/b> Free <b>Movies<\/b> &amp; TV Shows <b>Online<\/b> | Popcornflix","favicon":"\/\/s.qwant.com\/fav\/p\/o\/www_popcornflix_com.ico","url":"https:\/\/www.popcornflix.com\/","source":"https:\/\/www.popcornflix.com","desc":"<b>Watch<\/b> free <b>movies<\/b> and TV shows <b>online<\/b> at Popcornflix! <b>Watch<\/b> free <b>movies<\/b> and TV shows <b>online<\/b> at Popcornflix! <b>Watch<\/b> Free <b>Movies<\/b> &amp; TV Shows <b>Online<\/b> | Popcornflix","_id":"112ab3b1edcfbe4626de29b601ff6d20","score":0,"position":6},{"title":"<b>Watch Movies Online<\/b> Free, Streaming Films Without Downloading","favicon":"\/\/s.qwant.com\/fav\/1\/w\/1watchfree_me.ico","url":"https:\/\/1watchfree.me\/","source":"https:\/\/1watchfree.me","desc":"<b>Watch<\/b> latest and classical <b>movies online<\/b> for free. Various genres: action,animation,comedy,thriller, etc. Without downloading and registration, only streaming films at <b>Watch<\/b>-free.me","_id":"632dc70551be182c50d2c0f9c2ba5da3","score":0,"position":7},{"title":"Watchmoviesfree - best website for <b>watch movies<\/b> free ...","favicon":"\/\/s.qwant.com\/fav\/w\/a\/watchmoviesfree_org.ico","url":"https:\/\/watchmoviesfree.org\/","source":"https:\/\/watchmoviesfree.org","desc":"You can <b>watch movies<\/b> for free on our website without subscription, <b>watch<\/b> TV shows and don\u2019t have to pay for this. Watchmoviesfree.us works more than 3 years.","_id":"18023fb8f40c6ba265b9a82ca9cdbbe9","score":0,"position":8},{"title":"123movies4u | 123movies - <b>Watch Movies Online<\/b> Free | Watch ...","favicon":"\/\/s.qwant.com\/fav\/1\/2\/123movies4u_bid.ico","url":"https:\/\/123movies4u.bid\/","source":"https:\/\/123movies4u.bid","desc":"123movies, <b>watch movies<\/b>, <b>watch<\/b> latest <b>movies<\/b> 123movies, newly added movie list, daily updated movie free <b>online<\/b>. Putlocker <b>Movies<\/b>, Stream new <b>movies<\/b>.","_id":"3dd78b1a9358db68577f7804a7f54252","score":0,"position":9},{"title":"Movies123 | <b>Watch Movies Online<\/b> for Free in HD","favicon":"\/\/s.qwant.com\/fav\/m\/o\/movies123_pics.ico","url":"https:\/\/movies123.pics\/","source":"https:\/\/movies123.pics","desc":"<b>Watch<\/b> Tons Free Full <b>Movies<\/b> &amp; TV Show <b>Online<\/b> on Movies123! <b>Watch<\/b> <b>online<\/b> <b>movies<\/b> free on PC, Mac, Linux, Android, and iOS. No signup! No fee! No waiting\u200e!","_id":"a3c357124738941e6ca76214602813fa","score":0,"position":10}],"filters":{"freshness":{"label":"Freshness","name":"freshness","type":"dropdown","selected":"all","values":[{"value":"all","label":"All time","translate":true},{"value":"day","label":"Past 24 hours","translate":true},{"value":"week","label":"Past week","translate":true},{"value":"month","label":"Past month","translate":true}]}},"ads":[]}}}
```
tests/test_qwant.py
```.py
import json

import pytest

from searchit.scrapers.qwant import QwantScraper
from searchit.scrapers.scraper import ScrapeResponse


@pytest.yield_fixture(scope="function")
def qwant_json_response():
    with open('./files/qwant.json', 'r') as outfile:
        res_obj = json.load(outfile)
    yield ScrapeResponse("", 200, json=res_obj)


def test_qwant_paginate():
    q = QwantScraper()
    result = q._paginate("watch movies", "", "en_GB", 100)
    assert len(result) == 10


def test_qwant_parse(qwant_json_response):
    q = QwantScraper()
    results = []
    q._parse_json(results, qwant_json_response)
    assert len(results) == 10

```
tests/test_yandex.py
```.py
import pytest

from searchit.scrapers.yandex import YandexScraper
from searchit.scrapers.scraper import ScrapeResponse


@pytest.yield_fixture(scope='function')
def yandex_response():
    with open('./files/yandex.html', 'r', errors='ignore') as yandex_html:
        yield ScrapeResponse(yandex_html.read(), 200)


def test_yandex_parsing(yandex_response):
    y = YandexScraper()
    results = []
    y._parse_page(results, yandex_response)
    assert len(results) == 13

```

---

## anywebsearch

- [ ] Implement the `anywebsearch` backend with the exposed engines `google-anyws`, `bing-anyws`, `brave-anyws`, `qwant-anyws`, `yandex-anyws` in `anywebsearch.py`

Token Usage:
GitHub Tokens: 5679
LLM Input Tokens: 0
LLM Output Tokens: 0
Total Tokens: 5679

FileTree:
.github/workflows/publish.yml
.github/workflows/test.yml
.gitignore
README.md
anywebsearch/__init__.py
anywebsearch/engines/__init__.py
anywebsearch/engines/brave.py
anywebsearch/engines/duck.py
anywebsearch/engines/google.py
anywebsearch/engines/qwant.py
anywebsearch/engines/yandex.py
anywebsearch/search.py
anywebsearch/tools.py
pyproject.toml
requirements.txt
test.py

Analysis:
.github/workflows/publish.yml
```.yml
name: Publish Python Package

on:
  release:
    types: [created]

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: release
    permissions:
      id-token: write
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        cache: pip
        cache-dependency-path: pyproject.toml
    - name: Install dependencies
      run: |
        pip install setuptools wheel build
    - name: Build
      run: |
        python -m build
    - name: Publish
      uses: pypa/gh-action-pypi-publish@release/v1


```
.github/workflows/test.yml
```.yml
name: Test

on: [push, pull_request]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        cache: pip
        cache-dependency-path: pyproject.toml
    - name: Install dependencies
      run: |
        pip install '.[test]'
    - name: Run tests
      run: |
        pytest


```
.gitignore
```.gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

.fleet/
```
README.md
# Any Web Search

Unified internet search across different search engines: Google, Bing(ddg), Brave, Qwant, Yandex

anywebsearch/__init__.py
```.py
from .tools import Settings
from .search import multi_search

```
anywebsearch/engines/__init__.py
```.py
from .google import google_search
from .qwant import qwant_search
from .duck import duck_search
from .brave import brave_search
from .yandex import yandex_search

```
anywebsearch/engines/brave.py
```.py
from anywebsearch.tools import SearchResult, Settings, normalise_url, merge_results
from brave import Brave
import time


def brave_search(query, lang: str = None, reverse=None, offset=0, settings: Settings = Settings()):
    # Brave search API
    if lang is None:
        lang = settings.language
    try:
        brave_key = str(settings.extra.get('brave_key'))
    except KeyError:
        raise KeyError("Specify the brave_key in the settings class")
    try:
        brave = Brave(brave_key)
        sr = brave.search(
            q=query,
            count=settings.num_results,
            offset=offset if reverse else 0,
            search_lang=lang,
            result_filter='web',
            text_decorations=False,
            country=lang
        )
    except AttributeError as e:
        raise RuntimeError("Bad response! You probably provided an invalid brave_key", e)
    sr = [*sr][3][1].results  # unpack result -> WEB results field -> skip type (0) -> extract results
    sr = [
        SearchResult(result.title, result.description, normalise_url(result.url))
        for result in sr
    ]
    if not reverse and len(sr) < settings.num_results:
        i = 0
        while len(sr) < settings.num_results:
            i += 1
            sr = [*sr, *brave_search(query=query, lang=lang, reverse=sr, offset=i, settings=settings)]
            if settings.del_dups is True:
                sr = merge_results([sr])  # don't merge anything, just del dups
        sr = sr[:settings.num_results]
    return sr

```
anywebsearch/engines/duck.py
```.py
from duckduckgo_search import DDGS

from anywebsearch.tools import SearchResult, Settings, normalise_url, merge_results


def duck_search(query, lang: str = None, settings: Settings = Settings()):
    # ddg search API call
    lang_codes = {
        "AR": "xa-ar",
        "AU": "au-en",
        "AT": "at-de",
        "BE": "be-fr",
        "BR": "br-pt",
        "CA": "ca-en",
        "CL": "cl-es",
        "DK": "dk-da",
        "FI": "fi-fi",
        "FR": "fr-fr",
        "DE": "de-de",
        "HK": "hk-tzh",
        "IN": "in-en",
        "ID": "id-id",
        "IT": "it-it",
        "JP": "jp-jp",
        "KR": "kr-kr",
        "MY": "my-ms",
        "MX": "mx-es",
        "NL": "nl-nl",
        "NZ": "nz-en",
        "NO": "no-no",
        "CN": "cn-zh",
        "PL": "pl-pl",
        "PT": "pt-pt",
        "PH": "ph-en",
        "RU": "ru-ru",
        "SA": "za-en",
        "ZA": None,
        "ES": "es-es",
        "SE": "se-sv",
        "CH": "ch-de",
        "TW": "tw-tzh",
        "TR": "tr-tr",
        "GB": "uk-en",
        "US": "us-en",
        "ALL": "wt-wt",
    }
    if lang is None:
        lang = settings.language
    lang = lang_codes[lang.upper()] if lang.upper() in lang_codes.keys() else "us-en"
    sr = DDGS().text(
        query,
        region=lang,
        max_results=(
            settings.num_results + int(settings.num_results / 4)
            if settings.del_dups is True
            else settings.num_results
        )
        # +25% in case of duplicates, and the excess will be trimmed
    )
    sr = [
        SearchResult(result['title'], result['body'], normalise_url(result['href']))
        for result in sr
    ]
    if settings.del_dups is True:
        sr = merge_results([sr])  # don't merge anything, just del dups
    sr = sr[:settings.num_results]
    return sr

```
anywebsearch/engines/google.py
```.py
import googlesearch as gs

from anywebsearch.tools import SearchResult, Settings, normalise_url, merge_results


def google_search(query, lang: str = None, settings: Settings = Settings()):
    # Google search
    if lang is None:
        lang = settings.language
    sr = gs.search(
        query,
        advanced=True,
        num_results=(
            settings.num_results + int(settings.num_results / 4)
            if settings.del_dups is True
            else settings.num_results
        ),
        # +10 in case of duplicates, and the excess will be trimmed
        lang=lang
    )
    sr = [
        SearchResult(result.title, result.description, normalise_url(result.url))
        for result in sr
    ]
    if settings.del_dups is True:
        sr = merge_results([sr])  # don't merge anything, just del dups
    sr = sr[:settings.num_results]
    return sr

```
anywebsearch/engines/qwant.py
```.py
import requests

from anywebsearch.tools import SearchResult, Settings, normalise_url, random_agent, merge_results


def qwant_search(query, lang: str = None, reverse=None, offset=0, settings: Settings = Settings()):
    lang_codes = {
        "AR": None,
        "AU": "en_au",
        "AT": "de_at",
        "BE": "fr_be",
        "BR": "br_fr",
        "CA": "en_ca",
        "CL": "es_cl",
        "DK": "da_dk",
        "FI": "fi_fi",
        "FR": "fr_fr",
        "DE": "de_de",
        "HK": "zh_hk",
        "IN": None,
        "ID": None,
        "IT": "it_it",
        "JP": None,
        "KR": "ko_kr",
        "MY": "en_my",
        "MX": "es_mx",
        "NL": "nl_nl",
        "NZ": "en_nz",
        "NO": "nb_no",
        "CN": "zh_cn",
        "PL": "pl_pl",
        "PT": "pt_pt",
        "PH": None,
        "RU": None,
        "SA": None,
        "ZA": None,
        "ES": "es_es",
        "SE": "sv_se",
        "CH": "de_ch",
        "TW": "zh_tw",
        "TR": None,
        "GB": "en_gb",
        "US": "en_us",
        "ALL": None,
    }
    headers = {'User-Agent': random_agent()}
    if lang is None:
        lang = settings.language
    rlang = lang
    lang = (
        lang_codes[lang.upper()]
        if lang.upper() in lang_codes.keys() and lang_codes[lang.upper()]
        else 'ALL'
    )
    # print("Qwant used lang", lang)
    params = {
        'q': query,
        'offset': offset if reverse else 0,
        # &count is always 10
    }
    if lang != "ALL":
        params['locale'] = lang
    url = 'https://api.qwant.com/v3/search/web'  # ?q=elon%20musk&locale=de_de&offset=0
    raw_sr = requests.get(url, params=params, headers=headers)
    raw_sr.raise_for_status()
    sr = raw_sr.json()  # convert to json
    sr = sr['data']['result']['items']['mainline']  # extract results field from this complex json
    sr = [item for item in sr if item['type'] == 'web']  # extract only web results (there are also videos, ads, images)
    restructed_sr = []
    # There might be a few web blocks with items
    for block in sr:
        for item in block['items']:
            restructed_sr.append(item)
    sr = [
        SearchResult(result['title'], result['desc'], normalise_url(result['url']))
        for result in restructed_sr
    ]
    if not reverse and len(sr) < settings.num_results:
        i = 0
        while len(sr) < settings.num_results:
            i += 10
            sr = [*sr, *qwant_search(query, rlang, reverse=sr, offset=i, settings=settings)]
            if settings.del_dups is True:
                sr = merge_results([sr])  # don't merge anything, just del dups
        sr = sr[:settings.num_results]
    return sr

```
anywebsearch/engines/yandex.py
```.py
from anywebsearch.tools import SearchResult, Settings, normalise_url, merge_results, random_agent

import xmltodict
import requests


#   _      __  ____    ___    __ __        ____   _  __        ___    ___   ____   _____   ___    ____   ____   ____
#  | | /| / / / __ \  / _ \  / //_/       /  _/  / |/ /       / _ \  / _ \ / __ \ / ___/  / _ \  / __/  / __/  / __/
#  | |/ |/ / / /_/ / / , _/ / ,<         _/ /   /    /       / ___/ / , _// /_/ // (_ /  / , _/ / _/   _\ \   _\ \  
#  |__/|__/  \____/ /_/|_| /_/|_|       /___/  /_/|_/       /_/    /_/|_| \____/ \___/  /_/|_| /___/  /___/  /___/  
#                                                                                                                   

def yandex_search(query, lang: str = None, reverse=None, offset=0, settings: Settings = Settings()):
    if lang is None:
        lang = settings.language
        if lang != "ru":
            lang = "en"

    url = f"https://yandex.com/search/xml?folderid={settings.extra.get('ya_fldid')}&filter=moderate&lr=225&l10n={lang}"
    payload = """<?xml version="1.0" encoding="UTF-8"?>
    <request>
        <query>
            {query}
        </query>
        <groupings>
            <groupby attr="" mode="flat" groups-on-page="10" docs-in-group="1" />
        </groupings>
        <maxpassages>5</maxpassages>
        <page>{offset}</page>
    </request>
    """.format(query=query, offset=offset)
    print(payload)
    headers = {
        'Content-Type': 'application/xml',
        'User-Agent': random_agent(),
        'Authorization': f'Api-Key {settings.extra.get("ya_key")}'
    }
    response = requests.request("POST", url, data=payload, headers=headers, timeout=8)
    response.raise_for_status()
    sr = xmltodict.parse(response.content)

    try:
        sr = sr['yandexsearch']['response']['results']['grouping']['group']
    except KeyError as e:
        if sr['yandexsearch']['response']['error']['@code'] == '31':
            raise RuntimeError("Incorrect yandex API key or folder id")
        raise RuntimeError(e)

    sr = [group['doc'] for group in sr]
    # TODO
    sr = [
        SearchResult(
            result['title']['#text'] if type(result['title']) is dict else result['title'],
            result['passages']['passage']['#text'] if 'passages' in result and type(
                result['passages']['passage']) is dict else "no text",
            normalise_url(result['url'])
        )
        for result in sr
        if (not all(v is None for v in result))
    ]

    if not reverse and len(sr) < settings.num_results:
        i = 0
        while len(sr) < settings.num_results:
            i += 1
            sr = [*sr, *yandex_search(query, lang, reverse=sr, offset=i, settings=settings)]
        sr = sr[:settings.num_results]

    print(sr)

```
anywebsearch/search.py
```.py
from .tools import merge_results, Settings

from .engines import google_search, qwant_search, duck_search, brave_search, yandex_search

possible_engines = {
    'google': google_search,
    'qwant': qwant_search,
    'duck': duck_search,  # duck is DuckDuckGo (bing engine)
    'brave': brave_search,
    'yandex': yandex_search,
}


def multi_search(query, settings: Settings = Settings()):
    for e in settings.engines:
        if e not in possible_engines.keys():
            raise ValueError(f"Invalid search engine name: {e}")

    results_lists = []
    for e in settings.engines:
        results_lists.append(possible_engines[e](query=query, lang=settings.language, settings=settings))
    if settings.merge is True:
        return merge_results(results_lists)
    return results_lists

```
anywebsearch/tools.py
```.py
import re
import urllib.parse
import w3lib.url
import random


class Settings:
    def __init__(
            self,
            language: str = 'en',
            num_results: int = 20,
            merge: bool = True,
            engines: list = None,
            **kwargs
    ):
        """
        For settings only.
        When merge set True, dups will be deleted, and for multi search it will merge results as well.
        engines is a mandatory parameter for multi search - list of engines to use.
        You can set additionall settings in kwargs, like api keys (brave, yandex)
        possible:
            brave_key - brave api key
            ya_key - yandex cloud api key
            ya_fldid - yandex cloud folder id 
        """
        extra_keys = [
            'brave_key', 'ya_key', 'ya_fldid'
        ]
        # TODO: add check for possible lang codes # languages = ['en', ...]
        for k in kwargs:
            if k not in extra_keys:
                raise KeyError("Unexpected key given:", k)

        self.language = language
        self.num_results = num_results
        self.del_dups = merge  # for single search
        self.merge = merge  # for multi search
        self.engines = engines
        self.extra = kwargs


class SearchResult:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


def random_agent():
    return random.choice([
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6; en-US) Gecko/20100101 Firefox/45.4',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows; U; Windows NT 6.0; x64 Trident/4.0)'
        'Mozilla/5.0 (Linux i563 x86_64; en-US) Gecko/20100101 Firefox/55.0',
        'Mozilla/5.0 (Linux i573 x86_64; en-US) Gecko/20100101 Firefox/56.9',
        'Mozilla/5.0 (Linux; Linux x86_64) Gecko/20100101 Firefox/67.2',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_2) Gecko/20130401 Firefox/68.1',
        'Mozilla/5.0 (U; Linux x86_64; en-US) Gecko/20100101 Firefox/69.5',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 9_3_8; en-US) Gecko/20100101 Firefox/68.8',

    ])


def normalise_url(url):
    url = str(url)
    # Remove the scheme (http(s)://)
    url = re.sub(r'^https?://', '', url)
    # Remove the "www" if it exists
    url = re.sub(r'^www\.', '', url)
    # add slush to the end
    url = (url + "/") if not url.endswith("/") else url
    # decode if needed 
    url = urllib.parse.unquote(url)
    # Canonicalise url
    url = w3lib.url.canonicalize_url(url)
    return url


def merge_results(res_lists: list):
    """
        Merge results from diffirent engines by unique url
    """
    merged = []
    uniq_urls = []

    for lst in res_lists:
        # print("Engine results num =", len(lst))
        for item in lst:
            if item.url not in uniq_urls:
                merged.append(item)
                uniq_urls.append(item.url)

    # print("Total num =", len(merged))
    return merged

```
pyproject.toml
```.toml
[project]
name = "anywebsearch"
version = "0.1"
description = "Unified internet search across different search engines: Google, Bing(ddg), Brave, Qwant, Yandex"
readme = "README.md"
requires-python = ">=3.8.9"
authors = [{ name = "Timur Tunkin", email = "ch.houstone@zohomail.com" }]
license = { file = "LICENSE" }
classifiers = [
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Internet",
]
dependencies = [
    "googlesearch-python",
    "brave-search",
    "duckduckgo_search>=5.0",
    "w3lib>=2.1.2",
    "requests>=2.31.0",
    "xmltodict",
]

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project.urls]
Homepage = "https://github.com/tphlru/anywebsearch"
Changelog = "https://github.com/tphlru/anywebsearch/releases"
Issues = "https://github.com/tphlru/anywebsearch/issues"
CI = "https://github.com/tphlru/anywebsearch/actions"

```
requirements.txt
```.txt
googlesearch-python
brave-search
duckduckgo_search >= 5.0
w3lib>=2.1.2
requests >= 2.31.0
xmltodict
```
test.py
```.py
from anywebsearch.engines import google_search
from anywebsearch import Settings
from anywebsearch import multi_search

sett = Settings(num_results=30, language='ru', engines=['yandex'], merge=True,
                ya_key="AQVNzCh0OBoUltdwxSsAdKvjpKVzziCHp6XWfLuS", ya_fldid="b1gd3a1fipj0pq2l1f8a")

t = multi_search(query="Elon Musk", settings=sett)
for i in t:
    print(i)

print(len(t))

```

