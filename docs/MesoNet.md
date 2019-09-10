# MesoNet

## Content

- [Download Github Code](#download-github-code)
- [Deploy Environment](#deploy-environment)





### 1. Download Github Code <span id = "download-github-code">

> 我们提出了一种自动检测视频中面部篡改的方法。我们特别关注用于生成超逼真伪造视频的两种最新方法：deepfake和face2face。传统的图像取证技术通常不太适合视频，因为它们的压缩会严重降低数据质量。因此，我们遵循深度学习方法并构建两个网络，两者都具有较少的层数以关注图像的介观特性。我们在现有数据集和我们从在线视频构成的数据集上评估这些快速网络。我们的测试结果表明，对于深度检测，检测成功率超过98％，对于face2face检测成功检测率为95％。

Github地址：https://github.com/DariusAf/MesoNet

Paper地址：[WIFS 2018 conference](http://wifs2018.comp.polyu.edu.hk/)

全文：[Link to full paper](https://arxiv.org/abs/1809.00888)

Youtute：[Demonstrastion video (light)](https://www.youtube.com/watch?v=vch1CmgX0LA)

### 2. Deploy Environment <span id = "deploy-environment">

- [安装Ananconda并添加环境变量](#安装Ananconda并添加环境变量)
- [下载face_recognition库](#下载face_recognition库)
- [使用face_recognition库](#使用face_recognition库)
- [下载数据集](#下载数据集)

环境配置：

```
Python3.5
Numpy1.14.2
Keras2.1.5
```

如果您想通过视频中的面部提取来使用完整的管道，您还需要以下库：

- [Imageio](https://pypi.org/project/imageio/)
- [FFMPEG](https://www.ffmpeg.org/download.html)
- [face_recognition](https://github.com/ageitgey/face_recognition)

##### (1) 首先，安装Ananconda并添加环境变量：<span id = "安装Ananconda并添加环境变量">

![](../pictures/42-Ananconda-path.png)

   ```
   % 打开terminal
   activate % 激活Ananconda虚拟环境
   conda info --env % 查看有那些虚拟环境
   conda create -n python35 python=3.5 % 创建虚拟环境
   conda activate python35 % 激活指定虚拟环境
   pip list % 查看当前虚拟环境下的第三方包有哪些
   pip install numpy==1.14.2 % 安装指定版本第三方包
   pip install keras==2.1.5
   pip install imageio==2.5.0
   pip install ffmpeg
   ```

##### (2) 下载face_recognition库： <span id = "下载face_recognition库">

- 先下载dlib库：`pip install dlib`:
  - [@masoudr's Windows 10 installation guide (dlib + face_recognition)](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508)或者可以看我写的<a href = "../docs/Facenet-Opensource-Tool.md/#运行之前要先安装dlib库">教程</a>
  - 先下载安装Microsoft Visual Studio 2015 (or newer) with C/C++ Compiler installed. 
  - [`Boost`](https://blog.csdn.net/qq_27923041/article/details/76153125) library version 1.63 or newer.
  
- 下载face_recognition module from pypi using pip

  ```bash
  pip install face_recognition
  ```

- 如果你安装有问题的话，你也可以用这个提前配置好的[虚拟机](https://medium.com/@ageitgey/try-deep-learning-in-python-now-with-a-fully-pre-configured-vm-1d97d4c3e9b)。

##### (3) 使用face_recognition库 <span id = "使用face_recognition库">

- 当你下载好face_recognition库之后，你会得到两个简单的命令行程序：

  ```
  face_recognition % 识别照片或文件夹中的面部照片
  face_detection % 在很多照片中找到一张人脸
  ```

- 使用`face_recognition`命令行：

  - 你需要提供一个文件夹A，其中包含你已经知道的每个人的一张照片。并且，每个人都应该有一个图像文件，其中的文件根据图片中的人命名。

  - 接下来，您需要第二个文件夹B，其中包含您要识别的文件`unknown.jpg`。

  - 然后在您只需运行命令face_recognition，传入包含已知人员的文件夹A和包含未知人员的文件夹B（或单个图像），它会告诉您每个图像中的人分别是谁。

  - 命令如下：

    ```bash
    $ face_recognition ./known_people_pictures/ ./unknown_people_pictures/
    
    /unknown_pictures/unknown.jpg,Barack Obama
    /face_recognition_test/unknown_pictures/unknown.jpg,unknown_person
    ```

  - 每个人脸的输出中都有一行。数据以逗号分隔：`文件名，找到的人的姓名`。

  - `unknown_person`指的是图像中的这张脸（一张）与已知（在`known_people_pictures`文件夹中的）的任何人都不匹配的脸部。

- 使用`face_detection`命令行：

  - 使用face_detection命令可以查找图像中任何人脸的位置（像素坐标）。

  - 只需运行命令`face_detection`，传入图像文件夹进行检查（或单个图像）：

    ```bash
    $ face_detection ./folder_with_pictures/
    
    examples/image1.jpg,65,215,169,112
    examples/image2.jpg,62,394,211,244
    examples/image2.jpg,95,941,244,792
    ```

  - 它为检测到的每个人脸打印一行。报告的坐标是面的顶部，右侧，底部和左侧坐标（以像素为单位）。

- 调整容差/灵敏度（Adjusting Tolerance / Sensitivity）：

  - 如果同一个人获得多个匹配，则可能是您的照片中的人看起来非常相似，那么此时就需要较低的容差值来使面部比较更加严格。

  - 您可以使用`--tolerance`参数执行此操作。默认容差值为0.6，较低的数字使面部比较更严格：

    ```bash
    $ face_recognition --tolerance 0.54 ./known_people_pictures/ ./unknown_people_pictures/
    
    /unknown_pictures/unknown.jpg,Barack Obama
    /face_recognition_test/unknown_pictures/unknown.jpg,unknown_person
    ```

  - 如果你想要查看为了调整tolerance setting而为每个match计算的face distance，你可以使用`--show-distance true`：

    ```bash
    $ face_recognition --show-distance true ./known_people_pictures/ ./unknown_people_pictures/
    
    /unknown_pictures/unknown.jpg,Barack Obama,0.378542298956785
    /face_recognition_test/unknown_pictures/unknown.jpg,unknown_person,None
    ```

- 更多示例：

  - 如果您只是想知道每张照片中的人物名称但不关心文件名，您可以这样做：

    ```bash
    $ face_recognition ./known_people_pictures/ ./unknown_people_pictures/ | cut -d ',' -f2
    
    Barack Obama
    unknown_person
    ```

- 加快面部识别：

  如果您的计算机具有多个CPU核心，则可以并行完成面部识别。例如，如果您的系统有4个CPU内核，则可以通过并行使用所有CPU内核在相同的时间内处理大约4倍的图像。

  - 如果您使用的是Python 3.4或更高版本，传入`--cpus <number_of_cpu_cores_to_use>`参数：

    ```bash
    $ face_recognition --cpus 4 ./known_people_pictures/ ./unknown_people_pictures/
    ```

    你也可以传入`--cpus -1`来使用系统中的所有CPU核心。

  - 

- 你可以使用功能丰富的[face_recognition API](https://face-recognition.readthedocs.io/en/latest/face_recognition.html)

  - 自动查找一张图像中的所有脸部：

    ```python
    import face_recognition
    
    image = face_recognition.load_image_file("my_picture.jpg")
    face_locations = face_recognition.face_locations(image)
    
    # face_locations现在是一个列出每个面的坐标的数组！
    ```

    可以看这个[example](https://github.com/ageitgey/face_recognition/blob/master/examples/find_faces_in_picture.py)

    你也可以选择更准确的基于深度学习的人脸检测模型。

    注意：使用此模型可获得GPU加速（通过NVidia的CUDA库）以获得良好的性能。在compliling dlib时，你还需要启用CUDA支持。

    ```python
    import face_recognition
    
    image = face_recognition.load_image_file("my_picture.jpg")
    face_locations = face_recognition.face_locations(image, model="cnn")
    
    # face_locations现在是一个列出每个面的坐标的数组！
    ```

    可以看这个[example](https://github.com/ageitgey/face_recognition/blob/master/examples/find_faces_in_picture_cnn.py)

    如果你有很多图像和GPU，你也可以[批量找到面孔](https://github.com/ageitgey/face_recognition/blob/master/examples/find_faces_in_batches.py)。

  - 自动定位图像中人物的面部特征:

    ```python
    import face_recognition
    
    image = face_recognition.load_image_file("my_picture.jpg")
    face_landmarks_list = face_recognition.face_landmarks(image)
    
    # face_landmarks_list现在是一个数组，其中包含每个面部中每个面部特征的位置。
    # face_landmarks_list [0] ['left_eye']将是第一个人左眼的位置和轮廓。
    ```

    可以看这个[example](https://github.com/ageitgey/face_recognition/blob/master/examples/find_facial_features_in_picture.py)

  - 识别图像中的面部并识别它们的身份:

    ```python
    import face_recognition
    
    picture_of_me = face_recognition.load_image_file("me.jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
    
    # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!
    
    unknown_picture = face_recognition.load_image_file("unknown.jpg")
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
    
    # Now we can see the two face encodings are of the same person with `compare_faces`!
    
    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
    
    if results[0] == True:
        print("It's a picture of me!")
    else:
        print("It's not a picture of me!")
    ```

    可以看这个[example](https://github.com/ageitgey/face_recognition/blob/master/examples/recognize_faces_in_pictures.py)

- 其他的python代码，可以[点击此处](https://github.com/ageitgey/face_recognition)获得资料。

##### (4) 下载数据集 <span id = "下载数据集">

对齐的面部数据集：

| Set        | Size of the forged image class | Size of real image class |
| ---------- | ------------------------------ | ------------------------ |
| Training   | 5111                           | 7250                     |
| Validation | 2889                           | 4259                     |

```
- Training set (~150Mo)
- Validation set (~50Mo)
- Training + Validation video set (~1.4Go)
```































