# Define the output filenames
output_filenames = ['encfile1.txt', 'encfile2.txt', 'encfile3.txt', 'encfile4.txt']  # Input files
reconstructed_filename = 'reconstructed_lines.txt'  # Output file for reconstructed lines

# Initialize a list to hold lines
lines = []

# Read lines from each output file
for filename in output_filenames:
    with open(filename, 'r') as file:
        lines.append(file.readlines())  # Append the lines from each file

# Reconstruct the original order of lines
original_lines = []
max_length = max(len(group) for group in lines)  # Find the longest list of lines

# Interleave lines from each group based on their original order
for i in range(max_length):
    for j in range(len(lines)):
        if i < len(lines[j]):  # Check if the current index is valid
            original_lines.append(lines[j][i].strip())  # Add line, stripping whitespace

# Write the reconstructed lines to a new file
with open(reconstructed_filename, 'w') as reconstructed_file:
    for line in original_lines:
        reconstructed_file.write(line + '\n')

# Output confirmation
print(f"Original lines reconstructed and saved to {reconstructed_filename}.")
