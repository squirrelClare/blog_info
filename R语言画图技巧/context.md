# R语言ggplot画图技巧
## 手动设置颜色
```
scale_fill_manual(values=c("#999999","#00FA9A","#56B4E9","#D2691E", "#DAA520","#F0FFFF", "#F5DEB3","#FF6347"))
```
具体颜色值的数量需要根据实际需求设置
## 图片保存为pdf中文显示异常
library(Cairo)
CairoPDF("char_3.7_2.pdf")
ggplot(tree, aes(area = 占比, fill=科目,label = paste(round(占比*100,2), "%", sep=''))) + 
  scale_fill_manual(values=c("#999999","#00FA9A","#56B4E9","#D2691E", "#DAA520","#9932CC", "#F5DEB3","#FF6347"))+
  geom_treemap() +  geom_treemap_text(fontface = "italic", colour = "black", min.size = 4, place = "centre",reflow = TRUE,alpha=.5) + 
  theme(legend.position="bottom",legend.title = element_blank(),legend.text = element_text(size = 14, face = 'bold',family = "STKaiti"))
dev.off()
## 标题置空
有些地方不想要标题可以设置为element_blank()
legend.title = element_blank()