"""
该脚本演示了在MXNet中使用ART的简单示例。
该示例在MNIST数据集上训练一个小模型，并使用快速梯度符号方法创建对抗性示例。
这里我们使用ART分类器来训练模型，也可以为ART分类器提供一个预先训练好的模型。
选择这些参数是为了减少脚本的计算需求，而不是为了提高准确性。"""
import mxnet
from mxnet.gluon.nn import Conv2D, MaxPool2D, Flatten, Dense
import numpy as np

from art.attacks import FastGradientMethod
from art.classifiers import MXClassifier
from art.utils import load_mnist

# Step 1: 加载MNIST数据集 28x28的灰度图 70000张手写数字图(6:1)

(x_train, y_train), (x_test, y_test), min_pixel_value, max_pixel_value = load_mnist()

# Step 1a: 把轴转换到MXNet的NCHW格式

x_train = np.swapaxes(x_train, 1, 3)
x_test = np.swapaxes(x_test, 1, 3)

# Step 2: 创建模型

model = mxnet.gluon.nn.Sequential()
with model.name_scope():
    model.add(Conv2D(channels=4, kernel_size=5, activation='relu'))
    model.add(MaxPool2D(pool_size=2, strides=1))
    model.add(Conv2D(channels=10, kernel_size=5, activation='relu'))
    model.add(MaxPool2D(pool_size=2, strides=1))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(10))
    model.initialize()

loss = mxnet.gluon.loss.SoftmaxCrossEntropyLoss()
trainer = mxnet.gluon.Trainer(model.collect_params(), 'sgd', {'learning_rate': 0.01})

# Step 3: 创建ART分类器

classifier = MXClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), loss=loss,
                          input_shape=(28, 28, 1), nb_classes=10, optimizer=trainer, ctx=None, channel_index=1,
                          defences=None, preprocessing=(0, 1))

# Step 4: 训练ART分类器

classifier.fit(x_train, y_train, batch_size=64, nb_epochs=3)

# Step 5: 在良性的测试实例上评价ART分类器

predictions = classifier.predict(x_test)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on benign test examples: {}%'.format(accuracy * 100))

# Step 6: 生成对抗性测试示例
attack = FastGradientMethod(classifier=classifier, eps=0.2)
x_test_adv = attack.generate(x=x_test)

# Step 7: 通过对抗性测试实例对ART分类器进行评价

predictions = classifier.predict(x_test_adv)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on adversarial test examples: {}%'.format(accuracy * 100))
