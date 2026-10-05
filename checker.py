import ast
from datetime import datetime
from pathlib import PurePath

from lark import Tree

from parser import analisar


class ErroDeSemantica(ValueError):
    """Indica que o programa é sintaticamente correto, mas semanticamente inválido."""


def _texto(token) -> str:
    return ast.literal_eval(str(token))


def _verificar_conteudo(conteudo: Tree) -> None:
    tipo = str(conteudo.children[0])
    arquivo = _texto(conteudo.children[1].children[0])
    extensao = PurePath(arquivo).suffix.lower().lstrip(".")
    extensoes = {
        "foto": {"jpg", "jpeg", "png", "gif"},
        "video": {"mp4", "mov", "avi", "mkv"},
        "reel": {"mp4", "mov"},
        "story": {"jpg", "jpeg", "png", "mp4"},
    }
    if extensao not in extensoes[tipo]:
        permitidas = ", ".join(sorted(extensoes[tipo]))
        raise ErroDeSemantica(
            f'arquivo "{arquivo}" incompatível com {tipo}; use: {permitidas}'
        )


def verificar(programa: str):
    """Valida sintaxe e semântica, retornando a árvore se tudo estiver correto."""
    arvore = analisar(programa)
    for comando in arvore.iter_subtrees_topdown():
        if comando.data in {"postar", "agendar"}:
            _verificar_conteudo(comando.children[0])
            if comando.data == "agendar":
                data = str(comando.children[1])
                hora = str(comando.children[2])
                try:
                    datetime.strptime(f"{data}/{datetime.now().year} {hora}", "%d/%m/%Y %H:%M")
                except ValueError as erro:
                    raise ErroDeSemantica(f"data ou hora inválida: {data} às {hora}") from erro
    return arvore
