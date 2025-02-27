# pySciTools

A collection of useful tools for scientific computing.

## Installation

You can install the library via pip:

```bash
pip install pySciTools
```

## Usage

```python
from pySciTools import func1, func2

data = [1, 2, 3]
result = func1(data)
print(result)

sum_result = func2(3, 4)
print(sum_result)


```

# 上传到PyPI

```bash
# 安装打包工具
pip install twine setuptools wheel

# 构建包 
# 修改 setup.py 中的 version
rm -rf dist build *egg-info
python setup.py sdist bdist_wheel

# 上传包 
# 设置 $HOME/.pypirc  token
twine upload dist/*

# 导入
from sz1 import sz_utils

```
