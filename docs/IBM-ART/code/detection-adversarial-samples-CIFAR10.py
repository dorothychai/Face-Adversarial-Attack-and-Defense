"""
演示使用ART检测对抗性样本.
我们的分类器是针对CIFAR-10图像数据集的ResNet架构.
"""

# 1. 加载必要条件和数据

import warnings
warnings.filterwarnings('ignore')

from keras.models import load_model

from art import DATA_PATH
from art.utils import load_dataset, get_file
from art.classifiers import KerasClassifier
from art.attacks import FastGradientMethod
from art.detection import BinaryInputDetector

import numpy as np
# matplotlib inline
import matplotlib.pyplot as plt

# 1.1 加载CIFAR10数据集和类描述
(x_train, y_train), (x_test, y_test), min_, max_ = load_dataset('cifar10')

num_samples_train = 100
num_samples_test = 100
x_train = x_train[0:num_samples_train]  # 取训练集50000张的前100张
y_train = y_train[0:num_samples_train]  # 100
x_test = x_test[0:num_samples_test]  # 取训练集10000张的前100张
y_test = y_test[0:num_samples_test]  # 100
# 10个类
class_descr = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# 2. 评估分类器

# 2.1 加载预训练分类器(一种ResNet架构)
path = get_file('cifar_resnet.h5',extract=False, path=DATA_PATH,
                url='https://www.dropbox.com/s/ta75pl4krya5djj/cifar_resnet.h5?dl=1')
classifier_model = load_model(path)
classifier = KerasClassifier(clip_values=(min_, max_), model=classifier_model, use_logits=False, preprocessing=(0.5, 1))
classifier_model.summary()
"""
Total params: 470,218
Trainable params: 467,946
Non-trainable params: 2,272
"""

# 2.2 在前100张测试图像上评估分类器
x_test_pred = np.argmax(classifier.predict(x_test[:100]), axis=1)
nb_correct_pred = np.sum(x_test_pred == np.argmax(y_test[:100], axis=1))
print("Original test data (first 100 images):")
print("Correctly classified: {}".format(nb_correct_pred))
print("Incorrectly classified: {}".format(100-nb_correct_pred))
"""
Original test data (first 100 images):
Correctly classified: 98
Incorrectly classified: 2
"""
     
# 2.3 为了便于说明，请看前9张图片。(括号内为真标签。)
plt.figure(figsize=(10,10))
for i in range(0, 9):
    pred_label, true_label = class_descr[x_test_pred[i]], class_descr[np.argmax(y_test[i])]
    plt.subplot(330 + 1 + i)
    fig=plt.imshow(x_test[i])
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.text(0.5, -0.1, pred_label + " (" + true_label + ")", fontsize=12, transform=fig.axes.transAxes, horizontalalignment='center')

# 2.4 生成一些对抗性样本(用test image)
attacker = FastGradientMethod(classifier, eps=0.05)
x_test_adv = attacker.generate(x_test[:100]) # 大概需要2分钟

# 2.5 在100个对抗性样本上评价分类器:
x_test_adv_pred = np.argmax(classifier.predict(x_test_adv), axis=1)
nb_correct_adv_pred = np.sum(x_test_adv_pred == np.argmax(y_test[:100], axis=1))
print("Adversarial test data (first 100 images):")
print("Correctly classified: {}".format(nb_correct_adv_pred))
print("Incorrectly classified: {}".format(100-nb_correct_adv_pred))
"""
Adversarial test data (first 100 images):
Correctly classified: 20
Incorrectly classified: 80
"""

# 2.6 现在画出对抗性图像和它们的预测标签(括号内为真实标签)。
plt.figure(figsize=(10,10))
for i in range(0, 9):
    pred_label, true_label = class_descr[x_test_adv_pred[i]], class_descr[np.argmax(y_test[i])]
    plt.subplot(330 + 1 + i)
    fig=plt.imshow(x_test_adv[i])
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    fig.axes.text(0.5, -0.1, pred_label + " (" + true_label + ")", fontsize=12, transform=fig.axes.transAxes, horizontalalignment='center')

# 3. 训练检测器

# 3.1 加载检测器模型(它也使用ResNet架构)

path = get_file('BID_eps=0.05.h5',extract=False, path=DATA_PATH,
                url='https://www.dropbox.com/s/cbyfk65497wwbtn/BID_eps%3D0.05.h5?dl=1')
detector_model = load_model(path)
detector_classifier = KerasClassifier(clip_values=(-0.5, 0.5), model=detector_model, use_logits=False)
detector = BinaryInputDetector(detector_classifier)
detector_model.summary()
"""
Total params: 469,698
Trainable params: 467,426
Non-trainable params: 2,272
"""

# 3.2 训练探测器的准备工作:
#               用对抗性样本扩展了我们的训练集
#               将数据标记为0(原始)和1(对抗性)
x_train_adv = attacker.generate(x_train)
nb_train = x_train.shape[0]
x_train_detector = np.concatenate((x_train, x_train_adv), axis=0)
y_train_detector = np.concatenate((np.array([[1,0]]*nb_train), np.array([[0,1]]*nb_train)), axis=0)

# 3.3 执行训练工作(训练检测器)
detector.fit(x_train_detector, y_train_detector, nb_epochs=20, batch_size=20)

# 4. 评估检测器

# 4.1 将检测器应用到test image的对抗性例子上
flag_adv = np.sum(np.argmax(detector.predict(x_test_adv), axis=1) == 1)
print("Adversarial test data (first 100 images):")
print("Flagged: {}".format(flag_adv))
print("Not flagged: {}".format(100 - flag_adv))
"""
Adversarial test data (first 100 images):
Flagged: 100
Not flagged: 0
"""

# 4.2 将检测器应用到test image的前100张原始图片
flag_original = np.sum(np.argmax(detector.predict(x_test[:100]), axis=1) == 1)
print("Original test data (first 100 images):")
print("Flagged: {}".format(flag_original))
print("Not flagged: {}".format(100 - flag_original))
"""
Original test data (first 100 images):
Flagged: 100
Not flagged: 0
"""

# 4.3 对不同攻击强度eps下的检测器进行评估(注:检测器训练时，使用eps=0.05)
eps_range = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
nb_flag_adv = []
nb_missclass = []

for eps in eps_range:
    attacker.set_params(**{'eps': eps})
    x_test_adv = attacker.generate(x_test[:100])
    nb_flag_adv += [np.sum(np.argmax(detector.predict(x_test_adv), axis=1) == 1)]
    nb_missclass += [np.sum(np.argmax(classifier.predict(x_test_adv), axis=1) != np.argmax(y_test[:100], axis=1))]
    
eps_range = [0] + eps_range
nb_flag_adv = [flag_original] + nb_flag_adv
nb_missclass = [2] + nb_missclass

fig, ax = plt.subplots()
ax.plot(np.array(eps_range)[:8], np.array(nb_flag_adv)[:8], 'b--', label='Detector flags')
ax.plot(np.array(eps_range)[:8], np.array(nb_missclass)[:8], 'r--', label='Classifier errors')

legend = ax.legend(loc='center right', shadow=True, fontsize='large')
legend.get_frame().set_facecolor('#00FFCC')

plt.xlabel('Attack strength (eps)')
plt.ylabel('Per 100 adversarial samples')
plt.show()
"""
plot:
Detector flags
Classifier errors
"""
