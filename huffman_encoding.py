import os
import heapq
from collections import Counter
from bitarray import bitarray  # This requires 'pip install bitarray'
import time
from consts import INPUT_FILE_PATH, COMPRESSED_FILE_PATH, DECOMPRESSED_FILE_PATH

class HuffmanCoding:
    def __init__(self, input_file_path, 
                 compressed_file_path, decompressed_file_path):
        self.input_file_path = input_file_path
        self.compressed_file_path = compressed_file_path
        self.decompressed_file_path = decompressed_file_path

    def build_huffman_tree(self, frequency):
        heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            low = heapq.heappop(heap)
            high = heapq.heappop(heap)
            for pair in low[1:]:
                pair[1] = '0' + pair[1]
            for pair in high[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])
        return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

    def compress(self):
        start_time = time.time()
        with open(self.input_file_path, 'r', encoding='utf-8', errors='replace') as file:
            text = file.read()
            frequency = Counter(text)
        huffman_tree = self.build_huffman_tree(frequency)
        huffman_code = {symbol: code for symbol, code in huffman_tree}
        binary_string = ''.join(huffman_code[symbol] for symbol in text)
        compressed = bitarray(binary_string)   
        with open(self.compressed_file_path, 'wb') as file:
            compressed.tofile(file) 
        end_time = time.time()

        # Calculate sizes in megabytes and print
        original_size = os.path.getsize(self.input_file_path) / 1024**2
        compressed_size = os.path.getsize(self.compressed_file_path) / 1024**2
        compression_time = end_time - start_time
        compression_ratio = original_size / compressed_size

        print(f"Original size: {original_size:.2f} megabytes")
        print(f"Compressed size: {compressed_size:.2f} megabytes")
        print(f"Compression ratio: {compression_ratio:.2f}")
        print(f"Compression time: {compression_time:.4f} seconds")
        return huffman_code

    def decompress(self, huffman_code):
        start_time = time.time()
        with open(self.compressed_file_path, 'rb') as file:
            compressed = bitarray()
            compressed.fromfile(file) 
        reverse_huffman_code = {v: k for k, v in huffman_code.items()}
        binary_string = compressed.to01()
        current_code = ""
        decompressed_text = ""
        
        for digit in binary_string:
            current_code += digit
            if current_code in reverse_huffman_code:
                character = reverse_huffman_code[current_code]
                decompressed_text += character
                current_code = ""
        
        with open(self.decompressed_file_path, 'w') as file:
            file.write(decompressed_text)
        end_time = time.time()
        decompression_time = end_time - start_time
        print(f"Decompression time: {decompression_time:.4f} seconds")

# Example usage
huffman = HuffmanCoding(INPUT_FILE_PATH, COMPRESSED_FILE_PATH, DECOMPRESSED_FILE_PATH)
# Compression
huffman_code = huffman.compress()
# Decompression
huffman.decompress(huffman_code)
