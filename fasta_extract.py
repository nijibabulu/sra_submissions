#! /usr/bin/env python

import sys
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('FASTA')
parser.add_argument('ID_FILE')
parser.add_argument('--exclude',action='store_true',help='''do not include the 
                    sequences indicated by ID_FILE, instead exclude those.''')
args = parser.parse_args()

ids = set(l.strip() for l in open(args.ID_FILE))
if args.exclude:
    SeqIO.write((s for s in SeqIO.parse(open(args.FASTA),'fasta') 
                 if s.name not in ids), sys.stdout,'fasta')
else:
    SeqIO.write((s for s in SeqIO.parse(open(args.FASTA),'fasta') 
                 if s.name in ids), sys.stdout,'fasta')
