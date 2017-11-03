import collections
import itertools
import multiprocessing
from preprocessing import preprocess_pipeline
from url_processor import UrlProcessor


def file_to_words(url):
    return [(word, 1) for word in preprocess_pipeline(UrlProcessor.get_parsed_page(url).text_content())]


def count_words(item):
    word, occurances = item
    return word, sum(occurances)


class MapReduce(object):
    def __init__(self, map_func=file_to_words, reduce_func=count_words, num_workers=None):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)

    @staticmethod
    def partition(mapped_values):
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()

    def __call__(self, inputs, chunksize=1):
        map_responses = self.pool.map(self.map_func, inputs, chunksize=chunksize)
        partitioned_data = self.partition(itertools.chain(*map_responses))
        reduced_values = self.pool.map(self.reduce_func, partitioned_data)
        return reduced_values
