# Python-related

## Content

- [自定义包的导入和使用](#自定义包的导入和使用)











### # 1. 自定义包的导入和使用 <span id = "自定义包的导入和使用">

- [引用模块](#引用模块)
- [使用通配符导入某个module中的所有元素](#使用通配符导入某个module中的所有元素)
- [在package内部互相调用](#在package内部互相调用)
- [Python如何找到我们定义的module](#Python如何找到我们定义的module)

包(packages)其实也是模块，其类型Type也是module。通常引用字定义模块时有两种方法：

- 将两个文件放在同一个目录下。
- 在sys.path下添加要引用的py文件的路径，然后import。

这样的做法，对于少数文件是可行的，但是如果程序数目很多，层级很复杂时就比较麻烦了。此时<font color=800080>用package就能将多个py文件组织起来</font>，类似于第三方包一样地引用，要方便很多。

package的层次结构与程序所在目录的层次结构相同，且必须包含一个`__init__.py`的文件。`__init__.py`文件可以为空，只要它存在就表明此目录被作为一个package处理。

```bash
package1/
	__init__.py
	subPack1/
		__init__.py
		module_11.py
		module_12.py
		module_13.py
	subPack2/
		__init__.py
		module21.py
		module22.py
		module23.py
	...
...
% __init__.py文件可以为空，只要它存在就表明此目录被作为一个package处理
% 当然__init__.py文件中也可以设置相应的内容
```

好了，现在我们在`module_11.py`文件中定义一个函数：

```python
def funA():
    print("funcA in module_11")
    return
```

##### 引用模块 <span id = "引用模块">

在顶层目录(即`package1`所在的目录，把`package1`放在解释器能够搜索到的地方)运行python：

```python
from package1.subPack1.module_11 import funcA
funcA
```

这样，我们就按照`package1`的层次关系，正确调用了`module_11`中的函数。

##### 使用通配符导入某个module中的所有元素 <span id = "使用通配符导入某个module中的所有元素">

通配符：`*`

答案就在`__init.py`中，我们在`subPack1`的`__init__.py`文件中写：

```python
__all__ = ['module13','module_12']
```

然后进入python：

```python
from package1.subPack1 import *
module_11.funcA()
% ImportError: No module named module_11
```

也就是说，以`*`导入时，package里的module是受`__init__.py`限制的。

##### 在package内部互相调用 <span id = "在package内部互相调用">

- 如果希望调用同一个package里的module，则直接`import`即可。
  - 也就是说`module_12`中，可以直接使用`import module_11`。
- 如果不在同一个package中，例如我们希望在`module_21.py`中调用`module_11.py`中的`FuncA`，则应该这样：
  - `from subPack1.module_11 import funcA`

##### Python如何找到我们定义的module <span id = "Python如何找到我们定义的module">

在标准包`sys`中path属性记录了Python的包路径：

```python
import sys
print(sys.path)
```

通常我们可以将module的包路径放到环境变量PYTHONPATH中，该环境变量会自动添加到sys.path属性。

另一种方法是在编程中直接指定我们的module路径到sys.path中(通常也可以放在`\python3\lib\site-packages`文件夹下)。



































