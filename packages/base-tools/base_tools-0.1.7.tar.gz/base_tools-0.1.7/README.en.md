# base-tools

#### Description
This library implements some basic utility classes to help developers easily implement some common functions in Python, such as: file operation, string operation, time operation, network operation, etc.

#### Software Architecture
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

#### Installation

1. You need to install the Python environment, which requires no less than `3.10`. Then install the dependency library through `pip`
```shell
pip install base-tools
```
2. If you need to install a specific version, such as `0.0.1`, you can install it with the following command
```shell
pip install base-tools==0.0.1
```

#### Instructions
1. Import the required utility class through `import`. Taking the file operation utility class `FileUtil` as an example
```python
from cjlutils import FileUtil
```
2. Use the methods in `FileUtil`
```python
FileUtil.get_file_list('path')
```

#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request