#!/usr/bin/python3

'''
Author: Leonardo Souza

Tarefa da Matéria de Sistemas Concorrentes e Distribuídos do CEFET-RJ
Professor: Glauco Fiorott Amorim
Trabalho de Programação Multithreading

Implementação básica de um client para o Servidor Multithreading. 
'''
import socket


def connect(address, port):
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.connect((address, port))
    return ss


RECV_SIZE = 4096  # 2048

if __name__ == "__main__":
    with connect('127.0.0.1', 10000) as con:
        con.settimeout(0.5)

        msg = ""
        while True:
            try:
                msg = con.recv(RECV_SIZE).decode()
                print(msg, end="")

                if not len(msg):
                    raise BrokenPipeError()

            except socket.timeout as e:
                inp = input().encode()
                resp = con.sendall(inp)

            except BrokenPipeError as e:
                break
