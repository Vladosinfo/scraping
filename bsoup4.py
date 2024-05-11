import requests
import json
from bs4 import BeautifulSoup


class scrapyng():
    def __init__(self):
        self.BASE_URL = 'https://quotes.toscrape.com/'
        self.authors_list = []
        self.quotes_list = []


    def get_quotes(self, soup):
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        next_page = soup.find('li', class_='next')
        
        return quotes, authors, tags, next_page


    def select_save_author(self, author):

        dict_authors = {}

        author_tag_a = author.find_next_sibling('a')
        author_link_page = self.BASE_URL+author_tag_a['href']
        author_response = requests.get(author_link_page)
        soup_author = BeautifulSoup(author_response.text, 'lxml')
        author_born_date = soup_author.find('span', class_='author-born-date').text
        author_born_location = soup_author.find('span', class_='author-born-location').text
        author_description = soup_author.find('div', class_='author-description').text    
        
        dict_authors["fullname"] = author.text
        dict_authors["born_date"] = author_born_date
        dict_authors["born_location"] = author_born_location
        dict_authors["description"] = author_description.strip()
        self.authors_list.append(dict_authors)
        

    def scrapyng_quotes(self):
        response = requests.get(self.BASE_URL)
        soup = BeautifulSoup(response.text, 'lxml')
        next_page = soup.find('li', class_='next')

        quotes, authors, tags, next_page = self.get_quotes(soup)

        num = 1
        next_page_note_last = 0
        while next_page or next_page_note_last <= 1:
            for i in range(0, len(quotes)):
                quote_text = quotes[i].text[1:-1]

                # author
                author_obj = self.select_save_author(authors[i])

                # tags
                tagsforquote = tags[i].find_all('a', class_='tag')
                qtags = []
                for tagforquote in tagsforquote:
                    qtags.append(tagforquote.text)

                dict_quotes = {}
                dict_quotes["quotes"] = qtags
                dict_quotes["author"] = authors[i].text
                dict_quotes["quote"] = quote_text
                self.quotes_list.append(dict_quotes)

                qtags = ', '.join(qtags)
                print(str(num) + '. New added Quote: ' + quote_text[0:108] + '...')
                print('-- Author: ' + authors[i].text)
                print('-- Tags: ' + qtags)

                num+=1

            if next_page != None:
                next_link = self.BASE_URL+next_page.a['href']
                response = requests.get(next_link)
                soup = BeautifulSoup(response.text, 'lxml')
                quotes, authors, tags, next_page = self.get_quotes(soup)
            if next_page == None and next_page_note_last <= 1:
                next_page_note_last += 1

        return True
    

    def fill_authors_file(self):
        with open('authors.json', 'w', encoding='utf-8') as fd:
            json.dump(self.authors_list, fd, ensure_ascii=False, indent=2)
        print("Finish filling authors file")


    def fill_quotes_file(self):
        with open('quotes.json', 'w', encoding='utf-8') as fd:
            json.dump(self.quotes_list, fd, ensure_ascii=False, indent=2)
        print("Finish filling quotes file")


def main():
    scrapy = scrapyng()
    scrapy.scrapyng_quotes()
    scrapy.fill_authors_file()
    scrapy.fill_quotes_file()


if __name__ == "__main__":
    main()
    