# flink异常：java.lang.RuntimeException: Error while creating the channel

##  异常描述
flink将处理好的数据流写入rabbitmq可能报错以下错误
```
Exception in thread "main" org.apache.flink.runtime.client.JobExecutionException: Job execution failed.
	at org.apache.flink.runtime.jobmaster.JobResult.toJobExecutionResult(JobResult.java:146)
	at org.apache.flink.runtime.minicluster.MiniCluster.executeJobBlocking(MiniCluster.java:626)
	at org.apache.flink.streaming.api.environment.LocalStreamEnvironment.execute(LocalStreamEnvironment.java:117)
	at org.apache.flink.streaming.api.environment.StreamExecutionEnvironment.execute(StreamExecutionEnvironment.java:1507)
	at org.apache.flink.streaming.api.scala.StreamExecutionEnvironment.execute(StreamExecutionEnvironment.scala:654)
	at com.crie.secp.context.FlinkContext$.run(FlinkContext.scala:72)
	at com.crie.secp.App$.main(App.scala:23)
	at com.crie.secp.App.main(App.scala)
Caused by: java.lang.RuntimeException: Error while creating the channel
	at org.apache.flink.streaming.connectors.rabbitmq.RMQSink.open(RMQSink.java:154)
	at org.apache.flink.api.common.functions.util.FunctionUtils.openFunction(FunctionUtils.java:36)
	at org.apache.flink.streaming.api.operators.AbstractUdfStreamOperator.open(AbstractUdfStreamOperator.java:102)
	at org.apache.flink.streaming.api.operators.StreamSink.open(StreamSink.java:48)
	at org.apache.flink.streaming.runtime.tasks.StreamTask.openAllOperators(StreamTask.java:532)
	at org.apache.flink.streaming.runtime.tasks.StreamTask.invoke(StreamTask.java:396)
	at org.apache.flink.runtime.taskmanager.Task.doRun(Task.java:705)
	at org.apache.flink.runtime.taskmanager.Task.run(Task.java:530)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.IOException
	at com.rabbitmq.client.impl.AMQChannel.wrap(AMQChannel.java:124)
	at com.rabbitmq.client.impl.AMQChannel.wrap(AMQChannel.java:120)
	at com.rabbitmq.client.impl.AMQChannel.exnWrappingRpc(AMQChannel.java:142)
	at com.rabbitmq.client.impl.ChannelN.queueDeclare(ChannelN.java:952)
	at com.rabbitmq.client.impl.recovery.AutorecoveringChannel.queueDeclare(AutorecoveringChannel.java:333)
	at org.apache.flink.streaming.connectors.rabbitmq.RMQSink.setupQueue(RMQSink.java:124)
	at org.apache.flink.streaming.connectors.rabbitmq.RMQSink.open(RMQSink.java:149)
	... 8 more
Caused by: com.rabbitmq.client.ShutdownSignalException: channel error; protocol method: #method<channel.close>(reply-code=406, reply-text=PRECONDITION_FAILED - inequivalent arg 'durable' for queue 'JIANG_BEI_SUMMARY_DATA_LINE_15MIN' in vhost '/': received 'false' but current is 'true', class-id=50, method-id=10)
	at com.rabbitmq.utility.ValueOrException.getValue(ValueOrException.java:66)
	at com.rabbitmq.utility.BlockingValueOrException.uninterruptibleGetValue(BlockingValueOrException.java:36)
	at com.rabbitmq.client.impl.AMQChannel$BlockingRpcContinuation.getReply(AMQChannel.java:443)
	at com.rabbitmq.client.impl.AMQChannel.privateRpc(AMQChannel.java:263)
	at com.rabbitmq.client.impl.AMQChannel.exnWrappingRpc(AMQChannel.java:136)
	... 12 more
```
##  原因
异常信息显示rabbitmq内队列的durable和flink流中配置的队列的值不一致，经分析发现rabbitmq内的队列durable为true，而flink中使用的是RMQSink，该类的setupQueue方法源码如下：
```
	protected void setupQueue() throws IOException {
		if (queueName != null) {
			channel.queueDeclare(queueName, false, false, false, null);
		}
	}
```
channel.queueDeclare的第二个参数对应着队列的durable属性，此处被设置为false，这是造成上述异常的原因。因此只需要将该方法重载就可以解决掉异常。

##  解决方法
重载RMQSink类
```
import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSink;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSinkPublishOptions;
import org.apache.flink.streaming.connectors.rabbitmq.SerializableReturnListener;
import org.apache.flink.streaming.connectors.rabbitmq.common.RMQConnectionConfig;

import java.io.IOException;

public class RMQDurableSink<IN> extends RMQSink<IN> {

    /**
     * @param rmqConnectionConfig The RabbitMQ connection configuration {@link RMQConnectionConfig}.
     * @param queueName           The queue to publish messages to.
     * @param schema              A {@link SerializationSchema} for turning the Java objects received into bytes
     */
    public RMQDurableSink(RMQConnectionConfig rmqConnectionConfig, String queueName, SerializationSchema<IN> schema) {
        super(rmqConnectionConfig, queueName, schema);
    }

    /**
     * @param rmqConnectionConfig The RabbitMQ connection configuration {@link RMQConnectionConfig}.
     * @param schema              A {@link SerializationSchema} for turning the Java objects received into bytes
     * @param publishOptions      A {@link RMQSinkPublishOptions} for providing message's routing key and/or properties
     *                            In this case the computeMandatoy or computeImmediate MUST return false otherwise an
     */
    public RMQDurableSink(RMQConnectionConfig rmqConnectionConfig, SerializationSchema<IN> schema, RMQSinkPublishOptions<IN> publishOptions) {
        super(rmqConnectionConfig, schema, publishOptions);
    }

    /**
     * @param rmqConnectionConfig The RabbitMQ connection configuration {@link RMQConnectionConfig}.
     * @param schema              A {@link SerializationSchema} for turning the Java objects received into bytes
     * @param publishOptions      A {@link RMQSinkPublishOptions} for providing message's routing key and/or properties
     * @param returnListener      A SerializableReturnListener implementation object to handle returned message event
     */
    public RMQDurableSink(RMQConnectionConfig rmqConnectionConfig, SerializationSchema<IN> schema, RMQSinkPublishOptions<IN> publishOptions, SerializableReturnListener returnListener) {
        super(rmqConnectionConfig, schema, publishOptions, returnListener);
    }

    /**
     * Sets up the queue. The default implementation just declares the queue. The user may override
     * this method to have a custom setup for the queue (i.e. binding the queue to an exchange or
     * defining custom queue parameters)
     */
    @Override
    protected void setupQueue() throws IOException {
        if (queueName != null) {
            channel.queueDeclare(queueName, true, false, false, null);
        }
    }
}

```