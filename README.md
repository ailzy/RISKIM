## RISKIM基金资产配置框架
##### 基于多因子模型预测的动态组合调仓策略
### 项目说明

1. 概述

   从回测主引擎backtest.py说起：
   
   (1.1) 数据模拟
        
        构建datagate迭代器用于回测模拟，根据配置条件判断回测起止。
   
   (1.2) 账户构建 
   
        account模块包括单账户singleacct和多账户multacct。模拟收益指标、手续费扣除、仓位调整等。
   
   (1.3) 日志系统和配置初始化
   
   (1.4) 多超参数账户组
        
        稍后的算法流程中会介绍模型构建。backtest.ini中提供了几组模型构建必备参数（gridsearch超参数），
        我们为每一组交叉参数构建一个模型并绑定一个账户。
        
   (1.5）三种策略
   
        我们依据macct_dynamic_list中历史最优收益对应的超参数确定macct_dyaction。该超参数确定macct_dyaction
        的模型，并完成调仓。两个基线策略为:macct_oneshot即不做调仓，macct_constant为等市值调仓。

2. 多因子模型

![Markdown](https://github.com/ailzy/riskim/blob/master/tutorial/algoexplain.png)

...待完成

如有任何问题，联系作者lizhengyang.lzy@outlook.com，该项目仅供交流学习，不得用于商业目的。
