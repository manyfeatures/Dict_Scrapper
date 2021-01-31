from bs4 import BeautifulSoup
import requests
#import argparse


class Scrapper():
    def __init__(self, url, headers, proxy=None):
        self.url = url
        self.headers = headers
        self.proxy = proxy
        self.page_content = None

    def download_data(self, word):
        #    headers = {'user-agent': 'my-app/0.0.1'}
        url = ''.join([self.url, word])
        s = requests.Session()  # ?
        page = s.get(url,
                     headers=self.headers,
                     # params=data_to_send,
                     proxies={"http": self.proxy, "https": self.proxy},
                     stream=True  # ?
                     )
        # process connection error
        self.page_content = BeautifulSoup(page.content, 'html.parser')

    def find_word(self, word):
        self.download_data(word)
        # return self.page_content
        a = self.page_content.find(
            "div", {"class", "top-container"}).find('h1', {'class', 'headword'}).text
        return a.upper()


def main():
    url = 'https://www.oxfordlearnersdictionaries.com/definition/english/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br"}

    scr = Scrapper(url, headers)
    word = 'abandon'
    res = scr.find_word(word)
    print(res)


if __name__ == "__main__":
    main()
