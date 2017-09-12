#!/usr/bin/python3

from functools import wraps
from collections import defaultdict
from timeit import default_timer as timer
import argparse
import re
import numpy as np
import primer3
from Bio.Data. IUPACData import ambiguous_dna_values


class Primer:
    global_arg = {
        'PRIMER_LIBERAL_BASE': 1,
        'PRIMER_MAX_NS_ACCEPTED': 1,
        'PRIMER_OPT_SIZE': 20,
        'PRIMER_PICK_INTERNAL_OLIGO': 1,
        'PRIMER_INTERNAL_MAX_SELF_END': 8,
        'PRIMER_MIN_SIZE': 18,
        'PRIMER_MAX_SIZE': 25,
        'PRIMER_OPT_TM': 60.0,
        'PRIMER_MIN_TM': 57.0,
        'PRIMER_MAX_TM': 63.0,
        'PRIMER_MIN_GC': 20.0,
        'PRIMER_MAX_GC': 80.0,
        'PRIMER_MAX_POLY_X': 100,
        'PRIMER_INTERNAL_MAX_POLY_X': 100,
        'PRIMER_SALT_MONOVALENT': 50.0,
        'PRIMER_DNA_CONC': 50.0,
        'PRIMER_MAX_SELF_ANY': 12,
        'PRIMER_MAX_SELF_END': 8,
        'PRIMER_PAIR_MAX_COMPL_ANY': 12,
        'PRIMER_PAIR_MAX_COMPL_END': 8,
        'PRIMER_PRODUCT_SIZE_RANGE': [[26, 100], [250, 450], [450, 800]]
    }

    def __init__(self, name, seq, start=None, length=None):
        if start is None:
            start = 0
        if length is None:
            length = len(seq)
        seq_arg = {
            'SEQUENCE_ID': name,
            'SEQUENCE_TEMPLATE': seq,
            # 'SEQUENCE_INCLUDED_REGION': [start, length]
                   }
        self.seq_arg = seq_arg

    def change(self, **kargs):
        self.global_arg.update(kargs)

    def design(self):
        result = primer3.bindings.designPrimers(self.seq_arg, self.global_arg)
        return result


def print_time(function):
    @wraps(function)
    def wrapper(*args, **kargs):
        start = timer()
        result = function(*args, **kargs)
        end = timer()
        print('The function {0} Cost {1:3f}s.\n'.format(
            function.__name__, end-start))
        return result
    return wrapper


def get_ambiguous_dict():
    data = ambiguous_dna_values
    data = dict(zip(data.values(), data.keys()))
    # 2:{'AC': ['M',}
    data_with_len = defaultdict(lambda: dict())
    for key in data:
        data_with_len[len(key)][key] = data[key]
    return data_with_len


@print_time
def read(fasta):
    data = list()
    record = ['id', 'seq']
    with open(fasta, 'r') as raw:
        for line in raw:
            if line.startswith('>'):
                data.append([record[0], ''.join(record[1:])])
                name = line[1:-1]
                record = [name, ]
            else:
                record.append(line[:-1].upper())
        data.append([record[0], ''.join(record[1:])])
    data = data[1:]
    return data


@print_time
def convert(old):
    # order 'F' is a bit faster than 'C'
    # name = np.array([[i[0]] for i in old], dtype=np.bytes_)
    # seq = np.array([list(i[1]) for i in old], dtype=np.bytes_)
    # new = np.hstack((name, seq))
    new = np.array([list(i[1]) for i in old], dtype=np.bytes_, order='F')
    rows, columns = new.shape
    return new, rows, columns


@print_time
def count(alignment, rows, columns):
    # skip sequence id column
    data = [[rows, columns]]
    for index in range(columns):
        column = alignment[:, [index]]
        unique, counts = np.unique(column, return_counts=True)
        count_dict = {b'A': 0, b'T': 0, b'C': 0, b'G': 0, b'N': 0,
                      b'-': 0, b'?': 0}
        count_dict.update(dict(zip(unique, counts)))
        a = count_dict[b'A']
        t = count_dict[b'T']
        c = count_dict[b'C']
        g = count_dict[b'G']
        n = count_dict[b'N']
        gap = count_dict[b'-']
        question = count_dict[b'?']
        # is it necessary to count 'N' '-' and '?' ?
        other = rows - a - t - c - g - n - question - gap
        data.append([a, t, c, g, n, question, gap, other])
    # make sure rows and columns does not mixed
    assert len(data) == columns + 1
    return data


@print_time
def find_most(data, cutoff, gap_cutoff):
    most = [['location', 'base', 'count']]
    rows, columns = data[0]
    data = data[1:]
    gap_cutoff = rows * gap_cutoff
    cutoff = rows * cutoff
    ambiguous_dict = get_ambiguous_dict()

    def run():
        for location, column in enumerate(data, 1):
            finish = False
            value = dict(zip(list('ATCGN?-X'), column))
            base = 'N'

            sum_gap = sum([value['?'], value['-'], value['X']])
            if sum_gap >= gap_cutoff:
                base = '-'
                count = sum_gap
                yield [location, base, count]
                continue
            # 1 2 3 4
            for length in ambiguous_dict:
                if finish:
                    break
                for key in ambiguous_dict[length]:
                    if finish:
                        break
                    count = 0
                    for letter in list(key):
                        if finish:
                            break
                        count += value[letter]
                        if count >= cutoff:
                            base = ambiguous_dict[length][key]
                            finish = True
                            yield [location, base, count]
    for i in run():
        most.append(i)
    return most[1:]


@print_time
def find_continuous(most):
    continuous = list()
    fragment = list()
    most = [i for i in most if i[1] not in ('N', '-')]
    for index, value in enumerate(most):
        fragment.append(value)
        location, *_ = value
        try:
            location_next, *_ = most[index+1]
        except:
            fragment.append(value)
# to be continue
            break
        step = location_next - location
        if step > 1:
            continuous.append(fragment)
            fragment = list()
    return continuous


@print_time
def find_primer(continuous, most, length):
    poly = re.compile(r'([ATCG])\1\1\1\1')
    ambiguous_base = re.compile(r'[^ATCG]')
    tandem = re.compile(r'([ATCG]{2})\1\1\1\1')

    def is_good_primer(primer):
        # ref1. http://www.premierbiosoft.com/tech_notes/PCR_Primer_Design.html
        seq = ''.join([i[1] for i in primer])
        if re.search(poly, seq) is not None:
            return False, 'Poly(NNNNN) structure found'
        if re.search(tandem, seq) is not None:
            return False, 'Tandom(NN*5) exist'
            # no more 3 ambiguous base
        if len(re.findall(ambiguous_base, seq)) >= 3:
            return False, 'More than 3 ambiguous base'

        tm = primer3.calcTm(seq)
        hairpin_tm = primer3.calcHairpinTm(seq)
        homodimer_tm = primer3.calcHomodimerTm(seq)
        if max(tm, hairpin_tm, homodimer_tm) != tm:
            return False, 'Hairpin or homodimer found'

        return True, 'Ok'

    def get_best_primer(primers, template=None):
    # to be continue
        return best

    primer = list()
    min_len, max_len = length.split('-')
    min_len = int(min_len)
    max_len = int(max_len)
    continuous = [i for i in continuous if len(i) >= min_len]
    for fragment in continuous:
        len_fragment = len(fragment)
        for start in range(len_fragment-max_len):
            for p_len in range(min_len, max_len):
                seq = fragment[start:(start+p_len)]
                good_primer, detail = is_good_primer(seq)
                if good_primer:
                    primer.append(seq)
                else:
                    continue
    return primer


def write_primer(data, rows):
    # https://en.wikipedia.org/wiki/FASTQ_format
    quality = ('''!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'''
               '''[\]^_`abcdefghijklmnopqrstuvwxyz{|}~''')
    l = len(quality)
    output = open('primer.fastq', 'w')
    for item in data:
        i = [i[0] for i in item]
        start = item[0][0]
        end = item[-1][0]
        length = end - start
        seq = ''.join([i[1] for i in item])
        qual = [round((i[2]/rows)*l)-1 for i in item]
        qual = [quality[int(i)] for i in qual]
        output.write('@{}-{}-{}\n'.format(start, end, length))
        output.write(seq+'\n')
        output.write('+\n')
        output.write(''.join(qual)+'\n')


@print_time
def generate_consesus(data, output):
    with open(output, 'w') as out:
        seq = [i[1] for i in data]
        out.write('>Consensus\n{}\n'.format(''.join(seq)))


@print_time
def parse_args():
    arg = argparse.ArgumentParser(description=main.__doc__)
    arg.add_argument('input', help='input alignment file')
    arg.add_argument('-c', '--cutoff', type=float, default=1.0,
                     help='minium percent to keep')
    arg.add_argument('-g', '--gap_cutoff', type=float, default=0.5,
                     help='maximum percent for gap to cutoff')
    arg.add_argument('-o', '--output', default='consensus.fasta')
    arg.add_argument('-l', '--length', type=str, default='18-24',
                     help='primer length range')
    # arg.print_help()
    return arg.parse_args()


@print_time
def main():
    arg = parse_args()
    raw_alignment = read(arg.input)
    new, rows, columns = convert(raw_alignment)
    count_data = count(new, rows, columns)
    most = find_most(count_data, arg.cutoff, arg.gap_cutoff)
    generate_consesus(most, arg.output)
    continuous = find_continuous(most)
    primer = find_primer(continuous, most, arg.length)
    write_primer(primer, rows)


if __name__ == '__main__':
    main()