# 1、安装依赖
```
> poetry shell
> poetry install
```
# 2、配置环境变量
```
> export SESSDATA=...
> export BILI_JCT=...
> export BUVID3=...
or
将.env_sample更改为.env,并配置SESSDATA、BILI_JCT、BUVID3环境变量
```

# 3、运行
```
> python3 src/main.py serve
```

# 4、发布与构建
```
> poetry publish --build
```

# 5、docker
```
> docker build -t ylz_bilibili .
> docker run -id --rm -p 3000:3000 ylz_bilibili
```

# 6、其他系统安装与命令行
```
> pip3 install -U ylz_bilibili
> ylz_bilibili serve 
```

# 7、其他系统集成
```
> pip3 install -U ylz_bilibili

> vi main.py

from bilibili import BilibiliLib
if __name__=="__main__":
    bilibiliLib = BilibiliLib()
    res = bilibiliLib.parse_video(<buvid>)
```
