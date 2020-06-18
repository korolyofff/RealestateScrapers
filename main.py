import argparse

import parse as p


def arg_init():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', action="store",
                        default='',
                        help='URL of properties')

    parser.add_argument('--clear_csv', '-cc', action="store",
                        help='Clear CSV. --cc *filename*')

    parser.add_argument('--file', '-f', action="store",
                        help='Directory for save data', default='output.csv')
    parse = parser.parse_args()
    return parse, parse.file

def arg_parse():

    print('Preparing for scraping...')
    parse = arg_init()[0]

    if parse.clear_csv:
        with open(parse.clear_csv, 'w'):
            pass

        for _ in range(3):
            print('Cleared csv data in ' + parse.clear_csv)

    elif parse.url.startswith('https://www.domain.com.au'):
        print('auf')
        url_ = p.domain_com(parse.url)
        print('Scraping started. Pages to scrape: ' + str(url_.scrape_property_url()[2][0]))
        url_.direct_to_property(1)

    elif parse.url.startswith('https://www.funda.nl'):
        site = p.funda_nl(parse.url)
        site.direct_to_property(site.url)
        print('Scraping started')

    else:
        print('Not correct URL')
        raise exit(1)

def main():
    arg_parse()

if __name__ == '__main__':
    main()
