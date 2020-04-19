import os
import requests
import threading
import urllib.request
import urllib.error
import urllib.parse
import time

# Mengimport library threading, os, requests dan lain lain nya
url = "https://apod.nasa.gov/apod/image/1901/LOmbradellaTerraFinazzi.jpg"


def buildRange(value, numsplits):
    lst = []
    for i in range(numsplits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value /
                                               (numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
            # Menambahkan elemen pada array lst yang sudah dibuat
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0), 0)),
                                  int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    return lst


class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """

    def __init__(self, url, byteRange):
        super(SplitBufferThreads, self).__init__()
        self.__url = url
        self.__byteRange = byteRange
        self.req = None

        # Memisahkan buffer pada tiap thread dengan byte pada range tertentu

    def run(self):
        self.req = urllib.request.Request(
            self.__url,  headers={'Range': 'bytes=%s' % self.__byteRange})

    def getFileData(self):
        return urllib.request.urlopen(self.req).read()


def main(url=None, splitBy=3):
    # Memulai perintah recording waktu
    start_time = time.time()
    # terminate ural jika url belum ada
    if not url:
        print("Please Enter some url to begin download.")
        return

    # membagi nama file berdasarkan namanya dari path url posisi paling terakir
    fileName = url.split('/')[-1]

    # Mengukur besarnya file yang didownload
    sizeInBytes = requests.head(
        url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)

    # Mengoutputkan besarnya file
    print("%s bytes to download." % sizeInBytes)

    # Jika isi pada byte kosong, maka program akan selesai
    if not sizeInBytes:
        print("Size cannot be determined.")
        return

    # Membuat list baru
    dataLst = []

    # Melakukan perulangan sejumlah splitBy
    for idx in range(splitBy):

        # Membagi byte data sesuai dengan splitBy
        byteRange = buildRange(int(sizeInBytes), splitBy)[idx]

        # Mengassign thread dengan job sesuai dari pembagian yang dilakukan pada byterange
        bufTh = SplitBufferThreads(url, byteRange)

        # Memulai pengupload an
        bufTh.start()

        # main thread menunggu pekerjaan childtread selesai untuk dapat mengeksekusi pekerjaan lain nya
        bufTh.join()

        # Memasukkan data yang sudah dimasukan ke dalam list
        dataLst.append(bufTh.getFileData())

    # Menggabungkan isi datalst
    content = b''.join(dataLst)

    # Jika list dataLst berhasil terisi maka
    if dataLst:
        # Jika dalam folder memiliki nama file yang sama
        if os.path.exists(fileName):
            # Hapus file nya
            os.remove(fileName)
        # Outputkan waktu pekerjaan
        print("--- %s seconds ---" % str(time.time() - start_time))
        with open(fileName, 'wb') as fh:
            # Penulisan konten file
            fh.write(content)
        # Output selesai
        print("Finished Writing file %s" % fileName)


if __name__ == '__main__':
    # Menjalankan program utama
    main(url)
