
# Implementação MQTT

Os scripts implementados simulam uma "inscrição" em assuntos do HN(https://news.ycombinator.com/),
utilizando a api (https://github.com/HackerNews/API).

O arquivo jobstories é responsável por publicar tópicos sobre empregos públicados na HN. Por padrão, pública somente os 4 últimos anúncios e além disso, se inscreve no tópico de top stories e lê as mensagens do canal.

Já o arquivo topstories, publica tópicos dos top stories da HN(publica por padrão, 2) e lê as mensagens do canal de job stories.


# Rodando o código no Linux/*nix

- É necessário Python 3.6

- Crie uma env e instale as dependências
    python3 -m venv env

    source env/bin/activate 

    pip3 install -r requiriments.txt


Em um terminal rode:
python3 jobstories.py


Em outro:
python3 topstories.py
