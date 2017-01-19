# PDA 分析

## 1 依赖第三方包
+ `xlrd` : excel 读取包
+ `xlwt` : excel 写入包
+ `pulp` : 线性规划包
+ `numpy` : 矩阵计算包
+ `pandas` : 数据分析包

## 2 模块

### 2.1 Model 模块

+ `Energy` : 能源模块
    + `name` : 省份名称
    + `energy` : 集合对象，包含各个能源消耗,最后一个元素为总计
    + `total` : 能源总计
+ `Co2` : Co2模块
    + `name` : 省份名称
    + `co2` : 集合对象，包含各个Co2排放，最后一个元素为总计
    + `total` : Co2 总计
+ `Production` : 产值模块
    + `name` : 省份名称
    + `prodcution` : 该省份的产值
### 2.2 Dmu 模块
+  `name` : 省份名称
+ `ene` : 能源
+ `co2` : co2 排放
+ `Pro` : 产出

### 2.3 DataRead 模块

*read_dmus* 从 excel 表中读取某一个年份的所有的决策单元(decison making unit)

### 2.4 Algorithm 模块
+ `lambda_min` : 线性规划求最小值
+ `theta_max` :  线性规划求最大值

### 2.5 LMDI 模块
计算相邻年份之间的lmdi指数，包括 `cef`, `emx`, `pei`, `pis`, `isg`, `eue`, `est`, `yoe` 和 `yct` 

### 2.6 SinglePeriodAAM 模块
计算相邻年份之间的各个省份的各个指数的归因

### 2.7 MultiPeriodAAM 模块
计算跨年份的之间各个省份的各个指数的归因

### 2.8 WriteData 模块
按照年份输出结果

## 3 测试
所有测试模块以 `Test` 开头，测试框架为 unitest.

## 4 重构历史

1.2017年01月19日： 重构LMDI，增加缓存功能