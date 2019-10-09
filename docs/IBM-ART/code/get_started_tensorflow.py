# coding=utf-8
import tensorflow as tf
import numpy as np

from art.attacks import FastGradientMethod
from art.classifiers import TFClassifier
from art.utils import load_mnist
import time

start = time.clock()

# Step 1: 加载MNIST数据集 28x28的灰度图 70000张手写数字图(6:1)

(x_train, y_train), (x_test, y_test), min_pixel_value, max_pixel_value = load_mnist()

# print(x_train.shape) # (60000,28,28,1)  len(x_train)=60000
# print(y_train.shape) # (60000,10)  len(y_train)=60000
# print(x_test.shape) # (10000,28,28,1)
# print(y_test.shape) # (10000,10)

# Step 2: 创建模型

input_ph = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
# 此函数可以理解为形参，用于定义过程，在执行的时候再赋具体的值
# shape包含：batch, in_height, in_width, in_channels
labels_ph = tf.placeholder(tf.int32, shape=[None, 10])

# 第一个卷积层
x = tf.layers.conv2d(input_ph, filters=4, kernel_size=5, activation=tf.nn.relu)
# tf.layers.conv2d(inputs, filters个数=输出层深度, kernel_size, activation)
# 创造一个卷积核kernel,将输入进行卷积来输出一个tensor
# x是输入层的下一层=28-5+1=24 (?,24,24,4)
# 第一个池化层 又称“降采样” 其意义在于能够对输入进行抽象描述
# 卷积层、池化层和激活函数层：将原始数据映射到隐层特征空间
x = tf.layers.max_pooling2d(x, 2, 2)  # (?,12,12,4)
# x是MaxPool后的下一层 (24*24 / 2*2)然后开根号=12 (?,12,12,4)
# 第二个卷积层
x = tf.layers.conv2d(x, filters=10, kernel_size=5, activation=tf.nn.relu)  # 12-5+1=8 (?,8,8,10)
# 第二个池化层
x = tf.layers.max_pooling2d(x, 2, 2)  # (?,4,4,10)
x = tf.contrib.layers.flatten(x)
# Reshape 把x保留在第一个维度，把第一个维度包含的每一个子张量展开成一个行向量
# (?,160) 160=(?,4,4,10)=4*4*10=160
# 返回张量是一个二维的 shape=(batch_size,...) 一般用于卷积神经网络全连接层前的预处理
x = tf.layers.dense(x, 100, activation=tf.nn.relu)  # (?,100)
# dense ：全连接层(用于特征降维) 相当于添加一个层
# 主要目的就是维度变换，把高维的数据（分布式特征表示）变成低维（样本标记）
# 全连接层：将学到的“分布式特征表示”映射到样本标记空间 猫在哪儿我不管，我只要猫
# 全连接层之前：提取特征  全连接层：分类
logits = tf.layers.dense(x, 10)  # (?,10) print(logits.get_shape())

loss = tf.reduce_mean(tf.losses.softmax_cross_entropy(logits=logits, onehot_labels=labels_ph))
# Tensor("Mean:0", shape=(), dtype=float32)
# 计算张量tensor沿着指定的数轴（tensor某一维度）上的的平均值，主要用作降维或者计算tensor（图像）的平均值
# tf.losses.softmax_cross_entropy主要用于进行不同样本的loss计算
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
# tf.train.GradientDescentOptimizer是tf的常用优化器,实现的是梯度下降算法
# 需要资源更少、令模型收敛更快的最优化算法，才能从根本上加速机器的学习速度和效果
# 梯度下降法，是当今最流行的优化（optimization）算法，亦是至今最常用的优化神经网络的方法
train = optimizer.minimize(loss)
sess = tf.Session()
sess.run(tf.global_variables_initializer())
# global_variables_initializer()创建初始化的节点 sess.run执行这个节点的操作

# Step 3: 创建ART分类器

classifier = TFClassifier(clip_values=(min_pixel_value, max_pixel_value), input_ph=input_ph, output=logits,
                          labels_ph=labels_ph, train=train, loss=loss, learning=None, sess=sess)

# Step 4: 训练ART分类器

classifier.fit(x_train, y_train, batch_size=64, nb_epochs=3)

# Step 5: 在良性的测试实例上评价ART分类器

predictions = classifier.predict(x_test)
# (10000, 10) 对10000个testing image的数字进行预测0-9
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on benign test examples: {}%'.format(accuracy * 100))
# 对10000个testing image的数字进行预测，与10000个已有的label进行对比

# Step 6: 生成对抗性测试示例

attack = FastGradientMethod(classifier=classifier, eps=0.2)
x_test_adv = attack.generate(x=x_test)
# print(x_test_adv.shape) (10000, 28, 28, 1)

# Step 7: 通过对抗性测试实例对ART分类器进行评价

predictions = classifier.predict(x_test_adv)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on adversarial test examples: {}%'.format(accuracy * 100))
# 对10000个testing image生成对抗图片,然后用分类器对这10000个攻击进行预测

elapsed = (time.clock() - start)
print("Time used:", elapsed)
