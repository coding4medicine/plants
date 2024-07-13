#Copyright: Aaron Beaver
#released  under  MIT license
#Note: this file is intended to be run on the Coding4Medicine Server
from Bio import SeqIO
import glob
user = input("input your username ")
output = input("What should the output .fa file be called? ")
phylogeny = "/share/phylogeny.txt"
plastids =glob.glob("/share/genomes/*.fna") 
##eventually will have an option to find genuses besed on ID
## will need a program that will return the ID of a genus to allow for more customized pgr-tk results
family = input("what family do you want to find")
def filter(family):
	with open("/home/"+user+"/"+output+".fa", "w") as out:

		for plastid in plastids:
			for seq in SeqIO.parse(plastid, "fasta"):
				sequenceList = list(seq.description.split())
				temp = findFamily(sequenceList[1])
				if temp.lower() == family:
					print("check")
					SeqIO.write(seq,out,"fasta")



	return(seq)
## Modified version of Hannah Beaver's findGenus function
def findFamily(genus):
	family = ""
	tag = False
	with open(phylogeny, "r") as phylo:
		for line in phylo:
			tokenizedLine = line.strip().split("\t")
			if tokenizedLine[1].lower() == genus.lower():
				phyloTree = tokenizedLine[len(tokenizedLine)-1].split("|") 
				for branch in phyloTree:
					if tag == True and branch[-5:] != "aceae":
                                                ##this program assumes that the token immediatly following the genus is the Family
                                                ##this could possobly break if there are subfamilies in the phylogeny tree.
						tag = False
				##debug		print(branch.lower())
						return(branch.lower())
					if genus.lower() == branch.lower():
                                                tag = True



	return("")

filter(family)

