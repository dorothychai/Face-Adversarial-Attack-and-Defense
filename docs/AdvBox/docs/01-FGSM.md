# 01-FGSM

#### 1. 安装AdvBox

```bash
# 1.1 安装paddlepaddle
# (1)创建paddlepaddle环境
# 目前advbox仅支持python 2.*, paddlepaddle 0.12以上。
conda create -n pp python=2.7
# 激活paddlepaddle环境
source activate pp
# (2)安装paddlepaddle包
# pip install paddlepaddle
pip install paddlepaddle==0.12.0
# 如果希望使用GPU加速训练过程，可以安装GPU版本
pip install paddlepaddle-gpu
# paddlepaddle-gpu针对不同的cuDNN和CUDA具有不同的编译版本。一百度云上的GPU服务器为例，CUDA为8.0.61，cuDNN为5.0.21，对应的编译版本为paddlepaddle-gpu为paddlepaddle-gpu==0.14.0.post85
pip install paddlepaddle-gpu==0.14.0.post85
# 查看服务器的cuDNN和CUDA版本的方法为：
#cuda 版本
cat /usr/local/cuda/version.txt
#cudnn 版本 
cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2
#或者
cat /usr/include/cudnn.h | grep CUDNN_MAJOR -A 2
# 详细支持列表可以参考链接: http://paddlepaddle.org/docs/0.14.0/documentation/fluid/zh/new_docs/beginners_guide/install/install_doc.html
```

```bash
# 1.1 mac下安装paddlepaddle包
# mac下安装paddlepaddle包方式比较特殊，相当于在docker镜像直接运行。
docker pull paddlepaddle/paddle
docker run --name paddle-test -v $PWD:/paddle --network=host -it paddlepaddle/paddle /bin/bash
# 如果mac上没有装docker，需要提前下载并安装
https://download.docker.com/mac/stable/Docker.dmg
```

```bash
# 1.1 多GPU支持
# 部分场景需要使用多GPU加速，这个时候需要安装nccl2库，对应的下载地址为：https://developer.nvidia.com/nccl/nccl-download
# 下载对应的版本，以百度云为例，需要下载安装NCCL 2.2.13 for Ubuntu 16.04 and CUDA 8。下载完毕后，进行安装
apt-get install libnccl2=2.2.13-1+cuda8.0 libnccl-dev=2.2.13-1+cuda8.0
# 设置环境变量
export NCCL_P2P_DISABLE=1  
export NCCL_IB_DISABLE=1
```

#### 2. 部署AdvBox代码

```bash
# 2.1 直接同步advbox的代码
git clone https://github.com/baidu/AdvBox.git
# 示例代码在tutorials目录下
```

#### 3. hello world

安装完advbox后，可以运行自带的hello world示例代码。

#### 4. 生成测试模型

```bash
# 4.1 首先需要生成攻击用的模型，advbox的测试模型是一个识别mnist的cnn模型。
cd tutorials/
python mnist_model.py
# 运行完模型后，会将模型的参数保留在当前目录的mnist目录下。查看该目录，可以看到对应的cnn模型的每层的参数，可见有两个卷积层和两个全连接层构成
conv2d_0.b_0  
conv2d_0.w_0  
conv2d_1.b_0  
conv2d_1.w_0  
fc_0.b_0  
fc_0.w_0  
fc_1.b_0  
fc_1.w_0
```

#### 5. 运行攻击代码 

```bash
# 5.1 运行下基于FGSM算法的演示代码
python mnist_tutorial_fgsm.py
# 运行攻击脚本，对mnist数据集进行攻击，测试样本数量为500，其中攻击成功394个，占78.8%
attack success, original_label=4, adversarial_label=9, count=498
attack success, original_label=8, adversarial_label=3, count=499
attack success, original_label=6, adversarial_label=1, count=500
[TEST_DATASET]: fooling_count=394, total_count=500, fooling_rate=0.788000
fgsm attack done
```

































