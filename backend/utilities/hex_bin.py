from backend.utilities.hash import Hash


HEX_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111',
}


def hex_to_bin(hex_string):
    bin_string = ''
    for character in hex_string:
        bin = HEX_TABLE[character]
        bin_string += bin
    
    return bin_string

def main():
    test_number = 7323
    test_number_hex = hex(test_number)[2:]
    test_number_hex_bin = hex_to_bin(test_number_hex)
    original_number = int(test_number_hex_bin, 2)

    print(f"test_number: {test_number}")
    print(f"test_number_hex: {test_number_hex}")
    print(f"test_number_hex_bin: {test_number_hex_bin}")
    print(f"original_number: {original_number}\n\n")

    test_data = "foo-bar"
    test_data_hex = str(Hash.hash(test_data))
    test_data_bin = hex_to_bin(test_data_hex)

    print(f"test_data: {test_data}")
    print(f"test_data_hex: {test_data_hex}")
    print(f"test_data_bin: {test_data_bin}\n\n")



if __name__ == '__main__':
    main()