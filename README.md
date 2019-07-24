# BERT with SentencePiece.
This is a repository of BERT model with SentencePiece tokenizer.  

## Requirements
sentencepiece
tensorflow
nltk

## Extract Wikipedia articles

Uses Wikiextractor to mine the required language Wikipedia articles.

```
usage: download_wiki_corpus.py [-h] --language {eu,es,en,fr}
                               --wikipedia_dump_path WIKIPEDIA_DUMP_PATH
                               --output_file_path OUTPUT_FILE_PATH
example: python3 src/download_wiki_corpus.py 
    --language eu 
    --output_file_path corpus/processed_wikis/eu_wiki_processed 
    --wikipedia_dump_path corpus/
```
This will download euwiki_file.xml.bz2 wikipedia dump and then output the processed files to the specified eu_wiki_processed file.

## Preprocess 
Preprocess raw data files to split sentences as follows.

```
usage: sentence-split-nltk.py [-h] --text_dir TEXT_DIR [--do_lower_case]
exmaple: python3 src/sentence-split-nltk.py 
    --text_dir corpus/processed_wikis 
    --do_lower_case
```
This will split the sentences of all the processed files in corpus/processed_wikis using the nltk punkt module and will create a *.sent_splitted file for each of them.

### Training SentencePiece model
Train a SentencePiece model using the preprocessed data.

```
install -d spModels
usage: train-sentencepiece.py [-h] --vocab_size VOCAB_SIZE --text_dir TEXT_DIR
                              [--output OUTPUT]
                              [--unused_number UNUSED_NUMBER]

example:python3 src/train-sentencepiece.py 
    --vocab_size 30000 
    --text_dir corpus/processed_wikis/ 
    --output spModels/blax

```
This will create a *.model and *.vocab file using sentencepiece unigram language model. Then this vocab will be converted to WordPiece syntax and some [unused] tokens will be appended at the end. 

### Creating data for pretraining
Create .tfrecord files for pretraining.
By default, we mask whole words and we set to 512 the sequence length.

```
python3 bert/create_pretraining_data.py 
    --input_file=corpus/processed_wikis/eu_wiki_processed.sent_splited 
    --output_file=corpus/processed_wikis/pretraining.tf.data 
    --vocab_file=./spModels/blax.wpvocab 
    --do_lower_case=True 
    --max_seq_length=512 
    --do_whole_word_mask=True
```

This will create the tf.data for the pretraining of the BERT model. 

### Pretraining
You need GPU/TPU environment to pretrain a BERT model.  

First train the model with less max_seq_length (128) for 90% percent of the steps. 

```
python3 bert/run_pretraining.py \
  --config_file=bert_config.json \
  --input_file=corpus/eu/pretraining.tf.data \
  --output_dir=gureBERT/eu.gureBERT \
  --do_train=True \
  --do_eval=True \
  --train_batch_size=256 \
  --max_seq_length=128 \
  --max_predictions_per_seq=20 \
  --num_train_steps=90000 \
  --num_warmup_steps=10000 \
  --save_checkpoints_steps=10000 \
  --learning_rate=1e-4 \
```

Then complete the last 10% of the training with max_seq_length (512):

```
python3 bert/run_pretraining.py \
  --config_file=bert_config.json \
  --input_file=corpus/eu/pretraining.tf.data \
  --init_checkpoint=gureBERT/eu.gureBERT
  --output_dir=gureBERT/eu.gureBERT \
  --do_train=True \
  --do_eval=True \
  --train_batch_size=256 \
  --max_seq_length=128 \
  --max_predictions_per_seq=20 \
  --num_train_steps=90000 \
  --num_warmup_steps=10000 \
  --save_checkpoints_steps=10000 \
  --learning_rate=1e-4 \
```
