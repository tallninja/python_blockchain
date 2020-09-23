from backend.utilities.hex_bin import hex_to_bin

def test_hex_to_bin():
    original_number = 7323
    original_number_hex = hex(original_number)[2:]
    original_number_bin = hex_to_bin(original_number_hex)

    assert int(original_number_bin, 2) == original_number