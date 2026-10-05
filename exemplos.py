VALIDOS = [
    'postar foto "praia.jpg" legenda "Dia lindo!"',
    'postar reel "bastidores.mp4"',
    'agendar video "promo.mp4" legenda "Black Friday!" para 29/11 às 09:00',
    'postar story "cafe.jpg" legenda "Bom dia!"',
    'curtir post 12\ncomentar post 12 "Muito bom isso!"',
    'postar story "cafe.jpg" legenda "Bom dia!"\n'
    'agendar reel "promo.mp4" para 29/11 às 09:00',
    '''
    # campanha de fim de semana
    postar foto "praia.jpg" legenda "Dia lindo!"
    agendar reel "promo.mp4" para 29/11 às 09:00
    seguir perfil "joaosilva"
    parar de seguir perfil "joaosilva"
    listar posts
    deletar post 3
    ''',
]

INVALIDOS = [
    ('curtir 12', 'falta a palavra "post"'),
    ('postar audio "x.mp3"', 'tipo "audio" não existe'),
    ('agendar foto "a.jpg" para 25/09 18:00', 'falta o "às"'),
    ('comentar post 12 Muito bom', 'texto sem aspas'),
    ('deletar post', 'falta o número do post'),
    ('', 'programa vazio'),
]

SEMANTICAMENTE_INVALIDOS = [
    ('postar foto "video.mp4"', 'extensão incompatível com vídeo'),
    ('agendar foto "a.jpg" para 31/02 às 18:00', 'data inexistente'),
]
