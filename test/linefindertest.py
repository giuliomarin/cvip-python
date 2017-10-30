import sys
import os
from scipy.misc import imread
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

##################
# Parameters
##################

img_path = '/Users/giulio/Downloads/2017_10_09_10_29_37_color-1-2.png'

num_class_to_show = 5

if len(sys.argv) > 1:
    model_dir = sys.argv[1]
else:
    model_dir = '/Users/giulio/Downloads/train'

####################
# Evaluation
####################

img_raw = imread(img_path)
width = img_raw.shape[1]
height = img_raw.shape[0]
channels = 3
img = np.ones([1, height, width, channels], np.float32)
img[0, :, :, :] = np.asarray(img_raw[:, :, :channels], np.float32)

print '\nEvaluating'
graph = tf.Graph()
with graph.as_default():
    session_conf = tf.ConfigProto(allow_soft_placement=1)
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        # Load the last saved meta graph and restore variables
        checkpoint_dir = os.path.join(model_dir, 'checkpoints')
        checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
        print 'Restoring checkpoint: %s' % checkpoint_file
        saver = tf.train.import_meta_graph('%s.meta' % checkpoint_file)
        saver.restore(sess, checkpoint_file)

        # Get the placeholders from the graph by name
        img_input = graph.get_operation_by_name("img").outputs[0]
        dropout_keep_prob = graph.get_operation_by_name("dropout").outputs[0]

        # Tensors we want to evaluate
        probabilities_node = graph.get_operation_by_name("prediction/probabilities").outputs[0]

        # Compute the predictions
        print 'Compute predictions'
        prob = sess.run(probabilities_node, {img_input: img, dropout_keep_prob: 1.0})

        plt.figure('img')
        plt.imshow(img_raw)
        plt.colorbar()

        plt.figure('pred')
        plt.imshow(prob[0, :, :, 0], cmap=plt.cm.Reds)
        plt.colorbar()
plt.show()