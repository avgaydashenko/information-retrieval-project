import queue
import string
from multiprocessing import Process, Queue

from robot import Robot
from url_processor import UrlProcessor


def save_unstructered():
    pass  # TODO


def save_structered():
    pass  # TODO


def do_job(url_doc, to_do, another_to_do, letter, robot):
    while True:
        # print(len(url_doc))
        try:
            url = to_do.get_nowait()
        except queue.Empty:
            break
        else:
            if UrlProcessor.get_name(url)[0] in letter:
                if len(url_doc) >= pages_num:
                    break

                if url in url_doc or not robot.is_allowed(url):
                    continue

                parsed_page = UrlProcessor.get_parsed_page(url)
                url_doc[url] = parsed_page

                paper_link = UrlProcessor.check_arxiv(url)
                if not paper_link:
                    save_unstructered()
                else:
                    save_structered()

                # print(url, url_doc)

                for url_new in UrlProcessor.get_links(robot, url, url_doc, parsed_page):
                    to_do.put(url_new)
            else:
                another_to_do.put(url)
    return True

init_pages = ['https://arxiv.org/', 'https://search.crossref.org/']
pages_num = 2 # NOTE: for each process!

alphabet = string.ascii_lowercase
letter1, letter2 = alphabet[::4] + alphabet[1::4], alphabet[2::4] + alphabet[3::4]
robot1, robot2 = Robot(), Robot()
url_doc1, url_doc2 = {}, {}
to_do1, to_do2 = Queue(), Queue()

for page in init_pages:
    if UrlProcessor.get_name(page)[0] in letter1:
        to_do1.put(page)
    else:
        to_do2.put(page)

processes = [
    Process(target=do_job, args=[url_doc1, to_do1, to_do2, letter1, robot1]),
    Process(target=do_job, args=[url_doc2, to_do2, to_do1, letter2, robot2])
]

for p in processes:
    p.start()
for p in processes:
    p.join()
