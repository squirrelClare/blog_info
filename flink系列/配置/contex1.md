#  flink程序中加载配置文件

##  创建properties文件
在resources目录下创建application.properties文件，可以在内部自由写入配置信息
```
#   redis
service.redis.host=191.11.91.83
service.redis.port=6379
service.redis.password=
service.redis.timeout=10000

#   消息队列
service.rmq.host=112.118.19.23
service.rmq.port=5672
service.rmq.username=admin
service.rmq.password=admin12312
#   毫秒
service.rmq.timeout=10000
```
##   pom文件加入config依赖包
```
    <dependency>
      <groupId>com.typesafe</groupId>
      <artifactId>config</artifactId>
      <version>1.2.1</version>
    </dependency>
```

##   使用
```
object RedisConfig {
    val configInfo = ConfigFactory.load()
    def config(): FlinkJedisPoolConfig = {
        var config = new FlinkJedisPoolConfig.Builder()
                .setHost(configInfo.getString("service.redis.host"))
                .setPort(configInfo.getInt("service.redis.port"))
//                .setPassword(configInfo.getString("service.redis.password"))
                .setTimeout(configInfo.getInt("service.redis.timeout"))
                .build()
        config
    }
```