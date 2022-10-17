# Import dependencies.
from argparse import ArgumentParser
from pprint import pprint

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://news.ycombinator.com/news'


def scrape_hacker_news(url, page=1):
    """
    Scraps data from Hacker News feed.
    :param url: URL from which we'll scrape the data.
    :param page: page number.
    :return: two lists: the first one with the links and the other one with the subtext of each link
    """
    response = requests.get(f'{url}?p={page}')

    # Select the relevant components.
    soup = BeautifulSoup(response.text, features='html.parser')
    links = soup.select('.titleline')
    subtext = soup.select('.subtext')

    return links, subtext


def sort_stories_by_votes(hacker_news_list):
    """
    Sorts the Hacker News list by number of votes in descending order.
    :param hacker_news_list: News to sort.
    """
    return sorted(hacker_news_list, key=lambda element: element['votes'], reverse=True)


def fetch_custom_feed(url, pages, min_votes=100):
    """
    Fetches a custom feed from Hacker News.
    :param url: Base URL from which to fetch the news.
    :param pages: Number of result pages to scrap.
    :param min_votes: Minimum number of votes a news must have to appear in the result list.
    """
    hacker_news = []

    for p in range(1, pages + 1):
        print(f'Fetching data from page {p}...')
        links, subtext = scrape_hacker_news(url, p)
        for index, item in enumerate(links):
            title = links[index].getText()
            href = links[index].get('href', None)
            votes = subtext[index].select('.score')

            if len(votes) > 0:
                points = int(votes[0].getText().replace(' points', ''))

                if points >= min_votes:
                    hacker_news.append({
                        'title': title,
                        'link': href,
                        'votes': points
                    })

    return sort_stories_by_votes(hacker_news)


if __name__ == '__main__':
    # Creates input menu.
    argument_parser = ArgumentParser()
    argument_parser.add_argument('-p', '--pages', default=5, type=int, help='Number of pages to scrape (default: 5)')
    argument_parser.add_argument('-v', '--votes', default=100, type=int,
                                 help='Minimum number of votes an article must have to appear in the result list.')
    arguments = vars(argument_parser.parse_args())

    # Make sure the inputs are valid.
    assert arguments['pages'] > 0, '--pages must be > 0'
    assert arguments['votes'] > 0, '--votes must be > 0'

    # Fetch custom feed and display it in the console.
    feed = fetch_custom_feed(BASE_URL, arguments['pages'], arguments['votes'])
    pprint(feed)
