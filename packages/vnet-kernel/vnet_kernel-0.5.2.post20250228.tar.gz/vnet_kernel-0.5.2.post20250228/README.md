## 使用

```shell
$ sudo docker login --username=GnixAij crpi-fh5v47zqih6dmh6j.cn-hangzhou.personal.cr.aliyuncs.com
[OUTPUT]
Password: qwe123``
$ sudo docker pull crpi-fh5v47zqih6dmh6j.cn-hangzhou.personal.cr.aliyuncs.com/vnet/vnet-kernel:0.4.5
[OUTPUT]
0.4.5: Pulling from vnet/vnet-kernel
fd0410a2d1ae: Pull complete 
4f4fb700ef54: Pull complete 
2e828bf4b3ea: Pull complete 
0d57067b0070: Pull complete 
eebea7d23b79: Pull complete 
Digest: sha256:8e24d5a39d79b11d87bf5871d3b407d73ce8c38e9503b5cf2d29b103a3c080c6
Status: Downloaded newer image for crpi-fh5v47zqih6dmh6j.cn-hangzhou.personal.cr.aliyuncs.com/vnet/vnet-kernel:0.4.5
crpi-fh5v47zqih6dmh6j.cn-hangzhou.personal.cr.aliyuncs.com/vnet/vnet-kernel:0.4.5
```

## python

doc

```shell
$ uv pip install -r pyproject.toml --extra doc
$ mkdocs serve
```

dev

```shell
$ uv pip install -r pyproject.toml --extra dev
# test
$ make test
```

## IPC

1. 目前实现方案为使用 `json` 文件作为中间数据格式，Python 运行 HTTP 服务，C 通过 `curl.h` 构造 HTTP 请求
默认占用端口为 8000，执行时间在 1-3s； 2024.11.28
2. 使用 POSIX Message Queue 进行 VNet 与 C 的通信; 2024.11.30 

![alt text](assets/README.png)

## Ref

[VNet Labs](https://github.com/Efterklang/vnet-lab/blob/main/README.md)
