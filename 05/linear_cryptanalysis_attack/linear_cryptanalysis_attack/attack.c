//
//  attack.c
//  linear_cryptanalysis_attack
//
//  Created by Peter Čuřík Jr. on 24/10/2021.
//

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#define ALL_LAST_ROUND_SUB_KEYS (1<<8)
#define ALL_P_C_PAIRS (1<<13)

typedef struct _keydata {
    uint8_t key;
    int count;
    double bias;
} keydata;

int inverse_sbox[16] = {0xA, 0x6, 0xC, 0x3, 0x7, 0xE, 0x9, 0x4, 0x0, 0x5, 0xF, 0x2, 0x1, 0xB, 0x8, 0xD};

uint8_t apply_inverse_sboxes(uint8_t state) {
    uint8_t last4bit_extractor = 0xf;
    
    return
      (inverse_sbox[(state >>  0) & last4bit_extractor] << 0)
    ^ (inverse_sbox[(state >>  4) & last4bit_extractor] << 4);
}

uint8_t apply_key_xor(uint8_t ciphertext, uint8_t last_round_subkey) {
    return ciphertext ^ last_round_subkey;
}

int linear_approximation_attack(uint16_t plaintext, uint16_t ciphertext, uint8_t last_round_subkey) {
    uint8_t state = 0x0;
    uint8_t ciphertext_extracted = (ciphertext >> 4) & 0xff;
    uint8_t plaintext_extracted = (plaintext >> 5) & 0x7;
    
    state = apply_key_xor(ciphertext_extracted, last_round_subkey);
    state = apply_inverse_sboxes(state);
    
    int result = 0;
    state = state & 0x66;
    while(state) {
        result ^= state & 0x1;
        state >>= 1;
    }
    
    while(plaintext_extracted) {
        result ^= plaintext_extracted & 0x1;
        plaintext_extracted >>= 1;
    }
    
    if(result == 0) {
        return 1;
    }
    else {
        return 0;
    }
}

int main(int argc, const char * argv[]) {
    FILE *p_c_pairs = fopen("p_c_pairs.txt", "r");
    FILE *keytable_output = fopen("keytableoutput.txt", "w");
    char buffer[255];
    keydata keytable[ALL_LAST_ROUND_SUB_KEYS];
    
    // init keytable
    for(uint16_t i = 0; i < ALL_LAST_ROUND_SUB_KEYS; i++) {
        keytable[i].key = (uint8_t) i;
        keytable[i].count = 0;
        keytable[i].bias = 0.0;
    }
    
    while(fgets(buffer, 255, p_c_pairs)) {
        uint16_t plaintext = strtol(buffer, NULL, 16);
        fgets(buffer, 255, p_c_pairs);
        uint16_t ciphertext = strtol(buffer, NULL, 16);
        
        for(uint16_t k = 0; k < ALL_LAST_ROUND_SUB_KEYS; k++) {
            keytable[k].count += linear_approximation_attack(plaintext, ciphertext, (uint8_t) k);
        }
    }
    
    for(uint16_t i = 0; i < ALL_LAST_ROUND_SUB_KEYS; i++) {
        double tmp = keytable[i].count - (ALL_P_C_PAIRS / 2);
        keytable[i].bias = fabs(tmp) / ALL_P_C_PAIRS;
        printf("%2X: %f\n", keytable[i].key, keytable[i].bias);
        fprintf(keytable_output, "%f\n", keytable[i].bias);
    }
        
    return 0;
}

