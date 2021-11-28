//
//  square_attack.c
//  aes-64bit
//
//  Created by Peter Čuřík Jr. on 28/11/2021.
//

#include <stdio.h>
#include <stdlib.h>

#include "square_attack.h"
#include "main.h"

#define LAMBDASETSIZE 16
#define ROUNDS 4

typedef struct PotentialKey {
    uint64_t val;
    int isPotential;
    int occurrance;
} PotentialKey;

uint64_t plaintextSet[LAMBDASETSIZE] = {};
uint64_t ciphertextSet[LAMBDASETSIZE] = {};

PotentialKey potentialKeyNibbles[LAMBDASETSIZE] = {};

uint64_t keys[ROUNDS] = {};
const uint16_t reverse_rcon[ROUNDS] = {0x0800, 0x0400, 0x0200, 0x0100};
const uint8_t key_sbox[16] = {0x8, 0xC, 0xB, 0x3, 0x7, 0x9, 0x1, 0x4, 0xE, 0x6, 0x0, 0xD, 0x2, 0xF, 0x5, 0xA};

void generatePCset(int lambdaSetNibblePosition) {
    int shift = lambdaSetNibblePosition * 4;
    uint64_t filter = 0xf;
    
    for(uint64_t i = 0; i < LAMBDASETSIZE; i++) {
        plaintextSet[i] = (uint64_t) ((i << shift) & (filter << shift));
        ciphertextSet[i] = AESencrypt(plaintextSet[i]);
    }
}

uint64_t zeroXor(uint64_t states[]) {
    uint64_t xor = 0;
    uint64_t filter = 0xf;
    for(int i = 0; i < LAMBDASETSIZE; i++) {
        uint64_t tmp = states[i];
        xor ^= (tmp & filter);
    }
    
    return xor;
}

void attackNibble(int i) {
    uint64_t filter = 0xf;
    uint64_t states[LAMBDASETSIZE] = {};
    
    // for each nibble, try all keys 0 .. f
    for(uint64_t keyNibble = 0; keyNibble <= 0xf; keyNibble++) {
        // for each key 0 .. f, decrypt the last AES round with all ciphertexts
        for(int ciphertext = 0; ciphertext < LAMBDASETSIZE; ciphertext++) {
            states[ciphertext] = addRoundKey(keyNibble, (ciphertextSet[ciphertext] & (filter << (i * 4))) >> (i * 4));
            states[ciphertext] = subBytes(states[ciphertext], 0);
        }
        
        if(zeroXor(states) == 0) {
            potentialKeyNibbles[keyNibble].isPotential = 1;
            potentialKeyNibbles[keyNibble].occurrance += 1;
            potentialKeyNibbles[keyNibble].val = keyNibble;
        }
    }
}

uint64_t buildSubkey(uint64_t key, uint64_t keyNibble, int i) {
    return key |= keyNibble << i * 4;
}

void clearPotentialKeyNibbles() {
    for(int k = 0; k < LAMBDASETSIZE; k++) {
        potentialKeyNibbles[k].isPotential = 0;
        potentialKeyNibbles[k].val = 0x0;
        potentialKeyNibbles[k].occurrance = 0;
    }
}

void initPotentialKeyNibbles() {
    for(int k = 0; k < LAMBDASETSIZE; k++) {
        PotentialKey keyCandidate;
        keyCandidate.occurrance = 0;
        keyCandidate.isPotential = 0;
        keyCandidate.val = 0x0;
        potentialKeyNibbles[k] = keyCandidate;
    }
}

uint64_t computeMasterKey(uint64_t lastRoundSubkey) {
    uint64_t currentKey = lastRoundSubkey;

    for(int i = 0; i < ROUNDS; i++) {
        uint16_t currentRoundKeyColumn4 = (currentKey >>  0) & 0xffff;
        uint16_t currentRoundKeyColumn3 = (currentKey >> 16) & 0xffff;
        uint16_t currentRoundKeyColumn2 = (currentKey >> 32) & 0xffff;
        uint16_t currentRoundKeyColumn1 = (currentKey >> 48) & 0xffff;

        uint16_t newRoundKeyColumn4 = currentRoundKeyColumn4 ^ currentRoundKeyColumn3;
        uint16_t newRoundKeyColumn3 = currentRoundKeyColumn3 ^ currentRoundKeyColumn2;
        uint16_t newRoundKeyColumn2 = currentRoundKeyColumn2 ^ currentRoundKeyColumn1;

        //RotWord
        uint16_t newRoundKeyColumn1 = ((newRoundKeyColumn4 >> 12) & 0xf) ^ (newRoundKeyColumn4 << 4);
        //SubBytes
        newRoundKeyColumn1 = (key_sbox[(newRoundKeyColumn1 >>  0) & 0xf] << 0)
        ^ (key_sbox[(newRoundKeyColumn1 >>  4) & 0xf] << 4)
        ^ (key_sbox[(newRoundKeyColumn1 >>  8) & 0xf] << 8)
        ^ (key_sbox[(newRoundKeyColumn1 >> 12) & 0xf] << 12);
        //XOR
        newRoundKeyColumn1 ^= currentRoundKeyColumn1 ^ reverse_rcon[i];

        keys[i] = ((uint64_t) newRoundKeyColumn4 << 0)
        ^ ((uint64_t) newRoundKeyColumn3 << 16)
        ^ ((uint64_t) newRoundKeyColumn2 << 32)
        ^ ((uint64_t) newRoundKeyColumn1 << 48);
        
        currentKey = keys[i];
    }

    return keys[ROUNDS-1];
}

uint64_t squareAttack() {
    int lambdaSetNibblePosition = 0;
    generatePCset(lambdaSetNibblePosition);
    initPotentialKeyNibbles();
    
    uint64_t key = 0;
    // attack nibble after nibble
    for(int i = 0; i < 16; i++) {
        attackNibble(i);
        
        int count = 0;
        PotentialKey correctKeyBytes;
        for(int k = 0; k < LAMBDASETSIZE; k++) {
            if(potentialKeyNibbles[k].isPotential == 1) {
                correctKeyBytes = potentialKeyNibbles[k];
                count++;
            }
        }
        
        if(count == 1) {
            key = buildSubkey(key, correctKeyBytes.val, i);
        }
        
        else {
            int highestOccurance = 1;
            int soloWinner = 0;
            int lambdaSetNibblePositionCopy = lambdaSetNibblePosition;
            
            while(soloWinner != 1) {
                generatePCset(++lambdaSetNibblePositionCopy);
                attackNibble(i);
                for(int k = 0; k < LAMBDASETSIZE; k++) {
                    if(potentialKeyNibbles[k].occurrance > 1) {
                        if(potentialKeyNibbles[k].occurrance > highestOccurance) {
                            highestOccurance = potentialKeyNibbles[k].occurrance;
                            soloWinner = 1;
                            correctKeyBytes = potentialKeyNibbles[k];
                        }
                        else if(potentialKeyNibbles[k].occurrance == highestOccurance){
                            soloWinner = 0;
                        }
                    }
                }
            }
            
            key = buildSubkey(key, correctKeyBytes.val, i);
            generatePCset(lambdaSetNibblePosition);
        }
        
        clearPotentialKeyNibbles();
    }
    
    return computeMasterKey(key);
}
