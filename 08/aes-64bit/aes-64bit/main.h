//
//  main.h
//  aes-64bit
//
//  Created by Peter Čuřík Jr. on 28/11/2021.
//

#ifndef main_h
#define main_h
uint64_t addRoundKey(uint64_t key, uint64_t block);
uint64_t subBytes(uint64_t block, int mode);
uint64_t shiftRows(uint64_t block, int mode);
uint64_t mixColumns(uint64_t block, int mode);
uint64_t AESencrypt(uint64_t block);
uint64_t AESdecrypt(uint64_t block);
#endif /* main_h */
