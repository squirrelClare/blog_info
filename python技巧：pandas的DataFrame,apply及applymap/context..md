# python技巧：pandas的DataFrame,apply及applymap
## apply方法
```
    def apply(self, func, axis=0, broadcast=None, raw=False, reduce=None,
              result_type=None, args=(), **kwds):
```
参数：
- func: 函数体，可以为lambda表达式、自定义函数、内置函数。
- axis：0：func应用于数据框的列；1：0：func应用于数据框的行。
- broadcast：弃用，合并到result_type：。
- raw：弃用，合并到result_type。
- reduce：弃用，合并到result_type。
- result_type：
  - expand：func返回的列表类型结果转为数据框的多个列。
  - reduce：func返回的列表类型结果合并为Series类型，作用与expand相反。
  - broadcast：沿用原始数据框的列名和行索引，将fucn返回的数据按行或列进行填充。
###  示例
```
import pandas as pd
df = pd.DataFrame([[4, 9, 21],] * 3, columns=['A', 'B', 'C'])
```
运行结果
```
   A  B   C
0  4  9  21
1  4  9  21
2  4  9  21
```
### 行列运算
按行运算
```
print(df.apply(lambda x: np.sum(x),axis=1))
```
运行结果
```
0    34
1    34
2    34
```
---
按列运算
```
print(df.apply(lambda x: np.sum(x),axis=0))
```
运行结果
```
A    12
B    27
C    63
```
### result_type选择broadcast
按行运算，func返回单个元素
```
print(df.apply(lambda x: np.sum(x),axis=1, result_type="broadcast"))
```
运行结果
```
    A   B   C
0  34  34  34
1  34  34  34
2  34  34  34
```
按列运算，func返回单个元素
```
print(df.apply(lambda x: np.sum(x),axis=0, result_type="broadcast"))
```
运行结果
```
    A   B   C
0  12  27  63
1  12  27  63
2  12  27  63
```
按行运算，func返回列表
```
print(df.apply(lambda x: [1, 3, 4], axis=1, result_type="broadcast"))
```
返回结果
```
   A  B  C
0  1  3  4
1  1  3  4
2  1  3  4
```
按列运算，func返回列表
```
print(df.apply(lambda x: [1, 3, 4], axis=1, result_type="broadcast"))
```
返回结果
```
   A  B  C
0  1  1  1
1  3  3  3
2  4  4  4
```
### result_type选择expand
按行运算，func返回列表
```
print(df.apply(lambda x: [1, 4], axis=1, result_type="expand"))
```
返回结果
```
   0  1
0  1  4
1  1  4
2  1  4
```
按列运算，func返回列表
```
print(df.apply(lambda x: [1, 4], axis=0, result_type="expand"))
```
返回结果
```
   A  B  C
0  1  1  1
1  4  4  4
```