#!/usr/bin/python3

import hashlib
import sys
import socket
from threading import Thread, Lock


class WorkerThread(Thread):

    def __init__(self, conn, address, recv_size, *args, **kwargs):
        self.conn = conn
        self.address = address
        self.recv_size = recv_size

        super().__init__(*args, **kwargs)

    def header_message(self):
        message = "Informe uma mensagem para ser computada por funcoes hash\n"
        message += ">> "
        return message.encode()

    def hashes_messages(self, msg):
        mmsg = 'sha1     -:> ' + hashlib.sha1(msg).hexdigest() + '\n'
        mmsg += 'sha256   -:> ' + hashlib.sha256(msg).hexdigest() + '\n'
        mmsg += 'sha512   -:> ' + hashlib.sha512(msg).hexdigest() + '\n'
        mmsg += 'md5      -:> ' + hashlib.md5(msg).hexdigest() + '\n'

        return mmsg.encode()

    def footer_message(self):

        message = '\nTask resolvida pela WorkerThread-{0}\n'.format(
            self.native_id)

        message += '-'*78 + '\n'

        return message.encode()

    def _task(self, conn):

        conn.sendall(self.header_message())

        msg = conn.recv(self.recv_size)

        msg = self.hashes_messages(msg)
        conn.sendall(msg)

        conn.sendall(self.footer_message())

    def _run(self):
        try:
            with self.conn as conn:
                self._task(conn)
        except Exception as e:
            pass

    def run(self):
        try:
            with self.conn as conn:
                while True:
                    self._task(conn)
        except Exception as e:
            pass


class ServerThread(Thread):
    RECV_SIZE = 1024
    server_connection = None

    def __init__(self, lock, worker_cond, port=10000, address='0.0.0.0', listen=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = port
        self.address = address
        self.listen = listen
        self.lock = lock
        self.worker_cond = worker_cond

        self.connection_pool = []

    def connect(self):
        try:
            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ss.bind((self.address, self.port))
            ss.listen(self.listen)
            ServerThread.server_connection = ss
            return ss

        except OSError:
            return ServerThread.server_connection

    def header_message(self, addr):
        message = '-'*78 + '\n'
        message += "Bem vindo ao Servidor\n"
        message += 'connected by: {0}\n'.format(addr)
        message += 'ServerThread native ID : {0}\n'.format(self.native_id)
        message += "Informe mensagens para serem computadas por funcoes hash\n"
        message += "Para cancelar a conexao use Ctrl + C\n"
        message += "="*78 + "\n"

        return message.encode()

    def hashes_messages(self, msg):
        mmsg = 'sha1     -:> ' + hashlib.sha1(msg).hexdigest() + '\n'
        mmsg += 'sha256   -:> ' + hashlib.sha256(msg).hexdigest() + '\n'
        mmsg += 'sha512   -:> ' + hashlib.sha512(msg).hexdigest() + '\n'
        mmsg += 'md5      -:> ' + hashlib.md5(msg).hexdigest() + '\n'

        return mmsg.encode()

    def footer_message(self):
        return ('-'*78 + '\n').encode()

    def run(self):
        while True:

            with self.lock:
                conn, addr = self.connect().accept()
                print(addr)
                self.connection_pool.append((conn, addr))

            try:
                conn, addr = self.connection_pool.pop(0)
                conn.sendall(self.header_message(addr))

                if self.worker_cond:

                    WorkerThread(conn, addr, ServerThread.RECV_SIZE).start()
                else:
                    WorkerThread(conn, addr, ServerThread.RECV_SIZE)._run()

            except IndexError as e:
                raise e


if __name__ == "__main__":
    if len(sys.argv) < 3:
        message = "Use ./server.py server_thread_num   work_thread_cond\n"
        message += "onde server_thread_num é o numero de threads que o servidor terá\n"
        message += "e work_thread_cond é 0 ou 1, caso seja 1, será mantido\n"
        message += "um WorkerThread por conexão de usuário e além disso,\n"
        message += "será mantido a conexão do usuário após o trabalho feito \n"

        print(message)
        exit(1)

    server_thread_num = int(sys.argv[1])
    work_thread_cond = int(sys.argv[2])
    lock = Lock()
    server_thread_list = []

    for i in range(server_thread_num):
        st = ServerThread(lock, worker_cond=work_thread_cond)
        server_thread_list.append(st)

    for server in server_thread_list:
        server.start()
