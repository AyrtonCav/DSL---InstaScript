from lark.exceptions import UnexpectedInput

from checker import ErroDeSemantica, verificar
from exemplos import INVALIDOS, SEMANTICAMENTE_INVALIDOS, VALIDOS
from parser import GRAMATICA, analisar, parser


def executar_demo():
    print("=" * 60)
    print("PROGRAMAS VÁLIDOS")
    print("=" * 60)
    for indice, programa in enumerate(VALIDOS, 1):
        print(f"\n--- Exemplo {indice} ---")
        print(programa.strip())
        arvore = verificar(programa)
        print("\nÁrvore (pretty):")
        print(arvore.pretty())

    print("=" * 60)
    print("PROGRAMAS INVÁLIDOS (erros esperados)")
    print("=" * 60)
    for programa, motivo in INVALIDOS:
        try:
            verificar(programa)
            print(f"[ERRO] aceitou indevidamente: {programa!r}")
        except UnexpectedInput:
            print(f"[OK] rejeitado ({motivo}): {programa!r}")

    print("=" * 60)
    print("ERROS SEMÂNTICOS (erros esperados)")
    print("=" * 60)
    for programa, motivo in SEMANTICAMENTE_INVALIDOS:
        try:
            verificar(programa)
            print(f"[ERRO] aceitou indevidamente: {programa!r}")
        except ErroDeSemantica:
            print(f"[OK] rejeitado ({motivo}): {programa!r}")


if __name__ == "__main__":
    executar_demo()
