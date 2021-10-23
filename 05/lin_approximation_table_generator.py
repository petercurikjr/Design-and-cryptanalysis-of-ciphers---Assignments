sbox_input_binary = [
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 0],
    [1, 1, 0, 1],
    [1, 1, 1, 0],
    [1, 1, 1, 1]
]

# change this according to your S-box
sbox_output_binary = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 1, 1],
    [0, 0, 1, 1],
    [0, 1, 1, 1],
    [1, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 1, 0, 0],
    [1, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 0, 1, 0],
    [1, 1, 1, 1],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
]

linear_approximation_table = [[0 for i in range(16)] for j in range(16)]


def approximate_sbox(input_mask, output_mask):
    inputMaskToBinary = sbox_input_binary[input_mask]
    outputMaskToBinary = sbox_input_binary[output_mask]
    chosenBitsByMasks = []
    list_of_outputs = []

    # prejdi vsetkymi vstupmi Xi a vystupmi Yi
    for i in range(0xF + 1):
        # vyselektuj iba tie ktore urci maska
        for j in range(4):
            if inputMaskToBinary[j] == 1:
                chosenBitsByMasks.append(sbox_input_binary[i][j])
            if outputMaskToBinary[j] == 1:
                chosenBitsByMasks.append(sbox_output_binary[i][j])

        # v danej dvojici vstup/vystup vyselektovane bity zoxoruj a zapis vysledok
        output = 0
        if len(chosenBitsByMasks) > 1:
            for k in range(len(chosenBitsByMasks)):
                if k == 0:
                    output = chosenBitsByMasks[0] ^ chosenBitsByMasks[1]
                elif k > 1:
                    output ^= chosenBitsByMasks[k]

        else:
            output = chosenBitsByMasks[0]

        list_of_outputs.append(output)
        chosenBitsByMasks = []

    # vrat pocet nul - idealny vysledok (8)
    return list_of_outputs.count(0) - 8


if __name__ == '__main__':
    # input mask
    for i in range(0xF + 1):
        # output mask
        for j in range(0xF + 1):
            if i == 0 and j == 0:
                linear_approximation_table[i][j] = 8
                continue
            linear_approximation_table[i][j] = approximate_sbox(i, j)

    # pretty print the linear approximation table
    for i in range(len(linear_approximation_table)):
        for j in range(len(linear_approximation_table[0])):
            if linear_approximation_table[i][j] > 0:
                print('%+2i ' % linear_approximation_table[i][j], end='')
            else:
                print('%2i ' % linear_approximation_table[i][j], end='')
        print()


