#!/usr/bin/env python

import os
from Bio import SeqIO

GROUPHOME = os.environ['GROUPHOME']


def process_coords(coords_filename):

    queryend_positions = {}
    querystart_positions = {}
    with open(coords_filename, 'r') as coords_filehandle:
        for line in coords_filehandle:
            if 'NUCMER' in line or '[S1]' in line:
                continue
            column = line.rstrip('\n').split('\t')
            if '' in column:
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


def main():

    input_diff_reference = '/home/sbusby/workspace/sv-mummer/sea00042.svs-reference'
    input_diff_query = '/home/sbusby/workspace/sv-mummer/sea00042.svs-query'
    reference_file = GROUPHOME + '/resources/H37Rv.fasta'
    query_file = GROUPHOME + '/data/genomes/SEA00042.fasta'
    show_coords_file = '/home/sbusby/workspace/sv-mummer/sea00042.coords-sorted'

    reference_seq = []
    query_seq = []
    for seq_record in SeqIO.parse(open(reference_file, 'r'), 'fasta'):
        reference_seq.append(seq_record.seq)
    for seq_record in SeqIO.parse(open(query_file, 'r'), 'fasta'):
        query_seq.append(seq_record.seq)

    diff_reference = []
    diff_query = []
    # Loading reference show-diff output
    with open(input_diff_reference, 'r') as input_diff_filehandle:
        for line in input_diff_filehandle:
            column = line.rstrip('\n').split('\t')
            diff_reference.append(column)
    # Loading query show-diff output
    with open(input_diff_query, 'r') as input_diff_filehandle:
        for line in input_diff_filehandle:
            column = line.rstrip('\n').split('\t')
            diff_query.append(column)
    # Getting reference positions based on query
    qstartpos, qendpos = process_coords(show_coords_file)
    # Looping over each SV based on the query positions to get sequences
    for mutation in diff_query:
        chrom = mutation[0]
        sv_type = mutation[1]
        if int(mutation[2]) < int(mutation[3]):
            qstart = int(mutation[2])
            qend = int(mutation[3])
        else:
            qstart = int(mutation[3])
            qend = int(mutation[2])
        if 'GAP' in sv_type:
            gap_diff = int(mutation[6])
            # Insertion in query
            # TODO check 4411532 in reference, 4135134	4425664 in show-coords query columns
            if gap_diff > 0:
                if qstart - 1 in qstartpos.keys():
                    reference_position = qstartpos[qstart - 1][0]
                elif qstart - 1 in qendpos.keys():
                    reference_position = qendpos[qstart - 1][1]
                elif qstart + 1 in qendpos.keys():
                    reference_position = qendpos[qstart + 1][1]
                    # Need to reset the query start since it is off by one
                    qstart = qstart + 2
                elif qstart + 1 in qstartpos.keys():
                    reference_position = qstartpos[qstart + 1][0]
                    qstart = qstart + 2
                else:
                    print mutation
                    exit()
                ref_base = reference_seq[0][reference_position - 1]
                alt_base = query_seq[0][qstart - 2:qend - 1]
                # if ref_base != alt_base[0]:
                #     print mutation
                #     print qstart, qend, reference_position
                print '\t'.join(['1', str(reference_position), '.', ''.join(ref_base), ''.join(alt_base)])
            # Deletion in query
            elif gap_diff < 0:
                cur_index = diff_query.index(mutation)
                reference_line = diff_reference[cur_index - 1]
                if int(reference_line[2]) < int(reference_line[3]):
                    rstart = int(reference_line[2])
                    rend = int(reference_line[3])
                else:
                    rstart = int(reference_line[3])
                    rend = int(reference_line[2])
                ref_base = reference_seq[0][rstart - 1:rend]
                alt_base = reference_seq[0][rstart - 1]
                print '\t'.join(['1', str(rstart), '.', ''.join(ref_base), ''.join(alt_base)])

                # if qstart + 1 in qendpos.keys():
                #     print mutation
                #     print qendpos[qstart + 1]

if __name__ == '__main__':
    main()
