"""Test the languages that are provided.

"""


from unittest import TestCase
from txt2boil.langs import Racket, Python


class TestGen(TestCase):

    def checkGenerates(self, src, out):
        self.assertMultiLineEqual(out, self.gen(src))
        self.assertMultiLineEqual(out, self.gen(out))


class RacketConstantTester(TestGen, Racket):

    """Test the boilerplate generation in Racket code.

    """

    basicText = r"""
;; Constant Gen: r(\d+)/(\d+) (make-my-rational \1 \2)

r5/7
"""

    basicAnswer = r"""
;; Constant Gen: r(\d+)/(\d+) (make-my-rational \1 \2)
(define r5/7 (make-my-rational 5 7))

r5/7
"""

    blahComment = r"""
;; blah
"""

    def test_solecomment(self):
        """Test the constant generation.

        """

        self.checkGenerates(self.basicText, self.basicAnswer)

    def test_onecommentwithothers(self):
        """Test with the existence of other comments.

        """

        self.checkGenerates(self.blahComment + self.basicText,
                            self.blahComment + self.basicAnswer)

    def test_extractmany(self):
        """Test the extraction of many comments.

        """

        c = self.comments(r"""
;; foo

;; bar
""")
        self.assertEqual(c, ['foo\n', 'bar\n'])

    def test_commentextraction(self):
        """Test the extraction of comments.

        """

        c = self.comments(self.basicAnswer)
        self.assertEqual(
            c, [r"Constant Gen: r(\d+)/(\d+) (make-my-rational \1 \2)" +
                "\n"])

    lineGenTest = r"""
;; Line Gen:
;; r(\d+)/(\d+)
;; (define \g<0> (make-my-rational \1 \2))

r5/7
"""

    lineGenAnswer = r"""
;; Line Gen:
;; r(\d+)/(\d+)
;; (define \g<0> (make-my-rational \1 \2))
(define r5/7 (make-my-rational 5 7))

r5/7
"""

    def testLineGen(self):
        self.checkGenerates(self.lineGenTest, self.lineGenAnswer)


class PythonTester(Python, TestGen):

    basicTest = r"""
# Line Gen:
# g(\d+)_(\d+)
# \g<0> = divmod(\1, \2)

print g9_7
"""

    basicAnswer = r"""
# Line Gen:
# g(\d+)_(\d+)
# \g<0> = divmod(\1, \2)
g9_7 = divmod(9, 7)

print g9_7
"""

    def testBasic(self):
        self.checkGenerates(self.basicTest, self.basicAnswer)

