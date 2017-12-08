import pickle

class Ranging:
    def __init__(self, path_to_index='bm.pickle'):
        with open(path_to_index, 'rb') as f:
            self.index = pickle.load(f)

    def process_query(self, query):
        return [{'title': 'Im Fadenkreuz von politischer Polizei und Geheimdiensten: Albert Einstein',
                 'url': 'https://link.springer.com/chapter/10.1007%2F3-540-30595-5_7',
                 'content': 'Im Fadenkreuz von politischer Polizei und Geheimdiensten: Albert Einstein'},
                {'title': 'A Benchmarking Environment for Reinforcement Learning Based Task Oriented Dialogue Management',
                 'url': 'https://arxiv.org/abs/1711.11023',
                 'content': 'Dialogue assistants are rapidly becoming an indispensable daily aid. To avoid the significant effort need'},
                {'title': 'Particle Optimization in Stochastic Gradient MCMC',
                 'url': 'https://arxiv.org/abs/1711.10927',
                 'content': 'Dialogue assistants are rapidly becoming an indispensable daily aid. To avoid the significant effort need'},
                {'title': 'Introduction to Tensor Decompositions and their Applications in Machine Learning',
                 'url': 'https://arxiv.org/abs/1711.10781',
                 'content': 'Dialogue assistants are rapidly becoming an indispensable daily aid. To avoid the significant effort need'},
                {'title': 'Dimension Reduction for Robust Covariate Shift Correction',
                 'url': 'https://arxiv.org/abs/1711.10938',
                 'content': 'Dialogue assistants are rapidly becoming an indispensable daily aid. To avoid the significant effort need'},
                {'title': 'Deep Image Prior',
                 'url': 'https://arxiv.org/abs/1711.10925',
                 'content': 'Dialogue assistants are rapidly becoming an indispensable daily aid. To avoid the significant effort need'},
                {'title': 'Semi-Supervised Few-Shot Learning with Prototypical Networks',
                 'url': 'https://arxiv.org/abs/1711.10856',
                 'content': 'Dialogue assistants are rapidly becoming an indispensable daily aid. To avoid the significant effort need'},
                {'title': 'Tighter Lifting-Free Convex Relaxations for Quadratic Matching Problems',
                 'url': 'https://arxiv.org/abs/1711.10733',
                 'content': 'Dialogue assistants are rapidly becoming an indispensable daily aid. To avoid the significant effort need'},
                {'title': 'Valid Inference Corrected for Outlier Removal',
                 'url': 'https://arxiv.org/abs/1711.10635',
                 'content': 'Dialogue assistants are rapidly becoming an indispensable daily aid. To avoid the significant effort need'},
                {'title': 'TensorFlow Distributions',
                 'url': 'https://arxiv.org/abs/1711.10604',
                 'content': 'Dialogue assistants are rapidly becoming an indispensable daily aid. To avoid the significant effort need'}
                ], [
            {'title': 'Paper Title',
             'url': 'https://link.springer.com/chapter/10.1007%2F3-540-30595-5_7',
             'content': 'Authors: Albert Einstein, Some Other Guy'},
        ]
