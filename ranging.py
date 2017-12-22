import pickle
import numpy as np

class Ranging:
    def __init__(self, path_to_index='bm.pickle', path_to_meta='meta.pickle', path_to_authors='authors.pickle',
                 path_to_titles='titles.pickle'):
        with open(path_to_index, 'rb') as f_index:
            self.index = pickle.load(f_index)
        with open(path_to_meta, 'rb') as f_meta:
            self.meta = pickle.load(f_meta)
        with open(path_to_authors, 'rb') as f_authors:
            self.authors = pickle.load(f_authors)
        with open(path_to_titles, 'rb') as f_titles:
            self.titles = pickle.load(f_titles)

    def process_query(self, query, s):
        doc_score = {}
        for t in query:
            if t in self.index:
                for score, doc in self.index[t]:
                    if doc in doc_score:
                        doc_score[doc] += score
                    else:
                        doc_score[doc] = score
        scores = np.array(list(doc_score.items()))
        if len(scores) > 0:
            ind = np.argsort(scores[:, 1].astype(float))[::-1]
            result_pages = [self.meta[doc] for doc in scores[ind[:5], 0]]
        else:
            result_pages = []

        result_papers = []
        if s in self.authors:
            papers = self.authors[s]
            for paper in papers:
                _, title, url = paper.split('_')
                result_papers.append({'title': title, 'url': url})

        if len(result_papers) == 0:
            if s in self.titles:
                content, url = self.titles[s].split('_')
                result_papers = [{'title': s, 'url': url, 'content': content.replace("'", '')}]
        else:
            for curr_res in result_papers:
                if curr_res['title'] in self.titles:
                    curr_res['content'] = self.titles[curr_res['title']].split('_')[0].replace("'", '')

        return result_pages, result_papers
