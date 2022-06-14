# flink异常：Could not forward element to next operator

## 异常描述
当flink的数据流中的元素字段内存在字段值为null的时候会报以下异常信息
```
org.apache.flink.streaming.runtime.tasks.ExceptionInChainedOperatorException: Could not forward element to next operator
	at org.apache.flink.streaming.runtime.tasks.OperatorChain$CopyingChainingOutput.pushToOperator(OperatorChain.java:654)
	at org.apache.flink.streaming.runtime.tasks.OperatorChain$CopyingChainingOutput.collect(OperatorChain.java:612)
	at org.apache.flink.streaming.runtime.tasks.OperatorChain$CopyingChainingOutput.collect(OperatorChain.java:592)
```
解决这个问题的方法就是进入流的每一元素中值为null的字段全部赋值，具体操作如下。

## null填充类
```
import java.lang.reflect.{Field, Method}
import java.lang.{Double, Float}

import cn.hutool.core.util.StrUtil
import org.slf4j.LoggerFactory

import scala.collection.mutable.ListBuffer

object BeanUtil {
    val logger = LoggerFactory.getLogger(BeanUtil.getClass)
    def fillNull[T: Manifest](t: T, clazz: Class[T]): T = {
        val fields = getAllFields(clazz)
        var i = 0
        for (field <- fields) {

            try {
                fillNumber(field, t, clazz)
                fillString(field, t, clazz)
            } catch {
                case ex: Exception => logger.error("字段 %s 填充失败".format(field.getName))
            }
        }
        t
    }

    def fillString[T: Manifest](field: Field, bean: T, clazz: Class[T]): Unit = {
        if (field.getGenericType.toString.equals("class java.lang.String")) {
            val getMethod = clazz.getMethod("get" + getMethodName(field.getName))
            val value = getMethod.invoke(bean).asInstanceOf[String]
            val setMethod = clazz.getMethod("set" + getMethodName(field.getName), classOf[String])
            if (StrUtil.isEmpty(value)) {
                setMethod.invoke(bean, "")
            }
        }
    }
    def fillNumber[T: Manifest](field: Field, bean: T, clazz: Class[T]): Unit = {

        if (field.getGenericType.toString.equals("class java.lang.Double")) {
            val getMethod = clazz.getMethod("get" + getMethodName(field.getName))
            val value = getMethod.invoke(bean).asInstanceOf[Double]
            val setMethod = clazz.getMethod("set" + getMethodName(field.getName), classOf[Double])
            if (value == null) {
                setMethod.invoke(bean, Double.valueOf(0.0f))
            }
        }

        if (field.getGenericType.toString.equals("class java.lang.Float")) {
            val getMethod = clazz.getMethod("get" + getMethodName(field.getName))
            val value = getMethod.invoke(bean).asInstanceOf[Float]

            val setMethod = clazz.getMethod("set" + getMethodName(field.getName), classOf[Double])
            if (value == null) {
                setMethod.invoke(bean, Float.valueOf(0.0f))
            }
        }
        if (field.getGenericType.toString.equals("class java.lang.Integer")) {
            val getMethod = clazz.getMethod("get" + getMethodName(field.getName))
            val value = getMethod.invoke(bean).asInstanceOf[Integer]

            val setMethod = clazz.getMethod("set" + getMethodName(field.getName), classOf[Integer])
            if (value == null) {
                setMethod.invoke(bean, Integer.valueOf(0))
            }
        }
    }

    def getAllFields[T](t: Class[T]): List[Field] = {
        //将所有获取到的父类属性加进一个数组中
        val buffer = new ListBuffer[Field]
        var clazz: Class[_ >: T] = t
        while (clazz != null) {
            val fields: Array[Field] = clazz.getDeclaredFields()
            buffer.appendAll(fields)
            clazz = clazz.getSuperclass
        }
        buffer.toList
    }

    def getMethodName(fildeName: String): String = {
        val times = fildeName.getBytes()
        return fildeName.substring(0, 1).toUpperCase + fildeName.substring(1, fildeName.length)
    }
}
```
## 调用方法
```
steamSummary.map(e => BeanUtil.fillNull(e, classOf[MyBean]))
```