from reppy.robots import Robots
from url_processor import UrlProcessor


class Robot:
    def __init__(self):
        self.url_robot = {}

    def is_allowed(self, url):
        try:
            domain = UrlProcessor.get_domain(url)
            if domain in self.url_robot:
                return self.url_robot[domain].allowed(url)
            else:
                robot = Robots.fetch(UrlProcessor.get_robots(url))
                agent = robot.agent('bot')
                self.url_robot[domain] = agent
                return agent.allowed(url)
        except:
            return False
