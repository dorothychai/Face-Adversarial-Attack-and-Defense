"""
该脚本演示了一个将ART与Keras结合使用的简单示例。
该示例在MNIST数据集上训练一个小模型，并使用快速梯度符号方法创建对抗性示例。
这里我们使用ART分类器来训练模型，也可以为ART分类器提供一个预先训练好的模型。
选择这些参数是为了减少脚本的计算需求，而不是为了提高准确性。
"""
import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
import numpy as np

from art.attacks import FastGradientMethod
from art.classifiers import KerasClassifier
from art.utils import load_mnist

# Step 1: 加载MNIST数据集 28x28的灰度图 70000张手写数字图(6:1)

(x_train, y_train), (x_test, y_test), min_pixel_value, max_pixel_value = load_mnist()

# Step 2: 创建模型

model = Sequential()
# Keras有两种类型的模型，序贯模型（Sequential）和函数式模型（Model）
# 序贯模型是函数式模型的简略版，为最简单的线性、从头到尾的结构顺序，不分叉。
model.add(Conv2D(filters=4, kernel_size=(5, 5), strides=1, activation='relu', input_shape=(28, 28, 1)))
# (1)model.add 添加层 Conv2D卷积层
# print(model.output_shape)
# (None, 24, 24, 4) 24=28-5+1,4=filters
model.add(MaxPooling2D(pool_size=(2, 2)))
# (None,12,12,4) 12=(24*24 / 2*2)开根号,4=filters
# 添加池化层
model.add(Conv2D(filters=10, kernel_size=(5, 5), strides=1, activation='relu', input_shape=(23, 23, 4)))
# (None,8,8,10) 8=12-5+1,10=filters
model.add(MaxPooling2D(pool_size=(2, 2)))
# (None, 4, 4, 10) 4=(8*8 / 4*4),10=filters
model.add(Flatten())
# Reshape
# (None, 160) 160=4*4*10
model.add(Dense(100, activation='relu'))
# (None, 100) 100=100
model.add(Dense(10, activation='softmax'))
# (None, 10) 10=10

model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.SGD(lr=0.01), metrics=['accuracy'])
# (None, 10)
# (2)model.compile 模型训练的BP模式设置

# Step 3: 创建ART分类器

classifier = KerasClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), use_logits=False)

# Step 4: 训练ART分类器 loss越来越低，accuracy越来越高的过程

classifier.fit(x_train, y_train, batch_size=64, nb_epochs=3)
# epoch：1个epoch表示过了1遍训练集或测试集中的所有样本
# iteration：表示1次迭代（也叫training step），每次迭代更新1次网络结构的参数
# batch-size：1次迭代所使用的样本量

# 常用带mini-batch的随机梯度下降算法（Stochastic Gradient Descent, SGD）训练深层结构，
# 它有一个好处就是并不需要遍历全部的样本，当数据量非常大时十分有效。
# 可根据实际问题来定义epoch，例如定义10000次迭代为1个epoch：
# 若每次迭代的batch-size设为256，那么1个epoch相当于过了2560000个训练样本。


# Step 5: 在良性的测试实例上评价ART分类器

predictions = classifier.predict(x_test)
# print(predictions.size) 10000
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on benign test examples: {}%'.format(accuracy * 100))

# Step 6: 生成对抗性测试示例
attack = FastGradientMethod(classifier=classifier, eps=0.2)
x_test_adv = attack.generate(x=x_test)

# Step 7: 通过对抗性测试实例对ART分类器进行评价

predictions = classifier.predict(x_test_adv)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on adversarial test examples: {}%'.format(accuracy * 100))
