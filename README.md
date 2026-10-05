# DSL Instagram

## Objetivo e domínio

Esta DSL descreve ações comuns de uma rede social de imagens e vídeos: publicar, agendar, curtir, comentar, seguir ou deixar de seguir perfis, listar e deletar posts. Ela foi criada para representar um fluxo de gerenciamento de conteúdo de forma curta e legível, sem exigir chamadas de API, detalhes de autenticação ou código de uma aplicação completa.

O domínio é adequado para uma DSL porque possui vocabulário próprio, comandos repetitivos e regras específicas, como formatos de arquivo compatíveis com cada tipo de publicação e validação de datas. A mesma ideia poderia ser usada em testes automatizados, ferramentas de planejamento de campanhas e interfaces de linha de comando para redes sociais.

## Estrutura do projeto

- `parser.py`: tokens, gramática Lark e função `analisar`.
- `checker.py`: verificação semântica e exceção `ErroDeSemantica`.
- `exemplos.py`: programas válidos e inválidos.
- `main.py`: demonstração com `pretty()`.
- `test_dsl.py`: testes automatizados.
- `dsl_instagram.py`: ponto de entrada compatível.

Execute:

```powershell
.\venv\Scripts\python.exe dsl_instagram.py
.\venv\Scripts\python.exe -m unittest -v
```

## Tokens

| Token | Exemplos | Função |
|---|---|---|
| Palavras-chave | `postar`, `agendar`, `curtir`, `post`, `perfil` | Comandos fixos da linguagem |
| `TIPO` | `foto`, `video`, `reel`, `story` | Tipo de conteúdo |
| `TEXTO` | `"praia.jpg"`, `"Dia lindo!"` | Strings entre aspas |
| `NUMERO` | `12`, `3` | Identificador numérico de post |
| `DATA` | `29/11` | Dia e mês |
| `HORA` | `09:00` | Hora e minuto |
| `COMENTARIO` | `# campanha` | Comentário ignorado pelo parser |

Espaços, quebras de linha e comentários são ignorados.

## Gramática em EBNF

```ebnf
start            = comando , { comando } ;
comando          = postar | agendar | curtir | comentar | seguir
                 | parar_de_seguir | deletar | listar ;
postar           = "postar" , conteudo ;
agendar          = "agendar" , conteudo , "para" , DATA , "às" , HORA ;
curtir           = "curtir" , "post" , NUMERO ;
comentar         = "comentar" , "post" , NUMERO , TEXTO ;
seguir           = "seguir" , "perfil" , TEXTO ;
parar_de_seguir  = "parar" , "de" , "seguir" , "perfil" , TEXTO ;
deletar          = "deletar" , "post" , NUMERO ;
listar           = "listar" , "posts" ;
conteudo         = TIPO , arquivo , [ legenda ] ;
arquivo          = TEXTO ;
legenda          = "legenda" , TEXTO ;
```

Os terminais `TIPO`, `TEXTO`, `NUMERO`, `DATA` e `HORA` são definidos por expressões léxicas no arquivo `parser.py`.

## Exemplo de derivação

Para a sentença `postar foto "praia.jpg" legenda "Dia lindo!"`:

```text
start
=> comando
=> postar
=> "postar" conteudo
=> "postar" TIPO arquivo legenda
=> "postar" "foto" TEXTO "legenda" TEXTO
=> "postar" "foto" "praia.jpg" "legenda" "Dia lindo!"
```

A forma concreta usa espaços entre os símbolos, mas eles são ignorados pelo lexer.

## Árvore sintática

Para o mesmo exemplo, `verificar(programa).pretty()` produz uma estrutura equivalente a:

```text
start
  postar
    conteudo
      foto
      arquivo  "praia.jpg"
      legenda  "Dia lindo!"
```

A árvore faz sentido porque registra o programa, o comando de postagem, o tipo do conteúdo, o arquivo e a legenda opcional em níveis correspondentes à gramática.

## Decisões de sintaxe

- Comandos usam verbos em português para aproximar a linguagem do domínio.
- `post` e `perfil` tornam o alvo da ação explícito.
- Arquivos e textos usam aspas para diferenciar conteúdo livre de palavras-chave.
- Uma execução contém um ou mais comandos, permitindo descrever uma campanha inteira.
- Comentários começam com `#` e não alteram a árvore sintática.
- `legenda` é opcional, mas aparece com uma palavra-chave para evitar ambiguidades.
- A gramática reconhece o formato de data e hora; o checker valida se os valores realmente existem.

## Sistema de tipos e regras semânticas

A DSL possui tipos de conteúdo (`foto`, `video`, `reel` e `story`), tipo textual (`TEXTO`), tipo numérico (`NUMERO`), data e hora. Os comandos não são expressões gerais: cada um aceita apenas os tipos definidos por sua produção.

Compatibilidade de arquivos:

- `foto`: `.jpg`, `.jpeg`, `.png`, `.gif`;
- `video`: `.mp4`, `.mov`, `.avi`, `.mkv`;
- `reel`: `.mp4`, `.mov`;
- `story`: `.jpg`, `.jpeg`, `.png`, `.mp4`.

Exemplos válidos: `postar foto "praia.jpg"` e `agendar reel "video.mp4" para 29/11 às 09:00`.

Exemplos inválidos: `postar foto "video.mp4"` por incompatibilidade de extensão e `agendar foto "a.jpg" para 31/02 às 18:00` por data inexistente. O primeiro caso é rejeitado pelo checker; o segundo também passa pelo parser, mas falha na validação semântica.
