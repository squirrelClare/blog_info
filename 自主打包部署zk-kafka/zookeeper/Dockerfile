# FROM命令 定义基础包
FROM docker.io/centos:centos7.2.1511
# ADD命令 将打包文件上传到镜像的根目录/ ,会自动解压
ADD zookeeper.tar /opt
ADD jdk.tar /opt
# WORKDIR命令 定义工作目录
WORKDIR /opt
# ENV命令 设置环境
ENV JAVA_HOME /opt/jdk
ENV CLASSPATH .:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV PATH $JAVA_HOME/bin:$PATH
# RUN命令 执行制作镜像过程，一个RUN对应一层
#RUN yum clean all \
RUN rm -vf /etc/localtime \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime\
    #&& rm -rfv /usr/share/backgrounds/* \
    #&& rm -rfv /usr/share/doc/* \
    #&& rm -rfv /usr/share/man/* \
    #&& cd /usr/share/zoneinfo/ && ls |grep -v "Asia"|xargs rm -rfv \
    #&& rm -rfv /var/cache/yum/* \
    #&& rpm --rebuilddb \
    && chmod 755 /opt/zookeeper/bin/start-zookeeper.sh

ENTRYPOINT /opt/zookeeper/bin/start-zookeeper.sh

