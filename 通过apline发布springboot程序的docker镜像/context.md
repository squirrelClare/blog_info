---

- 张聪聪 华润智慧能源有限公司
- 2020-06-10

---
# 通过apline发布springboot程序的docker镜像
## 获取基于apline的jdk
Alpine Linux 是一个社区开发的面向安全应用的轻量级Linux发行版。选择基于Alpine的JDK8作为springboot程序的基础运行环境，可以大大减小最终的镜像包及容器运行时所使用的资源。可执行下属命令拉取apline的jdk镜像，该镜像仅104M。
```
docker pull yfrepo/apline-openjdk8
```
## docker镜像制作
- 创建一个新的目录，并进入到目录；
- 新建一个名为`Dockfile`的文件，`touch Dockfile`；
- 在文件内写入一下内容：
```
# Pull base image
FROM yfrepo/apline-openjdk8 

MAINTAINER zcc "zcc@136314853@163.com" 
VOLUME /tmp

# 添加
COPY *.jar app.jar
#RUN bash -c 'touch /app.jar'
# 设置东8时区
RUN echo 'http://mirrors.ustc.edu.cn/alpine/v3.5/main' > /etc/apk/repositories 
RUN echo 'http://mirrors.ustc.edu.cn/alpine/v3.5/community' >>/etc/apk/repositories
RUN apk update && apk add tzdata
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone
#设置变量 JAVA_OPTS 
ENV JAVA_OPTS=""
#这样写会以shell方式执行，会替换变量
ENTRYPOINT java ${JAVA_OPTS} -Djava.security.egd=file:/dev/./urandom -jar /app.jar
```
- 镜像创建，`docker build -t springbootdemo.v.10.19 .`;
## 容器运行
上述Dockfile文件中的JAVA_OPTS参数可以配置容器运行时所需要的内存大小，[博客]([链接地址](https://www.cnblogs.com/a393060727/p/13595434.html))中给出了集中常用的内存配置方案：
```
分配内存 堆配置推荐 
2G -Xmx1344M -Xms1344M -Xmn448M -XX:MaxMetaspaceSize=192M -XX:MetaspaceSize=192M 
3G -Xmx2048M -Xms2048M -Xmn768M -XX:MaxMetaspaceSize=256M -XX:MetaspaceSize=256M 
4G -Xmx2688M -Xms2688M -Xmn960M -XX:MaxMetaspaceSize=256M -XX:MetaspaceSize=256M 
5G -Xmx3392M -Xms3392M -Xmn1216M -XX:MaxMetaspaceSize=512M -XX:MetaspaceSize=512M 
6G -Xmx4096M -Xms4096M -Xmn1536M -XX:MaxMetaspaceSize=512M -XX:MetaspaceSize=512M 
7G -Xmx4736M -Xms4736M -Xmn1728M -XX:MaxMetaspaceSize=512M -XX:MetaspaceSize=512M 
8G -Xmx5440M -Xms5440M -XX:MaxMetaspaceSize=512M -XX:MetaspaceSize=512M 
```
使用如下命令可以将容器后台运行
```
docker run --name docker_test -e  JAVA_OPTS='-Xmx1344M -Xms1344M -Xmn448M -XX:MaxMetaspaceSize=192M -XX:MetaspaceSize=192M' -p 8083:8081 -d springbootdemo.v.10.19
```
此命令将心运行的容器命名为`docker_test`，并将外部访问端口8083映射到容器的8081端口。