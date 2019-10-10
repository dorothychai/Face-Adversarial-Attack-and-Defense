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

  | Framework | Time spent        | Accuracy on adversarial test examples (Before Adversarial training) | Accuracy on adversarial test examples (After Adversarial training) |
  | --------- | ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | keras     | 540.5198653479999 | (50.20%)                                                     |                                                              |

  > Create DeepFool attack.
  >
  > Craft attack on training examples.
  >
  > Success rate of DeepFool attack: 0.92%
  >
  > Craft attack on testing examples.
  >
  > Success rate of DeepFool attack: 0.87%
  >
  > Classifier before adversarial training.
  >
  > Accuracy on adversarial samples: 23.80%.
  >
  > Classifier with adversarial training.
  >
  > Accuracy on adversarial samples: 50.20%.
  >
  > Time used: 540.5198653479999.

  ```python
  [INFO] Create DeepFool attack.
  [INFO] Craft attack on training examples.
  
  
  ```

  

- <a href = "./code/adversarial_training_data_augmentation.py">adversarial_training_data_augmentation.py</a>









