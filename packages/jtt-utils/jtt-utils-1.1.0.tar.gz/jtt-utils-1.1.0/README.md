## D:\work\mwwork\JTT\jtt-tm-util
#### jtt 常用工具
* 

### 设计


### 设定
*

###产生分发包
``
python setup.py sdist
twine upload dist/*
``
### 运行
* python setup.py sdist build
* python setup.py install


### 修改记录
* 2020/03/23
```text
  v 0.0.4
  修改consul reader 增加read_service 的key参数,向上兼容 

```
* 2020/05/27
```text
  v 0.0.5
  修改consul reader 增加service_as_url向上兼容 

```

* 2020/06/11
```text
  v 0.0.6
  
  修改sync_basedata 增加read employee
```

* 2020/06/17
```text
  v 0.0.7
  
  修改sync_basedata 的bug
```

* 2023/03/16
```text
v 0.1.0

fix update line_config bug。
```
* 2023/03/17
```text
v 0.1.1

kong register add host param
```
* 2023/04/20
```text
v 0.1.2
sync basedata 同步支持 key_type='set' 方式
```

* 2023/04/20
```text
v 0.1.3
fix : consul read datebase driver 的错误
add read_dbdriver func
```

* 2023/04/20
```text
v 0.1.3
fix : consul read datebase driver 的错误
add read_dbdriver func
```

* 2024/07/31

```
v1.0.0
package name 改为 jtt-utils
v 1.0.1
kong.register_upstream_service 增加参数 custom_base_path 

v1.0.2
fix bug kong.register_upstream_service 增加参数 custom_base_path 
```

* 2025-2-26
```
version = 1.1.0
kong支持新版admin. v3.3.9 同时要求兼容旧版<"0.15"
```