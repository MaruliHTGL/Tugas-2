import sys
import socket
import logging



def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('172.16.16.101', 45000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = 'TIME INI ADALAH DATA YANG DIKIRIM ABCDEFGHIJKLMNOPQ \r\n'
        logging.warning(f"[CLIENT] sending {message.strip()}")
        sock.sendall(message.encode())
        
        # Look for the response
        data = sock.recv(64)  # buffer bisa disesuaikan
        logging.warning(f"[DITERIMA DARI SERVER] {data.decode().strip()}")
    finally:
        logging.warning("closing")
        sock.close()
    return


if __name__=='__main__':
    for i in range(1,10):
        kirim_data()
