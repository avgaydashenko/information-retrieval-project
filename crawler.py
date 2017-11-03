import queue
import string
import operator
from multiprocessing import Process, Queue

from robot import Robot
from url_processor import UrlProcessor
from mapreduce import MapReduce


def save_structured():
    pass  # TODO


def do_job(pages_num, index, processed, to_do, another_to_do, letter, robot):
    mapper = MapReduce()
    while pages_num >= 0:
        try:
            url = to_do.get_nowait()
        except queue.Empty:
            break
        else:
            if UrlProcessor.get_name(url)[0] in letter:
                if url in processed or not robot.is_allowed(url):
                    continue

                processed.append(url)

                parsed_page = UrlProcessor.get_parsed_page(url)
                paper_link = UrlProcessor.check_arxiv(url)
                if not paper_link:
                    word_counts = mapper([url])
                    word_counts.sort(key=operator.itemgetter(1))
                    word_counts.reverse()
                    index[url] = word_counts
                else:
                    save_structured()

                pages_num -= 1

                for url_new in UrlProcessor.get_links(url, parsed_page):
                    to_do.put(url_new)
            else:
                another_to_do.put(url)
    return True


init_pages = ['https://arxiv.org/', 'https://search.crossref.org/']
pages_num = 2  # NOTE: for each process!

alphabet = string.ascii_lowercase
letter1, letter2 = alphabet[::4] + alphabet[1::4], alphabet[2::4] + alphabet[3::4]
robot1, robot2 = Robot(), Robot()
to_do1, to_do2 = Queue(), Queue()
processed1, processed2 = [], []
index1, index2 = {}, {}

for page in init_pages:
    if UrlProcessor.get_name(page)[0] in letter1:
        to_do1.put(page)
    else:
        to_do2.put(page)

processes = [
    Process(target=do_job, args=[pages_num, index1, processed1, to_do1, to_do2, letter1, robot1]),
    Process(target=do_job, args=[pages_num, index2, processed2, to_do2, to_do1, letter2, robot2])
]

for p in processes:
    p.start()

for p in processes:
    p.join()
