import pickle
import numpy as np

class Ranging:
    def __init__(self, path_to_index='bm.pickle', path_to_meta='meta.pickle'):
        with open(path_to_index, 'rb') as f_index:
            self.index = pickle.load(f_index)
        with open(path_to_meta, 'rb') as f_meta:
            self.meta = pickle.load(f_meta)

    def process_query(self, query):
        doc_score = {}
        for t in query:
            for score, doc in self.index[t]:
                if doc in doc_score:
                    doc_score[doc] += score
                else:
                    doc_score[doc] = score
        scores = np.array(list(doc_score.items()))
        ind = np.argsort(scores[:, 1].astype(float))[::-1]
        result_pages = [self.meta[doc] for doc in scores[ind[:5], 0]]

        

        return result_pages, [
            {'title': 'Paper Title',
             'url': 'https://link.springer.com/chapter/10.1007%2F3-540-30595-5_7',
             'content': 'Authors: Albert Einstein, Some Other Guy'},
        ]
