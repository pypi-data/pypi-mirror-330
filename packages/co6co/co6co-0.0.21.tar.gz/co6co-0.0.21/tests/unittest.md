#  安装
方便测试
```
pip install nose
pip install coverage
```
执行
```
#测试一个文件
python -m unittest -v xxxx.test_xxx
#测试所有文件
python -v tests/* 
# 统计测试覆盖率
nosetests --with-coverage -v tests/*

```