import os
import subprocess 
from urllib.request import urlretrieve
import argparse 
import sys

CURDIR = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description='Download wiki dump and parse it')
parser.add_argument('--language', required=True, type=str, help='ISO code of the language', choices=['eu', 'es', 'en', 'fr'])

parser.add_argument('--output_path', required=True, type=str, help='output path for the wiki files')

args = parser.parse_args()

def reporthook(blocknum, blocksize, totalsize):
    '''
    Callback function to show progress of file downloading.
    '''
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

def extract(wiki_file):
    subprocess.call(['python3', os.path.join(CURDIR, os.pardir, 'wikiextractor', 'WikiExtractor.py'), wiki_file,"-o={}".format(args.output_path), "--filter_disambig_pages" ])

def download(lang_iso, output_file):
    if lang_iso == 'eu':
        url = 'https://dumps.wikimedia.org/euwiki/20190701/euwiki-20190701-pages-articles-multistream.xml.bz2'
        urlretrieve(url, output_file, reporthook)
    elif lang_iso == 'fr':
        url = 'https://dumps.wikimedia.org/frwiki/20190701/frwiki-20190701-pages-articles-multistream.xml.bz2'
        urlretrieve(url, output_file, reporthook)
    elif lang_iso == 'en':
        url = 'https://dumps.wikimedia.org/enwiki/20190701/enwiki-20190701-pages-articles-multistream.xml.bz2'
        urlretrieve(url, output_file, reporthook)
    elif lang_iso == 'es':
        url = 'https://dumps.wikimedia.org/eswiki/20190701/eswiki-20190701-pages-articles-multistream.xml.bz2'        
        urlretrieve(url, output_file, reporthook)

    

def main():
    output_file = os.path.join(args.output_path, args.language +  'wiki_file.xml.bz2')
    download(args.language, output_file)
    extract(output_file)

if __name__=='__main__':
    main()
