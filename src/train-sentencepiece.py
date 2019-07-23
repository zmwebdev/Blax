#!/usr/bin/env python3

import argparse
import configparser
import glob
import os
import sentencepiece as sp

parser = argparse.ArgumentParser(description='sentencepiece')
parser.add_argument('--config', required=True, type=str, help='config file')
parser.add_argument('--unused_number', required=False, type=int, default=100, help='number of unused tokens in vocab if new vocab words want to be used')
args = parser.parse_args()

CURDIR = os.path.dirname(os.path.abspath(__file__))
CONFIGPATH = os.path.join(CURDIR, os.pardir, args.config)
config = configparser.ConfigParser()
config.read(CONFIGPATH)

TEXTDIR = config['DATA']['TEXTDIR']
PREFIX = config['SENTENCEPIECE']['PREFIX']
VOCABSIZE = config['SENTENCEPIECE']['VOCABSIZE']
CTLSYMBOLS = config['SENTENCEPIECE']['CTLSYMBOLS']
#Append the special symbols that are not given as CTLSYMBOLS 
CTLSYMBOLSLIST = CTLSYMBOLS.split(",")
CTLSYMBOLSLIST.extend(('[UNK]','[PAD]','[SEP]'))

def _get_text_file(text_dir=TEXTDIR):
    file_list = glob.glob(f'{text_dir}/*.sent_splited')
    files = ",".join(file_list)
    return files

def train(prefix=PREFIX, vocab_size=VOCABSIZE, ctl_symbols=CTLSYMBOLS):
    files = _get_text_file()
    command = f'--normalization_rule_name=identity --input={files} --model_prefix={prefix} --vocab_size={vocab_size} --control_symbols={ctl_symbols} --unk_piece=[UNK] --pad_piece=[PAD] --eos_piece=[SEP] --bos_id=-1 --pad_id=3'
    sp.SentencePieceTrainer.Train(command)
    from_sp_2_wp_syntax()

def parse_sentencepiece_token(line, ctl_symbols = CTLSYMBOLSLIST):
    line_split = line.split('\t')
    token = line_split[0]
    value = line_split[1]
    if token in ctl_symbols:
        return token
    elif token.startswith("\u2581"):
        return token[1:]
    else:
        return "##" + token

#Read input in sentenpiece format and create a new vocab file in wordpiece format
def from_sp_2_wp_syntax(prefix=PREFIX):
    with open(prefix+'.vocab', 'rt', encoding='utf-8') as sent_piece_vocab:
        with open(prefix+'.wpvocab', 'wt', encoding='utf-8') as word_piece_vocab:
            output_vocab = list(map(parse_sentencepiece_token, sent_piece_vocab.readlines()))
            for i in range(args.unused_number):
                output_vocab.append('[unused' + str(i)+ ']')
            word_piece_vocab.write('\n'.join(output_vocab))

def main():
    train()

if __name__ == "__main__":
    main()
