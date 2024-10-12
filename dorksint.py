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

# Global User-Agent header to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
}

def get_page_title(url):
    """Fetch the title of a webpage."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.title.string if soup.title else "Title not found"
        else:
            return "Could not retrieve title (site error)"
    except Exception as e:
        return f"Error: {str(e)}"

def search_engine(query, search_url, result_selector, title_selector, link_selector):
    """Generic search function for different search engines."""
    try:
        response = requests.get(search_url.format(query=query), headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for item in soup.select(result_selector):
            title = item.select_one(title_selector).text if item.select_one(title_selector) else "No title"
            link = item.select_one(link_selector)['href'] if item.select_one(link_selector) else "No link"
            results.append((title, link))

        return results
    except Exception as e:
        print(f"{colored('[!]', 'red')} Error during search: {str(e)}.")
        return []

def search_bing(query):
    return search_engine(query, 
                         "https://www.bing.com/search?q={query}", 
                         'li.b_algo', 
                         'h2', 
                         'a')

def search_google(query):
    return search_engine(query, 
                         "https://www.google.com/search?q={query}", 
                         'div.g', 
                         'h3', 
                         'a')

def search_yandex(query):
    return search_engine(query, 
                         "https://yandex.com/search/?text={query}", 
                         'li.serp-item', 
                         'h2', 
                         'a')

def search_duckduckgo(query):
    return search_engine(query, 
                         "https://duckduckgo.com/html/?q={query}", 
                         'div.result__body', 
                         'a.result__a', 
                         'a')

def search_dork_all_engines(dork):
    """Search for a dork across multiple search engines."""
    search_engines = {
        'Yandex': search_yandex(dork),
        'Google': search_google(dork),
        'Bing': search_bing(dork),
        'DuckDuckGo': search_duckduckgo(dork),
    }

    for engine, results in search_engines.items():
        if results:
            print(colored(f"\n[+] {engine}:\n", 'cyan', attrs=['bold']))
            for title, link in results:
                print(f"{colored('[+]', 'green')} {colored('Title: ' + title)}")
                print(f"{colored('[+]', 'green')} {colored('Site: ' + link + '\n')}")
        else:
            print(colored(f'\n[!] {engine}: No results found.\n', 'red'))

def main():
    parser = argparse.ArgumentParser(description="DorkSint - OSINT Tool", usage="dorksint [-f] {your dork}")
    parser.add_argument("query", nargs='*', help="The search query (e.g., full name)")
    parser.add_argument("-f", "--filetypes", action="store_true", help="Include file-specific dork search")

    args = parser.parse_args()

    if not args.query:
        print(r"""
  .___                \       _____           .   
  /   `    __.  .___  |   ,  (      ` , __   _/_  
  |    | .'   \ /   \ |  /    `--.  | |'  `.  |   
  |    | |    | |   ' |-<        |  | |    |  |   
  /---/   `._.' /     /  \_ \___.'  / /    |  \__/
""")
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
        print(colored(f"[*] Searching with dork: {specific_dork}\n", 'light_magenta', attrs=['bold']))
        search_dork_all_engines(specific_dork)
    else:
        print(colored('[v] GitHub - https://github.com/vertex-coder/DorkSint\n', 'magenta', attrs=['bold']))
        print(colored(f"[*] Searching with dork: {query}\n", 'light_magenta', attrs=['bold']))
        search_dork_all_engines(query)


if __name__ == "__main__":
    main()
