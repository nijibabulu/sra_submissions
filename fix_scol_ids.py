#! /usr/bin/env python

import sys

if len(sys.argv) != 2: 
    raise SystemError, 'usage: %s FASTA' % sys.argv[0]

# the first ID that is a duplicate is fortunately exactly where the start 
# of the second half of the file is.
first_run_ids = set()
run_version = '1'
for line in open(sys.argv[1]):
    if line.startswith('>'):
        fields = line.split()
        id = fields[0][1:]
        if id in first_run_ids:
            run_version = '2'
        else:
            first_run_ids.add(id)

        id = 'TRINITY_R%s_' % run_version + \
                '_'.join(id.split('_')[1:])
        print '>%s %s' % (id,' '.join(fields[1:]))
    else:
        print line,

            
