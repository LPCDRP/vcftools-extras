#!/usr/bin/env python2.7

import sys,csv,os
from Bio import SeqIO

GROUPHOME = os.environ['GROUPHOME']


def convert_v3tov4(input_vcf):
    h37rv_fasta = GROUPHOME + '/resources/H37Rv.fasta'
    #reference_fasta = SeqIO.parse(h37rv_fasta, "fasta")
    #reference_fasta = h37rv_fasta
    output_file = open(sys.argv[2],'wb')
    writer = csv.writer(output_file,delimiter='\t')
    

    with open(input_vcf,'r') as vcf:
	for seq_record in SeqIO.parse(open(h37rv_fasta, 'r'), 'fasta'):

		for line in vcf:
		    column = line.rstrip('\n').split('\t')
		    if "#" in line[0]:
		        version = '3.3'
		        #str.replace(version, '4.0')
		        writer.writerow(column)
		        continue
		    position=int(column[1])
		    alt=column[4]
		    ref=column[3]

		    # SNPs #
		    if len(ref) > 1 and "D" not in alt and "I" not in alt:
		        snp_length=len(ref)
		        positions=[]
		        base_dict={}
		        for i in range(0, snp_length):
		            positions = position + i
		            base_dict[position+i]=[ref[i],alt[i]]

		        for key,value in base_dict.iteritems():
			    # print column[0], key, column[2], value[0], value[1], column[5], "PASS", column[7]
			    #output_list = [column[0], key, column[2], value[0], value[1], column[5],
		                                        #"PASS", column[7], '\n']
		            output_file.write('\t'.join([column[0], str(key), column[2], value[0], value[1], column[5], "PASS", column[7], '\n']))
		    # Deletions #
		    elif "D" in alt:
			#print seq_record.seq[position]
		        new_ref=seq_record.seq[position-1]+ref
		        new_alt=seq_record.seq[position-1]
		        output_file.write('\t'.join([column[0], str(position),  column[2], new_ref, new_alt, str(column[5]),
		                                    "PASS", str(column[7]), '\n']))
		    # Insertions #
		    elif "I" in alt:
			#print column, seq_record.seq[position]
		        new_ref=seq_record.seq[position-1]
		        int_newalt=seq_record.seq[position-1] + alt
		        new_alt=int_newalt.replace("I","")
		        output_file.write('\t'.join([column[0], str(position),  column[2], new_ref, new_alt, str(column[5]),
		                                    "PASS", str(column[7]), '\n']))
		    else:
		        column[6]="PASS"
		        output_file.write('\t'.join(column) + '\n')
    output_file.close()


def main():
    vcf = sys.argv[1]
    convert_v3tov4(vcf)


if __name__ == "__main__":
    main()
