# BERT with SentencePiece.
This is a repository of BERT model with SentencePiece tokenizer.  

## Requirements
sentencepiece
tensorflow
pandas

## Preprocess 
Preprocess raw data files to split sentences as follows.

```
python3 src/sentence-split-spacy.py --config eu.config.ini --do_lower_case --language eu
```

### Training SentencePiece model
Train a SentencePiece model using the preprocessed data.

```
install -d spModels
python3 src/train-sentencepiece.py --config eu.config.ini
```

### Creating data for pretraining
Create .tfrecord files for pretraining.
By default, we mask whole words and we set to 512 the sequence length.

```
python3 bert/create_pretraining_data.py \
    --input_file=corpus/eu/2014wiki.eu.sent_splited \
    --output_file=corpus/eu/pretraining.tf.data \
    --model_file=./spModels/eu.model \
    --vocab_file=./spModels/eu.vocab \
    --do_lower_case=True \
    --max_seq_length=512 \
    --do_whole_word_mask=True
```
### Pretraining
You need GPU/TPU environment to pretrain a BERT model.  

install -d gureBERT
python bert/run_pretraining.py \
  --config_file=eu.config.ini \
  --input_file=corpus/eu/pretraining.tf.data \
  --output_dir=gureBERT/eu.gureBERT \
  --do_train=True \
  --do_eval=True \
  --train_batch_size=256 \
  --max_seq_length=512 \
  --max_predictions_per_seq=20 \
  --num_train_steps=1000000 \
  --num_warmup_steps=10000 \
  --save_checkpoints_steps=10000 \
  --learning_rate=1e-4 \
