from consts import INPUT_FILE_PATH, COMPRESSED_FILE_PATH, DECOMPRESSED_FILE_PATH
from lz77_encoding import LZ77
from huffman_encoding import HuffmanCoding

print('Compressing using Lempel-Ziv77')
lz77 = LZ77(INPUT_FILE_PATH, COMPRESSED_FILE_PATH, DECOMPRESSED_FILE_PATH)
# Compress the file
lz77.compress_file()
# Decompress the file
lz77.decompress_file()
print('Compressing using HuffmanCoding')
huffman = HuffmanCoding(INPUT_FILE_PATH, COMPRESSED_FILE_PATH, DECOMPRESSED_FILE_PATH)
# Compression
huffman_code = huffman.compress()
# Decompression
huffman.decompress(huffman_code)
