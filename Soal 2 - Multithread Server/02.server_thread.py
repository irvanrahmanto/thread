# import socket, sys, traceback dan threading
import socket
import sys
import traceback
from threading import Thread

# jalankan server


def main():
    start_server()

# fungsi saat server dijalankan


def start_server():
    # tentukan IP server
    ip = '127.0.0.1'

    # tentukan port server
    port = 4343

    # buat socket bertipe TCP
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # option socket
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket dibuat")

    # lakukan bind
    try:
        soc.bind((ip, port))
    except:
        # exit pada saat error
        print("Bind gagal. Error : " + str(sys.exc_info()))
        sys.exit()

    # listen hingga 5 antrian
    soc.listen(5)
    print("Socket mendengarkan")

    # infinite loop, jangan reset setiap ada request
    while True:
        # terima koneksi
        c, addr = soc.accept()
        # dapatkan IP dan port
        ip, port = str(addr[0]), str(addr[1])
        print("Connected dengan " + ip + ":" + port)

        # jalankan thread untuk setiap koneksi yang terhubung
        try:
            Thread(target=client_thread, args=(c, ip, port)).start()
        except:
            # print kesalahan jika thread tidak berhasil dijalankan
            print("Thread tidak berjalan.")
            traceback.print_exc()

    # tutup socket
    soc.close()


def client_thread(connection, ip, port, max_buffer_size=4096):
    # flag koneksi
    is_active = True

    # selama koneksi aktif
    while is_active:

        # terima pesan dari client
        # client_input = receive_input(connection, max_buffer_size)
        client_input = receive_input(connection, max_buffer_size)

        # dapatkan ukuran pesan

        # print jika pesan terlalu besar

        # dapatkan pesan setelah didecode

        # jika "quit" maka flag koneksi = false, matikan koneksi
        if "quit" in client_input:
            # ubah flag
            is_active = True
            print("Client meminta keluar")

            # matikan koneksi
            connection.close()
            print("Connection " + ip + ":" + port + " ditutup")

        else:
            # tampilkan pesan dari client
            print("Processed result: {}".format(client_input))
            connection.sendall("-".encode("utf-8"))


def receive_input(connection, max_buffer_size):
    # terima pesan dari client
    client_input = connection.recv(max_buffer_size)
    # dapatkan ukuran pesan
    client_input_size = sys.getsizeof(client_input)

    # print jika pesan terlalu besar
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}").format(
            (client_input_size))

    # Dapatkan pesan setelah didecode
    decoded_input = client_input.decode("utf8").rstrip()
    result = process_input(decoded_input)
    return result


def process_input(input_str):
    print("Processing the input received from client")
    return str(input_str).upper()


# panggil fungsi utama
if __name__ == "__main__":
    main()
