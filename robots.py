from reppy.robots import Robots
from urllib.parse import urlsplit

class Robot:
    def __init__(self):
        self.url_robot = {}

    def get_domain(self, url):
        return "{0.scheme}://{0.netloc}/".format(urlsplit(url))

    def get_name(self, url):
        result = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        if result[:4] == 'www.':
            return result[4:]
        else:
            return result
    
    def get_robots(self, url):
        return self.get_domain(url) + 'robots.txt'

    def is_allowed(self, url):
        try:
            domain = self.get_domain(url)
            if domain in self.url_robot:
                return self.url_robot[domain].allowed(url)
            else:
                robot = Robots.fetch(self.get_robots(url))
                agent = robot.agent('bot')
                self.url_robot[domain] = agent
                return agent.allowed(url)
        except:
            return False
