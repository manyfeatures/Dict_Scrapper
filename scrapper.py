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

    def print_grammar_label(self, def_):
        # If there is a grammar in the line. What does it mean?
        try:  
            print(def_.find('span', {'class', 'grammar'}).get_text(), end = ' ')
        except:
            print(end='')

    def print_usage_label(self, def_):
        # usage structure?
        try:
            # this can be ambigous and can retieve example's tag "cf"
            # This is why we use loop to not get into the examples tags
            for child in def_.findChildren(recursive=False):
                #print('inside')
                try: # addition protection if index for some children out of range
                    if child['class'][0] == 'cf':
                        print(f' ["{child.text}"] ', end=': ')
                except:
                    pass
        except:
            print(end='')

    def print_label(self, def_):
        """ informal and other labels """
        try:
            # this can be ambigous and can retieve example's tag "cf"
            # This is why we use loop to not get into the examples tags
            for child in def_.findChildren(recursive=False):
                #print('inside')
                try: # addition protection if index for some children out of range
                    if child['class'][0] == 'labels':
                        print(f' ["{child.text}"] ', end=': ')
                except:
                    pass
        except:
            print(end='')

    def print_single_definition(self, def_):    
        self.print_grammar_label(def_)
        self.print_usage_label(def_)
        self.print_label(def_) 
        #definition
        print(def_.find('span', {'class', 'def'}).get_text())  
        print()

    def print_examples_(self, def_):
        # going through examples
        for i, examp in enumerate(def_.find(class_='examples').find_all('li')):
            # As some examples have "specification: text" structure
            # We need to try to take it
            print(f"{i})", end=' ')
            try:
                print(f' "{examp.find(class_="cf").text}" ', end=': ') 
                print(examp.find(class_ = 'labels').text, end=' ')
                print(examp.find(class_='x').text) # it has duplicate
                #print(examp.find('span', {'class', 'labels'}).get_text(), end=' ')
            # If there is no specification then it is skipped
            except (NameError, AttributeError) as e:
                try:
                    print(examp.find(class_ = 'labels').text, end=' ')
                    print(examp.find(class_='x').text) # it has duplicate
                except:
                    try:
                        print(examp.find(class_='x').text) # it has duplicate
                    except e:
                        #print(e)
                        pritn(None)

    def print_examples(self, def_):
        # We need try because 
        # there can ben objects corresponding to examples
        try:
            self.print_examples_(def_)
        except AttributeError as e:
            print('0) No examples')
        except:
            print("Unknow error")

    def get_definitions(self):
        defs = self.page.find('ol', {'class', 'senses_multiple'}).find_all(class_='sense')
        print('DEFINITIONS:\n')
        for i, def_ in enumerate(defs):
            print(f"#{i}")
            self.print_single_definition(def_)
            print('Examples:')
            self.print_examples(def_)
            print()
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
# [transitive, no passive] get something to receive something
# doesn't print get something
# there can be separated examples block


