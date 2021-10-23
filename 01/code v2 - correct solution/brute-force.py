from Crypto.Cipher import AES
import time, base64, random
from multiprocessing import cpu_count, Pool
from datetime import datetime

startTime = time.time()
startHex = 0x5FFFFFFD
endHex = 0x62590081
cores_arr = [1, 2, 3, 4, 5, 6, 7, 8]
iv = bytearray.fromhex('10000000000000000000000000000000')
with open('zadanie_ciphertext.txt') as f:
    ciphertext = f.read().replace('\n', '')


def decrypt1(start, end, f1):
    f1.write("Starting core 1. " + str(end) + "-" + str(start) + str(datetime.today().isoformat()) + '\n')
    f1.flush()
    for i in range(end, start, -1):
        key = bytearray.fromhex(hex(i)[2:] + '000000000000000000000000')
        decryptor = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = decryptor.decrypt(base64.b64decode(ciphertext))

        try:
            text = plaintext.decode()
        except UnicodeDecodeError:
            if not i % 10000000:
                f1.write('core 1: '+ str(((end-i) / end) * 100) + "% searched. (" + str(abs(i - end + 1)) + ") " + str(datetime.today().isoformat()) + '\n')
                f1.flush()
            pass
        else:
            endTime = time.time()
            print(text)
            f1.write(text + '\n\n\n\n' + 'time: ' + str(endTime - startTime) + '\n' + 'key: ' + str(i))
            f1.flush()
            f1.close()


def decrypt2(start, end, f2):
    f2.write("Starting core 2. " + str(end) + "-" + str(start) + str(datetime.today().isoformat()) + '\n')
    f2.flush()
    for i in range(end, start, -1):
        key = bytearray.fromhex(hex(i)[2:] + '000000000000000000000000')
        decryptor = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = decryptor.decrypt(base64.b64decode(ciphertext))

        try:
            text = plaintext.decode()
        except UnicodeDecodeError:
            if not i % 10000000:
                f2.write('core 2: '+ str(((end-i) / end) * 100) + "% searched. (" + str(abs(i - end + 1)) + ") " + str(datetime.today().isoformat()) + '\n')
                f2.flush()
            pass
        else:
            endTime = time.time()
            print(text)
            f2.write(text + '\n\n\n\n' + 'time: ' + str(endTime - startTime) + '\n' + 'key: ' + str(i))
            f2.flush()
            f2.close()


def decrypt3(start, end, f3):
    f3.write("Starting core 3. " + str(end) + "-" + str(start) + str(datetime.today().isoformat()) + '\n')
    f3.flush()
    for i in range(end, start, -1):
        key = bytearray.fromhex(hex(i)[2:] + '000000000000000000000000')
        decryptor = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = decryptor.decrypt(base64.b64decode(ciphertext))

        try:
            text = plaintext.decode()
        except UnicodeDecodeError:
            if not i % 10000000:
                f3.write('core 3: '+ str(((end-i) / end) * 100) + "% searched. (" + str(abs(i - end + 1)) + ") " + str(datetime.today().isoformat()) + '\n')
                f3.flush()
            pass
        else:
            endTime = time.time()
            print(text)
            f3.write(text + '\n\n\n\n' + 'time: ' + str(endTime - startTime) + '\n' + 'key: ' + str(i))
            f3.flush()
            f3.close()


def decrypt4(start, end, f4):
    f4.write("Starting core 4. " + str(end) + "-" + str(start) + str(datetime.today().isoformat()) + '\n')
    f4.flush()
    for i in range(end, start, -1):
        key = bytearray.fromhex(hex(i)[2:] + '000000000000000000000000')
        decryptor = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = decryptor.decrypt(base64.b64decode(ciphertext))

        try:
            text = plaintext.decode()
        except UnicodeDecodeError:
            if not i % 10000000:
                f4.write('core 4: '+ str(((end-i) / end) * 100) + "% searched. (" + str(abs(i - end + 1)) + ") " + str(datetime.today().isoformat()) + '\n')
                f4.flush()
            pass
        else:
            endTime = time.time()
            print(text)
            f4.write(text + '\n\n\n\n' + 'time: ' + str(endTime - startTime) + '\n' + 'key: ' + str(i))
            f4.flush()
            f4.close()


def decrypt5(start, end, f5):
    f5.write("Starting core 5. " + str(end) + "-" + str(start) + str(datetime.today().isoformat()) + '\n')
    f5.flush()
    for i in range(end, start, -1):
        key = bytearray.fromhex(hex(i)[2:] + '000000000000000000000000')
        decryptor = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = decryptor.decrypt(base64.b64decode(ciphertext))

        try:
            text = plaintext.decode()
        except UnicodeDecodeError:
            if not i % 10000000:
                f5.write('core 5: '+ str(((end-i) / end) * 100) + "% searched. (" + str(abs(i - end + 1)) + ") " + str(datetime.today().isoformat()) + '\n')
                f5.flush()
            pass
        else:
            endTime = time.time()
            print(text)
            f5.write(text + '\n\n\n\n' + 'time: ' + str(endTime - startTime) + '\n' + 'key: ' + str(i))
            f5.flush()
            f5.close()


def decrypt6(start, end, f6):
    f6.write("Starting core 6. " + str(end) + "-" + str(start) + str(datetime.today().isoformat()) + '\n')
    f6.flush()
    for i in range(end, start, -1):
        key = bytearray.fromhex(hex(i)[2:] + '000000000000000000000000')
        decryptor = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = decryptor.decrypt(base64.b64decode(ciphertext))

        try:
            text = plaintext.decode()
        except UnicodeDecodeError:
            if not i % 10000000:
                f6.write('core 6: '+ str(((end-i) / end) * 100) + "% searched. (" + str(abs(i - end + 1)) + ") " + str(datetime.today().isoformat()) + '\n')
                f6.flush()
            pass
        else:
            endTime = time.time()
            print(text)
            f6.write(text + '\n\n\n\n' + 'time: ' + str(endTime - startTime) + '\n' + 'key: ' + str(i))
            f6.flush()
            f6.close()


def decrypt7(start, end, f7):
    f7.write("Starting core 7. " + str(end) + "-" + str(start) + str(datetime.today().isoformat()) + '\n')
    f7.flush()
    for i in range(end, start, -1):
        key = bytearray.fromhex(hex(i)[2:] + '000000000000000000000000')
        decryptor = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = decryptor.decrypt(base64.b64decode(ciphertext))

        try:
            text = plaintext.decode()
        except UnicodeDecodeError:
            if not i % 10000000:
                f7.write('core 7: '+ str(((end-i) / end) * 100) + "% searched. (" + str(abs(i - end + 1)) + ") " + str(datetime.today().isoformat()) + '\n')
                f7.flush()
            pass
        else:
            endTime = time.time()
            print(text)
            f7.write(text + '\n\n\n\n' + 'time: ' + str(endTime - startTime) + '\n' + 'key: ' + str(i))
            f7.flush()
            f7.close()


def decrypt8(start, end, f8):
    f8.write("Starting core 8. " + str(end) + "-" + str(start) + str(datetime.today().isoformat()) + '\n')
    f8.flush()
    for i in range(end, start, -1):
        key = bytearray.fromhex(hex(i)[2:] + '000000000000000000000000')
        decryptor = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = decryptor.decrypt(base64.b64decode(ciphertext))

        try:
            text = plaintext.decode()
        except UnicodeDecodeError:
            if not i % 10000000:
                f8.write('core 8: '+ str(((end-i) / end) * 100) + "% searched. (" + str(abs(i - end + 1)) + ") " + str(datetime.today().isoformat()) + '\n')
                f8.flush()
            pass
        else:
            endTime = time.time()
            print(text)
            f8.write(text + '\n\n\n\n' + 'time: ' + str(endTime - startTime) + '\n' + 'key: ' + str(i))
            f8.flush()
            f8.close()


def wrapper(core):
    if core == 1:
        f1 = open('core_1.txt', 'w')
        decrypt1(startHex, ((endHex - startHex) // 8) * 1 + startHex, f1)
    if core == 2:
        f2 = open('core_2.txt', 'w')
        decrypt2(((endHex - startHex) // 8) * 1 + startHex, ((endHex - startHex) // 8) * 2 + startHex, f2)
    if core == 3:
        f3 = open('core_3.txt', 'w')
        decrypt3(((endHex - startHex) // 8) * 2 + startHex, ((endHex - startHex) // 8) * 3 + startHex, f3)
    if core == 4:
        f4 = open('core_4.txt', 'w')
        decrypt4(((endHex - startHex) // 8) * 3 + startHex, ((endHex - startHex) // 8) * 4 + startHex, f4)
    if core == 5:
        f5 = open('core_5.txt', 'w')
        decrypt5(((endHex - startHex) // 8) * 4 + startHex, ((endHex - startHex) // 8) * 5 + startHex, f5)
    if core == 6:
        f6 = open('core_6.txt', 'w')
        decrypt6(((endHex - startHex) // 8) * 5 + startHex, ((endHex - startHex) // 8) * 6 + startHex, f6)
    if core == 7:
        f7 = open('core_7.txt', 'w')
        decrypt7(((endHex - startHex) // 8) * 6 + startHex, ((endHex - startHex) // 8) * 7 + startHex, f7)
    if core == 8:
        f8 = open('core_8.txt', 'w')
        decrypt8(((endHex - startHex) // 8) * 7 + startHex, endHex, f8)


if __name__ == "__main__":
    with Pool(processes=cpu_count()) as pool:
        pool.map(wrapper, cores_arr)
