# springboot + jpa + h2内嵌文件整合
在使用h2之前，我折腾了一下sqlite3数据库，主要想通过内嵌的方式集成到springboot项目中，用以解决算法服务常用参数存储问题。在完成所有配置后，数据插入和查询功能一切正常，但是jpa无法自动在sqlite3中创建对应的标，手动方式创建表后，jpa也无法将数据写入表中，查询返回结果为空。在查遍百度和谷歌没找到解决方案后，只能放弃，投奔h2.

H2是一个很小的嵌入式数据库引擎，它提供JDBC、ODBC访问接口，支持三种连接方式：
- 内嵌模式（通过JDBC进行本地连接，应用和数据库在同一个JVM中）
- 服务器模式（通过JDBC或ODBC或TCP/IP进行远程连接）
- 混合模式（同时支持本地和远程连接）

 本文主要采用内嵌模式来使用h2，数据保存在本地文件汇总。
 
 ## pom.xml
 ```
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
 ```
 集成h2所需要的jar比集成sqlite3少很多，配置起来也方便很多。
 ## application.yml
```
spring:
  application:
    name: demo
  datasource:
    driverClassName: org.h2.Driver
    url: jdbc:h2:file:d:/tools/h2/mydb;AUTO_SERVER=TRUE;DB_CLOSE_DELAY=-1
    platform: h2
    username: ***
    password: ***
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
#    generate-ddl: false
    show-sql: true
    hibernate:
      ddl-auto: update # 自动建表
  h2: # h2的web管理端配置
    console:
      enabled: true
      path: /console
      settings:
        trace: false
        web-allow-others: true
```
## entity类
```
package com.****.****.pojo.po;
import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name = "t_city_temperature_per_month")
public class CityTemperaturePerMonthPo implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name="id")
    private Integer id;
    @Column(name = "city_id")
    private String cityId;
    @Column(name = "month")
    private int month;
    @Column(name = "temperature_value")
    private double temperatureValue;
}

```
Entity、Table、Id、GeneratedValue、Column全部来自于javax.persistence，没特殊需求不用去手动配置DataSourceConfig和JpaConfig以及连接池，毕竟算法服务常用的参数不是太多。

## web页面管理h2
启动springboot程序后，可以在浏览器中输入`http://localhost:8080/console`进入web管理页面，其中8080为springboot程序的启动端口。
![img1](./1588162581(1).png)
`JDBC URL`选项输入时一定要注意，保持和`application.yml`中数据库的位置一致。我开始的时候通过弹出手动定位数据库文件的路径，导致登录时用户名和密码错误，只能以无密码无用户的方式进入，进去后找不到jpa创建的表。这个坑差点让我放弃折腾嵌入式数据库。
## dbvis连接h2查看数据
dbvis这个数据库客户端是这次为了查看h2中的数据发现的，此前一直用的Navicat Premium不支持连接h2。连接h2的过程中大致看了，dbvis支持的数据库种类还是很多的，界面还行。通过dbvis查看h2的结果如下：
![img1](./1588163477(1).png)