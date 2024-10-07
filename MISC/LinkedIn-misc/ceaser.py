# Caesar Cipher Implementation for Paired Keys and Input Lines

def caesar_cipher(text, key):
    """
    Applies Caesar cipher to the input text using the given key.
    
    Parameters:
        text (str): The text to be encrypted.
        key (int): The shift key for the cipher.
    
    Returns:
        str: The encrypted text.
    """
    shifted_text = []
    
    for char in text:
        if char.isupper():
            # Shift uppercase letters
            shifted_char = chr((ord(char) - 65 + key) % 26 + 65)
            shifted_text.append(shifted_char)
        elif char.islower():
            # Shift lowercase letters
            shifted_char = chr((ord(char) - 97 + key) % 26 + 97)
            shifted_text.append(shifted_char)
        else:
            # Non-alphabetic characters remain unchanged
            shifted_text.append(char)
    
    return ''.join(shifted_text)

# List of keys to apply
keys = [1, 2, 4, 6, 7, 9, 10, 13, 15, 16, 18, 20, 21, 24, 25]

# Input URLs
input_lines = [
    	"youtu.be/j5a0jTc9S10?si=ACem-x3IpDsBioGq",
	"youtu.be/dQw4w9WgXcQ?si=qk5inKuwXPVMFhaM",
	"youtu.be/ub82Xb1C8os?si=Rnau1gl7Lzj1qv_t",
	"youtu.be/oHg5SJYRHA0?si=FHfgxDwbsE2k1O1a",
	"youtu.be/cvh0nX08nRw?si=FOX3pcQXPkymuXx0",
	"youtu.be/8ybW48rKBME?si=nez0bPagKTtXeK-H",
	"youtu.be/xbXoWRs2C8M?si=gymJDnlnX3H5bLi7",
	"youtu.be/0-16Z3GwNk4?si=hUTi3PHP4zDLynqT",
	"youtu.be/CttYJgr9vgQ?si=sP8JRo-joez8C0m-",
	"youtu.be/v7ScGV5128A?si=76rkWpP7KjMa0bS3",
	"youtu.be/xm3YgoEiEDc?si=Fo_A7mI4W-hpaJ5v",
	"youtu.be/oPLObjVAvIU?si=SN6eglt8b1ET4Kkn",
	"youtu.be/jvKCZ01ngcA?si=aXLKUuvCjz1d1xaT",
	"youtu.be/PrbgrxZMEOc?si=qRXUkDWU2eumcDqS",
	"youtu.be/-tMXNxmAO2k?si=kx_h1kIRg5JlL_Cx"
]
# Ensure the number of keys matches the number of input lines
if len(keys) != len(input_lines):
    print("Error: The number of keys does not match the number of input lines.")
else:
    # Apply Caesar cipher with corresponding key to each input line
    encrypted_lines = []
    for line, key in zip(input_lines, keys):
        encrypted_line = caesar_cipher(line, key)
        encrypted_lines.append(encrypted_line)
    
    # Print the encrypted URLs
    print("Encrypted URLs:\n")
    for idx, encrypted in enumerate(encrypted_lines, start=1):
        print(f"{idx}. {encrypted}")
