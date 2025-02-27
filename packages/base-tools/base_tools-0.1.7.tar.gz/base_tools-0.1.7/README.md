# base-tools

#### 介绍
本库实现了一些基础的工具类，帮助开发者可以简单的通过python实现一些常用的功能，比如：文件操作、字符串操作、时间操作、网络操作等。

#### 软件架构
cjlutils<br/>
├── __init__.py<br/>
├── AdbUtil.py<br/>
├── Base64Util.py<br/>
├── DictUtil.py<br/>
├── EncodeUtil.py<br/>
├── FileUtil.py<br/>
├── HttpUtil.py<br/>
├── ListUtil.py<br/>
├── PyplotUtil.py<br/>
├── ScpUtil.py<br/>
├── SshUtil.py<br/>
├── StringUtil.py<br/>
├── TimeUtil.py<br/>



#### 安装教程
首先需要安装python环境，要求不低于`3.10`，然后通过`pip`安装依赖库
```shell
pip install base-tools
```

如果需要安装指定版本，如`0.0.1`，可以通过以下命令安装
```shell
pip install base-tools==0.0.1
```
#### 使用说明
1. 通过`import`导入需要的工具类。以文件操作工具类`FileUtil`为例
```python
from cjlutils import FileUtil
```
2. 使用`FileUtil`中的方法
```python
FileUtil.get_file_list('path')
```
#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

