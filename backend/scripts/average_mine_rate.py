import time

from backend.blockchain.blockchain import Blockchain
from backend.config import TIME_S

blockchain = Blockchain()
times = []

for i in range(1000):
    start_time = time.time_ns() / TIME_S
    blockchain.add_block(i)
    end_time = time.time_ns() / TIME_S

    mine_time = end_time - start_time

    times.append(mine_time)
    average_time = sum(times) / len(times)

    print(f"Block No: {i}")
    print(f"last_block_difficulty: {blockchain.chain[-1].difficulty}")
    print(f"last_block_nonce: {blockchain.chain[-1].nonce}")
    print(f"last_block_hash: {blockchain.chain[-1].hash}")
    print(f"Time to mine block: {mine_time} seconds")
    print(f"Average_time: {average_time} seconds\n\n")
    
