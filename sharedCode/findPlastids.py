#copyright:HannahBeaver
#released under MIT lessons

from Bio import SeqIO
import glob
def findGenus(genus):
    family = ""
    order = ""
    with open("/share/phylogeny.txt", "r") as file:
        for line in file:                                         
            parts = line.strip().split("\t")                      
            if parts[1].lower()  == genus.lower():                
                parts = parts[2].split("|")                       
                flag = False                                     
                temp = ""
                for part in parts:                                
                    if part[-5:] == "aceae":                      
                        flag = True
                        temp = part
                    if part[-5:] != "aceae" and flag == True:     
                        family += temp
                        order += part
                        break
    return family, order                                          
plastids = glob.glob("/share/genomes/*.fna")
poales = {"bromeliaceae":0, "cyperaceae":0, "ecdeiocoleaceae":0, "eriocaulaceae":0, "flagellariaceae":0, "joinvilleaceae":0, "juncaceae":0, "mayacaceae":0, "poaceae":0, "rapateaceae":0, "restionaceae":0, "thurniaceae":0, "typhaceae":0, "xyridaceae":0}
for plastid in plastids:
    for seq in SeqIO.parse(plastid, "fasta"):
        l = list(seq.description.split())
        info = findGenus(l[1])
        if info[1].lower()  == "poales":
            poales[info[0].lower()] += 1
print(poales)
     
