import math
import re
from datetime import datetime

import requests
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, \
    ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import csv_ as log
import main as filename
from time import sleep

'''parse https://www.domain.com.au'''


class domain_com(log.csv_):
    def __init__(self, request):
        self.request = request
        session = requests.Session()
        session.max_redirects = 30
        try:
            web_page = session.get(self.request, allow_redirects=True).text

        except requests.exceptions.MissingSchema:
            print('Type correct url. Did you forget http / https?')
            raise (exit())

        self.soup = BeautifulSoup(web_page, 'lxml')

    def scrape_property_url(self):
        href_list = []
        try:
            count_property = self.soup.find('strong')
            count_property = re.findall(r'(\d+).+', count_property.string)

        except AttributeError:
            print('Type correct url')
            raise (exit())

        count_pages = math.ceil(int(count_property[0]) / 20)
        body = self.soup.find('div', 'css-1mf5g4s')
        href2 = re.findall(r'href="(.+?)"', str(body))
        for href in href2:
            if not href in href_list:
                href_list.append(href)
        return href_list, count_pages, count_property

    def direct_to_property(self, page):

        hrefs = self.scrape_property_url()[0]
        for href in hrefs:
            compile_domain(href)
        if page == 1:
            self.next_page()

    def next_page(self):
        page = 2
        pages = int(self.scrape_property_url()[1])
        while pages >= page:
            main_url = self.request + '&page=' + str(page)
            url = domain_com(main_url)
            url.direct_to_property(page)
            page += 1
        print('Done!')


    def buy_rent(self):
        tags = self.soup.find_all('span', class_='css-0')
        if tags[1].string == 'Sale' or tags[1].string == 'New Homes':
            return 'Buy'

        elif tags[1].string == 'Rent':
            return 'Rent'

    def bedBathCarSquare_count(self):
        try:
            tag = self.soup.find('span', 'css-9fxapx', string='Beds')
            bed_tag = (tag.find_parent())
            try:
                beds = list(bed_tag.strings)[0]
            except AttributeError:
                print('Beds not found')
                beds = '-'

            bath_tag = tag.find_next('span', 'css-1rzse3v')
            try:
                baths = list(bath_tag.strings)[0]
            except AttributeError:
                print('Baths not found')
                baths = '-'

            car_tag = bath_tag.find_next('span', 'css-1rzse3v')
            try:
                cars = list(car_tag.strings)[0]
            except AttributeError:
                print('Car places not found')
                cars = '-'

            square_tag = car_tag.find_next('span', 'css-1rzse3v')
            try:
                square = list(square_tag.strings)[0]
            except AttributeError:
                print('Square not found')
                square = '-'

            try:
                if int(square) < 15:
                    square = '-'
            except ValueError:
                pass

            return beds, baths, cars, square

        except AttributeError:
            try:
                square_tag = self.soup.find_next('span', 'css-1rzse3v')
                square = list(square_tag.strings)[0]
                try:
                    if int(square) < 15:
                        square = 'None'

                except ValueError:
                    pass

            except AttributeError:
                square = 'None'

            return '-', '-', '-', square

    def agent_name(self):
        try:
            agent = self.soup.find('a', 'is-a-link listing-details__agent-details-agent-name')
            return agent.string
        except AttributeError:
            print('Agent not found')
            return 'None'

    def property_addr(self):
        addr = self.soup.find('h1', 'listing-details__listing-summary-address')
        try:
            return addr.string
        except AttributeError:
            print('Adress not found')
            return 'None'

    def property_type(self):
        try:
            tag = self.soup.find('span', 'listing-details__property-type-features-text').string
        except AttributeError:
            try:
                tag = self.soup.find('p', 'listing-details__property-type').string

            except AttributeError:
                print('Property Type not found')
                return 'None'

        return tag

    def price_buy(self):
        price = self.soup.find('div', class_='listing-details__summary-title')
        try:
            return price.string

        except AttributeError:
            return 'Auction / No price'

    def price_rent(self):
        price = self.soup.find('div', 'listing-details__summary-title')
        try:
            return price.string

        except AttributeError:
            print('Property Price not found')
            return 'None'

    def property_features(self):
        try:
            features = [
                feature.string for feature in self.soup.find_all('li', 'listing-details__additional-features-listing')
            ]
        except AttributeError:
            print('Features not found')
            return 'None'

        if not features:
            print('Features not found')
            features = 'None'

        return features

    def property_description(self):
        try:
            full_desc = ''
            description = self.soup.find('div','listing-details__description')
            description =  description.find_all('p')
            for desc in description:
                full_desc += desc.string

        except AttributeError:
            full_desc = 'None'
            print('Descripton not found')

        except TypeError:
            full_desc = 'None'
            print('Descripton not found')

        return full_desc


class funda_nl(log.csv_):
    def __init__(self, url):
        self.page = 660
        self.url = url
        self.cur_url = ''
        self.options = webdriver.ChromeOptions()
        with open ('config.txt','r') as f:
            path = f.readline()
        self.options.add_argument(path)
        try:
            self.driver = webdriver.Chrome(options=self.options)

        except InvalidArgumentException:
            print('Close Chrome and try again')


    def direct_to_property(self, url):
        c = 0
        self.driver.implicitly_wait(4)
        self.driver.get(url)
        while True:
            try:
                links =  self.driver.find_elements_by_class_name('search-result__header-subtitle')

                try:
                    links[c].click()

                except ElementClickInterceptedException:
                    c += 1
                    continue

                html = self.driver.page_source
                self.cur_url =  self.driver.current_url
                self.scrape(html)
                self.driver.back()
                c += 1
            except IndexError:
                print('{F{F{F{F{F{ LOXXX')
                break

        url = '{}p{}/'.format(self.url,self.page)
        self.page +=1
        self.direct_to_property(url)



    def soup(self, html):
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def scrape(self, html):
        soup = self.soup(html)
        soup = soup.find('div','object-kenmerken-body')
        # listt = [self.buy_sell(html), self.url, self.agent(html), self.address(html),
        #              self.bedrooms(soup), self.bathrooms(soup), self.cars(soup),
        #              self.address(html), self.property_type(soup), self.square(soup),
        #              self.property_description(html), 'None']
        # print(listt)

        csv_list = [[self.buy_sell(html), self.cur_url, self.agent(html), self.price(soup),
                     self.address(html), self.bedrooms(soup), self.bathrooms(soup), self.cars(soup),
                     self.property_type(soup), self.square(soup),
                     self.property_description(html), 'None']]

        file = filename.arg_init()[1]
        self.csv_writer(csv_list, file)
        # self.driver.close()

    def price(self, soup):
        try:
            price = soup.find('dt', string='Asking price')
            price = list(price.next_siblings)
            price = re.findall(r'\d+,\d+,\d+|\d+,\d+|\d+$',str(price[1]))[0]
            price = ('€ {}'.format(price))
            print(price)

        except AttributeError or IndexError:
            print('Price not found')
            price = 'None'

        price = price.replace('\\n','')
        price = price.replace('\n','')
        return price

    def buy_sell(self,html):
        soup = self.soup(html)
        try:
            type_ = soup.find('title').string
        except AttributeError:
            return 'None'
        if re.findall(r'rent',str(type_)):
            print('Sale')
            return 'Rent'

        elif re.findall(r'sale', str(type_)):
            print('Buy')
            return 'Buy'
        else:
            print('Sale/Buy not known')
            return 'None'

    def square(self, soup):
        try:
            square = soup.find('dt', string='Living area')
            square = list(square.next_siblings)
            square = re.findall(r'\d+|\d+,\d+', str(square[1]))[0]
            square = ('{}m²'.format(square))
            print(square)

        except AttributeError:
            print('Square not found')
            square = 'None'

        except IndexError:
            print('Square not found')
            square = 'None'

        square = square.replace('\\n', '')
        square = square.replace('\n', '')
        return square

    def address(self, html):
        try:
            soup = self.soup(html)
            address = soup.find('h1', 'object-header__container')
            list_ = list(address.children)
            address = '{} | {}'.format(list_[1].string, list_[3].string)
            print(address)

        except AttributeError:
            address = 'None'
            print('Adress not found')

        address = address.replace('\\n', '')
        address = address.replace('\n', '')
        return address

    def bedrooms(self,soup):
        try:
            bed = soup.find('dt', string='Number of rooms')
            bed = list(bed.next_siblings)
            bed = str(bed[1].string.replace('\\n',''))
            # bed = re.findall(r'\d+ bedrooms?', str(bed[1]))[0]
            print(bed)

        except AttributeError:
            print('Bedrooms not found')
            bed = 'None'

        except IndexError:
            print('Bed not found')
            bed = 'None'

        bed = bed.replace('\\n', '')
        bed = bed.replace('\n', '')
        return bed


    def bathrooms(self,soup):
        try:
            bath = soup.find('dt', string='Number of bath rooms')
            bath = list(bath.next_siblings)
            bath = str(bath[1].string.replace('\\n',''))
            # bath = re.findall(r'\d+ bathrooms? and \d+ separate toilet|\d+ bathrooms?', str(bath[1]))[0]
            print(bath)

        except AttributeError:
            print('Bathrooms not found')
            bath = 'None'

        except IndexError:
            print('Bathrooms not found')
            bath = 'None'

        bath = bath.replace('\\n', '')
        bath = bath.replace('\n', '')

        return bath

    def cars(self,soup):
        try:
            cars = soup.find('dt', string='Capacity')
            cars = list(cars.next_siblings)
            cars = str(cars[1].string.replace('\\n',''))
            print(cars)

        except AttributeError:
            print('Car capacity not found')
            cars = 'None'

        except IndexError:
            print('Car capacity not found')
            cars = 'None'
        cars = cars.replace('\\n', '')
        cars = cars.replace('\n', '')

        return cars

    def agent(self,html):
        try:
            soup = self.soup(html)
            phone = soup.find('div','sticky-contact-button__phone')
            phone = phone.find_next('a')
            phone = re.findall(r'href=\"(.+?)\"', str(phone))[0]
            print(phone)


        except AttributeError:
            print('Phone number not found')
            phone = 'None'
        except IndexError:
            print('Phone number not found')
            phone = 'None'

        phone = phone.replace('\\n', '')
        phone = phone.replace('\n', '')

        return phone

    def property_type(self, soup):
        try:
            p_type = soup.find('dt', string='Kind of house')
            p_type = list(p_type.next_siblings)
            p_type = str(p_type[1].string).replace('\\n','')
            print(p_type)

        except AttributeError:
            print('Property type not found')
            p_type = 'None'

        except IndexError:
            print('Property type not found')
            p_type = 'None'

        p_type = p_type.replace('\\n', '')
        p_type = p_type.replace('\n', '')

        return p_type

    def property_description(self,html):
        soup = self.soup(html)
        try:
            desc = soup.find('div','object-description-body')
            desc = desc.string.replace('\\xe2\\x80\\xa6','')
            desc = desc.replace('\\n','')
            desc = desc.replace('\n','')

        except AttributeError:
            print('Description not found')
            desc = 'None'

        desc = desc.replace('\\n', '')
        desc = desc.replace('\n', '')

        return desc


def compile_domain(url):
    try:
        print(str(datetime.now()) + '| Scraping ' + url)
        site = domain_com(url)
        if site.buy_rent() == 'Buy':
            csv_list = [[site.buy_rent(), site.request, site.agent_name(),
                         site.price_buy(), site.property_addr(), site.bedBathCarSquare_count()[0],
                         site.bedBathCarSquare_count()[1], site.bedBathCarSquare_count()[2],
                         site.property_type(), site.bedBathCarSquare_count()[3], site.property_description(),
                         site.property_features()]]

        elif site.buy_rent() == 'Rent':
            csv_list = [[site.buy_rent(), site.request, site.agent_name(),
                         site.price_rent(), site.property_addr(), site.bedBathCarSquare_count()[0],
                         site.bedBathCarSquare_count()[1], site.bedBathCarSquare_count()[2],
                         site.property_type(), site.bedBathCarSquare_count()[3], site.property_description(),
                         site.property_features()]]

        else:
            csv_list = [['None', site.request, site.agent_name(),
                         site.price_buy(), site.property_addr(), site.bedBathCarSquare_count()[0],
                         site.bedBathCarSquare_count()[1], site.bedBathCarSquare_count()[2],
                         site.property_type(), site.bedBathCarSquare_count()[3], site.property_description(),
                         site.property_features()]]
        file = filename.arg_init()[1]
        site.csv_writer(csv_list, file)

        return csv_list
    except IndexError:
        print('The requested URL was not found on the server. ' + url)


if __name__ == '__main__':
    print('python3 main.py --url/-u ...')
    site = domain_com('https://www.domain.com.au/sale/merewether-nsw-2291/?excludeunderoffer=1')
    site.direct_to_property(1)
