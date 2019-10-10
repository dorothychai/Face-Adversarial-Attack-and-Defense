# [IBM-ART](https://github.com/IBM/adversarial-robustness-toolbox)

- [Setup](#set-up)
- [Examples](#Examples)
- [Applications](#Applications)
- [Notebooks](#Notebooks)



### Setup <span id = "set-up">

The Adversarial Robustness 360 Toolbox is designed to run with Python 3.

- Install with pip:

  ```bash
  pip install adversarial-robustness-toolbox
  ```

- Manual installation:

  ```bash
  # the most recent version of ART
  git clone https://github.com/IBM/adversarial-robustness-toolbox
  # install ART
  pip install .
  # unit tests
  bash run_tests.sh
  ```


### Examples

- <a href = "./code/get_started_tensorflow.py">get_started_tensorflow.py</a>
- <a href = "./code/get_started_keras.py">get_started_keras.py</a>
- <a href = "./code/get_started_pytorch.py">get_started_pytorch.py</a>
- <a href = "./code/get_started_mxnet.py">get_started_mxnet.py</a>
- <a href = "./code/get_started_xgboost.py">get_started_xgboost.py</a>
- <a href = "./code/get_started_lightgbm.py">get_started_lightgbm.py</a>

Time spent and Accuracy Comparison ：

| Framework  | Time spent         | Accuracy on benign test examples | Accuracy on adversarial test examples |
| ---------- | ------------------ | -------------------------------- | ------------------------------------- |
| tensorflow | 47.400915401000006 | 95.09%                           | 16.81%                                |
| keras      | 59.934484775       | 95.76%                           | 16.85%                                |
| pytorch    | 91.72811700999999  | 96.25%                           | 16.43%                                |
| mxnet      | 220.330242249      | 95.56%                           | 20.39%                                |
| xgboost    | 268.975837169      | 100.0%                           | 0.0%                                  |
| lightgbm   | 1067.466168427     | 100.0%                           | 80.0%                                 |





### Applications

- <a href = "./code/adversarial_training_cifar10.py">adversarial_training_cifar10.py</a>

  > trains a convolutional neural network on the CIFAR-10 dataset, then generates adversarial images using the DeepFool attack and retrains the network on the training set augmented with the adversarial images.

  | Framework | Time spent    | Accuracy on adversarial test examples (Before Adversarial training) | Accuracy on adversarial test examples (After Adversarial training) |
  | --------- | ------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | keras     | 683.046962082 | 24.60%                                                       | 52.40%                                                       |

  ```python
  [INFO] Create DeepFool attack.
  # 用DeepFool针对classifier A训练出具有攻击性的classifier B
  [INFO] Craft attack on training examples.
  # 用具有攻击性的classifier B针对从50000个训练集中选出来的5000个training samples X生成5000个adversarial examples Y
  [INFO] Success rate of DeepFool attack: 0.88%
  # 用A对X预测的向量!=用A对Y预测的向量/y_train.shape[0]
  [INFO] Craft attack on testing examples
  # 用具有攻击性的classifier B针对从10000个训练集中选出来的500个testing samples I生成500个testing examples J
  [INFO] Success rate of DeepFool attack: 0.86%
  # 用A对I预测的向量!=用A对J预测的向量/y_train.shape[0]
  [INFO] Before adversarial training
  [INFO] Classifier before adversarial training
  [INFO] Accuracy on adversarial samples: 24.60%
  # 用A对J预测的向量==实际的testing label/y_test.shape[0]
  
  # 数据扩充:用对抗性样本展开训练集,并用此数据集重新训练CNN生成classifier C
  # x_train = np.append(x_train, x_train_adv, axis=0) 10000
  # y_train = np.append(y_train, y_train, axis=0) 10000
  [INFO] After adversarial training
  [INFO] Classifier with adversarial training
  [INFO] Accuracy on adversarial samples: 52.40%
  # 用C对J预测的向量==实际的testing label/y_test.shape[0]
  # 经过训练后得到的分类器C对对抗性例子J的识别性(识别为正确的label的意思)提高了
  Time used: 683.046962082
  ```

- <a href = "./code/adversarial_training_data_augmentation.py">adversarial_training_data_augmentation.py</a>

  > shows how to use ART and Keras to perform adversarial training using data generators for CIFAR-10.

  

- 



### Notebooks

- 对抗性训练
  - [adversarial_retraining.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/adversarial_retraining.ipynb)展示了如何加载和评估经过Sinn等人2019年合成和对抗性训练的MNIST和CIFAR-10模型。
  - [adversarial_training_mnist.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/adversarial_training_mnist.ipynb)演示了如何在MNIST数据集上，用神经网络进行对抗性训练，以增强模型对对抗性样本的抵抗力。
- Tensorflow v2
  - [art-for-tensorflow-v2-callable.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/art-for-tensorflow-v2-callable.ipynb)演示了如何使用ART和Tensorflow v2在eager execution mode模式下使用可调用类或python函数形式的模型。
  - [art-for-tensorflow-v2-keras.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/art-for-tensorflow-v2-keras.ipynb)演示了在没有eager execution mode模式的时候，ART与Tensorflow v2如何使用Tensorflow.keras。
- 攻击
  - [attack_adversarial_patch.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/attack_adversarial_patch.ipynb)演示了如何使用ART创建真实世界的对抗性补丁，欺骗真实世界的对象检测和分类模型。
  - [attack_decision_based_boundary.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/attack_decision_based_boundary.ipynb)演示了基于决策的对抗攻击(边界)攻击。这是一个黑盒攻击，只需要类的预测。
  - [attack_decision_tree.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/attack_decision_tree.ipynb)展示了如何使用决策树上来计算出对抗性例子(Papernot等，2016)。它通过遍历决策树分类器的结构来创建对抗性的例子，无需显式的梯度就可以计算出来。
  - [attack_defence_imagenet.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/attack_defence_imagenet.ipynb)解释了将ART与防御和攻击一起用于ImageNet神经网络分类器的基本工作流程。
  - [attack_hopskipjump.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/attack_hopskipjump.ipynb)演示了HopSkipJumpAttack。这是一个黑盒攻击，只需要类预测。这是边界攻击的高级版本。
- 分类器
  - [classifier_blackbox.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_blackbox.ipynb)演示了BlackBoxClassifier，ART中最通用和万能的分类器，只需要一个单一的预测函数定义，不需要任何额外的假设或要求。该笔记展示了如何使用BlackBoxClassifier分类器和HopSkiJump攻击去攻击一个远程部署的模型(在本例中是在IBM Watson机器学习上，https://cloud.ibm.com)。
  - [classifier_blackbox_tesseract.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_blackbox_tesseract.ipynb)演示了对Tesseract OCR的黑盒攻击。它利用BlackBoxClassifier和HopSkipJump攻击将一个单词的图像转换成另一个单词的图像，并展示了如何应用预处理的防御。
  - [classifier_catboost.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_catboost.ipynb)展示了如何使用ART的CatBoost模型。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
  - [classifier_gpy_gaussian_process.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_gpy_gaussian_process.ipynb)演示了如何为GPy的高斯过程分类器创建对抗性示例。它创造出专门针对Gaussian Process classifiers的HighConfidenceLowUncertainty (HCLU)攻击(Grosse et al.， 2018)，并将其与投影梯度下降Projected Gradient Descent(PGD)作比较(Madry et al.， 2017)。
  - [classifier_lightgbm.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_lightgbm.ipynb)演示了如何使用ART的LightGBM模型。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
  - 





















