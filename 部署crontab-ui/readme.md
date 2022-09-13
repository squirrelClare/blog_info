# centos8部署crontab-ui
## 清理系统原始源
- 切换目录`cd /etc/yum.repos.d/`
- 备份源文件信息`tar zcf /home/yum.repos.d.tar.gz /etc/yum.repos.d/
- 清除无用的源文件信息`rm -rf CentOS-*.rpmsave`
- 注释CentOS-Epel.repo源文件中的failovermethod=priority
- 修改软件源mirrors 地址
    ```
    # 进入/etc/yum.repos.d目录
    cd /etc/yum.repos.d/

    # 修改所有源的链接地址
    # 注释掉mirrorlist链接路径
    sed -i 's/mirrorlist=/#mirrorlist=/g' /etc/yum.repos.d/CentOS-*
    # 解开并修改baseurl链接路径
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

    # 重建缓冲
    yum clean all && yum makecache
    ```

- 修改源地址为阿里地址
```
# 继续第二步进行修改baseurl链接路径
# 修改为阿里源路径
sed -i 's|baseurl=http://mirrors.tencentyun.com/epel/$releasever/Everything/$basearch|baseurl=http://mirrors.aliyun.com/epel-archive/8/Everything/$basearch|g' /etc/yum.repos.d/CentOS-Epel.repo
sed -i 's|baseurl=http://vault.centos.org/$contentdir/$releasever/BaseOS/$basearch/os/|baseurl=http://mirrors.aliyun.com/centos-vault/8.5.2111/BaseOS/$basearch/os/|g' /etc/yum.repos.d/CentOS-Linux-BaseOS.repo
sed -i 's|baseurl=http://vault.centos.org/$contentdir/$releasever/AppStream/$basearch/os/|baseurl=http://mirrors.aliyun.com/centos-vault/8.5.2111/AppStream/$basearch/os/|g' /etc/yum.repos.d/CentOS-Linux-AppStream.repo
sed -i 's|baseurl=http://vault.centos.org/$contentdir/$releasever/extras/$basearch/os/|baseurl=http://mirrors.aliyun.com/centos-vault/8.5.2111/extras/$basearch/os/|g' /etc/yum.repos.d/CentOS-Linux-Extras.repo

# 重建缓冲
yum clean all && yum makecache
```
## npm安装
```
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
yum -y install nodejs
# 供升级使用
npm install -g npm@8.19.1
```
### crontab-ui部署
- 安装`npm install crontab-ui -g`
- 开放9000端口
    ```
    firewall-cmd --zone=public --add-port=9000/tcp --permanent
    firewall-cmd --reload
    ```
- 启动 `BASIC_AUTH_USER=zhangcc BASIC_AUTH_PWD=DSIJHif12498 CRON_DB_PATH=/opt/crontab-ui HOST=0.0.0.0 PORT=9000 BASE_URL=/alse crontab-ui`
- 目前没有找到后台启动的方式。

<!-- 20 18 * * * python3 /home/zhangcc/mission/mission_feature_top_5_percent_ratio.py -->
