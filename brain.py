__author__ = 'gkour'

import tensorflow as tf
import tensorflow.contrib.slim as slim
import brain_utils as brain_utils
import numpy as np


class Brain:
    tf.reset_default_graph()
    sess = tf.Session()

    def __init__(self, lr, s_size, action_size, h_size, scope, copy_from):
        self._s_size = s_size
        self._action_size = action_size
        self._h_size = h_size
        self._regularization_param = 0.001

        # Implementing F(state)=action
        self.state_in = tf.placeholder(shape=[None, self._s_size], dtype=tf.float32)
        self.reward_holder = tf.placeholder(shape=[None], dtype=tf.float32)
        self.action_holder = tf.placeholder(shape=[None], dtype=tf.int32)

        self.action_distribution = self._construct_policy_model(scope)

        tf.summary.histogram('Action Probability', self.action_distribution)

        taken_action_probability = Brain.get_decision_probability(self.action_holder, self.action_distribution)

        entropy = tf.reduce_mean(tf.nn.softmax(self.action_distribution) * tf.nn.log_softmax(self.action_distribution))
        self.loss = -tf.reduce_mean(tf.log(taken_action_probability) * self.reward_holder) - 0.1 * entropy

        tf.summary.scalar('loss_act', self.loss)
        self.optimize = tf.train.GradientDescentOptimizer(learning_rate=lr).minimize(self.loss)

        # Initialize Variables
        Brain.sess.run(tf.variables_initializer(tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope)))
        if copy_from is not None:
            Brain.sess.run(brain_utils.update_target_graph(copy_from, scope))

        self.saver = tf.train.Saver()
        self.merged = tf.summary.merge_all()

    def _construct_policy_model(self, scope):
        with tf.variable_scope(scope):
            # imgs = tf.reshape(self.state_in, shape=(-1, 28, 28, 1))
            # net = slim.convolution2d(imgs, 10, [5, 5], scope='conv2_1', padding='VALID')
            # net = slim.max_pool2d(net, [2, 2])
            # net = slim.convolution2d(net, 20, [5, 5], scope='conv2_2', padding='VALID')
            # net = slim.max_pool2d(net, [2, 2])
            # net = slim.flatten(net)

            net = slim.stack(self.state_in, slim.fully_connected, [self._h_size],
                             activation_fn=tf.nn.relu, scope='fc')

            action_output = slim.fully_connected(net, self._action_size, activation_fn=tf.nn.softmax,
                                                 weights_regularizer=slim.l2_regularizer(self._regularization_param),
                                                 scope='fc_act')

        return action_output

    @staticmethod
    def get_decision_probability(actual_decision, decisions_probabilities):
        action_indexes = tf.range(0, tf.shape(decisions_probabilities)[0]) * tf.shape(decisions_probabilities)[
            1] + actual_decision
        return tf.gather(tf.reshape(decisions_probabilities, [-1]), action_indexes)

    def save_model(self, path):
        self.saver.save(Brain.sess, path)

    def load_model(self, path):
        self.saver.restore(Brain.sess, path)

    def act(self, obs):
        action_dist = Brain.sess.run(self.action_distribution, feed_dict={self.state_in: [obs]})
        action = brain_utils.dist_selection(action_dist[0])
        # action = utils.epsilon_greedy(0.01, action_dist[0])
        return action

    def act_dist(self, sess, obs):
        action_dist = sess.run(self.action_distribution, feed_dict={self.state_in: [obs]})
        return action_dist[0]

    def train(self, batch_obs, batch_acts, batch_rews):
        feed_dict = {self.reward_holder: batch_rews,
                     self.action_holder: batch_acts,
                     self.state_in: np.vstack(batch_obs)}

        Brain.sess.run([self.optimize], feed_dict=feed_dict)
