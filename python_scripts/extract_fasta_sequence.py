#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
from sys import argv, exit 


def readFasta(fastaFile):
    """
    read a fasta file and return a dictionary, 
    the key is entry id and the value is the sequence in upcase
    
    Parameters:
    fastaFile : str
        Path of FASTA file
        
    Return:
    dict
        key: seq_id
        value: sequence
    """
    f1 = gzip.open(fastaFile, 'rt') if fastaFile.endswith('gz') else open(fastaFile)
    line = f1.readline()
    sequence = ""
    fasta_dict = {}
    header = ""
    while True:
        if line:
            if line[0] == '>':
                if len(sequence) > 0:
                    fasta_dict[header] = sequence
                    sequence = ""
                header = line.strip()[1:]
            else:
                sequence += line.strip()
        else:
            break 
        line = f1.readline()
    f1.close()
    if header and sequence:
        fasta_dict[header] = sequence

    return fasta_dict

if __name__ == '__main__':
    if len(argv) != 4:
        exit(f"python3 {argv[0]} <fasta_file_path> <extract_sequence_ids_file> <extract_file_path>")
    
    fasta_dict = readFasta(argv[1])
    sequence_ids = [line.strip() for line in open(argv[2])]
    ouf_w = open(argv[3], 'w')

    for sequence_id in sequence_ids:
        if sequence_id in fasta_dict:
            ouf_w.write(">"+sequence_id+"\n"+fasta_dict[sequence_id]+"\n")
        else:
            print(f"{sequence_id} not in {argv[1]} file!" )
    ouf_w.close()