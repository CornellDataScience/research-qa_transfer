"""
Training script.
"""

from hyperparams import Hyperparams as Hp
from loader import Loader
from model import Model
from tqdm import tqdm

def train():
    # TODO: validation set
    data = Loader(Hp.batch_size, load=True)
    # build a tensor graph
    quacc = Model()
    saver = tf.train.Saver()
    best_val_acc = 0

     # initialize graph
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter(Hp.log_dir + '/train', sess.graph)
        test_writer = tf.summary.FileWriter(Hp.log_dir + '/val')
        sess.run(init)

        for ep in tqdm(range(Hp.training_epoch)):
            tr_loss, tr_acc = 0, 0

            for itr in tqdm(range(data.n_batches)):
                # get next batch
                p_batch, q_batch, p_lengths, q_length, ptr_batch = data.next_batch()
                # build a feed dict
                train_dict = {quacc.p_word_inputs: p_batch,
                              quacc.q_word_inputs: q_batch,
                              quacc.p_word_lengths: p_lengths,
                              quacc.q_word_lengths: q_length,
                              quacc.labels: ptr_batch}
                loss, acc = sess.run([quacc.loss, quacc.exact_match], feed_dict=train_dict)
                tr_loss += loss
                tr_acc += acc

                if itr % 100 == 0:
                    # tensorboard
                    summ = sess.run(merged, feed_dict=train_dict)
                    train_writer.add_summary(summ, itr)




if __name__ == '__main__':
    train()
