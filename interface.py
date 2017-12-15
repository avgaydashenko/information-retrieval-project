import pyforms

from pyforms import BaseWidget
from pyforms.Controls import ControlText, ControlList

from PyQt4 import QtCore, QtGui

from webbrowser import open as open_url

from ranging import Ranging
from nltk import PorterStemmer

ranging = Ranging()
process_query = ranging.process_query


def query_words(query):
    stemmer = PorterStemmer()
    return set([stemmer.stem(word).encode("utf8") for word in query.lower().split(' ')])


def format_text(query, document, intent, num_words_to_show=10):
    title = '<span style="font-size:15pt; color: blue">' + document['title'] + '</span>'
    url = '<span style="color: green">' + document['url'] + '</span>'
    content = []
    stemmer = PorterStemmer()
    relevance = []
    for num, word in enumerate(document['content'].split(' ')):
        if stemmer.stem(word.lower()).encode("utf8") in query:
            content.append('<span style="background-color: #ffffcc">' + word + '</span>')
            relevance.append(1)
        else:
            content.append(word)
            relevance.append(0)
    max_rel = 0
    max_rel_ind = -1
    curr_rel = 0
    for i, rel in enumerate(relevance):
        curr_rel += rel - (0 if i < num_words_to_show else relevance[i - num_words_to_show])
        if curr_rel >= max_rel:
            max_rel = curr_rel
            max_rel_ind = i
    return '<br>{title}<br>{url}<br>{continuation}{content}{continuation}<br>'.format(title=title, url=url,
                                    continuation='' if intent == 'papers' else '...',
                                    content=' '.join(content[max(0, max_rel_ind - num_words_to_show) : max_rel_ind]))


class Interface(BaseWidget):

    def __init__(self):
        super(Interface, self).__init__('IR project')

        self._query = ControlText(label='Type your query and press "Enter"; for example:',
                                  defaultValue='Albert Einstein')

        self._query.key_pressed = self.__enter_pressed_event

        self._pages_result = ControlList('Found web-pages:')
        self._pages_result.readOnly = True
        self._pages_result.currentCellChanged = self.__page_selected
        self._pages_displayed = []

        self._papers_result = ControlList('Found papers:')
        self._papers_result.readOnly = True
        self._papers_result.currentCellChanged = self.__paper_selected
        self._papers_displayed = []

        self.formset = ['_query', ('_pages_result', '_papers_result')]

    def __enter_pressed_event(self, e):
        if e.key() == QtCore.Qt.Key_Return:

            query = query_words(self._query.value)
            self._pages_displayed, self._papers_displayed = process_query(query)

            self._pages_result.clear()
            self._pages_result.value = [(QtGui.QLabel(format_text(query, document, 'pages')),)
                                        for document in self._pages_displayed]
            self._pages_result.resizeRowsToContents()

            self._papers_result.clear()
            self._papers_result.value = [(QtGui.QLabel(format_text(query, document, 'papers')),)
                                        for document in self._papers_displayed]
            self._papers_result.resizeRowsToContents()

    def __page_selected(self, next_row, unused1, unused2, unused3):
        open_url(self._pages_displayed[next_row]['url'])

    def __paper_selected(self, next_row, unused1, unused2, unused3):
        open_url(self._papers_displayed[next_row]['url'])

if __name__ == '__main__':
    pyforms.startApp(Interface)