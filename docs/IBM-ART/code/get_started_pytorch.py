"""
该脚本演示了在PyTorch中使用ART的简单示例。
该示例在MNIST数据集上训练一个小模型，并使用快速梯度符号方法创建对抗性示例。
这里我们使用ART分类器来训练模型，也可以为ART分类器提供一个预先训练好的模型。
选择这些参数是为了减少脚本的计算需求，而不是为了提高准确性。"""
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

from art.attacks import FastGradientMethod
from art.classifiers import PyTorchClassifier
from art.utils import load_mnist


# Step 0: 定义神经网络模型，在前向方法中返回logits而不是activation

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv_1 = nn.Conv2d(in_channels=1, out_channels=4, kernel_size=5, stride=1)
        self.conv_2 = nn.Conv2d(in_channels=4, out_channels=10, kernel_size=5, stride=1)
        self.fc_1 = nn.Linear(in_features=4 * 4 * 10, out_features=100)
        self.fc_2 = nn.Linear(in_features=100, out_features=10)

    def forward(self, x):
        x = F.relu(self.conv_1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv_2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 10)
        x = F.relu(self.fc_1(x))
        x = self.fc_2(x)
        return x


# Step 1: 加载MNIST数据集 28x28的灰度图 70000张手写数字图(6:1)

(x_train, y_train), (x_test, y_test), min_pixel_value, max_pixel_value = load_mnist()

# Step 1a: 将坐标轴切换到PyTorch的NCHW格式

x_train = np.swapaxes(x_train, 1, 3).astype(np.float32)
x_test = np.swapaxes(x_test, 1, 3).astype(np.float32)

# Step 2: 创建模型

model = Net()

# Step 2a: 定义损失函数和优化器

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

# Step 3: 创建ART分类器

classifier = PyTorchClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), loss=criterion,
                               optimizer=optimizer, input_shape=(1, 28, 28), nb_classes=10)

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
