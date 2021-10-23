//
//  main.c
//  lfsr
//
//  Created by Peter Čuřík Jr. on 10/10/2021.
//
//  using polynomial x^32 + x^22 + x^2 + x^1 + 1
//  file output adjusted to fit PARANOYA statistical tests

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

unsigned char buffer = 0;
unsigned count = 0;

unsigned int numexperiments = 100;
unsigned int registersize = 32;
unsigned char LFSR_register[32];

void writeFile(unsigned char bit, FILE *file) {
    buffer <<= 1;
    
    if(bit == 1) {
        buffer |= 1;
    }
    
    count++;
    if(count == 8) {
        fwrite(&buffer, sizeof(buffer), 1, file);
        buffer = 0;
        count = 0;
    }
}

void printLFSR() {
    printf("LFSR: ");
    for(int j = 0; j < registersize; j++) {
        printf("%i ", LFSR_register[j]);
    }
    printf("\n");
}

int main(int argc, const char * argv[]) {
    srand((unsigned int) time(NULL));
    
    // which indexes in LFSR to xor according to polynomial
    unsigned int polynomial[4] = {
        (registersize - 1) - 0,
        (registersize - 1) - 1,
        (registersize - 1) - 2,
        (registersize - 1) - 22
    };
    
    //create files
    FILE *f[numexperiments];
    
    // generate 100 pseudorandom LFSR sequences
    for(int i = 0; i < numexperiments; i++) {
        
        char filename[20];
        sprintf(filename, "data%i.dat", i);
        f[i] = fopen(filename, "wb");
        
        // generate a random LFSR before i-th experiment
        LFSR_register[0] = 1;
        LFSR_register[registersize - 1] = 1;
        for(int j = 1; j < registersize - 1; j++) {
            LFSR_register[j] = rand() % 2;
        }
        
        printf("Initial ");
        printLFSR();
        
        // 8 000 000 bits = 1MB
        for(int j = 0; j < 80000000; j++) {
            unsigned int new_LFSR_bit = LFSR_register[polynomial[0]];
            
            // xor all bits together
            for(int k = 1; k < sizeof(polynomial) / sizeof(polynomial[0]); k++) {
                new_LFSR_bit ^= LFSR_register[polynomial[k]];
            }
            
            // write the last bit of LSFR to file before shifting the register
            writeFile(LFSR_register[registersize - 1], f[i]);
            
            // shift all elements in LFSR by one to the right
            for(int k = registersize - 1; k > 0; k--) {
                LFSR_register[k] = LFSR_register[k - 1];
            }
            LFSR_register[0] = new_LFSR_bit;
        }
        
        fclose(f[i]);
        printf("Sequence %3i: \t completed.\n", (i + 1));
    }
    
    return 0;
}
