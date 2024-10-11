import argparse
import requests
from bs4 import BeautifulSoup
from termcolor import colored

def get_page_title(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.title.string if soup.title else "Title not found"
        else:
            return "Could not retrieve title (site error)"
    except Exception as e:
        return f"Error: {str(e)}"

def search_bing(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    search_url = f"https://www.bing.com/search?q={query}"
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for item in soup.find_all('li', {'class': 'b_algo'}):
            title = item.find('h2').text if item.find('h2') else "No title"
            link = item.find('a')['href'] if item.find('a') else "No link"
            summary = item.find('p').text if item.find('p') else "No summary"
            results.append((title, link, summary))

        return results
    except Exception as e:
        print(colored(f"[!] Error during Bing search: {str(e)}", 'red'))
        return []

def search_google(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    search_url = f"https://www.google.com/search?q={query}"
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for item in soup.find_all('div', class_='g'):
            title = item.find('h3').text if item.find('h3') else "No title"
            link = item.find('a')['href'] if item.find('a') else "No link"
            summary = item.find('span', {'class': 'aCOpRe'}).text if item.find('span', {'class': 'aCOpRe'}) else "No summary"
            results.append((title, link, summary))

        return results
    except Exception as e:
        print(colored(f"[!] Error during Google search: {str(e)}", 'red'))
        return []

def search_yandex(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    search_url = f"https://yandex.com/search/?text={query}"
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for item in soup.find_all('li', {'class': 'serp-item'}):
            title = item.find('h2').text if item.find('h2') else "No title"
            link = item.find('a')['href'] if item.find('a') else "No link"
            summary = item.find('div', {'class': 'text-container'}).text if item.find('div', {'class': 'text-container'}) else "No summary"
            results.append((title, link, summary))

        return results
    except Exception as e:
        print(colored(f"[!] Error during Yandex search: {str(e)}", 'red'))
        return []

def search_duckduckgo(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    search_url = f"https://duckduckgo.com/html/?q={query}"
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for item in soup.find_all('div', {'class': 'result__body'}):
            title = item.find('a', {'class': 'result__a'}).text if item.find('a', {'class': 'result__a'}) else "No title"
            link = item.find('a')['href'] if item.find('a') else "No link"
            summary = item.find('a', {'class': 'result__snippet'}).text if item.find('a', {'class': 'result__snippet'}) else "No summary"
            results.append((title, link, summary))

        return results
    except Exception as e:
        print(colored(f"[!] Error during DuckDuckGo search: {str(e)}", 'red'))
        return []



def search_dork_all_engines(dork):
    search_engines = {
        'Yandex': search_yandex(dork),
        'Google': search_google(dork),
        'Bing': search_bing(dork),
        'DuckDuckGo': search_duckduckgo(dork),
    }

    for engine, results in search_engines.items():
        if results:
            print(colored(f"[+] {engine}:\n", 'cyan', attrs=['bold']))
            for title, link, summary in results:
                print(f"{colored('[+]', 'green')} {colored('Title: ' + title)}")
                print(colored(f"{colored('[+]', 'green')} {colored('Site: ' + link)}"))
                print(colored(f"{colored('[+]', 'green')} {colored('Summary: ' + summary)}\n"))

        else:
            print(colored(f'[!] {engine}: Not found.\n', 'red'))

def main():
    parser = argparse.ArgumentParser(description="Dork Detective Tool")
    parser.add_argument("query", nargs='+', help="The search query (e.g., full name)")
    parser.add_argument("-f", "--filetypes", action="store_true", help="Include file-specific dork search")

    args = parser.parse_args()

    query = ' '.join(args.query)
    query = f'"{query}"'

    if args.filetypes:
        file_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'sql', 'db', 'csv']
        file_type_dork = ' OR '.join([f'filetype:{ft}' for ft in file_types])
        specific_dork = f'"{query}" {file_type_dork}'
        print(f"[*] Searching with dork: {specific_dork}")
        search_dork_all_engines(specific_dork)

    else:
        
        print(f"[*] Searching with dork: {query}\n")
        search_dork_all_engines(args.query)


if __name__ == "__main__":
    main()
