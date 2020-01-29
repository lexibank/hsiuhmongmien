"""
Check for consistency in the structure.
"""
import string
import pathlib
from collections import defaultdict
from pylexibank import progressbar

from lingpy import Wordlist
from lingpy import basictypes as bt
from sinopy import segments
from lexibank_hsiuhmongmien import Dataset
from tabulate import tabulate


def run(args):
    ds = Dataset(args)


    wl = Wordlist.from_cldf(ds.cldf_dir.joinpath('cldf-metadata.json'))
    errors = {
            'length': [],
            'tone': []
            }
    for idx, doculect, concept, tokens in wl.iter_rows(
            'doculect',
            'concept',
            'tokens'):
        for i, (strucs, morph) in enumerate(segments.get_structure(tokens, zipped=True)):
            struc = [x[0] for x in strucs]
            check = [x[1] for x in strucs]
            if len(struc) != len(morph):
                errors['length'] += [(
                    idx, i, doculect, concept, 
                    str(tokens), ' '.join(struc), ' '.join(morph))]
            elif not 't' in struc:
                errors['tone'] += [(idx, i, doculect, concept, 
                    str(tokens), ' '.join(struc), ' '.join(morph))]
    args.log.info('Found {0} errors by length'.format(len(errors['length'])))
    args.log.info('Found {0} errors by length'.format(len(errors['tone'])))


    with open(ds.dir.joinpath('STRUCTURE.md').as_posix(), 'w') as f:
        f.write('# Errors in the length of computed structure\n\n')
        f.write(tabulate(errors['length']))
        f.write('\n')
        f.write('# Errors in missing tones in syllables\n\n')
        f.write(tabulate(errors['tone']))
        f.write('\n')
    args.log.info('see STRUCTURE.md for detailed error report')

