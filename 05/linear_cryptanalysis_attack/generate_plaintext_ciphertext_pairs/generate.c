//
//  generate.c
//  generate_plaintext_ciphertext_pairs
//
//  Created by Peter Čuřík Jr. on 24/10/2021.
//

#include <stdio.h>
#include <stdint.h>

#define CIPHER_ROUNDS 4
#define ALL_PLAINTEXTS (1<<13)

int sbox[16] = {0x8, 0xC, 0xB, 0x3, 0x7, 0x9, 0x1, 0x4, 0xE, 0x6, 0x0, 0xD, 0x2, 0xF, 0x5, 0xA};

uint16_t apply_permutation(uint16_t before_perm) {
    // ukazka na konkretnom priklade pre pochopenie:
    // nech 1101 0010 1011 1001 je vystup z s-boxu pripraveny na permutaciu
    // potom je s bitmi narabane nasledovne:
    
    uint16_t a1 = (before_perm >> 12) & 0xf;        // 0000 0000 0000 1101 - prva stvorica bitov vstupu
    uint16_t a2 = (before_perm >>  8) & 0xf;        // 0000 0000 0000 0010 - druha stvorica bitov vstupu
    uint16_t a3 = (before_perm >>  4) & 0xf;        // 0000 0000 0000 1101 - tretia stvorica bitov vstupu
    uint16_t a4 = (before_perm >>  0) & 0xf;        // 0000 0000 0000 1001 - posledna stvorica bitov vstupu
    
    uint16_t perm_output1 =                         // 0000 0000 0000 1011 - prva stvorica bitov po aplikovani permutacie
    ((a1 & 0x8) << 0)   >> 0
    ^ ((a2 & 0x8) << 0) >> 1
    ^ ((a3 & 0x8) << 0) >> 2
    ^ ((a4 & 0x8) << 0) >> 3;
    
    uint16_t perm_output2 =                         // 0000 0000 0000 1000 - druha stvorica bitov po aplikovani permutacie
    ((a1 & 0x4) << 1)   >> 0
    ^ ((a2 & 0x4) << 1) >> 1
    ^ ((a3 & 0x4) << 1) >> 2
    ^ ((a4 & 0x4) << 1) >> 3;
    
    uint16_t perm_output3 =                         // 0000 0000 0000 0110 - tretia stvorica bitov po aplikovani permutacie
    ((a1 & 0x2) << 2)   >> 0
    ^ ((a2 & 0x2) << 2) >> 1
    ^ ((a3 & 0x2) << 2) >> 2
    ^ ((a4 & 0x2) << 2) >> 3;
    
    uint16_t perm_output4 =                         // 0000 0000 0000 1011 - posledna stvorica bitov po aplikovani permutacie
    ((a1 & 0x1) << 3)   >> 0
    ^ ((a2 & 0x1) << 3) >> 1
    ^ ((a3 & 0x1) << 3) >> 2
    ^ ((a4 & 0x1) << 3) >> 3;
    
    return (perm_output1 << 12)                     // 1011 1000 0110 1011 - vystup z permutacie merge-nuty dokopy do 16bit
    ^ (perm_output2 << 8)
    ^ (perm_output3 << 4)
    ^ (perm_output4);
}

uint16_t apply_sboxes(uint16_t state) {
    uint16_t last4bit_extractor = 0xf;
    
    return
      (sbox[(state >>  0) & last4bit_extractor] << 0)
    ^ (sbox[(state >>  4) & last4bit_extractor] << 4)
    ^ (sbox[(state >>  8) & last4bit_extractor] << 8)
    ^ (sbox[(state >> 12) & last4bit_extractor] << 12);
}

uint16_t apply_key_xor(uint16_t plaintext, uint16_t round_key) {
    return plaintext ^ round_key;
}

uint16_t SPN_encrypt(uint16_t plaintext, uint32_t key) {
    uint16_t state = plaintext, round_key;
    
    for(int r = 0; r < CIPHER_ROUNDS; r++) {
        round_key = key << (CIPHER_ROUNDS * r) >> 16;
        state = apply_key_xor(state, round_key);
        state = apply_sboxes(state);
        
        if(r == 3) {
            round_key = key << (CIPHER_ROUNDS * (r + 1)) >> 16;
            state = apply_key_xor(state, round_key);
        }
        else {
            state = apply_permutation(state);
        }
    }
    
    return state;
}

int main(int argc, const char * argv[]) {
    uint32_t key = 0xC825881F;
    uint16_t ciphertext;
    FILE *p_c_pairs = fopen("p_c_pairs.txt", "w");
    
    for(uint16_t plaintext = 0; plaintext < ALL_PLAINTEXTS; plaintext++) {
        ciphertext = SPN_encrypt(plaintext, key);
        fprintf(p_c_pairs, "%x\n", plaintext);
        fprintf(p_c_pairs, "%x\n", ciphertext);
        printf("%x : %x\n", plaintext, ciphertext);
    }
    
    return 0;
}

