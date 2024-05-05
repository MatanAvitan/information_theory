import os
import heapq
from collections import Counter
from bitarray import bitarray  # Install this package using 'pip install bitarray'
import time
from consts import ENCODING_SAMPLE_PATH, COMPRESSED_FILE_PATH

class HuffmanCoding(object):
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        
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
        with open(self.input_file_path, 'r') as file:
            text = file.read()
            frequency = Counter(text)

        huffman_tree = self.build_huffman_tree(frequency)
        huffman_code = {symbol: code for symbol, code in huffman_tree}
        binary_string = ''.join(huffman_code[symbol] for symbol in text)
        compressed = bitarray(binary_string)

        with open(self.output_file_path, 'wb') as file:
            compressed.tofile(file)

        return frequency, huffman_code, len(text.encode('utf-8')) * 8  # Returning the original size in bits

    def decompress(self):
        with open(self.input_file_path, 'rb') as file:
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

        with open(self.output_file_path, 'w') as file:
            file.write(decompressed_text)

# Example usage
huffman = HuffmanCoding()
input_text_file = 
compressed_file = '/Users/yoavkatzav/Desktop/MSc Mathematics & Data Science/Semester A 2024/information theory/compressed.bin'  # Replace with your compressed file path
decompressed_file = '/Users/yoavkatzav/Desktop/MSc Mathematics & Data Science/Semester A 2024/information theory/decompressed.txt'  # Replace with your output file path

huffman = HuffmanCoding()

# Measure compression time
start_time = time.time()
frequency, huffman_code, original_size = huffman.compress(input_text_file, compressed_file)
end_time = time.time()
compression_time = end_time - start_time
print(f"Compression completed in {compression_time:.4f} seconds")

# Measure decompression time
start_time = time.time()
huffman.decompress(compressed_file, decompressed_file, huffman_code)
end_time = time.time()
decompression_time = end_time - start_time
print(f"Decompression completed in {decompression_time:.4f} seconds")

# Displaying metrics
compressed_size = os.path.getsize(compressed_file) * 8  # Size in bits
print(f"Original size: {original_size} bits")
print(f"Compressed size: {compressed_size} bits")
print(f"Compression ratio: {original_size / compressed_size:.2f}")
