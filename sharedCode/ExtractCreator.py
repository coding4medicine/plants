#Copyright 2024: Addy Veerendra
#Released under MIT License

from Bio import SeqIO
import glob

# Define orders and genera
orders = {"Lamiales"}
genera = {"Primulina"}

# File paths
phylogeny_file_path = "/share/phylogeny.txt"
names_file_path = "/share/names.txt"
results_file_path = "/home/umaveerendra/pgr-tk/Lamiales.txt"
output_file_path = "/home/umaveerendra/pgr-tk/NewExtract.fa"

# Collect plastid files
plastid_files = glob.glob('share/genomes/*.fna')

# Load the species IDs from names.txt
with open(names_file_path, 'r') as names_file:
    species_ids = {line.strip().lower() for line in names_file}

'''
First part: Find all species of the specified order and write to the results file.
'''
# Open the file to write results in
with open(results_file_path, 'w') as results_file:
    # Open the phylogeny file
    with open(phylogeny_file_path) as phylogeny:
        # Access each line
        for line in phylogeny:
            line = line.strip()
            # Split the line into Count and the rest
            parts = line.split(maxsplit=2)
            if len(parts) < 3:
                continue  # Skip lines that don't have all three parts
            count, genus, phylogeny_info = parts
            # Access each order
            for order in orders:
                # Check if the order is in the phylogeny_info
                if order.lower() in phylogeny_info.lower():
                    genus_from_phylogeny = phylogeny_info.split('|')[0].split()[0]
                    for species_id in species_ids:
                        Genus_ID = species_id.split()[1]
                        if genus_from_phylogeny.lower() == Genus_ID.lower():
                            # Write the species ID to the results file
                            results_file.write(species_id + '\n')
                            print(species_id)

'''
Second part: Extract sequences for specified genera and write to a FASTA file.
'''
# Read the species IDs from the results file
with open(results_file_path, 'r') as results_file:
    filtered_species_ids = {line.strip().lower() for line in results_file}

# Open the output file to write the extracted sequences
with open(output_file_path, 'w') as extract_file:
    # Access each plastid file
    for plastid_file in plastid_files:
        # Open the plastid file and check each record
        for seq_record in SeqIO.parse(plastid_file, "fasta"):
            description = seq_record.description.lower()
            # Check if the species ID is in the filtered species IDs
            if any(species_id in description for species_id in filtered_species_ids):
                # Check if the genus is one of the specified genera
                if any(genus.lower() in description for genus in genera):
                    # Modify the description to include only the species name
                    # Assuming the species name is the first two words after the genus name
                    description_parts = seq_record.description.split()
                    # Find the index of the genus in the description
                    genus_index = next((i for i, part in enumerate(description_parts) if part.lower() in genera), None)
                    # Extract the species ID and name
                    species_id = description_parts[0]
                    species_name = " ".join(description_parts[genus_index:genus_index + 3])
                    # Join the ID and the name
                    joined_description = f"{species_id}_{species_name}"
                    # Update the seq_record's description
                    seq_record.description = joined_description
                    # Write the sequence to the output file
                    SeqIO.write(seq_record, extract_file, "fasta")
                    # Optionally, print the modified description of the sequence
                    print(seq_record.description)