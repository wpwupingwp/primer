import sys
from Bio import SeqIO

def main():
    handle=open(sys.argv[1],'r')
    data=SeqIO.parse(handle,'gb')
    target=list()
    for record in data:
        organism=record.annotations['organism']
        accession=record.annotations['accessions'][0]
        for feature in record.features:
            if feature.type=='gene' and 'gene' in feature.qualifiers:
                gene=str(feature.qualifiers['gene'][0])
                sequence=str(record.seq[feature.location.start:feature.location.end])
                target.append([organism,accession,gene,sequence])
    handle_out=open('_'.join([sys.argv[1],'simplify']),'w')
    for item in target:
        handle_out.write('>')
        handle_out.write('|'.join([item[:3]]))
        handle_out.write('\n')
        handle_out.write(item[3])
        handle_out.write('\n')
    print('Done.')

if __main__='main':
    main()