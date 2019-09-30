# 对抗攻击

## Content

- [对抗攻击概念](#对抗攻击概念)
- [对抗攻击分类](#对抗攻击分类)
- [对抗攻击实现工具](#对抗攻击实现工具)
- [研究对抗攻击的数据集](#研究对抗攻击的数据集)





### 对抗攻击概念

通过对输入添加微小的扰动<font color=800080>使得分类器分类错误</font>，一般对用于深度学习的网络的攻击算法最为常见，应用场景包括目前大热的CV和NLP方向，例如，通过对图片添加精心准备的扰动噪声使得分类器分错，或者通过对一个句子中的某些词进行同义词替换使得情感分类错误。

### 对抗攻击分类

##### (1) 从攻击环境来分：黑盒攻击、白盒攻击、灰盒攻击

- 黑盒攻击：攻击者对攻击的模型的内部结构，训练参数，防御方法（如果加入了防御手段的话）等等一无所知，<font color=800080>只能通过输出输出与模型进行交互</font>，通过输入样本观察输出获得预测结果。
  - Transferable Adversarial Attacks for Image and Video Object Detection
  - FGSN
  - AdvGAN
  - Zeroth Order Optimization Based Black-box Attacks
  - Evolutionary Attack
  - Machine Learning as an Adversarial Service: Learning Black-Box Adversarial Examples
- 白盒攻击：与黑盒模型相反，攻击者对模型一切都可以掌握，在黑盒的基础上还可以获取模型的参数、梯度等信息。目前大多数攻击算法都是白盒攻击。
- 灰盒攻击：介于黑盒攻击和白盒攻击之间，仅仅了解模型的一部分。（例如仅仅拿到模型的输出概率，或者只知道模型结构，但不知道参数）

##### (2) 从攻击的目的来分：有目标攻击、无目标攻击

- 无目标攻击：以图片分类为例，攻击者只需要让目标模型对样本分类错误即可，但并不指定分类错成哪一类。
-  有目标攻击：攻击者指定某一类，使得目标模型不仅对样本分类错误并且需要<font color=800080>错成指定的类别</font>。从难度上来说，有目标攻击的实现要难于无目标攻击。

##### (3) 从扰动的强度大小来分：无穷范数攻击、二范数攻击、0范数攻击

![](./pictures/01-范数攻击.png)

- 无穷范数攻击，当p趋近于无穷大时，上式子表示扰动中最大的一个，通常在论文里，对于MNIST数据集，限制是（-0.3，0.3）
- 二范数攻击，即p=2
- 0范数攻击（单像素攻击）此时限制的是可以改变的像素个数，不关心具体每个像素值改变了多少。在MNIST数据集中，一般限制是12个。

##### (4) 从攻击的实现来分：基于梯度的攻击、基于优化的攻击、基于决策面的攻击或者其他

- 基于梯度的攻击：
  - <a href = "./docs/FGSM.md">FGSM（Fast Gradient Sign Method)</a>　　
  - PGD（Project Gradient Descent）
  - MIM（Momentum Iterative Method）
  - DeepFool（a simple and accurate method to fool deep neural networks）
- 基于优化的攻击：CW（Carlini-Wagner Attack）
- 基于决策面的攻击：DEEPFOOL
- 其他：Pointwise

### 对抗攻击实现工具

![](./pictures/02-对抗攻击工具.png)

- IBM开源了检测模型及对抗攻击的工具箱 [Adversarial Robustness Toolbox](https://www.oschina.net/p/adversarial-robustness-toolbox)，该工具箱是用 Python 撰写而成，因为 Python 是建立、测试和部署深度神经网路最常用的语言，包含了对抗和防御攻击的方法。


### 研究对抗攻击的数据集

- 人脸
  - [FaceForensics](https://github.com/ondyari/FaceForensics)
  - 

- 













