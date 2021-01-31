from bs4 import BeautifulSoup
import requests
import argparse

# correct place?
url = 'https://www.oxfordlearnersdictionaries.com/definition/english/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br"}


class Scrapper():
    def __init__(self, url, headers, proxy=None):
        self.url = url
        self.headers = headers
        self.proxy = proxy
        self.page = None
        self.def_ = None  # this is just the word

    def download_data(self, word):
        url = ''.join([self.url, word])
        s = requests.Session()  # ?
        page = s.get(url,
                     headers=self.headers,
                     # params=data_to_send,
                     proxies={"http": self.proxy, "https": self.proxy},
                     stream=True  # ?
                     )
        self.page = BeautifulSoup(page.content, 'html.parser')

    # def get_definition(self, word):
    #     self.def_ = self.page.find("div", {"class", "top-container"}).\
    #                      find('h1', {'class', 'headword'}).text
    #     print(self.def_.upper())

    def get_top_block(self):
        tmp = self.page.find("div", {"class", "top-container"})
        #print(tmp)
        #definition
        self.def_  = tmp.find('h1', {'class', 'headword'}).text # make method?
        print(f"Word: {self.def_.upper()}")
        #phonetics        
        print('Phonetics:')
        phone = tmp.find(class_='phonetics')
        # transcriptions
        br_pron = phone.find(class_="phons_br").get_text().strip()
        print(f"Br: {br_pron}")
        am_pron = phone.find(class_="phons_n_am").get_text().strip()
        print(f"Am: {br_pron}")

    def print_definition(self, def_):    
        # grammar. What does it mean? 
        print(def_.find('span', {'class', 'grammar'}).get_text(), end = ' ')
        # labels
        if def_.find('span', {'class', 'labels'}) is not None:
            print(def_.find('span', {'class', 'labels'}).get_text())
        else:
            print()
        #defenition
        print(def_.find('span', {'class', 'def'}).get_text())  
        print()

    def print_examples(self, def_):
        # We need try if there is no objects corresponding to examples
        try:
            # going through examples
            for i, examp in enumerate(def_.find(class_='examples').find_all('li')):
                # As some examples have "specification: text" structure
                # We need to try to take it
                try:
                    print(f"{i}) {examp.find(class_='cf').text}", end=': ')
                    print(examp.find(class_='x').text) # it has duplicate
                # If there is no specification then it is skipped
                except (NameError, AttributeError) as e:
                    try:
                        print(example.find(class_='x').text) # it has duplicate
                    except:
                        print(None)
        except AttributeError:
            print('0) No examples')
 
    def get_definitions(self):
        defs = self.page.find('ol', {'class', 'senses_multiple'}).find_all(class_='sense')
        print('DEFINITIONS:\n')
        for def_ in defs:
            self.print_definition(def_)
            self.print_examples(def_)
            print('------------------------')


def parse_args():
    parser = argparse.ArgumentParser(description="OXygEN Dictinary package v0.1")
    parser.add_argument("word", help="Enter a word to search")
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"args: {args}")
    print(args.word)  # check

    scrapper = Scrapper(url, headers)
    word = args.word
    # Get the content
    scrapper.download_data(word) 
    scrapper.get_top_block()
    print('---------------------')
    scrapper.get_definitions() 
    #res = scrapper.search_word(word)
    #print(res)


if __name__ == "__main__":
    main()


# python scrapper.py -h show description
