# flink异常：A typical reason for `AskTimeoutException` is that the recipient actor didn't send a reply.

## 异常描述
flink程序本地idea研发环境汇总使用正常，部署到flink web端后报以下错误信息
```
akka.pattern.AskTimeoutException: Ask timed out on [Actor[akka://flink/user/dispatcher#243037388]] after [10000 ms]. Message of type [org.apache.flink.runtime.rpc.messages.LocalFencedMessage]. A typical reason for `AskTimeoutException` is that the recipient actor didn't send a reply.
	at akka.pattern.PromiseActorRef$$anonfun$2.apply(AskSupport.scala:635)
	at akka.pattern.PromiseActorRef$$anonfun$2.apply(AskSupport.scala:635)
	at akka.pattern.PromiseActorRef$$anonfun$1.apply$mcV$sp(AskSupport.scala:648)
	at akka.actor.Scheduler$$anon$4.run(Scheduler.scala:205)
	at scala.concurrent.Future$InternalCallbackExecutor$.unbatchedExecute(Future.scala:601)
	at scala.concurrent.BatchingExecutor$class.execute(BatchingExecutor.scala:109)
	at scala.concurrent.Future$InternalCallbackExecutor$.execute(Future.scala:599)
	at akka.actor.LightArrayRevolverScheduler$TaskHolder.executeTask(LightArrayRevolverScheduler.scala:328)
	at akka.actor.LightArrayRevolverScheduler$$anon$4.executeBucket$1(LightArrayRevolverScheduler.scala:279)
	at akka.actor.LightArrayRevolverScheduler$$anon$4.nextTick(LightArrayRevolverScheduler.scala:283)
	at akka.actor.LightArrayRevolverScheduler$$anon$4.run(LightArrayRevolverScheduler.scala:235)
	at java.lang.Thread.run(Thread.java:745)
```
##  解决方法
升级flink运行环境的jdk版本。