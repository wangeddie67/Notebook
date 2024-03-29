# 第9章 先进传感器技术

## 9.1 传感器简介

$\triangle$ 传感器可以将外部物理量转化为设备及系统可识别并处理的信号，是物理世界和电子设备之间的主要接口。

### 9.1.1 传感器概述

$\triangle$ 传感器系统通常由敏感元件、信号转换电路和电源设备组成。

- 敏感元件可直接感知或响应外界物理量，信号转换电路能将感质量转换为适合传输或测量的信号类型。

**图9.1 常见的传感器应用**

**图9.2 典型传感器系统的主要组成部分**

$\triangle$ 合格的传感器应同时满足六个要求：

- 具有足够的量程范围，保证一定的抗过载能力。
- 具有良好的接口兼容性，确保与主系统之间的通信顺畅。
- 具有较快的反应速度和一定的可靠性。
- 对测量对象的影响较小，自身噪声小并能抵抗干扰。
- 具有一定的精度和较高的稳定性。
- 使用成本可控且工作寿命满足要求。

### 9.1.2 传感器的分类及特点

$\triangle$ 按输入信号类型进行分类，分为物理型，化学型和生物型。

$\triangle$ 按输出信号类型进行分类，分为模拟信号型和数字信号型。

$\triangle$ 按被测量对象对传感器进行分类。如温度传感器，加速度传感器，图像传感器。

- 根据材料和原理再进行分类。

**图9.3 传感器按输入、输出信号类型的分类**

### 9.1.3 常见传感类型

#### 1. 电容传感原理

$\triangle$ 电容式传感器是通过电容值的变化来感知被测物理量变化的一种传感器。
$$
C=\frac{Q}{V}=\frac{\varepsilon S}{d}
$$
其中，$S$是极板有效面积，$d$是两极板间距。

$\triangle$ 变极距型电容传感器由固定极板和可动极板构成。

- 主要分为线位移式结构和角位移式结构。
- 结构简单，功耗低和响应快等特点，用于位移，加速度，压力，温湿度，厚度，液位等参数的测量中。

**图9.4 常见电容式传感器原理**

$\triangle$ 常见的电容式传感器测量电路包括桥式电路，双T形电桥电路和脉宽调制电路的。

#### 2. 压电传感原理

$\triangle$ 压电效应指某些电介质在机械应力的作用下发生形变，进而产生电极化现象。

- 电介质的某两表面出现极化相反的电荷积累，且表面电荷密度与应力大小成正比，称为正压电效应。
- 在电场作用下，这些电介质也会发生机械形变，这种现象称为逆压电效应。

$\triangle$ 灵敏度高，瞬态响应快，信噪比大，结构尺寸小，切可靠性高等优点。常用的传感器有加速度传感器，压力传感器，声学传感器和流量传感器。应用于汽车，船舶，航空航天，生物力学，医疗技术和消费电子的你。

**图9.5 压电效应原理示意图**

$\triangle$ 压电式加速传感器包括压电敏感元件，质量块，弹簧外壳和机座。

$\triangle$ 压电敏感元件电极面产生的电荷量$Q$为
$$
Q=\sigma A=d_{zz}TA=d_{zz}F=d_{zz}ma
$$
其中，$A$为压电敏感元件的受力面积，$F$为质量块作用的压电敏感元件上的力，$m$为质量块的质量，$a$为加速度。

$\triangle$ 压电式压力传感器包括压电敏感元件，膜片、外壳，质量块和基座构成。

$\triangle$ 两电极面的电势差$V$为
$$
V=\frac{Q}{C}=\frac{\sigma A}{\frac{\varepsilon A}{t}}=\frac{td_{zz}T}{\varepsilon}
$$
**图9.6 压电传感原理**



## 9.2 微机电系统传感器

$\triangle$ MEMS主要特点是采用与集成电路兼容的制备工艺，可大批量生产。主要分为微传感器和微执行器。

### 9.2.1 微机电系统的定义

$\triangle$ MEMS模组主要由MEMS传感器、MEMS执行器和信号处理电路单元三部分构成。

**图9.7 MEMS模组示意图**

### 9.2.2 微机电系统技术的发展历史

**图9.8 MEMS微型电动机和硅基微静电驱动电动机**

### 9.2.3 微机电系统传感器的应用领域

#### 1. 航空航天领域中的MEMS传感器

**图9.9 MEMS传感器分类**

**图9.10 姿态控制传感器模组**

#### 2. 汽车工业领域中的MEMS传感器

**图9.11 汽车中MEMS传感器的应用情况**

#### 3. 消费电子领域中的MEMS传感器

**图9.12 智能手机中的MEMS传感器**



## 9.3 微机电系统传感器的设计

$\triangle$ MEMS传感器的设计主要强调功能化、集成化和整体性。

**图9.13 MEMS传感器设计的3个相关层次**

### 9.3.1 微机电系统传感器的设计理论

#### 1. 尺度效应

$\triangle$ 物体的表面积$S$与体积$V$之间的关系为
$$
S \propto V^{\frac{2}{3}}=V^{0.67}
$$
**图9.14 尺寸缩小引起的重力和表面力变化情况**

**表9.1 常见的物理特性与特征尺寸L之间的关系**

#### 2. 微观力学

$\triangle$ MEMS传感器在力的作用下产生的形变
$$
F=-k\delta
$$
$\triangle$ 杨氏模量，应力与应力张量之间的关键
$$
\sigma=E\varepsilon
$$
$\triangle$ 泊松比主要描述的是施加一个方向的力而导致物体其他方向的多维变化趋势
$$
v=-\frac{\varepsilon_x}{\varepsilon_y}
$$
**图9.15 轴向力、切向应力和他们的应变张力**

$\triangle$ 雷诺数来表征物体在某一特定流体介质中的不同流动特性和热传递特性。
$$
Re=\frac{\rho VL}{\eta}
$$

#### 3. 静电致动

$\triangle$​​ 传感器和制动器的本质是将某一形式的能量转换成另一个能量形式。主要包括静电制动，压电制动，热制动，形状记忆合金制动和电磁制动。

**图9.16 常见的静电致动MEMS传感器结构**

### 9.3.2 微机电系统传感器的设计流程与方法

#### 1. MEMS传感器设计的基本流程

**图9.17 MEMS传感器设计的总体流程及设计要素**

**表9.2 MEMS传感器设计中不同应用阶段对设计要求的侧重**

#### 2. MEMS传感器设计方法概述

$\triangle$ 自底向上设计；自顶向下设计。

### 9.3.3 微机电系统传感器的设计与仿真软件

#### **1. 计算力学分析方法：有限元分析**

$\triangle$ 有限元分析的求解步骤：结构离散化、设定变量、求解有限元方程组。

#### 2. MEMS设计与仿真软件



## 9.4 微机电系统传感器的制程

### 9.4.1 微机电系统传感器材料

#### 1. 硅及硅的化合物

$\triangle$ 优势：良好的力学和电学稳定性，高熔点，极低热膨胀系数。硅在集成电路领域，具备成熟的工艺体系。

#### 2. III-V族元素化合物

$\triangle$ 适用于传感器的高速调控和信号处理单元。

#### 3. 高分子聚合物

$\triangle$ 主要用于生物传感器和微流控芯片等器件。

### 9.4.2 微机电系统传感器的加工工艺

**图9.19 简单的光刻-蒸镀-剥离工艺流程**

#### 1. 体硅微加工

$\triangle$ 体硅微加工是通过刻蚀方法有选择性地去除衬底的部分材料以形成独立的机械结构或特殊三维结构的工艺。

**图9.19 利用体硅微加工制备微尺度楔形结构的工艺流程**

**表9.3 干法刻蚀和湿法刻蚀的原理和特性**

**图9.20 刻蚀的类别及硅的微观结构晶面**

#### 2. 表面微加工

$\triangle$ 表面微加工是在衬底上，通过逐层材料生长与逐层刻蚀技术，形成微机械结构的工艺。

**图9.21 表面微加工**

#### 3. LIGA工艺

$\triangle$ LIGA是光刻、电镀和压模的缩写。

- 利用X射线进行光刻，可以将掩模板的图案转移到厚度为数百微米的光刻胶上，在利用电镀和压模工艺实现大深宽比、边沿垂直光滑的三维立体微结构制备。

$\triangle$ LIGA工艺流程包括光刻、电铸制模、压模与脱模3个步骤。

**图9.22 LIGA工艺的制备流程**



## 9.5 主流微机电系统传感器

### 9.5.1 声学应用：微机电系统传声器

**图9.23 市场上典型的内置MEMS传声器的产品**

**图9.24 MEMS传声器的结构示意图**

### 9.5.2 光学应用：红外热电堆检测传感器

**图9.25 封闭膜结构红外热电堆检测传感器的结构及实物**

### 9.5.3 电学应用：微机电系统加速度计

**表9.4 电容式、压阻式、压电式MEMS加速度计的性能对比**

**图9.26 一种采用叉指形结构的MEMS电容式加速度计**



## 9.6 新型传感器技术

**图9.27 智能传感器的结构**

### 9.6.1 磁学传感器

#### 1. GMR传感器

#### 2. TMR传感器

**图9.28 GMR传感器的基本结构**

**图9.29 TMR传感器的基本结构和特性**

### 9.6.2 医工交叉传感器

**图9.30 医工交叉传感器设计的学科**

**图9.31 基于微流控的医工交叉传感器**

**图9.32 太赫兹超材料传感器**



## 本章小结