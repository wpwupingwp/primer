from Bio import SeqIO
import csv
def main():
#    FileIn="gb"
#    Record=SeqIO.read(FileIn,"genbank")
    Taxon=Record.features[0].qualifiers["db_xref"][0].replace("taxon:","")
    Organism=Record.annotations["organism"]
    Accession=Record.annotations["accessions"][0]
    Gene=[]
    All=[]
    for i in Record.features:
        if i.type=="gene" and "gene" in i.qualifiers:
            if i.location_operator!="join":
                Type="gene"
                Start=int(i.location.start)
                End=int(i.location.end)
                Sequence=str(Record.seq[Start:End])
                Name=str(i.qualifiers["gene"][0])
                Strand=int(i.location.strand)
                rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence]
                Gene.append(rec)
            elif i.location_operator=="join":
                Type="gene"
                Start=int(i.sub_features[0].location.start)
                End=int(i.sub_features[0].location.end)
                Name=str(i.qualifiers["gene"][0])
                Strand=int(i.location.strand)
                Sequence=""
                rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence]
                Gene.append(rec)
                Start=int(i.sub_features[1].location.start)
                End=int(i.sub_features[1].location.end)
                Sequence="".join([str(Record.seq[Start:End]),str(Record.seq[Start:End])])
                rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence]
                Gene.append(rec)
        elif i.type=="rRNA":
            Type="rRNA"
            Start=int(i.location.start)
            End=int(i.location.end)
            Sequence=str(Record.seq[Start:End])
            Name=str(i.qualifiers["product"][0]).replace(" ","_")
            Strand=int(i.location.strand)
            rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence]
            All.append(rec)
        elif i.type=="exon":
            Type="exon"
            Start=int(i.location.start)
            End=int(i.location.end)
            Sequence=str(Record.seq[Start:End])
            Name="_".join([str(i.qualifiers["gene"][0]),"exon",str(i.qualifiers["number"][0])])
            Strand=int(i.location.strand)
            rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence]
            All.append(rec)
        elif i.type=="intron":
            Type="intron"
            Start=int(i.location.start)
            End=int(i.location.end)
            Sequence=str(Record.seq[Start:End])
            Strand=int(i.location.strand)
            if "number" in i.qualifiers:
                Name="_".join([str(i.qualifiers["gene"][0]),"intron",str(i.qualifiers["number"][0])])
            else:
                Name="_".join([str(i.qualifiers["gene"][0]),"intron"])
            rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence]
            All.append(rec)
    Gene.sort(key=lambda x:x[5])
    for i in range(len(Gene)-1):
        Type="spacer"
        This=Gene[i]
        Next=Gene[i+1]
        Tail=This[6]+1
        Head=Next[5]-1
        Sequence=str(Record.seq[Tail:Head])
        Name="_".join(["-".join([This[3],Next[3]]),"Spacer"])
        Strand=This[7]
        rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence]
        All.append(rec)
    All.extend(Gene)
    All.sort(key=lambda x:x[5])
    Database.extend(All)
    FileOut=open(".".join([Accession,"fasta"]),"w")
    for i in All:
        if i[8]!="":
            FileOut.write(">%s|%s|%s|\n"%(Organism,i[3],Accession,))
            FileOut.write("%s\n"%(i[8]))
    FileOut.write(">%s|Complete Sequence\n%s"%(Organism,str(Record.seq)))
    return 


Database=[]
FileIn=input("File name:\n")
Records=list(SeqIO.parse(FileIn,"genbank"))
for Record in Records:
    main()

csvfile=open("Data.csv","w")
writer=csv.writer(csvfile)
writer.writerow(["Taxon","Organism","Accession","Name","Type","Start","End","Strand","Sequence"])
for item in Database:
    if item[8]!="":
        writer.writerow(item)
csvfile.close()