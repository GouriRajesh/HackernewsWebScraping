# This program scrapes Hacker News website for articles with points greater than 100

import requests
from bs4 import BeautifulSoup
import pprint

links = ['https://news.ycombinator.com/', 'https://news.ycombinator.com/news?p=2', 'https://news.ycombinator.com/news?p=3']
# For 3 pages
all_link_tags = []
all_subtext_tags = []


def get_all_links(links, all_link_tags, all_subtext_tags):
    '''
    Collects the link tags and subtext tags of all the links mentioned in links list
    :param links:
    :param all_link_tags:
    :param all_subtext_tags:
    :return:
    '''
    for linkitems in links:
        response = requests.get(linkitems)
        # Get the html code from this website
        soup = BeautifulSoup(response.text, 'html.parser')
        # Parse the grabbed string into a html file
        links = soup.select('.storylink')
        # Get all the links with class attribute storylink
        all_link_tags += links
        subtext = soup.select('.subtext')
        # Get all the classes with attribute subtext
        all_subtext_tags += subtext
    return all_link_tags, all_subtext_tags


def sorted_stories(hnlist):
    '''
    Sorts the news from highest number of votes to lowest number of votes but greater than 100
    :param hnlist:
    :return:
    '''
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

def custom_hackernews(alllinks, allsubtext):
    '''
    Collects the title,link and votes of news which have votes > 100
    :param alllinks:
    :param allsubtext:
    :return:
    '''
    hn = []
    for index, item in enumerate(alllinks):
        title = item.getText()
        href_link = item.get('href', None)
        # Get the actual link attribute not just the text
        votes = allsubtext[index].select('.score')
        # Get the score of each title
        if len(votes):
            # If votes exists
            # Remove " Points" word
            points = votes[0].getText().replace(' points', '')
            # Remove " Point" word
            points = int(points.replace(' point', ''))
            if points > 99:
                hn.append({'title': title, 'link': href_link, 'votes': points})
    return sorted_stories(hn)


get_all_links(links, all_link_tags, all_subtext_tags)
pprint.pprint(custom_hackernews(all_link_tags, all_subtext_tags))
