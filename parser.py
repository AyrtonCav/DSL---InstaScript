from lark import Lark

GRAMATICA = r'''
start: comando+

?comando: postar
        | agendar
        | curtir
        | comentar
        | seguir
        | parar_de_seguir
        | deletar
        | listar

postar:          "postar" conteudo
agendar:         "agendar" conteudo "para" DATA "às" HORA
curtir:          "curtir" "post" NUMERO
comentar:        "comentar" "post" NUMERO TEXTO
seguir:          "seguir" "perfil" TEXTO
parar_de_seguir: "parar" "de" "seguir" "perfil" TEXTO
deletar:         "deletar" "post" NUMERO
listar:          "listar" "posts"

conteudo: TIPO arquivo legenda?
arquivo:  TEXTO
legenda:  "legenda" TEXTO

TIPO:       "foto" | "video" | "reel" | "story"
TEXTO:      ESCAPED_STRING
NUMERO:     /[0-9]+/
DATA:       /[0-9]{2}\/[0-9]{2}/
HORA:       /[0-9]{2}:[0-9]{2}/
COMENTARIO: /#[^\n]*/

%import common.ESCAPED_STRING
%import common.WS
%ignore WS
%ignore COMENTARIO
'''

parser = Lark(GRAMATICA, start="start", parser="lalr")


def analisar(programa: str):
    """Analisa sintaticamente um programa e retorna sua árvore Lark."""
    return parser.parse(programa)
