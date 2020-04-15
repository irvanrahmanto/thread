# import os, re dan threading
from threading import Thread
import os
import re

# import time
import time

received_packages = re.compile(r"Received = (\d)")

# buat kelas ip_check


class ip_check(Thread):

    # fungsi __init__; init untuk assign IP dan hasil respons = -1
    def __init__(self, ip):

        # fungsi utama yang diekseskusi ketika thread berjalan
        Thread.__init__(self)
        self.ip = ip
        self.status = -1

    def run(self):
        # lakukan ping dengan perintah ping -n (gunakan os.popen())
        pingaling = os.popen("Ping -n 2 " + self.ip, "r")

        # loop forever
        while True:
            # baca hasil respon setiap baris
            line = pingaling.readline()
            # break jika tidak ada line lagi
            if not line:
                break

            # baca hasil per line dan temukan pola Received = x
            if received_packages.findall(line):
                n_received = received_packages.findall(line)

        # tampilkan hasilnya
        print((self.ip, status[int(n_received[0])]))


'''	    if n_received:
	        print((status[int(n_received[0])]))
'''

# if n_received:
#     print((status[int(n_received[0])]))

# fungsi untuk mengetahui status; 0 = tidak ada respon, 1 = hidup tapi ada loss, 2 = hidup

# def status(self):
# 0 = tidak ada respon

# 1 = ada loss

# 2 = hidup

# -1 = seharusnya tidak terjadi

# buat regex untuk mengetahui isi dari r"Received = (\d)"

# catat waktu awal

# buat list untuk menampung hasil pengecekan

# lakukan ping untuk 20 host


# Buat regex untuk mengetahui isi dari r"Received = (\d)
status = ('No respond', 'loss', 'Nyala')

# catat waktu awal
start = time.time()

# list untuk menampung hasil pengecekan
ping_list = []

# Melakukan ping untuk 20 host
for suffix in range(1, 20):
    # tentukan IP host apa saja yang akan di ping
    ip = "192.168.1."+str(suffix+1)
    # panggil thread untuk setiap IP
    current = ip_check(ip)
    # masukkan setiap IP dalam list
    ping_list.append(current)
    # jalankan thread
    current.start()
    # untuk setiap IP yang ada di list

# for el in check_results:
for el in ping_list:

    # tunggu hingga thread selesai
    el.join()

    # dapatkan hasilnya


# catat waktu berakhir
end = time.time()

# tampilkan selisih waktu akhir dan awal
print('Waktu ping : ', end-start)
