# Ubuntu系统中的环境变量

## Content

- [1. 查看环境变量](#查看环境变量)
- [2. 设置环境变量](#设置环境变量)
- [3. 环境变量的作用域](#环境变量的作用域)
- [4. 环境变量的配置文件](#环境变量的配置文件)





### 1. 查看环境变量 <span id = "查看环境变量">

查看环境变量有三个命令：

- `env`：env命令是environment的缩写，用于列出所有的环境变量。
- `export`：单独使用export命令也可以像env列出所有的环境变量，不过export命令还有其他额外的功能。
- `echo $PATH`： echo $PATH用于列出变量PATH的值，里面包含了已添加的目录。

### 2. 设置环境变量 <span id = "设置环境变量">

设置环境变量通常有两种方式：

1. **直接把你的路径添加到环境变量`PATH`中**。`$PATH`表示变量PATH的值，包含已有的目录：

   ```bash
   # 这种方法需要注意路径的顺序，如果遇到有同名的命令，那么PATH里面哪个目录先被查询，则那个目录下的命令就会被先执行.
   export PATH=$PATH:/path/to/your/dir # 加到PATH末尾
   export PATH=/path/to/your/dir:$PATH # 加到PATH开头
   ```

2. **命名一个新的环境变量**，用于其他程序的引用：

   ```bash
   export VAR_NAME=value
   ```

### 3. 环境变量的作用域 <span id = "环境变量的作用域">

环境变量的作用域通常有三个：

1. 作用于当前终端：

   ```bash
   # 打开一个终端，输入添加环境变量的语句
   export CLASS_PATH=./JAVA_HOME/lib:$JAVA_HOME/jre/lib
   # 终端所添加的环境变量是临时的，只适用于当前终端，关闭当前终端或在另一个终端中，添加的环境变量无效
   ```

2. 作用于当前用户：

   ```bash
   # 如果只需要添加的环境变量对当前用户有效，可以写入用户主目录下的.bashrc文件
   vim ~/.bashrc
   ```

   添加语句：

   ```bash
   export CLASS_PATH=./JAVA_HOME/lib:$JAVA_HOME/jre/lib
   # 注销或者重启可以使修改生效，如果要使添加的环境变量马上生效：
   source ~/.bashrc
   ```

3. 作用于所有用户：

   ```bash
   # 要使环境变量对所有用户有效，可以修改profile文件
   sudo vim /etc/profile 
   ```

   添加语句：

   ```bash
   export CLASS_PATH=./JAVA_HOME/lib:$JAVA_HOME/jre/lib
   # 注销或者重启可以使修改生效，如果要使添加的环境变量马上生效：
   source /etc/profile
   ```

### 4. 环境变量的配置文件 <span id = "环境变量的配置文件">

Ubuntu Linux系统环境变量配置文件分为两种：

- [系统级文件](#系统级文件)
- [用户级文件](#用户级文件)
- [/etc/profile与/etc /enviroment的比较](#/etc/profile与/etc /enviroment的比较)
- [设置环境变量的方法](#设置环境变量的方法)

##### 系统级文件 <span id = "系统级文件">

- **/etc/profile**:在登录时,操作系统定制用户环境时使用的第一个文件，此文件为系统的每个用户设置环境信息,当用户第一次登录时,该文件被执行。并从/etc/profile.d目录的配置文件中搜集shell的设置。这个文件一般就是调用/etc/bash.bashrc文件。
- **/etc/bash.bashrc**：系统级的bashrc文件，为每一个运行bash shell的用户执行此文件.当bash shell被打开时,该文件被读取。
- **/etc/environment**: 在登录时操作系统使用的第二个文件,系统在读取你自己的profile前,设置环境文件的环境变量。

##### 用户级文件 <span id = "用户级文件">

- **~/.profile**: 在登录时用到的第三个文件 是.profile文件,每个用户都可使用该文件输入专用于自己使用的shell信息,当用户登录时,该文件仅仅执行一次!默认情况下,他设置一些环境变量,执行用户的.bashrc文件。
- **~/.bashrc**:该文件包含专用于你的bash shell的bash信息,当登录时以及每次打开新的shell时,该该文件被读取。不推荐放到这儿，因为每开一个shell，这个文件会读取一次，效率上讲不好。
- ~/.bash_profile：每个用户都可使用该文件输入专用于自己 使用的shell信息,当用户登录时,该文件仅仅执行一次!默认情况下,他设置一些环境变量,执行用户的.bashrc文件。~/.bash_profile 是交互式、login 方式进入 bash 运行的~/.bashrc是交互式 non-login 方式进入 bash 运行的通常二者设置大致相同，所以通常前者会调用后者。
- ~**./bash_login:**不推荐使用这个，这些不会影响图形界面。而且.bash_profile优先级比bash_login高。当它们存在时，登录shell启动时会读取它们。
- **~/.bash_logout:**当每次退出系统(退出bash shell)时,执行该文件。
- **~/.pam_environment**：用户级的环境变量设置文件。

另外,/etc/profile中设定的变量(全局)的可以作用于任何用户,而~/.bashrc等中设定的变量(局部)只能继承 /etc/profile中的变量,他们是"父子"关系。 

##### /etc/profile与/etc /enviroment的比较 <span id = "/etc/profile与/etc /enviroment的比较">

用户环境建立的过程先执行/etc/environment，后执行/etc/profile。 

/etc/environment是设置整个系统的环境，而/etc/profile是设置所有用户的环境，前者与登录用户无关，后者与登录用户有关。

系统应用程序的执行与用户环境可以是无关的，但与系统环境是相关的。

##### 设置环境变量的方法

- /etc/profile全局的，随系统启动设置(设置这个文件是一劳永逸的办法)


- /root/.profile和/home/myname/.profile只对当前窗口有效。


- /root/.bashrc和 /home/yourname/.bashrc随系统启动，设置用户的环境变量(平时设置这个文件就可以了)

要配置Ubuntu的环境变量，就是在这几个配置文件中找一个合适的文件进行操作了；如想将一个路径加入到$PATH中，可以由下面这样几种添加方法：

- 控制台中：

  ```bash
  $PATH="$PATH:/my_new_path"  # 关闭shell，会还原PATH
  ```

- 修改profile文件：

  ```bash
  $sudo gedit /etc/profile
  # 在里面加入:
  # export PATH="$PATH:/my_new_path"
  # 重新注销系统才能生效
  # 通过echo命令测试一下：$ echo $PATH
  ```

- 修改.bashrc文件：

  ```bash
  $ sudo gedit /root/.bashrc
  # 在里面加入:
  # export PATH="$PATH:/my_new_path"
  # 重新注销系统才能生效
  # 通过echo命令测试一下：$ echo $PATH
  ```

  



























