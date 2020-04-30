# springboot + jpa + h2 内嵌文件整合

在使用 h2 之前，我折腾了一下 sqlite3 数据库，主要想通过内嵌的方式集成到 springboot 项目中，用以解决算法服务常用参数存储问题。在完成所有配置后，数据插入和查询功能一切正常，但是 jpa 无法自动在 sqlite3 中创建对应的标，手动方式创建表后，jpa 也无法将数据写入表中，查询返回结果为空。在查遍百度和谷歌没找到解决方案后，只能放弃，投奔 h2.

H2 是一个很小的嵌入式数据库引擎，它提供 JDBC、ODBC 访问接口，支持三种连接方式：

- 内嵌模式（通过 JDBC 进行本地连接，应用和数据库在同一个 JVM 中）
- 服务器模式（通过 JDBC 或 ODBC 或 TCP/IP 进行远程连接）
- 混合模式（同时支持本地和远程连接）

本文主要采用内嵌模式来使用 h2，数据保存在本地文件汇总。

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

集成 h2 所需要的 jar 比集成 sqlite3 少很多，配置起来也方便很多。

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

h2 采用以本地文件形式存储数据仅支持同一时刻一个客户端访问，如果要支持多客户端访问需要采用服务器方式部署。h2 的 bin 目录下 b2.bat、h2.sh 分别为 windows 和 linux 下的启动脚本，在 h2 启动后，将上面配置文件中的`url`设置为`jdbc:h2:tcp://localhost/~/mydb`即可。

## entity 类

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

Entity、Table、Id、GeneratedValue、Column 全部来自于 javax.persistence，没特殊需求不用去手动配置 DataSourceConfig 和 JpaConfig 以及连接池，毕竟算法服务常用的参数不是太多。

## web 页面管理 h2

启动 springboot 程序后，可以在浏览器中输入`http://localhost:8080/console`进入 web 管理页面，其中 8080 为 springboot 程序的启动端口。
![img1](<./1588162581(1).png>)
`JDBC URL`选项输入时一定要注意，保持和`application.yml`中数据库的位置一致。我开始的时候通过弹出手动定位数据库文件的路径，导致登录时用户名和密码错误，只能以无密码无用户的方式进入，进去后找不到 jpa 创建的表。这个坑差点让我放弃折腾嵌入式数据库。

## dbvis 连接 h2 查看数据

dbvis 这个数据库客户端是这次为了查看 h2 中的数据发现的，此前一直用的 Navicat Premium 不支持连接 h2。连接 h2 的过程中大致看了，dbvis 支持的数据库种类还是很多的，界面还行。通过 dbvis 查看 h2 的结果如下：
![img1](<./1588163477(1).png>)
