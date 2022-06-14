# flink：异常Could not restore keyed state backend for WindowOperator_dc884d3afcb3f5eae0b484f0f1cb3fe2_(1/1) 
## 异常描述
```
java.lang.Exception: Exception while creating StreamOperatorStateContext.
2021/2/4 上午10:42:40	at org.apache.flink.streaming.api.operators.StreamTaskStateInitializerImpl.streamOperatorStateContext(StreamTaskStateInitializerImpl.java:191)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.api.operators.AbstractStreamOperator.initializeState(AbstractStreamOperator.java:255)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.runtime.tasks.StreamTask.initializeStateAndOpen(StreamTask.java:1015)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.runtime.tasks.StreamTask.lambda$beforeInvoke$0(StreamTask.java:460)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.runtime.tasks.StreamTaskActionExecutor$SynchronizedStreamTaskActionExecutor.runThrowing(StreamTaskActionExecutor.java:94)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.runtime.tasks.StreamTask.beforeInvoke(StreamTask.java:455)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.runtime.tasks.StreamTask.invoke(StreamTask.java:467)
2021/2/4 上午10:42:40	at org.apache.flink.runtime.taskmanager.Task.doRun(Task.java:708)
2021/2/4 上午10:42:40	at org.apache.flink.runtime.taskmanager.Task.run(Task.java:533)
2021/2/4 上午10:42:40	at java.lang.Thread.run(Thread.java:748)
2021/2/4 上午10:42:40Caused by: org.apache.flink.util.FlinkException: Could not restore keyed state backend for WindowOperator_dc884d3afcb3f5eae0b484f0f1cb3fe2_(1/1) from any of the 1 provided restore options.
2021/2/4 上午10:42:40	at org.apache.flink.streaming.api.operators.BackendRestorerProcedure.createAndRestore(BackendRestorerProcedure.java:135)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.api.operators.StreamTaskStateInitializerImpl.keyedStatedBackend(StreamTaskStateInitializerImpl.java:304)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.api.operators.StreamTaskStateInitializerImpl.streamOperatorStateContext(StreamTaskStateInitializerImpl.java:131)
2021/2/4 上午10:42:40	... 9 more
2021/2/4 上午10:42:40Caused by: org.apache.flink.runtime.state.BackendBuildingException: Failed when trying to restore heap backend
2021/2/4 上午10:42:40	at org.apache.flink.runtime.state.heap.HeapKeyedStateBackendBuilder.build(HeapKeyedStateBackendBuilder.java:116)
2021/2/4 上午10:42:40	at org.apache.flink.runtime.state.filesystem.FsStateBackend.createKeyedStateBackend(FsStateBackend.java:529)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.api.operators.StreamTaskStateInitializerImpl.lambda$keyedStatedBackend$1(StreamTaskStateInitializerImpl.java:288)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.api.operators.BackendRestorerProcedure.attemptCreateAndRestore(BackendRestorerProcedure.java:142)
2021/2/4 上午10:42:40	at org.apache.flink.streaming.api.operators.BackendRestorerProcedure.createAndRestore(BackendRestorerProcedure.java:121)
2021/2/4 上午10:42:40	... 11 more
2021/2/4 上午10:42:40Caused by: java.io.FileNotFoundException: /opt/flink/checkpoints/7537dc3f6f78550f2c00c4916c5759d1/chk-120/75613fb4-ca59-4264-850c-acfb3aee282b (No such file or directory)
2021/2/4 上午10:42:40	at java.io.FileInputStream.open0(Native Method)
2021/2/4 上午10:42:40	at java.io.FileInputStream.open(FileInputStream.java:195)
2021/2/4 上午10:42:40	at java.io.FileInputStream.<init>(FileInputStream.java:138)
2021/2/4 上午10:42:40	at org.apache.flink.core.fs.local.LocalDataInputStream.<init>(LocalDataInputStream.java:50)
2021/2/4 上午10:42:40	at org.apache.flink.core.fs.local.LocalFileSystem.open(LocalFileSystem.java:142)
2021/2/4 上午10:42:40	at org.apache.flink.core.fs.SafetyNetWrapperFileSystem.open(SafetyNetWrapperFileSystem.java:85)
2021/2/4 上午10:42:40	at org.apache.flink.runtime.state.filesystem.FileStateHandle.openInputStream(FileStateHandle.java:68)
2021/2/4 上午10:42:40	at org.apache.flink.runtime.state.KeyGroupsStateHandle.openInputStream(KeyGroupsStateHandle.java:117)
2021/2/4 上午10:42:40	at org.apache.flink.runtime.state.heap.HeapRestoreOperation.restore(HeapRestoreOperation.java:124)
2021/2/4 上午10:42:40	at org.apache.flink.runtime.state.heap.HeapKeyedStateBackendBuilder.build(HeapKeyedStateBackendBuilder.java:114)
2021/2/4 上午10:42:40	... 15 more
```
## 原因
checkpoint建立失败。
## 解决方法
延长检查点的创建时间，具体设置如下：
```
    env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)
    // 每隔1000 ms进行启动一个检查点【设置checkpoint的周期】
    env.enableCheckpointing(20000)
    // 高级选项：
    // 设置模式为exactly-once （这是默认值）
    env.getCheckpointConfig.setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE)
    // 确保检查点之间有至少500 ms的间隔【checkpoint最小间隔】
    env.getCheckpointConfig.setMinPauseBetweenCheckpoints(1000)
    // 检查点必须在一分钟内完成，或者被丢弃【checkpoint的超时时间】
    env.getCheckpointConfig.setCheckpointTimeout(60000)
    // 同一时间只允许进行一个检查点
    env.getCheckpointConfig.setMaxConcurrentCheckpoints(3)
    env.getCheckpointConfig.setTolerableCheckpointFailureNumber(12)
    // 表示一旦Flink处理程序被cancel后，会保留Checkpoint数据，以便根据实际需要恢复到指定的Checkpoin
    //ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION:表示一旦Flink处理程序被cancel后，会保留Checkpoint数据，以便根据实际需要恢复到指定的Checkpoint
    //ExternalizedCheckpointCleanup.DELETE_ON_CANCELLATION: 表示一旦Flink处理程序被cancel后，会删除Checkpoint数据，只有job执行失败的时候才会保存checkpoint
    env.getCheckpointConfig.enableExternalizedCheckpoints(CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION)
```