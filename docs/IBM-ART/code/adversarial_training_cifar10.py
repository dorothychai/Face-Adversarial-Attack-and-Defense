# -*- coding: utf-8 -*-
"""
在CIFAR-10数据集上训练卷积神经网络，然后使用DeepFool攻击生成对抗性图像，并在用对抗性图像增强的训练集上对网络进行再训练。"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import keras.backend as k
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Activation, Dropout
import numpy as np

from art.attacks import DeepFool
from art.classifiers import KerasClassifier
from art.utils import load_dataset
import time

start = time.clock()

# 配置一个日志程序来捕获ART的输出，这些结果是打印在控制台的，详细级别设置为INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 读取CIFAR10数据集 60000(5:1)张color图 32x32x3(通道:RGB) 0-9label 分为10个类，每类6000张图 这10类都是各自独立的，不会出现重叠
(x_train, y_train), (x_test, y_test), min_, max_ = load_dataset(str('cifar10'))
# x_train.shape=(50000, 32, 32, 3)  y_train.shape=(50000, 10)
# x_test.shape=(10000,32,32,3)  y_test.shape=(10000,10)
x_train, y_train = x_train[:5000], y_train[:5000]
# train取训练集的前5000个image
x_test, y_test = x_test[:500], y_test[:500]
# test取测试集的前500个image
im_shape = x_train[0].shape  # (32,32,3)

# 创建Keras卷积神经网络- Keras示例的基本架构
# Source here: https://github.com/keras-team/keras/blob/master/examples/cifar10_cnn.py
model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]))
# model.shape = (None,32,32,32)
# Conv2D(filters=输出空间的维度,kernel_size=2D卷积窗口的宽度和高度)
# 2D 卷积层 (例如对图像的空间卷积),该层创建了一个卷积核,对输入层进行卷积,以生成输出张量
# 当使用该层作为模型第一层时，需要提供 input_shape 参数
# 例如input_shape=x_train.shape[1:] (32,32,3) 表示一个32x32的RGB图像
# padding='same'时，输出大小=输入大小/步长,然后向上取整
# padding='valid'时,输出大小=(输入大小-滤波器大小+1)/步长,然后向上取整
# 所以第一、二个32=输入大小32/步长1，然后向上取整 第三个32=filters
# padding 存在的意义在于:不丢弃原图信息,保持feature map的大小与原图一致,
# 让更深层的layer的input依旧保持有足够大的信息量,为了实现目的且不做多余的事情，padding出来的pixel的值都是0不存在噪音问题
model.add(Activation('relu'))
# model.shape = (None,32,32,32)
model.add(Conv2D(32, (3, 3)))
# model.shape = (None, 30, 30, 32)   padding默认='valid'
# 30 = 输入大小32-滤波器大小3+1
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.shape = (None, 15, 15, 32)
model.add(Dropout(0.25))
# model.shape = (None, 15, 15, 32)
# Dropout层用于防止过拟合：为输入数据加入Dropout，在训练过程中随机地“抛弃”一些神经元
# 在训练过程中每次更新参数时按一定概率（rate）随机断开输入神经元
# keras.layers.core.Dropout(rate, noise_shape=None, seed=None)
# 丢弃率rate：0~1的浮点数，控制需要断开的神经元的比例
# 20%就是说每轮迭代时每五个输入值就会被随机抛弃一个

model.add(Conv2D(64, (3, 3), padding='same'))
# model.shape = (None, 15, 15, 64) 15/1=15
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))  # 默认padding是'valid'
# model.shape = (None, 13, 13, 64) (15-3+1)/1=13
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.shape = (None, 6, 6, 64)  13/2向下取整=6
model.add(Dropout(0.25))

model.add(Flatten())
# model.shape = (None, 2304) 2304=6*6*64
model.add(Dense(512))
# model.shape = (None, 512)
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(10))
# model.shape = (None, 10)
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.shape = (None, 10)
print(model.output_shape)

# 创建分类器包装器classifier wrapper
classifier = KerasClassifier(model=model, clip_values=(min_, max_))
classifier.fit(x_train, y_train, nb_epochs=10, batch_size=128)
# classifier._output = 0
# classifier.input_shape = (32,32,3)
# epoch：1个epoch等于使用训练集中的全部样本训练一次
# batchsize：批大小,一般采用SGD训练，每次训练在训练集中取batchsize个样本训练
# iteration：1个iteration等于使用batchsize个样本训练一次
# 训练集有1000个样本，batchsize=10，那么训练完整个样本集需要：100次iteration，1次epoch

# 用DeepFool制作对抗性样本
logger.info('Create DeepFool attack')
adv_crafter = DeepFool(classifier)  # 针对classifier训练一个对抗性的classifier
logger.info('Craft attack on training examples')
x_train_adv = adv_crafter.generate(x_train)  # 用对抗性的classifier去训练image--对抗性示例
logger.info('Craft attack on testing examples')
x_test_adv = adv_crafter.generate(x_test)

# 在对抗性样本上评价分类器
preds = np.argmax(classifier.predict(x_test_adv), axis=1)
acc = np.sum(preds == np.argmax(y_test, axis=1)) / y_test.shape[0]
logger.info('---Before adversarial training---')
logger.info('Classifier before adversarial training')
logger.info('Accuracy on adversarial samples: %.2f%%', (acc * 100))

# 数据扩充:用对抗性样本展开训练集
x_train = np.append(x_train, x_train_adv, axis=0)  # 5000+5000=10000
# axis = 0 代表对横轴操作 axis = 1 代表对纵轴操作
y_train = np.append(y_train, y_train, axis=0)  # 5000+5000=10000

# 在扩展数据集上重新训练CNN
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
classifier.fit(x_train, y_train, nb_epochs=10, batch_size=128)

# 用测试集评估经过对抗例子训练的分类器
preds = np.argmax(classifier.predict(x_test_adv), axis=1)
acc = np.sum(preds == np.argmax(y_test, axis=1)) / y_test.shape[0]
logger.info('---After adversarial training---')
logger.info('Classifier with adversarial training')
logger.info('Accuracy on adversarial samples: %.2f%%', (acc * 100))

elapsed = (time.clock() - start)
print("Time used:", elapsed)
