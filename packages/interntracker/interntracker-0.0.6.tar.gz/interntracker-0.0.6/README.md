# tracker-python

## release

### 生成分发文件
`python setup.py sdist bdist_wheel`

### 保存 ~/.pypirc
```
[distutils]
index-servers =
    pypi

[pypi]
  username = __token__
  password = pypi-AgEIcHxxxxx
```

### 上传到 PyPI
`twine upload dist/*`
