import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = 'https://no-smoking-smoky.vercel.app'
OUTPUT_DIR = '.'

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
})

downloaded_urls = set()

def download_file(url, local_path):
    # Remove fragments
    url = url.split('#')[0]
    local_path = local_path.split('#')[0]
    
    if url in downloaded_urls:
        return
    downloaded_urls.add(url)
    
    # Clean query strings from local path
    local_path = local_path.split('?')[0]
    
    if local_path.endswith('/'):
        local_path += 'index.html'
    elif not os.path.splitext(local_path)[1]:
        # if no extension, it's a page route like /en
        local_path += '.html'
        
    local_path = os.path.join(OUTPUT_DIR, local_path.lstrip('/'))
    
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    try:
        print(f"Downloading {url} -> {local_path}")
        resp = session.get(url, timeout=10)
        if resp.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(resp.content)
                
            # If it's HTML, parse it for more assets
            content_type = resp.headers.get('Content-Type', '')
            if 'text/html' in content_type:
                parse_html(resp.text, url)
            elif 'text/css' in content_type:
                parse_css(resp.text, url)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def parse_html(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    tags = {
        'link': 'href',
        'script': 'src',
        'img': 'src',
        'source': 'srcset',
        'a': 'href'
    }
    
    for tag, attr in tags.items():
        for el in soup.find_all(tag):
            link = el.get(attr)
            if not link:
                continue
                
            # handle srcset
            if attr == 'srcset':
                links = [l.strip().split(' ')[0] for l in link.split(',')]
            else:
                links = [link]
                
            for l in links:
                if l.startswith('data:') or l.startswith('#') or l.startswith('javascript:'):
                    continue
                
                # Handle next/image
                if l.startswith('/_next/image?url='):
                    import urllib.parse
                    parsed = urllib.parse.urlparse(l)
                    qs = urllib.parse.parse_qs(parsed.query)
                    if 'url' in qs:
                        img_url = qs['url'][0]
                        if img_url.startswith('/'):
                            full_url = urljoin(BASE_URL, img_url)
                            download_file(full_url, img_url)
                
                full_url = urljoin(base_url, l)
                if full_url.startswith(BASE_URL):
                    parsed_url = urlparse(full_url)
                    path = parsed_url.path
                    if path == '/':
                        continue # already handled
                    download_file(full_url, path)

def parse_css(css_content, base_url):
    import re
    urls = re.findall(r'url\((["\']?)([^)"\']+)\1\)', css_content)
    for _, url in urls:
        if url.startswith('data:'):
            continue
        full_url = urljoin(base_url, url)
        if full_url.startswith(BASE_URL):
            parsed_url = urlparse(full_url)
            path = parsed_url.path
            download_file(full_url, path)

# Start with the main pages
pages = ['/', '/en', '/ar']
for page in pages:
    url = urljoin(BASE_URL, page)
    if page == '/':
        download_file(url, '/index.html')
    else:
        download_file(url, page)

print("Scraping completed!")
