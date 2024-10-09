# extract.py

# Define the correct magic bytes
correct_magic_bytes = bytes.fromhex("DC 41 22 FF")

# Read the corrupted binary file
with open('original.bin', 'rb') as f:
    data = f.read()

# Check magic bytes
if data[:4] != correct_magic_bytes:
    print("Magic bytes do not match. The file may be corrupted.")
else:
    # Skip magic bytes
    obfuscated_data = data[4:]

    # Assuming the last part of the data is the obfuscated flag, we will recover it.
    # Use the length of the original flag to extract the obfuscated part.
    original_flag_length = 41  # Adjust this based on your known flag length
    obfuscated_flag = obfuscated_data[-original_flag_length:]

    # XOR key for deobfuscation
    xor_key = b'minersreachtownhall'

    # Recover the original flag using XOR
    recovered_flag = bytes([b ^ xor_key[i % len(xor_key)] for i, b in enumerate(obfuscated_flag)])

    # Print the recovered flag
    print("Recovered Flag:", recovered_flag.decode('utf-8', errors='ignore'))
