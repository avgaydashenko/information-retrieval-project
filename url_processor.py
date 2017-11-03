from urllib.parse import urlsplit
import requests
from lxml import html
from re import search


class UrlProcessor:
    @staticmethod
    def get_domain(url):
        return "{0.scheme}://{0.netloc}/".format(urlsplit(url))

    @staticmethod
    def get_name(url):
        result = "{0.netloc}".format(urlsplit(url))
        return result[4:] if result[:4] == 'www.' else result

    @staticmethod
    def get_robots(url):
        return UrlProcessor.get_domain(url) + 'robots.txt'

    @staticmethod
    def get_parsed_page(url):
        return html.fromstring(requests.get(url).content)

    @staticmethod
    def get_links(url, parsed_page):
        result = []
        post_urls = parsed_page.xpath('//a/@href')
        for post_url in post_urls:
            if len(post_url) == 0:
                continue
            if post_url[0] == '/':
                post_url = url + (post_url[1:] if post_url[-1] == '/' else post_url)
            result.append(post_url)
        return result

    @staticmethod
    def check_arxiv(url):
        paper_id = search('arxiv\.org\/.*\/?(?P<id>\d{4}\.\d{5})', url)
        return False if paper_id is None else 'https://arxiv.org/pdf/{}.pdf'.format(paper_id.group('id'))