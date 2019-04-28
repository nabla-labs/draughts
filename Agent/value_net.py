import numpy as np
import tensorflow as tf


HEIGHT = 8
WIDTH = 8
CHANNELS = 3  # oder 2?
NR_FILTERS = 32
NR_FILTERS2 = 64
POOLING_FILTERS = NR_FILTERS2
KERNEL_SIZE = 3
KERNEL_SIZE2 = 2
ACTIVATION = tf.nn.relu
NODES_FC1 = NR_FILTERS2


class ValueNet:

    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.sess = tf.Session()

        with tf.name_scope("inputs"):
            self.X = tf.placeholder(
                tf.float32, shape=[None, HEIGHT * WIDTH], name="X")
            self.X = tf.reshape(self.X, shape=[-1, HEIGHT, WIDTH, CHANNELS])
            self.y = tf.placeholder(tf.int32, shape=[None], name="y")

            self.conv1 = tf.layers.Conv2D(
                filters=NR_FILTERS, kernel_size=KERNEL_SIZE, activation=ACTIVATION)(self.X)
            self.conv2 = tf.layers.Conv2D(
                filters=NR_FILTERS2, kernel_size=KERNEL_SIZE2, activation=ACTIVATION)(self.conv1)

        with tf.name_scope("pool3"):
            self.pool3 = tf.nn.max_pool(self.conv2, ksize=[1, 2, 2, 1], strides=[
                1, 2, 2, 1], padding="VALID")
            self.pool3_flat = tf.reshape(
                self.pool3, shape=[-1, POOLING_FILTERS * 7 * 7])

        with tf.name_scope("fc1"):
            self.fc1 = tf.layers.Dense(
                NODES_FC1, activation=ACTIVATION, name="fc1")(self.pool3_flat)

        with tf.name_scope("output"):
            self.logits = tf.layers.Dense(1, name="output")(self.fc1)
            self.Y_proba = tf.nn.softmax(self.logits, name="Y_proba")

        with tf.name_scope("train"):
            self.xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
                logits=self.logits, labels=self.y)
            self.loss = tf.reduce_mean(self.xentropy)
            optimizer = tf.train.AdamOptimizer()
            self.training_op = optimizer.minimize(self.loss)

        with tf.name_scope("eval"):
            self.correct = tf.nn.in_top_k(self.logits, self.y, 1)
            self.accuracy = tf.reduce_mean(tf.cast(self.correct, tf.float32))

        with tf.name_scope("init_and_save"):
            self.init = tf.global_variables_initializer()
            self.saver = tf.train.Saver()
        self.sess.run(self.init)

    def predict(state):
        return self.sess.run(self.X, feed_dict={X: state})

    def train(buffered_states):
        self.sess.run(self.training_op, feed_dict={
                      X: buffered_states[:, 0], y: buffered_states[:, 1]})
        self.sess.run(self.accuracy, feed_dict={
                      X: buffered_states[:, 0], y: buffered_states[:, 1]})
        self.saver.save(sess, './my_model_value_net')


if __name__ == '__main__':
    vn = ValueNet(10)
