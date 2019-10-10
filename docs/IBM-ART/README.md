# [IBM-ART](https://github.com/IBM/adversarial-robustness-toolbox)

- [Dataset](#Dataset)
- [Setup](#set-up)
- [Examples](#Examples)
- [Applications](#Applications)
- [Notebooks](#Notebooks)
- [Self-experiment](#Self-experiment)

### Dataset

| Dataset      | total data | training data | testing data | format  | label data |
| ------------ | ---------- | ------------- | ------------ | ------- | ---------- |
| **MNIST**    | 70000      | 60000         | 10000        | 20x20x1 | 10         |
| **CIFAR-10** | 60000      | 50000         | 10000        | 32x32x3 | 10         |



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
  - [classifier_scikitlearn_AdaBoostClassifier.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_scikitlearn_AdaBoostClassifier.ipynb)演示了如何使用ART的Scikit-learn AdaBoostClassifier。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
  - [classifier_scikitlearn_BaggingClassifier.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_scikitlearn_BaggingClassifier.ipynb)演示如何使用ART的Scikit-learn BaggingClassifier。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
  - [classifier_scikitlearn_DecisionTreeClassifier.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_scikitlearn_DecisionTreeClassifier.ipynb)演示如何使用ART的Scikit-learn DecisionTreeClassifier。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
  - [classifier_scikitlearn_ExtraTreesClassifier.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_scikitlearn_ExtraTreesClassifier.ipynb)演示如何使用ART的Scikit-learn ExtraTreesClassifier。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
  - [classifier_scikitlearn_GradientBoostingClassifier.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_scikitlearn_GradientBoostingClassifier.ipynb)演示如何使用ART的Scikit-learn GradientBoostingClassifier。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
  - [classifier_scikitlearn_LogisticRegression.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_scikitlearn_LogisticRegression.ipynb)演示如何使用ART的Scikit-learn LogisticRegression。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
  - [classifier_scikitlearn_pipeline_pca_cv_svc.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_scikitlearn_pipeline_pca_cv_svc.ipynb)包含一个使用黑箱攻击生成对抗性示例的example，该攻击针对的是由主成分分析(PCA)、交叉验证(CV)和支持向量机分类器(SVC)组成的scikit-learn管道，但是其他任何有效的管道也可以。使用带交叉验证的网格搜索优化管道。对抗样本是用黑箱HopSkipJump攻击创建的。训练数据是MNIST，因为它的直观的可视化，但任何其他数据集，包括表格数据也将是合适的。
  - [classifier_scikitlearn_RandomForestClassifier.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_scikitlearn_RandomForestClassifier.ipynb)演示如何使用ART的Scikit-learn RandomForestClassifier。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
  - [classifier_scikitlearn_SVC_LinearSVC.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_scikitlearn_SVC_LinearSVC.ipynb)演示如何使用ART的Scikit-learn SVC和LinearSVC支持向量机。它使用Iris和MNIST数据集演示和分析了针对”linear和radial-basis-function kernels的二分和多分的分类器“的Projected Gradient Descent attacks。
  - [classifier_xgboost.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/classifier_xgboost.ipynb)演示如何使用ART的Scikit-learn XGBoost 。它使用Iris和MNIST数据集演示和分析了Zeroth Order Optimisation攻击。
- 检测器
  - [detection_adversarial_samples_cifar10.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/detection_adversarial_samples_cifar10.ipynb)演示了如何使用ART的针对对抗性例子的检测器。这个分类器是一个针对CIFAR-10数据集的在Keras中ResNet结构的神经网络。
- 毒药攻击Poisoning
  - [poisoning_attack_svm.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/poisoning_attack_svm.ipynb)演示了针对支持向量机的中毒攻击。
  - [poisoning_dataset_mnist.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/poisoning_dataset_mnist.ipynb)在神经网络中演示了通过对训练数据集进行施毒后，后门的生成和检测。
- 认证和验证
  - [output_randomized_smoothing_mnist.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/output_randomized_smoothing_mnist.ipynb)演示了如何通过随机平滑来实现神经网络的对抗性鲁棒性。
  - [robustness_verification_clique_method_tree_ensembles_gradient_boosted_decision_trees_classifiers.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/robustness_verification_clique_method_tree_ensembles_gradient_boosted_decision_trees_classifiers.ipynb)利用XGBoost、LightGBM和Scikit-learn对决策树集成分类器(梯度增强决策树、随机森林等)中的对抗鲁棒性进行了验证。
- MNIST
  - [fabric_for_deep_learning_adversarial_samples_fashion_mnist.ipynb](https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/fabric_for_deep_learning_adversarial_samples_fashion_mnist.ipynb)展示如何使用ART中的由Fabric for Deep Learning (FfDL)训练的深度学习模型。

### Self-experiment

- 对抗性例子检测器：<a href = "./code/detection-adversarial-samples-CIFAR10.py">detection-adversarial-samples-CIFAR10.py</a>
- 神经网络鲁棒性验证：<a href = "./code/output-randomized-smoothing-mnist.py">output-randomized-smoothing-mnist.py</a>
- 分类器鲁棒性验证：<a href = "./code/robustness-verification-clique-method-tree-ensembles-gradient-boosted-decision-trees-classifiers.py">robustness-verification-clique-method-tree-ensembles-gradient-boosted-decision-trees-classifiers.py</a>
- 分类器：<a href = "./code/classifier_blackbox.py">classifier_blackbox.py</a>
- 

















