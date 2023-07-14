from Crypto.Cipher import DES, Blowfish, AES
from Crypto.Random import get_random_bytes
import time
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm



def test(bytes):
    data = get_random_bytes(bytes)

    key_des = get_random_bytes(8)
    cipher_des = DES.new(key_des, DES.MODE_ECB)

    key_blowfish = get_random_bytes(56)
    cipher_blowfish = Blowfish.new(key_blowfish, Blowfish.MODE_ECB)

    key_aes128 = get_random_bytes(16)
    cipher_aes128 = AES.new(key_aes128, AES.MODE_ECB)

    key_aes192 = get_random_bytes(24)
    cipher_aes192 = AES.new(key_aes192, AES.MODE_ECB)

    key_aes256 = get_random_bytes(32)
    cipher_aes256 = AES.new(key_aes256, AES.MODE_ECB)

    start_time = time.time()
    enc_des = cipher_des.encrypt(data)
    destimeE = time.time() - start_time

    start_time = time.time()
    dec_des = cipher_des.decrypt(enc_des)
    destimeD = time.time() - start_time

    start_time = time.time()
    enc_blowfish = cipher_blowfish.encrypt(data)
    bftimeE = time.time() - start_time

    start_time = time.time()
    dec_blowfish = cipher_blowfish.decrypt(enc_blowfish)
    bftimeD = time.time() - start_time

    start_time = time.time()
    enc_aes = cipher_aes128.encrypt(data)
    aestimeE128 = time.time() - start_time

    start_time = time.time()
    dec_aes = cipher_aes128.decrypt(enc_aes)
    aestimeD128= time.time() - start_time

    start_time = time.time()
    enc_aes = cipher_aes192.encrypt(data)
    aestimeE192 = time.time() - start_time

    start_time = time.time()
    dec_aes = cipher_aes192.decrypt(enc_aes)
    aestimeD192 = time.time() - start_time
    start_time = time.time()

    enc_aes = cipher_aes256.encrypt(data)
    aestimeE256 = time.time() - start_time

    start_time = time.time()
    dec_aes = cipher_aes256.decrypt(enc_aes)
    aestimeD256 = time.time() - start_time

    encode = destimeE, bftimeE, aestimeE128, aestimeE192, aestimeE256
    decode = destimeD, bftimeD, aestimeD128, aestimeD192, aestimeD256

    return [destimeE, destimeD, bftimeE, bftimeD, aestimeE128, aestimeD128, aestimeE192, aestimeD192, aestimeE256, aestimeD256]

def get_avg(bytes, times=30):
    avg = np.zeros(10)
    for i in range(times):
        results = np.array(test(bytes))
        avg += results
    avg = avg / times
    return avg

def iteratebytes(start=16, stop=10485760, steps=25):
    results = {
    "des": {
        "encode": {},
        "decode": {}
    },
    "bf": {
        "encode": {},
        "decode": {}
    },
    "aes128": {
        "encode": {},
        "decode": {}
    },
    "aes192": {
        "encode": {},
        "decode": {}
    },
    "aes256": {
        "encode": {},
        "decode": {}
    }
}
    step_size = (stop - start) / (steps - 1)  # calculate the step size
    step_size = int((step_size + 127) // 128 * 128)  # round up to nearest 128-bit divisible size
    sizes = [i * step_size for i in range(steps)]
    for idx,size in tqdm(enumerate(sizes)):
        times = get_avg(size)
        results["des"]["encode"][size] = times[0]
        results["des"]["decode"][size] = times[1]
        results["bf"]["encode"][size] = times[2]
        results["bf"]["decode"][size] = times[3]
        results["aes128"]["encode"][size] = times[4]
        results["aes128"]["decode"][size] = times[5]
        results["aes192"]["encode"][size] = times[6]
        results["aes192"]["decode"][size] = times[7]
        results["aes256"]["encode"][size] = times[8]
        results["aes256"]["decode"][size] = times[9]
    return results


def create_plot(data, action):
    plt.figure(figsize=(10,6))
    for method, stats in data.items():
        byte_sizes = list(stats[action].keys())
        times = list(stats[action].values())
        plt.plot(byte_sizes, times, label=method)
    plt.xlabel('Byte Size')
    plt.ylabel('Time')
    plt.title(f'{action.capitalize()} Time vs Byte Size for Different Encryption Methods')
    plt.legend()
    plt.grid(True)
    plt.show()

# Call the function for encoding and decoding
data = iteratebytes(start=16, stop=1048, steps=10)

create_plot(data, 'encode')
create_plot(data, 'decode')

aes_data = {method: stats for method, stats in data.items() if 'aes' in method}

create_plot(aes_data, 'encode')
create_plot(aes_data, 'decode')


