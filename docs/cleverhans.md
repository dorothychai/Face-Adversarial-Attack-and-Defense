# cleverhans

## Content

- [Download Github Code](#download-github-code)
- d



### 1. Download Github Code <span id = "download-github-code">

cleverhans是用于构建攻击，构建防御和对两者进行基准测试的对抗性示例库。

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



































