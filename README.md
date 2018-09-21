# BarcodeFinder
Automatic discover novel DNA barcode with universal primers.
## Prerequisite
### Software
* Python3
* BLAST+
* IQTREE
* MAFFT
### Python module
* Biopython
* matplotlib
* numpy
* primer3-py
### Internet
The data retrive function requires Internet connection. Please ensure you have
stable network and inexpensive net fee when downloading large size of data.
## Installation
Assume that you alreadly installed [Python3](https://www.python.org/downloads/)
(3.5 or above). Firstly, install BarcodeFinder.
The easiest way is to download 
[BarcodeFinder.py](https://github.com/wpwupingwp/BarcodeFinder) and put it 
into wherever you want.
If you would like to use pip, then:
```
# as administator
pip3 install BarcodeFinder
# normal user
pip3 install BarcodeFinder --user
```
Secondly, you need to install dependent software and python modules.
Althrough BarcodeFinder has assistant function to automaticly install 
dependent softwares and modules if it cannot find them. However, it is 
highly recommended to follow official installation procedure to make it 
easy for management and give you a clean working directory.
For Linux user, if you have root privileges, just use your package manager:
```
# Ubuntu and Debian
sudo apt install mafft ncbi-blast+ iqtree
# Fedora
sudo dnf install mafft ncbi-blast+ iqtree
# Fedora 2
sudo yum install mafft ncbi-blast+ iqtree
# ArchLinux
sudo pacman -S mafft ncbi-blast+ iqtree
# FreeBSD
sudo pkg install mafft ncbi-blast+ iqtree
```
For MacOSX user, assume you have root privileges, if you do not have 
*brew*, install it:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Then:
```
brew install blast mafft brewsci/science/iqtree
```
If you are Windows user or you do not have root privileges, follow these
instructions:
1. BLAST+
* [Windows](https://www.ncbi.nlm.nih.gov/books/NBK52637/)
* [Linux and MacOSX](https://www.ncbi.nlm.nih.gov/books/NBK52640/)
2. MAFFT
* [Windows](https://mafft.cbrc.jp/alignment/software/windows.html)
Choose "All-in-one version", download and unzip. Then follow the step in
BLAST+ installation manual to set _PATH_.
* [Linux](https://mafft.cbrc.jp/alignment/software/linux.html)
Choose "Protable package", download and unzip. Then follow the instruction of
BLAST+ to set _PATH_.
* [MacOSX](https://mafft.cbrc.jp/alignment/software/macosx.html)
Choose "All-in-one version", download and unzip. Then follow the step in
BLAST+ installation manual to set _PATH_.
3. IQTREE
[Download](http://www.iqtree.org/#download) according to your OS.
Unzip and add the path of subfolder *bin* into _PATH_
## Usage
### Quick examples
Download all rbcL sequences of plants:
```
# Windows
python BarcodeFinder.py -query rbcL -group plants -stop 1 -out rbcL
# Linux and macos
python3 BarcodeFinder.py -query rbcL -group plants -stop 1 -out rbcL
```
Download all ITS sequences of Rosa and do preprocess:
```
# Windows
python BarcodeFinder.py -query "internal transcribed spacer" -taxon Rosa -stop 2 -out Rosa_its
# Linux and macos
python3 BarcodeFinder.py -query "internal transcribed spacer" -taxon Rosa -stop 2 -out Rosa_its
```
Download all Rosaceae chloroplast genome sequences, plus your data  as fasta 
format, then do analyze:
```
# Windows
python BarcodeFinder.py -organelle chloroplast -taxon Rosaceae -out Poaceae_cpg -fasta my_data.fasta
# Linux and macos
python3 BarcodeFinder.py -organelle chloroplast -taxon Rosaceae -out Poaceae_cpg -fasta my_data.fasta
```
Download sequences of Zea mays, set length between 100 bp and 3000 bp, plus
your aligned data, then do analyze:
```
# Windows
python BarcodeFinder.py -taxon "Zea mays" -min_len 100 -max_len 3000 -out Zea_mays -aln my_data.aln
# Linux and macos
python3 BarcodeFinder.py -taxon "Zea mays" -min_len 100 -max_len 3000 -out Zea_mays -aln my_data.aln
```
Download all Oryza chloroplast genomes, divide them into fragments, and skip
analyze:
```
# Windows
python BarcodeFinder.py -taxon Oryza -organelle chloroplast -stop 2 -out Oryza_cp
# Linux and macos
python3 BarcodeFinder.py -taxon Oryza -organelle chloroplast -stop 2 -out Oryza_cp
```

