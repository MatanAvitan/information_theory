import zlib
import time
import os
from consts import INPUT_FILE_PATH, COMPRESSED_FILE_PATH, DECOMPRESSED_FILE_PATH

class LZ77(object):
    def __init__(self, input_file_path, 
                 compressed_file_path, decompressed_file_path):
        self.input_file_path = input_file_path
        self.compressed_file_path = compressed_file_path
        self.decompressed_file_path = decompressed_file_path
    
    def compress_file(self):
        start_time = time.time()
        with open(self.input_file_path, 'rb') as file:
            data = file.read()
            compressed_data = zlib.compress(data)

        with open(self.compressed_file_path, 'wb') as file:
            file.write(compressed_data)

        end_time = time.time()
        compression_time = end_time - start_time
        original_size = os.path.getsize(self.input_file_path) / 1e6
        compressed_size = os.path.getsize(self.compressed_file_path) / 1e6

        print(f"Original size: {original_size} megabytes")
        print(f"Compressed size: {compressed_size} megabyte")
        print(f"Compression ratio: {original_size / compressed_size:.2f}")
        print(f"Compression time: {compression_time:.4f} seconds")


    def decompress_file(self):
        start_time = time.time()
        with open(self.compressed_file_path, 'rb') as file:
            compressed_data = file.read()
            data = zlib.decompress(compressed_data)

        with open(self.decompressed_file_path, 'wb') as file:
            file.write(data)

        end_time = time.time()
        decompression_time = end_time - start_time

        print(f"Decompression time: {decompression_time:.4f} seconds")

lz77 = LZ77(INPUT_FILE_PATH, COMPRESSED_FILE_PATH, DECOMPRESSED_FILE_PATH)
# Compress the file
lz77.compress_file()
# Decompress the file
lz77.decompress_file()

