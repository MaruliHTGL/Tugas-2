from socket import *
import socket
import threading
import logging
from datetime import datetime

def proses_string(request_string):
    balas = "ERROR\r\n"
    if request_string.startswith("TIME") and request_string.endswith("\r\n"):
        now = datetime.now()
        waktu = now.strftime("%H:%M:%S")
        balas = f"JAM {waktu}\r\n"
    elif request_string.startswith("QUIT") and request_string.endswith("\r\n"):
        balas = "XXX"
    return balas

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        try:
            buffer = ""
            while True:
                data = self.connection.recv(32)
                if not data:
                    break
                buffer += data.decode()
    
                # Periksa apakah buffer sudah mengandung pesan lengkap (berakhir \r\n)
                while "\r\n" in buffer:
                    # Pisahkan pesan sampai \r\n
                    request_s, buffer = buffer.split("\r\n", 1)
                    logging.warning(f"[SERVER] menerima request: {request_s.strip()}")
                    balas = proses_string(request_s + "\r\n")  # tambahkan \r\n lagi karena fungsi proses_string mengecek
    
                    if balas == "XXX":
                        self.connection.close()
                        return
                    self.connection.sendall(balas.encode())
        except Exception as e:
            logging.error(f"Exception: {e}")
        finally:
            self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5) 
        logging.warning("[SERVER] Listening on port 45000")
        while True:
            connection, client_address = self.my_socket.accept()
            logging.warning(f"[SERVER] Connection from {client_address}")

            clt = ProcessTheClient(connection, client_address)
            clt.start()
            self.the_clients.append(clt)

# Fungsi main
def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
