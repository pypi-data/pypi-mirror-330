# SmartPush_AutoTest



## Getting started

## 打包/上传的依赖
```
pip install wheel
pip install twine
```


## 打包-打包前记得修改版本号
```
python setup.py sdist bdist_wheel
```


## 上传到pipy的命令
```
twine upload dist/*
```