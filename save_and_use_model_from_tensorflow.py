import tensorflow as tf
import numpy as np
import time
from tensorflow.examples.tutorials.mnist import input_data

print("Start get data")
mnist = input_data.read_data_sets('MNIST_data', one_hot=False)
print("Finish get data")
x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.int32, [None, ])
input_layer = tf.reshape(x, [-1, 28, 28, 1])
conv1 = tf.layers.conv2d(
    inputs=input_layer,
    filters=32,
    kernel_size=[5, 5],
    padding="same",
    activation=tf.nn.relu)
pool1 = tf.layers.max_pooling2d(
    inputs=conv1,
    pool_size=[2, 2],
    strides=2)
conv2 = tf.layers.conv2d(
    inputs=pool1,
    filters=64,
    kernel_size=[5, 5],
    padding="same",
    activation=tf.nn.relu)
pool2 = tf.layers.max_pooling2d(
    inputs=conv2,
    pool_size=[2, 2],
    strides=2)
pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])
dense = tf.layers.dense(
    inputs=pool2_flat,
    units=1024,
    activation=tf.nn.relu)
dropout = tf.layers.dropout(
    inputs=dense,
    rate=0.4)
logits = tf.layers.dense(inputs=dropout, units=10)
loss = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=logits)
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
train_op = optimizer.minimize(
    loss=loss,
    global_step=tf.train.get_global_step())
correct_prediction = tf.equal(tf.cast(tf.argmax(logits, 1), tf.int32), y_)
acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

saver = tf.train.Saver(max_to_keep=2)

for i in range(100):
    max_acc = 0
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_op, feed_dict={x: batch_xs, y_: batch_ys})
    val_loss, val_acc = sess.run([loss, acc], feed_dict={x: mnist.test.images[:100], y_: mnist.test.labels[:100]})
    print('epoch:%d, val_loss:%f, val_acc:%f' % (i, val_loss, val_acc))
    if val_acc > max_acc:
        max_acc = val_acc
        saver.save(sess, '/home/lian/Work/work_test/', global_step=i + 1)
sess.close()


model_file = tf.train.latest_checkpoint('/home/lian/Work/work/')
saver = tf.train.import_meta_graph('/home/lian/Work/work/model.ckpt-20000.meta')
saver.restore(sess, model_file)

for i in range(100):
    val_loss, val_acc = sess.run([loss, acc], feed_dict={x: mnist.test.images[i * 100:i * 101],
                                                         y_: mnist.test.labels[i * 100:i * 101]})
    print('val_loss:%f, val_acc:%f' % (val_loss, val_acc))
