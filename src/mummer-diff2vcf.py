#!/usr/bin/env python

import os
from Bio import SeqIO

GROUPHOME = os.environ['GROUPHOME']
reference_fasta = GROUPHOME + '/resources/H37Rv.fasta'


def sequence(fasta_file):
    seq = []
    for seq_record in SeqIO.parse(open(fasta_file, 'r'), 'fasta'):
        seq.append(seq_record.seq)
    return seq


def diff_output_list(diff_output):

    diff_list = []
    with open(diff_output, 'r') as input_diff_filehandle:
        for line in input_diff_filehandle:
            column = line.rstrip('\n').split('\t')
            if '/' in column[0] or 'NUCMER' in column or '' in column or '[' in column[0]:
                continue
            diff_list.append(column)
    return diff_list


def process_coords(coords_filename):

    queryend_positions = {}
    querystart_positions = {}
    with open(coords_filename, 'r') as coords_filehandle:
        for line in coords_filehandle:
            column = line.rstrip('\n').split('\t')
            if '/' in column[0] or 'NUCMER' in column or '' in column or '[' in column[0]:
                continue
            rstart = int(column[0])
            rend = int(column[1])
            if int(column[2]) < int(column[3]):
                qstart = int(column[2])
                qend = int(column[3])
            else:
                qstart = int(column[3])
                qend = int(column[2])
            queryend_positions[qend] = [rstart, rend]
            querystart_positions[qstart] = [rstart, rend]
    return querystart_positions, queryend_positions


def gaps(mutation_line, qstart_dict, qend_dict, query_fasta, cur_index, diff_reference):

    query_seq = sequence(query_fasta)
    reference_seq = sequence(reference_fasta)

    if int(mutation_line[2]) < int(mutation_line[3]):
        qstart = int(mutation_line[2])
        qend = int(mutation_line[3])
    else:
        qstart = int(mutation_line[3])
        qend = int(mutation_line[2])
    gap_diff = int(mutation_line[6])

    # Insertion in query
    if gap_diff > 0:
        if qstart - 1 in qstart_dict.keys():
            reference_position = qstart_dict[qstart - 1][0]
        elif qstart - 1 in qend_dict.keys():
            reference_position = qend_dict[qstart - 1][1]
        elif qstart + 1 in qend_dict.keys():
            reference_position = qend_dict[qstart + 1][1]
            qstart = qstart + 2  # Need to reset the query start since it is off by one
        elif qstart + 1 in qstart_dict.keys():
            reference_position = qstart_dict[qstart + 1][0]
            qstart = qstart + 2
        else:
            print mutation_line
            exit()
        ref_base = reference_seq[0][reference_position - 1]
        alt_base = query_seq[0][qstart - 2:qend - 1]
        # print '\t'.join(['1', str(reference_position), '.', ''.join(ref_base), ''.join(alt_base)])
    # Deletion in query
    elif gap_diff < 0:
        reference_line = diff_reference[cur_index - 1]
        if int(reference_line[2]) < int(reference_line[3]):
            rstart = int(reference_line[2])
            rend = int(reference_line[3])
        else:
            rstart = int(reference_line[3])
            rend = int(reference_line[2])
        ref_base = reference_seq[0][rstart - 1:rend]
        alt_base = reference_seq[0][rstart - 1]
        # print '\t'.join(['1', str(rstart), '.', ''.join(ref_base), ''.join(alt_base)])


def inversions(mutation_line, qstart_dict, qend_dict, query_fasta):

    print mutation_line


def relocations(mutation_line):
    print mutation_line


def main():

    input_diff_reference = '/home/sbusby/workspace/sv-mummer/sea00042.svs-reference'
    input_diff_query = '/home/sbusby/workspace/sv-mummer/sea00042.svs-query'
    query_file = GROUPHOME + '/data/genomes/SEA00042.fasta'
    show_coords_file = '/home/sbusby/workspace/sv-mummer/sea00042.coords-sorted'

    # Loading reference show-diff output
    diff_reference = diff_output_list(input_diff_reference)
    diff_query = diff_output_list(input_diff_query)
    # Loading query show-diff output
    with open(input_diff_query, 'r') as input_diff_filehandle:
        for line in input_diff_filehandle:
            column = line.rstrip('\n').split('\t')
            diff_query.append(column)
    # Getting reference positions based on query
    qstartpos, qendpos = process_coords(show_coords_file)
    # Looping over each SV based on the query positions to get sequences
    for mutation in diff_query:
        sv_type = mutation[1]
        if 'GAP' in sv_type:
            gaps(mutation_line=mutation,
                 qstart_dict=qstartpos,
                 qend_dict=qendpos,
                 query_fasta=query_file,
                 diff_reference=diff_reference,
                 cur_index=diff_query.index(mutation))
        elif 'JMP' in sv_type:
            relocations(mutation)
            # inversions(mutation_line=mutation,
            #            qstart_dict=qstartpos,
            #            qend_dict=qendpos,
            #            query_fasta=query_file)


if __name__ == '__main__':
    main()
