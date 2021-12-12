# code adapted from https://github.com/GPSingularity/Deep-Learning-in-TensorFlow/blob/master/NeuralNet.ipynb
import os
import tensorflow as tf
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import cv2
from django.conf import settings
from tensorflow.examples.tutorials.mnist import input_data  # importing input_data python file
from tensorflow.contrib.tensorboard.plugins import projector
import subprocess

media_root = settings.MEDIA_ROOT.replace('\\', '/')
inputDir = media_root + "/uby/"
DIR = media_root + "/graph-images/"
logs_path = media_root + "/logs/embedding/"  # path to the folder that we want to save the logs for Tensorboard


# input_data file imports read_data_sets from mnist.py

img_h = img_w = 100

def start():
    """ Sets up the hyperparameters. """
    for file in os.listdir(inputDir):
        path = os.path.join(inputDir, file)
        ext = os.path.splitext(path)[-1].lower()
        if ext != ".gz":
            raise Exception('please make sure all input files are in gz format')
    global candlestick
    candlestick = input_data.read_data_sets(inputDir, one_hot=True)

    learning_rate = 0.001  # The optimization learning rate

    epochs = 10  # Total number of training epochs

    batch_size = 100  # Training batch size

    display_freq = 100  # Frequency of displaying the training results

    # We know that candlestick images are 28 pixels in each dimension.
    img_h = img_w = 100

    # Images are stored in one-dimensional arrays of this length.
    img_size_flat = img_h * img_w

    # Number of classes, one class for each of 10 digits.
    n_classes = 10

    # number of units in the first hidden layer
    h1 = 200

    return inputDir, h1, n_classes, img_size_flat, img_w, img_h, display_freq, batch_size, epochs, learning_rate, logs_path, candlestick


# weight and bias wrappers
def weight_variable(name, shape):
    """
    Create a weight variable with appropriate initialization
    :param name: weight name
    :param shape: weight shape
    :return: initialized weight variable
    """
    initer = tf.truncated_normal_initializer(stddev=0.01)
    return tf.get_variable('W_' + name,
                           dtype=tf.float32,
                           shape=shape,
                           initializer=initer)


def bias_variable(name, shape):
    """
    Create a bias variable with appropriate initialization
    :param name: bias variable name
    :param shape: bias variable shape
    :return: initialized bias variable
    """
    initial = tf.constant(0., shape=shape, dtype=tf.float32)
    return tf.get_variable('b_' + name,
                           dtype=tf.float32,
                           initializer=initial)


def fc_layer(x, num_units, name, use_relu=True):
    """
    Create a fully-connected layer
    :param x: input from previous layer
    :param num_units: number of hidden units in the fully-connected layer
    :param name: layer name
    :param use_relu: boolean to add ReLU non-linearity (or not)
    :return: The output array
    """
    with tf.variable_scope(name, reuse=tf.AUTO_REUSE):
        in_dim = x.get_shape()[1]
        W = weight_variable(name, shape=[in_dim, num_units])
        tf.summary.histogram('W', W)
        b = bias_variable(name, [num_units])
        tf.summary.histogram('b', b)
        layer = tf.matmul(x, W)
        layer += b
        if use_relu:
            layer = tf.nn.relu(layer)
        return layer




def createNet(variables):
    """ Creates the a tensorflow session. """
    inputDir = variables[0]
    h1 = variables[1]
    n_classes = variables[2]
    img_size_flat = variables[3]
    img_w = variables[4]
    img_h = variables[5]
    display_freq = variables[6]
    batch_size = variables[7]
    epochs = variables[8]
    learning_rate = variables[9]
    logs_path = variables[10]
    candlestick = variables[11]
    with tf.variable_scope('Input', reuse=tf.AUTO_REUSE):
        x = tf.placeholder(tf.float32, shape=[None, img_size_flat], name='X')

        tf.summary.image('input_image', tf.reshape(x, (-1, img_w, img_h, 1)), max_outputs=5)

        y = tf.placeholder(tf.float32, shape=[None, n_classes], name='Y')
    fc1 = fc_layer(x, h1, 'Hidden_layer', use_relu=True)

    output_logits = fc_layer(fc1, n_classes, 'Output_layer', use_relu=False)

    # Define the loss function, optimizer, and accuracy
    with tf.variable_scope('Train', reuse=tf.AUTO_REUSE):
        with tf.variable_scope('Loss', reuse=tf.AUTO_REUSE):
            loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=output_logits), name='loss')
            tf.summary.scalar('loss', loss)
        with tf.variable_scope('Optimizer', reuse=tf.AUTO_REUSE):
            optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate, name='Adam-op').minimize(loss)
        with tf.variable_scope('Accuracy', reuse=tf.AUTO_REUSE):
            correct_prediction = tf.equal(tf.argmax(output_logits, 1), tf.argmax(y, 1), name='correct_pred')

            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')
            tf.summary.scalar('accuracy', accuracy)
            # Network predictions
            cls_prediction = tf.argmax(output_logits, axis=1, name='predictions')

    # Initializing the variables
    init = tf.global_variables_initializer()
    merged = tf.summary.merge_all()
    return inputDir, h1, n_classes, img_size_flat, img_w, img_h, display_freq, batch_size, epochs, learning_rate, logs_path, candlestick, x, y, fc1, output_logits, loss, optimizer, correct_prediction, accuracy, cls_prediction, init, merged



def train(variables):
    """ Trains the neural network in the tensorflow session. """
    inputDir = variables[0]
    h1 = variables[1]
    n_classes = variables[2]
    img_size_flat = variables[3]
    img_w = variables[4]
    img_h = variables[5]
    display_freq = variables[6]
    batch_size = variables[7]
    epochs = variables[8]
    learning_rate = variables[9]
    logs_path = variables[10]
    candlestick = variables[11]
    x = variables[12]
    y = variables[13]
    fc1 = variables[14]
    output_logits = variables[15]
    loss = variables[16]
    optimizer = variables[17]
    correct_prediction = variables[18]
    accuracy = variables[19]
    cls_prediction = variables[20]
    init = variables[21]
    merged = variables[22]

    sess = tf.InteractiveSession()  # using InteractiveSession instead of Session to test network in separate cell
    sess.run(init)
    train_writer = tf.summary.FileWriter(logs_path, sess.graph)
    num_tr_iter = int(candlestick.train.num_examples / batch_size)
    global_step = 0
    for epoch in range(epochs):
        # print('Training epoch: {}'.format(epoch + 1))
        for iteration in range(num_tr_iter):
            batch_x, batch_y = candlestick.train.next_batch(batch_size)
            global_step += 1
            # Run optimization op (backprop)
            feed_dict_batch = {x: batch_x, y: batch_y}
            _, summary_tr = sess.run([optimizer, merged], feed_dict=feed_dict_batch)
            train_writer.add_summary(summary_tr, global_step)

            if iteration % display_freq == 0:
                # Calculate and display the batch loss and accuracy
                loss_batch, acc_batch = sess.run([loss, accuracy],
                                                 feed_dict=feed_dict_batch)

        feed_dict_valid = {x: candlestick.validation.images, y: candlestick.validation.labels}
        loss_valid, acc_valid = sess.run([loss, accuracy], feed_dict=feed_dict_valid)

    return inputDir, h1, n_classes, img_size_flat, img_w, img_h, display_freq, batch_size, epochs, learning_rate, logs_path, candlestick, x, y, fc1, output_logits, loss, optimizer, correct_prediction, accuracy, cls_prediction, init, merged, sess, train_writer, num_tr_iter, global_step




# Load the test set

def presprites(variables):
    """ Creates the metadata.tsv file """
    inputDir = variables[0]
    h1 = variables[1]
    n_classes = variables[2]
    img_size_flat = variables[3]
    img_w = variables[4]
    img_h = variables[5]
    display_freq = variables[6]
    batch_size = variables[7]
    epochs = variables[8]
    learning_rate = variables[9]
    logs_path = variables[10]
    candlestick = variables[11]
    x = variables[12]
    y = variables[13]
    fc1 = variables[14]
    output_logits = variables[15]
    loss = variables[16]
    optimizer = variables[17]
    correct_prediction = variables[18]
    accuracy = variables[19]
    cls_prediction = variables[20]
    init = variables[21]
    merged = variables[22]
    sess = variables[23]
    train_writer = variables[24]
    num_tr_iter = variables[25]
    global_step = variables[26]

    x_test = candlestick.test.images
    y_test = candlestick.test.labels

    # Initialize the embedding variable with the shape of our desired tensor
    tensor_shape = (x_test.shape[0], fc1.get_shape()[1].value)  # [test_set , h1] = [10000 , 200]
    embedding_var = tf.Variable(tf.zeros(tensor_shape),
                                name='fc1_embedding')
    # assign the tensor that we want to visualize to the embedding variable
    embedding_assign = embedding_var.assign(fc1)


    # Create a config object to write the configuration parameters
    config = projector.ProjectorConfig()

    # Add embedding variable
    embedding = config.embeddings.add()
    embedding.tensor_name = embedding_var.name

    # Link this tensor to its metadata file (e.g. labels) -> we will create this file later
    embedding.metadata_path = logs_path + 'metadata.tsv'

    # Specify where you find the sprite. -> we will create this image later
    embedding.sprite.image_path = logs_path + 'sprite_images.png'
    embedding.sprite.single_image_dim.extend([img_w, img_h])

    # Write a projector_config.pbtxt in the logs_path.
    # TensorBoard will read this file during startup.
    projector.visualize_embeddings(train_writer, config)

    # Run session to evaluate the tensor
    x_test_fc1 = sess.run(embedding_assign, feed_dict={x: x_test})

    # Save the tensor in model.ckpt file
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(logs_path, "model.ckpt"), global_step)

    return inputDir, h1, n_classes, img_size_flat, img_w, img_h, display_freq, batch_size, epochs, learning_rate, logs_path, candlestick, x, y, fc1, output_logits, loss, optimizer, correct_prediction, accuracy, cls_prediction, init, merged, sess, train_writer, num_tr_iter, global_step, x_test, y_test, tensor_shape, embedding_var, embedding_assign, config, embedding, x_test_fc1, saver



def write_sprite_image(filename, images):
    """
        Create a sprite image consisting of sample images
        :param filename: name of the file to save on disk
        :param shape: tensor of flattened images
    """

    # Invert grayscale image
    images = 1 - images

    # Calculate number of plot
    n_plots = int(np.ceil(np.sqrt(images.shape[0])))

    # Make the background of sprite image
    sprite_image = np.ones((img_h * n_plots, img_w * n_plots))

    for i in range(n_plots):
        for j in range(n_plots):
            img_idx = i * n_plots + j
            if img_idx < images.shape[0]:
                img = images[img_idx]
                sprite_image[i * img_h:(i + 1) * img_h,
                j * img_w:(j + 1) * img_w] = img

    plt.imsave(filename, sprite_image, cmap='BrBG')




#remember to change this to a temp

def getlabels():
    """ Generate the labels. """
    filename_list = []
    for img in os.listdir(DIR):
        path = os.path.join(DIR, img)
        new_path = path.split('/')[-1]
        new_path_str = str(new_path)
        filename_list.append(new_path_str)

    return filename_list


def write_metadata(filename, labels, filename_list):
    """
            Create a metadata file image consisting of sample indices and labels
            :param filename: name of the file to save on disk
            :param shape: tensor of labels
    """

    with open(filename, 'w') as f:
        f.write("Filename\tLabel\n")
        counter = 0
        for index, label in enumerate(labels):
            f.write("{}\t{}\n".format(filename_list[counter], label))
            counter += 1






def final(variables):
    """ Creates logs/embeddings. """
    # Reshape images from vector to matrix
    x_test_images = 0
    x_test_labels = 0
    inputDir = variables[0]
    h1 = variables[1]
    n_classes = variables[2]
    img_size_flat = variables[3]
    img_w = variables[4]
    img_h = variables[5]
    display_freq = variables[6]
    batch_size = variables[7]
    epochs = variables[8]
    learning_rate = variables[9]
    logs_path = variables[10]
    candlestick = variables[11]
    x = variables[12]
    y = variables[13]
    fc1 = variables[14]
    output_logits = variables[15]
    loss = variables[16]
    optimizer = variables[17]
    correct_prediction = variables[18]
    accuracy = variables[19]
    cls_prediction = variables[20]
    init = variables[21]
    merged = variables[22]
    sess = variables[23]
    train_writer = variables[24]
    num_tr_iter = variables[25]
    global_step = variables[26]
    x_test = variables[27]
    y_test = variables[28]
    tensor_shape = variables[29]
    embedding_var = variables[30]
    embedding_assign = variables[31]
    config = variables[32]
    embedding = variables[33]
    x_test_fc1 = variables[34]
    saver = variables[35]
    filename_list = getlabels()

    x_test_images = np.reshape(np.array(x_test), (-1, img_w, img_h))
    # Reshape labels from one-hot-encode to index
    x_test_labels = np.argmax(y_test, axis=1)


    write_sprite_image(os.path.join(logs_path, 'sprite_images.png'), x_test_images)
    write_metadata(os.path.join(logs_path, 'metadata.tsv'), x_test_labels, filename_list)
    sess.close()


def run():
    final(presprites(train(createNet(start()))))


def run1(variable):
    final(presprites(train(variable)))
