# 安装 CentOS7/8/9 系统（最小化安装即可）
原始博客地址https://itcn.blog/p/4757531005.html
## Docker安装
- 安装yum命令行工具
`yum install -y yum-utils`
- 安装清华源
```
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo sed -i 's+download.docker.com+mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
```
- 安装Docker-CE
`yum install -y docker-ce`
- 添加Docker加速源
```
vim /etc/docker/daemon.json
 
{
    "registry-mirrors": [
        "https://docker.mirrors.ustc.edu.cn",
        "https://registry.docker-cn.com",
        "https://hub-mirror.c.163.com",
        "https://mirror.ccs.tencentyun.com",
        "http://f1361db2.m.daocloud.io"
    ]
}
```
- 设置Docker开机自启
`systemctl enable docker`
- 启动Docker服务
`systemctl start docker`
## 创建青龙面板
- 拉取青龙镜像（我这里选择 edge 最新版本）
`docker pull whyour/qinglong:edge`
- 创建目录（自行斟酌，可不创建目录映射）
```
mkdir -p /opt/ql/data/config
mkdir -p /opt/ql/data/db
mkdir -p /opt/ql/data/scripts
mkdir -p /opt/ql/data/repo
mkdir -p /opt/ql/data/log
```
- 创建青龙容器
```
docker run -dit -p 5700:5700 -v /ql/data/config:/opt/ql/data/config -v /ql/data/db:/opt/ql/data/db -v /ql/data/scripts:/opt/ql/data/scripts -v /ql/data/repo:/opt/ql/data/repo -v /ql/data/log:/opt/ql/data/log --name=qinglong --hostname=qinglong --restart=Always whyour/qinglong:edge
```
- 查看容器状态
`docker ps`
- 基础环境配置
    -进入容器
    `docker exec -it qinglong bash`
    - 修改npm源
    `npm config set registry https://registry.npm.taobao.org`
    - 安装pnpm管理工具
    `npm install pnpm -g`
    - 一键安装大部分依赖
    `curl -fsSL https://github.91chi.fun/https://raw.githubusercontent.com/FlechazoPh/QLDependency/main/Shell/QLOneKeyDependency.sh | sh`
- 重新启动容器

```
exit 退出容器
docker restart qinglong
docker exec -it qinglong bash
pnpm i
```