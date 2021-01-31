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
        self.page_content = None
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
        self.page_content = BeautifulSoup(page.content, 'html.parser')

    # def get_definition(self, word):
    #     self.def_ = self.page_content.find("div", {"class", "top-container"}).\
    #                      find('h1', {'class', 'headword'}).text
    #     print(self.def_.upper())

    def get_top_block(self):
        tmp = self.page_content.find("div", {"class", "top-container"})
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
    #res = scrapper.search_word(word)
    #print(res)


if __name__ == "__main__":
    main()


# python scrapper.py -h show description
