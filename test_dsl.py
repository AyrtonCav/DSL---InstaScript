import unittest

from checker import ErroDeSemantica, verificar
from exemplos import INVALIDOS, SEMANTICAMENTE_INVALIDOS, VALIDOS
from lark.exceptions import UnexpectedInput


class TestDSLInstagram(unittest.TestCase):
    def test_validos(self):
        for programa in VALIDOS:
            verificar(programa)

    def test_invalidos_sintaticos(self):
        for programa, _ in INVALIDOS:
            with self.subTest(programa=programa):
                with self.assertRaises(UnexpectedInput):
                    verificar(programa)

    def test_invalidos_semanticos(self):
        for programa, _ in SEMANTICAMENTE_INVALIDOS:
            with self.subTest(programa=programa):
                with self.assertRaises(ErroDeSemantica):
                    verificar(programa)


if __name__ == "__main__":
    unittest.main()
