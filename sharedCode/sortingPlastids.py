#Copyright: Aditya Vinukonda
#released under MIT license

from Bio import SeqIO
import glob



genera = set([])
orders = {}
sequences = []

#create a set with all the names of the genera
plastids = glob.glob("/share/genomes/*.fna")
for plastid in plastids:

        for seq in SeqIO.parse(plastid, "fasta"):
                l = list(seq.description.split())
                genera.add(l[1])
#function to find the orders of the genera
def findOrder(genus):
        order = ''
        with open("/share/phylogeny.txt","r") as file:
                for line in file:
                        parts = line.strip().split("\t")
                        if parts[1].lower() == genus.lower():
                                parts = parts[2].split("|")
                                flag = False
                                temp = ""
                                for part in parts:
                                        if part[-5:] == "aceae":
                                                flag = True
                                        if part[-5:] != "aceae" and flag == True:
                                                order += part
                                                break
        return order
#sorting the orders and genera in a dictionary
for genus in genera:
        order = findOrder(genus.lower()).lower()
        if order in orders:
                orders[order].append(genus.lower())
        elif order not in orders:
                orders[order] = [genus.lower()]

key = "ericales"
print(orders[key])
for plastid in plastids:
        for seq in SeqIO.parse(plastid,"fasta"):
                for genus in orders[key]:
                        if genus in seq.description.lower():
                                sequences.append(seq)
file_path = key + ".fasta"
with open(file_path, 'w') as file:
        r = SeqIO.write(sequences, file, 'fasta')

