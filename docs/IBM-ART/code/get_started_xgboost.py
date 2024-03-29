"""
该脚本演示了在XGBoost中使用ART的简单示例。
该示例在MNIST数据集上训练一个小模型，并使用Zeroth Order Optimization attack攻击创建对抗性示例。
在这里，我们提供一个预先训练的模型给ART分类器。
选择这些参数是为了减少脚本的计算需求，而不是为了提高准确性。
"""
import xgboost as xgb
import numpy as np

from art.attacks import ZooAttack
from art.classifiers import XGBoostClassifier
from art.utils import load_mnist
import time

start = time.clock()

# Step 1: 加载MNIST数据集 28x28的灰度图 70000张手写数字图(6:1)

(x_train, y_train), (x_test, y_test), min_pixel_value, max_pixel_value = load_mnist()

# Step 1a: Flatten数据集

x_test = x_test[0:5]
y_test = y_test[0:5]

nb_samples_train = x_train.shape[0]
nb_samples_test = x_test.shape[0]
x_train = x_train.reshape((nb_samples_train, 28 * 28))
x_test = x_test.reshape((nb_samples_test, 28 * 28))

# Step 2: 创建模型

params = {'objective': 'multi:softprob', 'metric': 'accuracy', 'num_class': 10}
dtrain = xgb.DMatrix(x_train, label=np.argmax(y_train, axis=1))
dtest = xgb.DMatrix(x_test, label=np.argmax(y_test, axis=1))
evals = [(dtest, 'test'), (dtrain, 'train')]
model = xgb.train(params=params, dtrain=dtrain, num_boost_round=10, evals=evals)

# Step 3: 创建ART分类器

classifier = XGBoostClassifier(model=model, clip_values=(min_pixel_value, max_pixel_value), nb_features=28 * 28,
                               nb_classes=10)

# Step 4: 训练ART分类器

# The model has already been trained in step 2

# Step 5: 在良性的测试实例上评价ART分类器

predictions = classifier.predict(x_test)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on benign test examples: {}%'.format(accuracy * 100))

# Step 6: 生成对抗性测试示例
attack = ZooAttack(classifier=classifier, confidence=0.0, targeted=False, learning_rate=1e-1, max_iter=200,
                   binary_search_steps=10, initial_const=1e-3, abort_early=True, use_resize=False,
                   use_importance=False, nb_parallel=5, batch_size=1, variable_h=0.01)
x_test_adv = attack.generate(x=x_test)

# Step 7: 通过对抗性测试实例对ART分类器进行评价

predictions = classifier.predict(x_test_adv)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print('Accuracy on adversarial test examples: {}%'.format(accuracy * 100))

elapsed = (time.clock() - start)
print("Time used:", elapsed)