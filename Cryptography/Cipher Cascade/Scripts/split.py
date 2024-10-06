# Define the filename
input_filename = 'clear.txt'  # Input file name
output_filenames = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']  # Output files

# Initialize lists for each file
file_lines = [[] for _ in range(4)]  # Create a list of lists for four files

# Read lines from the input file
with open(input_filename, 'r') as file:
    lines = file.readlines()  # Read all lines into a list

# Distribute lines into four files based on their indices
for index, line in enumerate(lines):
    file_index = index % 4  # Determine which file to assign the line
    file_lines[file_index].append(line.strip())  # Strip whitespace and add to the correct list

# Write lines to each corresponding output file
for i in range(4):
    with open(output_filenames[i], 'w') as output_file:
        for line in file_lines[i]:
            output_file.write(line + '\n')

# Output confirmation
for i in range(4):
    print(f"Lines saved to {output_filenames[i]}.")
