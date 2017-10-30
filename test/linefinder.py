import os
import numpy as np
from scipy.misc import imread
import matplotlib.pyplot as plt
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

plt.ion()

class NetCNN(object):
    """
    CNN for line finder.
    """
    def __init__(self, width, height, channels):

        #######################
        # Input
        #######################

        # Placeholders for input, output and dropout
        self.img = tf.placeholder(tf.float32, [None, width, height, channels], name="img")
        self.gt = tf.placeholder(tf.float32, [None, width, height, 1], name="gt")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout")

        #######################
        # Hidden layers
        #######################

        # Create a convolution + maxpool layer
        with tf.variable_scope("conv-maxpool-1"):
            self.W = tf.Variable(tf.truncated_normal([5, 5, channels, 1], stddev=0.1), name="W")
            self.b = tf.Variable(tf.constant(0.1, shape=[1]), name="b")
            conv = tf.nn.conv2d(self.img, self.W, strides=[1, 1, 1, 1], padding="SAME", name="conv")
            conv1 = tf.nn.relu(tf.nn.bias_add(conv, self.b), name="relu")

        with tf.variable_scope("conv-maxpool-2"):
            W = tf.Variable(tf.truncated_normal([15, 15, 1, 1], stddev=0.1), name="W")
            b = tf.Variable(tf.constant(0.1, shape=[1]), name="b")
            conv = tf.nn.conv2d(conv1, W, strides=[1, 1, 1, 1], padding="SAME", name="conv")
            conv2 = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")

        with tf.variable_scope("conv-maxpool-3"):
            W = tf.Variable(tf.truncated_normal([15, 15, 1, 1], stddev=0.1), name="W")
            b = tf.Variable(tf.constant(0.1, shape=[1]), name="b")
            conv = tf.nn.conv2d(conv2, W, strides=[1, 1, 1, 1], padding="SAME", name="conv")
            conv3 = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")

        with tf.variable_scope("conv-maxpool-4"):
            W = tf.Variable(tf.truncated_normal([25, 25, 1, 1], stddev=0.1), name="W")
            b = tf.Variable(tf.constant(0.1, shape=[1]), name="b")
            conv = tf.nn.conv2d(conv3, W, strides=[1, 1, 1, 1], padding="SAME", name="conv")
            conv4 = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")

        # Prediction
        with tf.variable_scope('prediction'):
            self.features_drop = tf.nn.dropout(conv4, self.dropout_keep_prob)
            self.maxpool = tf.nn.max_pool(self.features_drop, ksize=[1, height, width, 1], strides=[1, 1, 1, 1], padding='VALID')
            self.probabilities = tf.divide(self.features_drop, self.maxpool, name="probabilities")

        # Optimization
        with tf.variable_scope('optimization'):
            weight_loss = tf.multiply(300.0, tf.cast(tf.equal(self.gt, 1), tf.float32)) + 1
            self.loss = tf.losses.absolute_difference(self.gt, self.probabilities, weights=weight_loss)
            self.global_step = tf.Variable(0, name="global_step", trainable=False)
            self.learning_rate = tf.placeholder(tf.float32, name='learning_rate')
            self.optimizer = tf.train.AdagradOptimizer(self.learning_rate).minimize(self.loss, global_step=self.global_step, name="optimizer")

        # Initializer
        self.init = tf.global_variables_initializer()

# Test network
if __name__ == '__main__':
    ###############
    # Prepare data
    ###############

    num_epochs = 100
    num_checkpoints = 100
    checkpoint_every = 1

    data_dir = '/Users/giulio/Downloads/var0_line1_crop300_resize_conv'
    out_dir = '/Users/giulio/Downloads/train'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    print '\nOutput folder: %s' % out_dir
    print 'For debugging: tensorboard --logdir %s' % os.path.join(out_dir, "summaries")

    rows = open('/Users/giulio/Downloads/videolistFull.txt', 'r').readlines()

    def loaddata(r):
        img_raw = np.asarray(imread('%s/%s_color.png' % (data_dir, r)), np.float32)
        gt_raw = np.asarray(imread('%s/%s_label.png' % (data_dir, r)), np.float32) / 255.0

        width = img_raw.shape[1]
        height = img_raw.shape[0]
        channels = img_raw.shape[2]

        img = np.ones([1, height, width, channels], np.float32)
        img[0, :, :, :] = img_raw

        gt = np.ones([1, height, width, 1], np.float32)
        gt[0, :, :, 0] = gt_raw
        return img, gt

    img, gt = loaddata('2017_10_09_10_29_37')

    width = img.shape[2]
    height = img.shape[1]
    channels = img.shape[3]

    ###############
    # Test training
    ###############

    with tf.Session() as sess:
        cnn = NetCNN(width, height, channels)

        # Initialize model
        sess.run(cnn.init)

        img_test, gt_test = loaddata('2017_10_09_10_29_37')
        feed_dict_test = {
            cnn.img: img_test,
            cnn.dropout_keep_prob: 1,
        }
        # plt.figure('img')
        # plt.imshow(img_test[0, :, :, :3])
        # plt.colorbar()
        # plt.figure('gt')
        # plt.imshow(gt_test[0, :, :, 0], cmap=plt.cm.Reds)
        # plt.colorbar()

        # Summaries for loss and probabilities
        loss_summary = tf.summary.scalar("loss", cnn.loss)
        probabilities_summaries = tf.summary.image("plot", cnn.probabilities)

        # Train Summaries
        train_summary_op = tf.summary.merge([loss_summary, probabilities_summaries])
        train_summary_dir = os.path.join(out_dir, "summaries", "train")
        train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

        # Test Summaries
        test_summary_op = tf.summary.merge([probabilities_summaries])
        test_summary_dir = os.path.join(out_dir, "summaries", "test")
        test_summary_writer = tf.summary.FileWriter(test_summary_dir, sess.graph)

        # Checkpoint directory
        checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
        checkpoint_prefix = os.path.join(checkpoint_dir, "model")
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=num_checkpoints)

        current_step = 0
        for e in range(num_epochs):
            print 'Epoch %d' % e
            for i, r in enumerate(rows):
                img, gt = loaddata(r.strip())
                feed_dict = {
                    cnn.img: img,
                    cnn.gt: gt,
                    cnn.dropout_keep_prob: 0.5,
                    cnn.learning_rate: 0.01
                }
                _, train_summaries, loss, prob, W, b, maxpool = sess.run([cnn.optimizer, train_summary_op, cnn.loss, cnn.probabilities, cnn.W, cnn.b, cnn.maxpool], feed_dict)
                print '[%d] loss: %f' % (i, loss)
                current_step = tf.train.global_step(sess, cnn.global_step)
                train_summary_writer.add_summary(train_summaries, current_step)

            if e % checkpoint_every == 0:
                checkpoint_path = saver.save(sess, checkpoint_prefix, global_step=e)

            # Run one test iteration
            prob, test_summaries = sess.run([cnn.probabilities, test_summary_op], feed_dict_test)
            test_summary_writer.add_summary(test_summaries, current_step)
            # plt.figure('pred')
            # # plt.clf()
            # plt.imshow(prob[0, :, :, 0], cmap=plt.cm.Reds)
            # # plt.colorbar()
            # plt.draw()
            # plt.pause(0.01)

plt.ioff()
plt.show()
