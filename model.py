"""
Main model.
"""

from hyperparams import Hyperparams
import tensorflow as tf
from tensorflow.contrib.rnn import GRUCell
from layers import *
from util import load_glove
from loader import *


class Model(object):
    """Main model

    Attributes:
        load_pretrained (bool):         if True, load the model at the instantiation
        char_embeddings (tf.Variable):  mxn matrix that contains character embedding
                                        each row represents character token and
                                        columns represent embedded dimension
        word_embeddings (tf.Variable):  mxn matrix that contains word embedding
                                        each row represents one word and
                                        columns represent embedded dimension
        q_input_char (tf.placeholder):  placeholder for a question converted to
                                        character ids
        q_input_word (tf.placeholder):  placeholder for a question converted to
                                        word ids
        q_encoded_char (tensor):        a tensor after encoding the input character
                                        to the glove embedding
        q_encoded_word (tensor):        a tensor after encoding the input words
                                        to the glove embedding
    """
    def __init__(self, load_pretrained=True):
        if load_pretrained:
            print('start loading character embedding')
            char_embeddings = np.zeros([Hyperparams.char_vocab_size+1, Hyperparams.emb_size])
            char_glove = load_glove(Hyperparams.glove_char)  # load matrixå
            for char, i in Hyperparams.char2id.items():
                if char in char_glove:
                    char_embeddings[i] = char_glove.get(char)  # insert embedding
                else:
                    # TODO is initializing with zero vector smart?
                    char_embeddings[i] = np.zeros(Hyperparams.emb_size)
            # build a tensor for the lookup
            self.char_embeddings = tf.Variable(tf.constant(char_embeddings), trainable=True, name="char_embeddings")

            print('start loading word embedding')
            word_embeddings = np.zeros([Hyperparams.word_vocab_size+1, Hyperparams.emb_size])
            word_glove = load_glove(Hyperparams.glove_word)  # load matrix
            for word, i in Hyperparams.word2id.items():
                if word in word_glove:
                    word_embeddings[i] = word_glove.get(word)  # insert embedding
                else:
                    # TODO is initializing with zero vector smart?
                    word_embeddings[i] = np.zeros(Hyperparams.emb_size)
            # build a tensor for the lookup
            self.word_embeddings = tf.Variable(tf.constant(word_embeddings), trainable=False, name="word_embeddings")

        else:
            self.char_embeddings = tf.Variable(tf.constant(0.0, shape=[Hyperparams.char_vocab_size+1, Hyperparams.emb_size]),
                                               trainable=True, name="char_embeddings")
            self.word_embeddings = tf.Variable(tf.constant(0.0, shape=[Hyperparams.word_vocab_size+1, Hyperparams.emb_size]),
                                               trainable=False, name="word_embeddings")

        # input placeholders
        self.q_input_char = tf.placeholder(tf.int32, [None, Hyperparams.max_question_c], "question_c")
        self.q_input_word = tf.placeholder(tf.int32, [None, Hyperparams.max_question_w], "question_w")
        # encode the words using glove
        self.q_encoded_word, q_encoded_char = \
        encoding(self.q_input_word, self.q_input_char, self.word_embeddings, self.char_embeddings)
        # store the final layer of bidirectional gru unit for the character embedding
        self.q_encoded_char = bidirectional_rnn(q_encoded_char, [Hyperparams.max_question_c], Hyperparams.rnn1_cell_type, \
        Hyperparams.rnn1_num_units, Hyperparams.rnn1_num_layers, Hyperparams.rnn1_dropout)


if __name__ == '__main__':
    sample_qc = convert_to_ids('What is in front of the Notre Dame Main Building?', mode='character')
    sample_qw = convert_to_ids('What is in front of the Notre Dame Main Building?', mode='word')

    QuACC = Model(load_pretrained=True)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        feed_dict = {QuACC.q_input_char : sample_qc.reshape(1, -1), QuACC.q_input_word : sample_qw.reshape(1, -1)}
        index = sess.run([QuACC.q_encoded_char], feed_dict=feed_dict)

        print (index[0]) # 1 x 80 x (2 x char len)
