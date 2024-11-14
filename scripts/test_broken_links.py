import warnings

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

ALREADY_CHECKED_LINKS = set()


def check_link(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code >= 400:
            warnings.warn(f"Broken link: {url} - Status code: {response.status_code}")
        else:
            pass
            # print(f"OK link: {url}")
        return response.status_code
    except requests.RequestException as e:
        warnings.warn(f"Error checking link: {url} - {e}")
        return None


def crawl_and_check(base_url, max_depth=2, current_depth=0):
    print(f"Opening: {base_url}")
    if max_depth is not None and current_depth > max_depth:
        return

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [urljoin(base_url, link.get('href')) for link in soup.find_all('a', href=True)]

        for link in links:
            # Only check internal links
            if urlparse(link).netloc == urlparse(base_url).netloc and link not in ALREADY_CHECKED_LINKS:
                ALREADY_CHECKED_LINKS.add(link)
                check_link(link)
                # Recursive crawl
                crawl_and_check(link, max_depth, current_depth + 1)
            elif link not in ALREADY_CHECKED_LINKS:
                # For external links, just check status without recursion
                ALREADY_CHECKED_LINKS.add(link)
                check_link(link)
    except requests.RequestException as e:
        print(f"Error retrieving page: {base_url} - {e}")


crawl_and_check('https://preflib.github.io/PrefLib-Jekyll/', max_depth=None)
