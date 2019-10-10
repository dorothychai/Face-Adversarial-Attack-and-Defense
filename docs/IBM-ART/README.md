# IBM-ART

- [Setup](#set-up)
- [Examples](#Examples)
- [Applications](#Applications)



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









