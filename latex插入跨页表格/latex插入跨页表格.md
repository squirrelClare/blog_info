#  latex插入跨页表格
论文或其它文档写作中经常遇到跨页表格，在latex中手撕代码写敲表格费时费力。简单的表格可以通过[https://tableconvert.com/](https://tableconvert.com/)、[http://www.tablesgenerator.com/](http://www.tablesgenerator.com/)等网站在线编辑表格然后生成latex代码。但是针对复杂表格特别是跨页表格，这种方式显然也是不适用的。写作用遇到的表格大多是来源于excel，如果不是可以将表格转为excel格式，这样就可以通过[excel2latex](https://ctan.org/tex-archive/support/excel2latex)将excel表格转为latex表格。
## excel2latex安装
首先登陆[https://ctan.org/tex-archive/support/excel2latex](https://ctan.org/tex-archive/support/excel2latex)下载并解压excel2latex，双击`Excel2LaTeX.xla`将宏安装到excel。

![img1](./1585793640(1).png)
## 表格转换为latex代码
在excel选定需要转换的表格区域，在加载项栏目中点击`Convert Table to  Latex`即可获得表格对应的latex代码。
![img1](./1585793964(1).png)
```
% Table generated by Excel2LaTeX from sheet 'Sheet1'
\begin{table}[htbp]
  \centering
  \caption{Add caption}
    \begin{tabular}{|c|c|c|}
    \toprule
    日期    & 2019A & 2019E \\
    \midrule
    类型    & 年报    & 年报 \\
    \midrule
    单位    & 万元    & 万元 \\
    \midrule
    \textbf{资产} &       &  \\
    \midrule
    \textbf{流动资产} &       &  \\
    \midrule
    现金及等价物 & 658,779 & 752,978 \\
    \midrule
    应收账款（账面） & 1,673,742 & 1,651,648 \\
    \midrule
    存货    & 322,294 & 326,511 \\
    \midrule
    预付款及其他 &                      -    & 10,832 \\
    \midrule
    短期金融资产 &       &  \\
    \midrule
    其他流动资产 & 5,201 & \textcolor[rgb]{ .267,  .447,  .769}{11,379} \\
    \bottomrule
    \end{tabular}%
  \label{tab:addlabel}%
\end{table}%
```
对于普通表格，可直接将上述代码粘贴到latex的tex文件中即可。不过改代码显示的表格竖线呈间断状。
![img1](./1585794224(1).png)

此时可以将源码中的`\midrule`、 `\toprule`、`\bottomrule`等替为`\hline`即可解决。

## 跨页表格
对于跨页表格若仅对excel转换后的源码进行上述修改，则会出现表格内容出现截断的情况，致使表格超出部分不显示。这里需要通过`\usepackage{longtable}`加载`longtable`包，并对源码进行修改，修改后的源码如下：
```
% Table generated by Excel2LaTeX from sheet 'Sheet1'
\begin{center}
    \setlength{\tabcolsep}{0.7mm}{
    \begin{longtable}{c|c|c}
        \caption{华电国际资产负债表对比}
        \label{tab:addlabe6} \\
        \hline
        日期    & 2019A & 2019E \\
        \hline
        类型    & 年报    & 年报 \\
        \hline
        单位    & 万元    & 万元 \\
        \hline
        \textbf{资产} &       &  \\
        \hline
        \textbf{流动资产} &       &  \\
        \hline
        现金及等价物 & 658,779 & 752,978 \\
        \hline
        应收账款（账面） & 1,673,742 & 1,651,648 \\
        \hline
        存货    & 322,294 & 326,511 \\
        \hline
        预付款及其他 &                      -    & 10,832 \\
        \hline
        短期金融资产 &       &  \\
        \hline
        其他流动资产 & 5,201 & \textcolor[rgb]{ .267,  .447,  .769}{11,379} \\
        \hline
        \end{longtable}%
    }
\end{center}%
```
需要注意的是下面部分源码
```
        \caption{华电国际资产负债表对比}
        \label{tab:addlabe6} \\
        \toprule
```
`caption`和`label`一定要放在`hline`前面且第一个`hline`前一行的结尾要加入`\\`。

将修改完后的源码粘贴到tex文件编译后就可以得到跨页显示的表格。
## 跨页表格的分页键入“接上表”
长表在跨越多个页面后，若需要在每页表格的顶部加入“接上表”等示意字段，可通过`\endfirsthead`和`\endhead`来实现，具体示例如下
```
 \begin{longtable}{cccccc}
      \label{tab:addlabel}                                                                      \\
      \caption{示例表}                                                                      \\
      \hline
      日期                     & 2006      & 2007      & 2008      & 2009     & 2010      \\
      \hline
      \endfirsthead
      \multicolumn{6}{c}{(接上表)}                                                              \\
      \endhead
      字段1                 &            &            &            &            &            \\

      字段2             & 646    & 7486    & 613    & 758    & 111  \\

      字段3                 & 120  & 167  & 1654  & 1648  & 1577 
      \hline
  \end{longtable}%
```
其中关键在于
```
      \endfirsthead
      \multicolumn{6}{c}{(接上表)}                                                              \\
      \endhead
```
`\multicolumn{6}{c}{(接上表)} `中的6表示的是表的列数，`c`表示“接上表”三字居中显示，若左侧显示可以改为`l`，右侧显示可改为`r`。