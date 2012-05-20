# -*- coding: utf-8 -*-

import unittest
from markdown import Markdown


class MarkdownTest(unittest.TestCase):
    def test_h1(self):
        text = '# h1'
        html = Markdown.convert(text)
        self.assertEqual(html, '<h1>h1</h1>\n')

    def test_h2(self):
        text = '## h2'
        html = Markdown.convert(text)
        self.assertEqual(html, '<h2>h2</h2>')

if __name__ == '__main__':
    unittest.main()
