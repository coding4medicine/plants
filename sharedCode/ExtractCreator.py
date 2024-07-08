from Bio import SeqIO
import glob

# Define orders and genera
orders = {"lamiales"}
genera = {"scrophularia", "schrebera", "lavandula"}

# File paths
phylogeny_file_path = "/share/phylogeny.txt" # Add a backslash before the file path if running on the server
names_file_path = "/share/names.txt" # Add a backslash before the file path if running on the server
results_file_path = "Lamiales.txt" # Change accordingly
output_file_path = "NewExtract.fa" # Change accordingly

# Collect plastid files
plastid_files = glob.glob('/share/genomes/*.fna')

# Load the species IDs from names.txt
with open(names_file_path, 'r') as names_file:
    species_ids = {line.strip().lower() for line in names_file}
'''
First part: Find all species of the specified order, and write to the results file.
'''
# Open the file to write results in
with open(results_file_path, 'w') as results_file:
    # Open the phylogeny file
    with open(phylogeny_file_path) as phylogeny:
        # Access each line
        for line in phylogeny:
            # Split the line into Count, Genus, and Phylogeny
            words = line.lower().split()
            # Access each "word"
            for word in words:
                # Access each order
                for order in orders:
                    # Check if the order is in the "word"
                    if order in word:
                        # Split the phylogeny, and retrieve the first part (genus)
                        genus = word.split('|')[0]
                        # Access each species ID
                        for species_id in species_ids:
                            # Check if the genus is in the species ID
                            if genus in species_id:
                                # Write the species ID to the results file
                                results_file.write(species_id + '\n')
'''
Second part: Extract sequences for specified genera and write to a FASTA file.
'''
# Open the output file to write the extracted sequences
with open(output_file_path, 'w') as extract_file:
    # Access each genus
    for genus in genera:
        # Access each plastid file
        for plastid_file in plastid_files:
            # Open the plastid file
            for seq_record in SeqIO.parse(plastid_file, "fasta"):
                # Check if the genus is found in the sequence description
                if genus.lower() in seq_record.description.lower():
                    # Write the sequence to the output file
                    SeqIO.write(seq_record, extract_file, "fasta")
                    # Print the description of the sequence (Optional)
                    print(seq_record.description)
