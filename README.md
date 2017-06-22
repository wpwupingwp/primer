# About
Here are some python scripts I wrote. Most of them process fasta/fastq/gb
files.

From now on, I will add some descriptions for each program.

You can type 
>python3 pyfile -h

or

>python3 pyfile

to print usage of each program.

You can ask me any question about these programs via
**wpwupingwp@outlook.com** .

# Requirement

1. [python3](https://www.python.org/downloads/)

    Be sure to install python3 rather than python 2.7. Besides, to use
    subprocess.call(), you would better install python **3.5** or above.

2. [biopython](http://biopython.org/wiki/Download)

3. [BLAST Suite](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)

And notice that all scripts were just tested on Linux system, although
theoretically they may works fine on Windows.

# Batch

Many of programs in this repository support batch mode. See examples below.
Note that "\*.fasta" is files you want to process, and _i_ is variable you can
use other name if you want. And parameters of program was omitted.

## Microsoft Windows

> for i in (\*.fasta) do python program.py %i

## Linux

> for i in \*.fasta;do python3 program.py $i

# This folder

## trim.py

Trim fragment in given fasta file, replace trimmed bases with 'N'.

Usage:

> python3 trim.py input.fasta start-end

Here _start_ and _end_ are integers, and end could larger than length of
sequence if you want to cut off sequence's tail.

## no_same.py

Remove identical sequence in give fasta/nexus file. New file will be write
into ".new" with the same format of input file.

Duplicated sequences will be printed on screen.

Usage:

> python3 no_same.py input_file

## vlookup_assistant.py

Expand a given table according to range.

Input table (CSV format) looks like this:

>    A,B,C

It will generate a new table:

>    D,E 

where D was expanded from range(B, C) and E is related A.

## add_gene_name.py

Rename fasta files in one directory according to gene info provided by the
first record in each file

## pick.py

Pick fasta record according to id list

## screen.py

Screen sequence assembled by _spades_ according to sequence length and
coverage info in sequence id.

**Warning: This program use regular expression to recognize infomation, it may
generate wrong output when it was used on other sequence if format.**

# old

Some old code.

# cp

Some program to deal with genbank files, most of them belongs to chloroplast.

# plot

Use *matplotlib* to draw figures for my master thesis.

# inhibitor

Some code to analyze data from microreader. For Cystathionine beta-synthase
inhibitor project.

# Template

Some useful code fragments.
