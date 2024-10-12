#  .___                \       _____           .   
#  /   `    __.  .___  |   ,  (      ` , __   _/_  
#  |    | .'   \ /   \ |  /    `--.  | |'  `.  |   
#  |    | |    | |   ' |-<        |  | |    |  |   
#  /---/   `._.' /     /  \_ \___.'  / /    |  \__/

# GitHub - https://github.com/vertex-coder/DorkSint


import argparse
import requests
from bs4 import BeautifulSoup
from termcolor import colored


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
}


def getPageTitle(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.title.string if soup.title else "Title not found"
        else:
            return "Could not retrieve title (site error)"
    except Exception as e:
        return f"Error: {str(e)}"


def searchBing(query):

    search_url = f"https://www.bing.com/search?q={query}"
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for item in soup.find_all('li', {'class': 'b_algo'}):
            title = item.find('h2').text if item.find('h2') else "No title"
            link = item.find('a')['href'] if item.find('a') else "No link"
            results.append((title, link))

        return results
    except Exception as e:
        print(f"{colored('[!]', 'red')} Error during Bing search: {str(e)}.")
        return []

def searchGoogle(query):

    search_url = f"https://www.google.com/search?q={query}"
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for item in soup.find_all('div', class_='g'):
            title = item.find('h3').text if item.find('h3') else "No title"
            link = item.find('a')['href'] if item.find('a') else "No link"
            
            results.append((title, link, summary))

        return results
    except Exception as e:
        print(f"{colored('[!]', 'red')} Error during Google search: {str(e)}.")
        return []

def searchYandex(query):

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
        print(f"{colored('[!]', 'red')} Error during Yandex search: {str(e)}")
        return []

def searchDuckDuckGo(query):

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
        print(f"{colored('[!]', 'red')} Error during DuckDuckGo search: {str(e)}.")
        return []



def search_dork_all_engines(dork):
    search_engines = {
        'Yandex': searchYandex(dork),
        'Google': searchGoogle(dork),
        'Bing': searchBing(dork),
        'DuckDuckGo': searchDuckDuckGo(dork),
    }

    for engine, results in search_engines.items():
        if results:
            print(colored(f"[+] {engine}:\n", 'cyan', attrs=['bold']))

            for title, link, summary in results:
                print(f"{colored('[+]', 'green')} {colored('Title: ' + title)}")
                print(colored(f"{colored('[+]', 'green')} {colored('Site: ' + link)}"))

        else:
            print(colored(f'[!] {engine}: Not found.\n', 'red'))

def main():
    parser = argparse.ArgumentParser(description="DorkSint - OSINT Tool", usage="dorksint [-f] {your dork}")
    parser.add_argument("query", nargs='*', help="The search query (e.g., full name)")
    parser.add_argument("-f", "--filetypes", action="store_true", help="Include file-specific dork search")

    args = parser.parse_args()

    
    if not args.query:
        print(f'{colored('[!]', 'red')} Invalid usage.\n')
        print(f'{colored('[+]', 'green')} Usage:\n')
        print(f"{colored('[+]', 'green')}"+" Default search: dorksint [your dork]")
        print(f"{colored('[+]', 'green')}"+" Search with PDF, WORD, EXCEL, DB files: dorksint -f [your dork]\n")
        return  

    query = ' '.join(args.query)
    query = f'"{query}"'

    if args.filetypes:
        print(colored('[v] GitHub - https://github.com/vertex-coder/DorkSint\n', 'magenta', attrs=['bold']))
        file_types = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'sql', 'db', 'csv']
        file_type_dork = ' OR '.join([f'filetype:{ft}' for ft in file_types])
        specific_dork = f'{query} {file_type_dork}'
        print(f"[*] Searching with dork: {specific_dork}")
        search_dork_all_engines(specific_dork)
    else:
        print(colored('[v] GitHub - https://github.com/vertex-coder/DorkSint\n', 'magenta', attrs=['bold']))
        print(f"[*] Searching with dork: {query}\n")
        search_dork_all_engines(query)


if __name__ == "__main__":
    main()
