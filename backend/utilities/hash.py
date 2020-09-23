import hashlib
import json

class Hash:
    """
    This will be used to generate the hashes of our blocks using sha 256 algorithim
    """

    def __init__(self, data, hash): #takes multiple arguments 
        self.data = data #stringifies the data so that it can be hashed since encoding does not work on integer data types
        self.hash = hash


    def __repr__(self):
        return f'{self.hash}'

    
    @staticmethod
    def hash(*args):
        stringified_data = sorted(map(lambda data: json.dumps(data), args)) #stringifies all items in the list of arguments
        joined_data = "".join(stringified_data)
        hashed_data = hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

        return Hash(joined_data, hashed_data)



    
def main():
    print(f'{Hash.hash("one", 2, [3])}')
    print(f'{Hash.hash(2, "one", [3])}')


if __name__ == '__main__':
    main()
