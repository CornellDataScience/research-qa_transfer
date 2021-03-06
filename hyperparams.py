"""
All hyperparameters. Implemented as a class for convenience, but operates identically to an argument parser.
"""

import json
import tensorflow as tf


class Hyperparams:

    # pre-trained models
    glove_word = './models/glove.840B.300d.txt'
    glove_char = './models/glove.840B.300d-char.txt'

    # data
    data_dir = './data'

    # log
    log_dir = './log'

    # training
    dropout = 0.2
    optimizer = 'adam'
    learning_rate = 0.0001
    batch_size = 100
    n_epochs = 100

    # architecture
    emb_size = 300
    rnn1_cell = tf.contrib.rnn.GRUCell
    rnn1_layers = 3
    rnn1_units = 75
    rnn1_dropout = 0.2

    rnn2_cell = tf.contrib.rnn.GRUCell
    rnn2_layers = 3
    rnn2_units = 75
    rnn2_attn_size = 75
    rnn2_dropout = 0.2

    rnn3_cell = tf.contrib.rnn.GRUCell
    rnn3_layers = 3
    rnn3_units = 75
    rnn3_attn_size = 75
    rnn3_dropout = 0.2

    attn_cell = tf.contrib.rnn.GRUCell
    attn_mech = tf.contrib.seq2seq.LuongAttention
    attn_layers = 3
    attn_units = 75
    attn_dropout = 0.2

    ptr_cell = tf.contrib.rnn.GRUCell
    ptr_layers = 1
    ptr_units = 75
    ptr_dropout = 0.2

    # SQuAD related info
    with open('./data/word2id.json', 'r') as f:
        word2id = json.load(f)
    with open('./data/id2word.json', 'r') as f:
        id2word = json.load(f)
    with open('./data/char2id.json', 'r') as f:
        char2id = json.load(f)
    with open('./data/id2char.json', 'r') as f:
        id2char = json.load(f)

    # vocabulary sizes
    word_vocab_size = len(word2id)
    char_vocab_size = len(char2id)

    # input size
    max_q_chars = 300
    max_q_words = 60

    # input size
    max_p_chars = 2500
    max_p_words = 500
