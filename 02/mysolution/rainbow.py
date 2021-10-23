# mnozina plaintextov: (ais_id + 00000000) - (ais_id + 99999999) to je jeden milion
# mnozina ciphertextov: priestor velky 2^256

from Crypto.Hash import SHA256
from random import randint
from time import time

my_ais_id = b'91764'
my_ais_id_str = '91764'


class Table:
    def __init__(self, m, t, table_dict):
        self.m = m
        self.t = t
        self.table_dict = table_dict


def generate_ciphertexts():
    hashes = []
    for i in range(1000):
        pin = bytearray(generate_pin(999999), 'utf-8')
        hashes.append(SHA256.new(my_ais_id + pin).hexdigest())

    return hashes


def generate_pin(boundary):
    pin = list(str(randint(0, boundary)))
    pin_arr = ['0', '0', '0', '0', '0', '0']

    j = -1
    for i in range(len(pin) - 1, -1, -1):
        pin_arr[j] = pin[i]
        j -= 1

    return ''.join(pin_arr)


def generate_rainbow_table(m, t):
    table_dict = dict()
    for i in range(m):
        chain = []
        starting_point = my_ais_id_str + generate_pin(30000)
        chain.append(starting_point)
        for j in range(t):
            sha_output = SHA256.new(bytes(chain[j], 'utf-8')).hexdigest()
            chain.append(reduction_function(sha_output, j))

        ending_point = chain[-1]
        table_dict[ending_point] = starting_point

    t = Table(m, t, table_dict)
    return t


def reduction_function(hash_input, p):
    numeric_hash = int(hash_input, 16)
    pin = str((numeric_hash + p) % 1000000)
    pin_arr = ['0', '0', '0', '0', '0', '0']

    j = -1
    for i in range(len(pin) - 1, -1, -1):
        pin_arr[j] = pin[i]
        j -= 1

    return my_ais_id_str + ''.join(pin_arr)


def browse_rainbow_chain(ciphertext, reduced_ciphertext, table, endpoint):
    if endpoint == reduced_ciphertext:
        chain = [table.table_dict[endpoint]] # starting point
        for i in range(table.t):
            sha_output = SHA256.new(bytes(chain[i], 'utf-8')).hexdigest()
            reduced = reduction_function(sha_output, i)
            if reduced == reduced_ciphertext:
                return false_alarm_check(ciphertext, chain[-1])

            chain.append(reduced)

    else:
        chain = [reduced_ciphertext]
        for i in range(table.t):
            sha_output = SHA256.new(bytes(chain[i], 'utf-8')).hexdigest()
            potential_endpoint = reduction_function(sha_output, i)

            if potential_endpoint in table.table_dict:
                chain = [table.table_dict[potential_endpoint]]
                for j in range(table.t):
                    sha_output = SHA256.new(bytes(chain[j], 'utf-8')).hexdigest()
                    reduced = reduction_function(sha_output, j)
                    if reduced == reduced_ciphertext:
                        return false_alarm_check(ciphertext, chain[-1])

                    chain.append(reduced)

            chain.append(potential_endpoint)

    return None


def false_alarm_check(ciphertext, plain_text_candidate):
    if SHA256.new(bytes(plain_text_candidate, 'utf-8')).hexdigest() == ciphertext:
        return plain_text_candidate
    else:
        print('False alarm!', plain_text_candidate)
        return None


def rainbow_tables_attack(ciphertext, table):
    print('Cracking ciphertext', ciphertext, 'with a Rainbow table with m:', str(table.m) + ', t:', str(table.t) + '.')
    reduced_ciphertext = reduction_function(ciphertext)
    for endpoint in table.table_dict:
        # checking if an endpoint matches reduced ciphertext
        if endpoint == reduced_ciphertext:
            print('Found a matching endpoint.')
            plaintext = browse_rainbow_chain(ciphertext, reduced_ciphertext, table, endpoint)
            if plaintext is not None:
                return plaintext

    # none of the endpoints matched. start iteratively transforming ciphertext to one of potential endpoints
    plaintext = browse_rainbow_chain(ciphertext, reduced_ciphertext, table, 0)
    if plaintext is not None:
        return plaintext

    return None


if __name__ == '__main__':
    cipher_texts = generate_ciphertexts()
    successes = 0

    # ------------------------------------------------ HELLMAN TABLES ------------------------------------------------ #
    print('Generating Hellman tables.')
    rt = generate_rainbow_table(100, 100)
    #rt2 = generate_rainbow_table(100, 10000)
    #rt3 = generate_rainbow_table(10000, 100)
    rt_arr = [rt]#, rt2, rt3]

    print('Starting attack using Rainbow tables.')
    for r_table in rt_arr:
        print('\nCracking ciphertexts with a Rainbow table with m:', str(r_table.m) + ', t:', str(r_table.t) + '.')
        start_t = time()
        nth_ciphertext = 1
        for c in cipher_texts:
            print(str(nth_ciphertext) + ': ', end='')
            result = rainbow_tables_attack(c, r_table)
            if result:
                successes += 1
                print('Ciphertext cracked successfully. The plaintext for the given hash', c, 'was', result)
            else:
                print('Failed')

            nth_ciphertext += 1
        end_t = time()

        percentage_success = str(successes / len(cipher_texts) * 100)
        print('Rainbow table method cracked', successes, 'out of', len(cipher_texts), 'ciphertexts ('
              + percentage_success + '%).')
        print('Duration: ' + str(end_t - start_t) + 's.')
        successes = 0
