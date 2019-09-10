# cleverhans

## Content

- [Download Github Code](#download-github-code)
- [Deploy Environment](#deploy-environment)
- [Scripts](#scripts)
- [Examples](#examples)
- [Ready-to-hand](#ready-to-hand)



### 1. Download Github Code <span id = "download-github-code">

这个项目是tensorflow的子项目（https://github.com/tensorflow/cleverhans），原始的代码版本是PYTHON 2.7环境，于代码下载后进行了重构和3.6版本的编译。

CleverHans是一个Python库，用于将机器学习系统中的漏洞与对抗性示例进行对比。具体来说，就是用于构建攻击，构建防御和对两者进行基准测试的对抗性示例库。

CleverHans是一个Python库，用于将机器学习系统的漏洞与对抗性示例进行对比。您可以在随附的博客中了解有关此类漏洞的更多信息。

Github地址：https://github.com/tensorflow/cleverhans

Youtute：https://www.youtube.com/watch?v=CIfsB_EYsVI

IBM Adversarial Robustness Toolbox：https://www.youtube.com/watch?v=gguyhEwoecI

CleverHans将很快支持3个框架：JAX, PyTorch, and TF2。该软件包本身将重点放在其最初的原则上：参考<font color=800080>实施针对机器学习模型的攻击</font>，以帮助针对<font color=800080>对抗性示例</font>对基准模型进行基准测试。

此存储库还将包含两个文件夹：`tutorials/`包含演示CleverHans的特点的脚本，`defenses/`包含在3个支持的框架之一中进行防御的权威实现的脚本，用于在3个受支持的框架之一中包含防御的权威实现的脚本。未来存储库的结构如下所示：

```
cleverhans/
  jax/
    attacks/
      ...
    tests/
      ...
  tf2/
    attacks/
      ...
    tests/
      ...
  torch/
    attacks/
      ...
    tests/
      ...
defenses/
  jax/
    ...
  tf2/
    ...
  torch/
    ...
tutorials/
  jax/
    ...
  tf2/
    ...
  torch/
    ...
```

同时，所有这些文件夹都可以在相应的`future /`子目录中找到。（例如`cleverhans/future/jax/attacks`, `cleverhans/future/jax/tests` ，`defenses/future/jax/`）

### 2. Deploy Environment <span id = "deploy-environment">

- [Dependencies](#dependencies)
- [Installation](#installation)

##### (1) Dependencies <span id = "dependencies">

该库使用TensorFlow来加速许多机器学习模型执行的图形计算。因此，安装TensorFlow是一个先决条件。

你可以在[这里](https://www.tensorflow.org/install/)找到指示。为了获得更好的性能，还建议安装带有GPU支持的TensorFlow（有关如何执行此操作的详细说明，请参阅TensorFlow安装文档）。

安装TensorFlow将处理所有其他依赖项，如numpy和scipy。

##### (2) Installation <span id = "installation">

一旦完成依赖关系，您可以使用pip或克隆此Github存储库来安装CleverHans。

如果使用pip安装CleverHans，请在安装TensorFlow后运行以下命令：

```
pip install cleverhans
```

这将安装上传到Pypi的最新版本。如果您想要安装最新版本，请使用：

```
pip install git+https://github.com/tensorflow/cleverhans.git#egg=cleverhans
```

如果你想对CleverHans进行可编辑的安装，以便开发库并提供更改，首先在GitHub上fork存储库，然后将fork克隆到你选择的目录中：

```
git clone https://github.com/tensorflow/cleverhans
```

然后，您可以在“可编辑”模式下安装本地程序包，以便将其添加到PYTHONPATH：

```
cd cleverhans
pip install -e .
```

虽然CleverHans可能会在许多其他机器配置上工作，但作者目前在Ubuntu 14.04.5 LTS（Trusty Tahr）上使用Python 3.5和TensorFlow {1.8,1.12}对其进行测试。不推荐支持Python 2.7。 CleverHans 3.0.1支持Python 2.7，主分支可能会继续在Python 2.7中运行一段时间，但作者不再在Python 2.7中运行测试，作者不打算在2019-07之后修复仅影响Python 2.7的错误-04。不推荐在1.12之前支持TensorFlow。这些版本的向后兼容性包装可能会在2019-07-07之后删除，作者将不会在该日期之后修复这些版本的错误。对TensorFlow 1.7及更早版本的支持已被弃用：作者不修复这些版本的错误，这些版本的任何剩余包装代码可能会被删除。

如果您有支持请求，请在<font color=800080>StackOverflow</font>上提出问题，而不是在GitHub跟踪器中打开问题。 GitHub问题跟踪器只应用于报告错误或发出功能请求。

##### (3) Scripts <span id = "scripts">

`scripts`目录包含命令行实用程序。在许多情况下，您可以使用它们在已保存的模型上运行CleverHans功能，而无需编写任何自己的Python代码。

您可能希望设置`.bashrc `/ `.bash_profile`文件以将CleverHans脚本目录添加到PATH环境变量中，以便可以从任何目录方便地执行这些脚本。

为了帮助您开始使用此库提供的功能，cleverhans_tutorials /文件夹附带以下教程：

- 带有`FGSM`的MNIST（[代码](https://github.com/tensorflow/cleverhans/blob/master/cleverhans_tutorials/mnist_tutorial_tf.py)）：本教程介绍如何<font color=800080>使用TensorFlow训练MNIST模型</font>，使用快速梯度符号方法<font color=800080>制作对抗性示例</font>，并使用对抗性训练<font color=800080>使模型对对抗性示例更加健壮</font>。

  ```
  % FGSM是 Goodfellow等人提出的比较典型的对抗样本生成算法。
  % 将生成后的FGSM扰动数据送到图像识别模型中如代码中给出的inceptionv3中，可以看到图像的识别结果全部变乱了。
  % cleverhans集成的代码也是tensorflow models中的相关代码。
  % 本质上而言，它需要在扰动的图片上进行训练，从而才能实现对扰动的代码进行准确识别。
  % 实际代码中，cleverhans提供了两种对抗训练，一种是基于inceptionv3的，一种是inception-resnet-v2的增强版。则扰动后的图片，也能被正确识别。
  ```

- 带有`Keras的FISTM`的MNIST（[代码](https://github.com/tensorflow/cleverhans/blob/master/cleverhans_tutorials/mnist_tutorial_keras_tf.py)）：本教程介绍如何<font color=800080>使用Keras定义MNIST模型</font>并使用TensorFlow训练它，使用快速梯度符号方法制作对抗性示例，并使用对抗性训练使模型对于对抗性示例更加健壮。

- 带有`JSMA`的MNIST（[代码](https://github.com/tensorflow/cleverhans/blob/master/cleverhans_tutorials/mnist_tutorial_jsma.py)）：第二个教程介绍了如何使用Keras定义MNIST模型并使用TensorFlow进行训练，并使用基于雅可比的显着性映射方法制作对抗性示例。

- 带有`黑盒攻击`的MNIST（[代码](https://github.com/tensorflow/cleverhans/blob/master/cleverhans_tutorials/mnist_blackbox.py)）：本教程实现了本文所述的黑盒攻击。对手训练一个替代模型：通过观察黑盒模型分配给对手仔细选择的输入的标签来模仿黑盒模型的副本。然后，对手使用替代模型的渐变来查找由黑盒模型错误分类的对抗性示例。

##### (4) Examples <span id = "examples">

`examples /`文件夹包含其他脚本，用于展示CleverHans库的不同用途，或者让您开始参加不同的对抗示例竞赛。

cleverhans代码库提供了多样性的对抗样本生成方法，具体如下：

```
sample_attacks/ - directory with examples of attacks:
sample_attacks/fgsm/ - Fast gradient sign attack.
sample_attacks/noop/ - No-op attack, which just copied images unchanged.
sample_attacks/random_noise/ - Attack which adds random noise to images.
sample_targeted_attacks/ - directory with examples of targeted attacks:
sample_targeted_attacks/step_target_class/ - one step towards target class attack. This is not particularly good targeted attack, but it demonstrates how targeted attack could be written.
sample_targeted_attacks/iter_target_class/ - iterative target class attack. This is a pretty good white-box attack, but it does not do well in black box setting.
sample_defenses/ - directory with examples of defenses:
sample_defenses/base_inception_model/ - baseline inception classifier, which actually does not provide any defense against adversarial examples.
sample_defenses/adv_inception_v3/ - adversarially trained Inception v3 model from Adversarial Machine Learning at Scale paper.
sample_defenses/ens_adv_inception_resnet_v2/ - Inception ResNet v2 model which is adversarially trained against an ensemble of different kind of adversarial examples. Model is described in Ensemble Adversarial Training: Attacks and Defenses paper.
```

同时也提供了好几个example。还是对抗样本生成与对抗训练非常好的一个库。

你可以在[cleverhans.readthedocs.io](https://cleverhans.readthedocs.io/en/latest/)上找到完整列表攻击及其功能签名。

##### (5) Ready-to-hand <span id = "ready-to-hand">





















