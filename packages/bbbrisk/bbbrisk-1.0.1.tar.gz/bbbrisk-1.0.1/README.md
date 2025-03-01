# bbbrisk-bbb风控包
本代码由bbbdata为评分卡专门开发的小贷风控包
评分卡教程和本代码的使用说明请参考:https://www.bbbdata.com

## Install and Upgrade · 安装与升级
Pip

```bash
pip install bbbrisk # to install
pip install -U bbbrisk # to upgrade
```

## Key features · 主要功能
- 变量分箱与分析
例如变量自动分箱,如下：

```python
bin_set  = bins.autoBin(x, y,enum_var=['city','marital'])    # 自动分箱,如果有枚举变量,必须指出哪些是枚举变量
bin_stat = bins.bin_stat(x,y,bin_set)                        # 统计各个变量的分箱情况
```

对单个变量使用自动分箱,如下：
```python
bin_set  = bins.merge.chi2(x,y,bin_num=5,init_bin_num=10)    # 使用卡方分箱对变量进行分箱
bin_stat = bins.Bins(bin_set).binStat(x,y)                   # 统计分箱结果
```

对单个变量手动分箱,如下：
```python
bin_set  = [['-',0],[0,0.37],[0.37,1.2],[1.2,2],[2,'+']]     # 手动设置变量的分箱
bin_stat = bins.Bins(bin_set).binStat(x,y)                   # 统计分箱结果
```
统计结果中就会打印出变量在各个分箱的badrate、iv值等

- 构建评分卡
设置好分箱后,就可以将数据构建构建评分卡,如下：
```python
model,card = model.scoreCard(x,y,bin_set)                    # 构建评分卡
card.featureScore                                            # 评分卡-特征得分表
card.baseScore                                               # 评分卡-基础
model.w                                                      # 逻辑回归模型的变量权重
model.b                                                      # 逻辑回归模型的阈值
```

- 打印相关报告
例如打印阈值表、分数分布图等,如下：
```python
thd_tb    = report.get_threshold_tb(score,y,bin_step=10)     # 阈值表
report.draw_score_disb(score,y,bin_step=10)                  # 分数分布
```

## Documents · 文档
- [评分卡教程](https://www.bbbdata.com/ml)



## 更新日志
- v1.0.0: 添加数据
- v1.0.0: 初步上传