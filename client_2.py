import sys
import socket
import logging
import threading


def kirim_data(nama="kosong"):
    logging.warning(f"nama {nama}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('172.16.16.101', 45000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = 'TIME INI ADALAH DATA YANG DIKIRIM ABCDEFGHIJKLMNOPQ \r\n'
        logging.warning(f"[CLIENT {nama}] sending {message.strip()}")
        sock.sendall(message.encode())
        
        # Look for the response
        data = sock.recv(64)
        logging.warning(f"[CLIENT {nama}] [DITERIMA DARI SERVER] {data.decode().strip()}")
    finally:
        logging.warning(f"[CLIENT {nama}] closing")
        sock.close()
    return


if __name__ == '__main__':
    threads = []
    for i in range(3):
        t = threading.Thread(target=kirim_data, args=(i,))
        threads.append(t)

    for thr in threads:
        thr.start()

    for thr in threads:
        thr.join()