"""
Layers of neural network architecture.
"""

import tensorflow as tf
from tensorflow.contrib.rnn import DropoutWrapper, MultiRNNCell


def encoding(word, char, word_embeddings, char_embeddings, scope='embedding'):
    """Encode the list of word ids and character ids to pretrained embeddings using tf.nn.embedding_lookup
    Args:
        word (list):                   list of word ids
        char (list):                   list of char ids
        word_embeddings (tf.Variable): pretrained [(size of vocabulary) x (embedding dimension; default 300)] matrix
        char_embeddings (tf.Variable): pretrained [(size of vocabulary) x (embedding dimension; default 300)] matrix
        scope (str):                   tensorflow variable scope

    Returns:
        word_encoding (tensor)
        char_encoding (tensor)
    """
    with tf.variable_scope(scope):
        word_encoding = tf.nn.embedding_lookup(word_embeddings, word)
        char_encoding = tf.nn.embedding_lookup(char_embeddings, char)
        return word_encoding, char_encoding


def bidirectional_rnn(inputs, input_lengths, cell_type, num_units, num_layers, dropout_prob, is_training=True,
                      scope='Bi_RNN'):
    """Bidirectional RNN.

    Args:
        inputs (tensor):        3-dimensional input tensor of shape [batch_size, max_document_length, embedding_size]
        input_lengths (tensor): 1-dimensional tensor of length batch_size specifying actual length of each document
        cell_type (method):     type of RNN cell (e.g. tf.contrib.rnn.GRUCell)
        num_units (int):        number of units in the RNN cell
        num_layers (int):       number of layers in the RNN
        dropout_prob (float):   probability of dropping a node during dropout
        is_training (bool):     whether the model is training or testing
        scope (str):            tensorflow variable scope

    Returns:
        tensor:                 output tensor or hidden state tensor depending on setting of output
    """
    with tf.variable_scope(scope):
        input_dims = inputs.get_shape().as_list()
        assert len(input_dims) == 3, "Input tensor must be 3-dimensional."

        def rnn_cell():
            # only use dropout during training
            keep_prob = 1 - dropout_prob if is_training else 1
            return DropoutWrapper(cell_type(num_units), output_keep_prob=keep_prob)

        if num_layers > 1:
            # if there is more than one hidden layer, use MultiRNNCell
            cell_fw = MultiRNNCell([rnn_cell() for _ in range(num_layers)])
            cell_bw = MultiRNNCell([rnn_cell() for _ in range(num_layers)])
        else:
            cell_fw, cell_bw = rnn_cell(), rnn_cell()

        outputs, states = tf.nn.bidirectional_dynamic_rnn(cell_fw, cell_bw, inputs, input_lengths, dtype=tf.float64)
        return outputs, states


def attention(inputs, bias=False, scope='attention'):
    # TODO: check correctness; allow inputs to be concatenation of previous context vector
    with tf.variable_scope(scope):
        _, state_size, seq_len = inputs.get_shape().as_list()
        w = tf.get_variable('W', initializer=tf.truncated_normal([None, state_size, state_size]))
        v = tf.get_variable('v', initializer=tf.truncated_normal([None, state_size]))
        activation = tf.matmul(inputs, w)
        if bias:
            b = tf.get_variable('b', initializer=tf.zeros([None, state_size]))
            activation += b
        s = tf.reduce_sum(tf.multiply(v, tf.tanh(activation)))
        a = tf.nn.softmax(s)
        return tf.multiply(a, inputs)


def pointer_net(inputs, cell_type, num_pointers, num_units, initial_state=None):
    """Implementation of a pointer network as described in https://arxiv.org/abs/1506.03134

    Args:
        inputs (tensor):        input tensor of shape [batch_size, max_time, size]
        cell_type (method):     type of RNN cell (e.g. tf.contrib.rnn.GRUCell)
        num_pointers (int):     number of pointers to return
        num_units (int):        number of units in the hidden RNN cell
        initial_state (tensor): tensor to use as initial hidden state of decoder RNN
    Returns:

    """
    batch_size, max_time, size = inputs.get_shape().as_list()
    if initial_state is None:
        initial_state = tf.zeros([batch_size, num_units])


def cnn_embedding(inputs):
    pass
