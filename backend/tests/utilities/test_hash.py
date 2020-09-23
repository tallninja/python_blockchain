from backend.utilities.hash import Hash

def test_hash():
    #checks if the hash is the same regardless of the order of the data

    order_1_hash = str(Hash.hash("one", 2, [3]))
    order_2_hash = str(Hash.hash(2, "one", [3]))
    assert order_1_hash == order_2_hash

    #Asserts that the hash is an instace of the Block class
    hash = Hash.hash("foo")
    assert isinstance(hash, Hash)

    #Asserts that the hashing algorithm is correct 
    assert str(Hash.hash("foo")) == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'