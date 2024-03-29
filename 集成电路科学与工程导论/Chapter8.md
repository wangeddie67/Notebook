# 第8章 先进存储器技术

## 8.1 存储器概述

### 8.1.1 存储器的主要指标和架构

$\triangle$ 衡量存储器性能的主要指标有，存储容量，访问时间，存储周期，存储字长和存储带宽的。

**图8.1 存储器的字寻址和字节寻址方式示意图**

**图8.2 计算机系统中存储器的组织架构**

### 8.1.2 存储器的分类

$\triangle$ 按照存储原理及断点后能否保留数据，存储器分为易失性存储器（Volatile Memory，VM）与非易失性存储器（Non-Volatile Memory，NVM）。

$\triangle$ 按照存储器所采用的存储元素，可分为光学存储器、磁性存储器、半导体存储器。



## 8.2 半导体存储器

$\triangle$ 半导体存储器按照对所存储数据的操作属性可分为两大类，即只读存储器（Read-Only Memory, ROM）和随机存取存储器（Random Access Memory, RAM）。

- ROM的优点是电路简单，而且掉电以后数据不会丢失。

**表8.1 ROM与RAM的性能对比**

$\triangle$ 常用的RAM又分为SRAM和DRAM。ROM分为固定ROM、可编程ROM。可编程ROM又分为PROM、EPROM、EERPROM和Flash。

**图8.3 半导体存储器的分类**

### 8.2.1 静态随机存储器

$\triangle$ SRAM具有与标准CMOS工艺完全兼容、快速存取、低功耗、超低工作电压等特点。

#### 1. 存储单元

$\triangle$ SRAM通常包含行/列译码器、存储阵列和输入/输出电路等几个部分。

$\triangle$ SRAM的存储核心是一对完全对称、首尾相连、交叉耦合的反相器。

**图8.4 SRAM的基本架构**

**图8.5 SRAM的6T基本存储单元**

#### 2. 存储操作

$\triangle$ 存储单元共有三种工作状态，分别为保持态，数据读出状态和数据写入状态。

**图8.6 SRAM的读写操作**

#### 3. 发展历史与现状

**图8-7 1978-2006年日立的SRAM技术演进路线**

### 8.2.2 动态随机存取存储器

$\triangle$ DRAM的主要用途是主存。需要对存储的信息不停的刷新。

#### 1. 存储单元

$\triangle$ DRAM的存储单元由一个晶体管和一个电容器构成的1T1C结构。

**图8.8 DRAM的基本存储单元和存储排列电路**

$\triangle$ DRAM以电容器两端的电压差大小表示逻辑1和0。

$\triangle$ 为了解决电容器漏电问题，DRAM引入了差分感应放大器和刷新控制器。

$\triangle$ 读操作分为预充电（Pre-Charge）、导通（Access）、感应（Sense）、复原（Restore）四步。

读取前先对位线进行预充电，将位线电压抬升到$V_{REF}$，进而使晶体管导通，电容器中存储的电荷将使位线电压发生变化，根据所存储的数据不同，形成电压略高的$V_{REF+}$或略低的$V_{REF-}$两种信号，通过将该信号与$V_{REF}$进行差分比较，即可读出所需要的数据。读出数据后，位线读取数据产生的高电平或低电平将对电容中存储的数据进行复原，从而使系统回到读取前的状态。

$\triangle$ 针对电针对漏电导致的数据丢失，需要每隔一段时间对电容器的数据进行刷新。由刷新控制器进行控制。

- 不进行读写操作情况下，电容器能够保持数据的时间是64毫秒。
- DRAM刷新模式分为自动刷新和自刷新。

$\triangle$ DRAM的优势在于所需要的晶体管更少，存储密度更大。但是存储速度相对较慢，需要定时刷新，刷新期间CPU不能对其进行读写操作。

#### 2. 内部构造

$\triangle$ DRAM的内部构造多采用堆叠式电容器和掩埋字线结构。

**图8.9 DRAM的内部构造**

#### 3. 发展历史

**图8.10 DRAM技术的发展历史**

**表8.2 SDRAM相关技术标准对比**

**图8.11 HMC与HBM的存储结构示意图**

#### 4. 工艺演进

**表8.3 DRAM 10nm量级技术节点情况**

#### 5. 应用场景

$\triangle$ 根据应用场景可以分为用于PC、服务器的标准DDR，用于手机等移动设备的LPDDR以及用于数据密集型业务的GDDR。

**图8.12 DRAM分类示意图**

#### 6. 未来发展趋势

### 8.2.3 可编程只读存储器

$\triangle$ ROM的存储阵列结构主要包括地址译码器、存储矩阵、输出缓存等。

$\triangle$ 淹模ROM，在制造过程中将数据一种特殊光罩烧录于电路中，之后不能更改。

$\triangle$​ PROM（Programmable ROM）为一次可编程只读存储器，典型结构是熔丝结构与PN结型结构。

**图8.13 掩模式ROM存储阵列结构示意图**

$\triangle$ EPROM，可以实现重复，擦除和写入。EEPROM使用电擦除没有感光孔。

**图8.14 EPROM和EEPROM实物对比**

### 8.2.4 闪速存储器

$\triangle$ 闪存存储器简称闪存（Flash），是一种特殊的、允许在工作中被多次擦写的只读存储器。

- 优点包括存储密度高，成本低，非易失快速以及电可擦除等。
- 广泛运用于各个领域。通常用于存放程序代码，常量表以及一些在系统掉电后需要保存的用户数据。

**表8.4 Flash与各种ROM的性能参数对比**

#### 1. Flash的分类

$\triangle$ Flash主要分为三类，与非（NAND）型、或非（NOR）型和AG-AND型。

**图8.15 NAND Flash和NOR Flash的基本结构**

$\triangle$​ NOR Flash主要用于嵌入式存储，NAND Flash用于大规模独立数据存储。

- NAND Flash具有更短的擦写时间、更小的存储单元面积、更大的存储密度和更低的成本。但是l/O接口没有随机存取能力,，以区块的方式进行读写。韩长江航运。大概是东。他会满过后甲板上的税吗？而且传的两个。这么

**图8.16 黄定律揭示Flash的存储密度每12个月翻一番**

#### 2. 存储原理

$\triangle$ 存储单元为三端口器件，分为栅极，源极和漏极。Flash有两个栅极，一个是控制栅，一个是浮置栅极或浮栅，使得Flash具有保持电荷的能力。

**图8.17 Flash的基本存储单元和存储原理示意图**

$\triangle$ 方案是是一种电压控制性存储器件。存储操作包括写入，擦除和读取三个过程。

- 写入本质是向电荷是势阱注入电荷。有两种技术路径：电子注入和F-N隧道效应。

**图8.18 Flash的数据写入、擦除和读取的过程**

#### 3. 存储单元

$\triangle$ 在三维堆叠技术之前，常用的提高Flash存储密度的方法就是提高单个存储单元所能存储的位数，由此衍生出单阶存储单元（SLC）、多阶存储单元（MLC）、三阶存储单元（TLC）和四阶存储单元（QLC）。

**图8.19 SLC、MLC、TLC和QLC所能存储的数据位数**

**表8.5 多种Flash存储单元的性能对比**

#### 4. 3D NAND Flash颗粒技术

**图8.20 典型的3D NAND Flash结构**

#### 5. NAND Flash控制技术

$\triangle$ Flash需要内置一个存储控制芯片，负责控制，包括读取，写入数据，执行垃圾回收，耗损均衡，算法，纠错，加密等操作。

- 根据不同应用场景分为嵌入式多媒体控制器（Embedded Multi Media Card, eMMC）、通用Flash存储器（Universal Flash Storage，UFS）和SSD。

**图8.21 SSD主控芯片的内部结构及与外部系统通信示意图**

**表8.6 不同PCIe接口的性能指标**

#### 6. NAND Flash未来技术发展趋势

**图8.22 3D NAND Flash主要生产厂商的技术路线**



## 8.3 新型非易失性存储器

$\triangle$ 传统半导体器件面临的问题：第一，漏电流变得更高；第二，电荷总数的微小扰动会带来更大的影响；第三，纳米尺寸下的加工过程会遇到工艺扰动的挑战。

$\triangle$ 一种方案是缩短内存和处理器之间的数据传输，增加片上缓存容量，采用近存计算或者存算一体的新型计算方式；另一种是采用三维堆叠技术增加存储容量。

**表8.7 半导体存储器与新型非易失性存储器的性能参数对比**

### 8.3.1 磁性随机存储器

$\triangle$ MRAM最突出的特征就是利用电子自旋方向的差异实现数据存储，并具有非易失性。

$\triangle$ MRAM的核心器件是磁隧道结（Magnetic Tunneling Junction, MTJ）。

$\triangle$ 当前主流的写入方法是通过注入电流引起的自旋转移矩（Spin Transfer Torque, STT）效应。

**图8.23 MTJ的结构、STT效应原理及1T1MTJ架构存储单元**

**表8.8 2021年以来已报道的STT-MRAM芯片及相关参数**

$\triangle$ 复合写入型MRAM器件原型：基于STT与SOT协同翻转效应的TST-MRAM；基于VCMA辅助SOT翻转的VCSOT-MRAM器件。

**图8.24 基于写入方式的MRAM技术演进路线**

### 8.3.2 阻变随机存取存储器

$\triangle$ RRAM又称忆阻器。

$\triangle$ 典型的RRAM器件是基于某种薄膜材料在电激励作用下，电阻值在高阻态和低阻态之间变化的现象进行数据存储。

**图8.25 典型RRAM器件的结构及特性**

$\triangle$ 根据电阻值发生变化时，所施加的电压极限可以分为单级型(Unipolar)和双极型(Bipolar)两大类。

$\triangle$ 具有结构简单，功耗低，可微缩性好等优势。

### 8.3.3 相变存储器

$\triangle$ PCM基于硫系相变材料，在不同温度下呈现出不同状态的特性，通过电脉冲控制PCM介质单元的温度来改变单元中介质的状态，利用晶态与非晶态所体现出的不同的电阻值来实现数据存储。

**图8.26 PCM的结构及原理**

**表8.9 相变存储材料性能与PCM性能之间的关系**

**表8.10 PCM发展的重要节点及事件**

$\triangle$ 3D-XPoint是基于PCM和双阈值开关在传统crossbar结构基础上垂直堆叠的一种新型存储器技术。

**图8.27 3D-XPoint存储器阵列示意图**

### 8.3.4 铁电随机存取存储器

$\triangle$ FeRAM利用铁电材料的铁电极性特性存储数据。

- 两种类型：场效应管式（FeFET）和电容式（Capacitor-Type）。

**图8.28 FeFET存储过程示意图**

**图8.29 FeFET、1T/1C FeRAM和2T/2C FeRAM的读取方式**



## 8.4 存储器在计算中的应用

$\triangle$ 近存计算（Processing Near-Memory, PNM）技术：把更多的内存集成在处理器周围，以减少处理器芯片内外的数据迁移。

$\triangle$ 存算一体（Processing In-Memory, PIM）技术：通过在存储器中嵌入一定的计算能力来执行一些简单，延迟敏感，带宽密集的任务。

### 8.4.1 存算一体技术概述

$\triangle$ PIM的本质特征是存储器即能存储数据也能处理数据，因此可以彻底消除存储器与处理器之间的数据搬移。

$\triangle$ 一种是基于传统半导体器件，另一种是基于新型非易失存储器。

### 8.4.2 数字存算一体技术

$\triangle$ 比较流行的逻辑计算范式可以归纳为三类，布尔逻辑、大数逻辑、蕴涵逻辑。

#### 1. 基于读取电路的数字逻辑实现

$\triangle$ 需要对同时选中两个或多个存储单元进行读取操作。存储单元只有两种状态，高阻态和低阻态。

**图8.30 基于读取电路的数字逻辑实现方法示意图**

$\triangle$ 优点在于不需要对于原来的存储阵列进行修改，只需要修改外围读取点，且计算速度快。面临的问题：首先是工艺误差，其次是需要更复杂的读取电路以实现精确的参考电流，最后需要将两个输入单元所存储的数据搬运到从一条位线上。

#### 2. 基于多个存储单元的数字逻辑实现

**图8.31 基于多个RRAM存储单元实现数字逻辑运算**

#### 3. 基于单个存储单元的数字逻辑实现

**图8.32 基于自旋磁随机存储器单元的写入式逻辑范式**

### 8.4.3 模拟存算一体技术

$\triangle$ 利用非易失性存储器，基于施加的模拟电压或电路信号实现神经网络计算。

#### 1. 基于单比特存储器件的模拟计算

$\triangle$ 第1种思路是利用单个存储单元存储1bit权重数据，实现二值神经网络。对字线上的单元每行施加不同的输入电压，在位线上通过模数转换将汇集起来的电流转换为数字逻辑值，即乘加运算的结果。

$\triangle$​ 第2种思路是利用多个单元构成一个宏存储单元。每行的输入电压不再是二值，而是一个区间内的多个电压值。

#### 2. 基于多比特存储器件的模拟计算

$\triangle$​ 拥有多个阻态的非易失性存储器在模拟计算，尤其是在神经网络方面的模拟计算上有着天然的优势。这是由于其多阻态值可以与模拟神经网络中的权值实现一一对应。

$\triangle$ 权值保存在RRAM矩阵中。

**图8.33 利用RRAM的Crossbar结构实现全连接神经网络中的矩阵乘加运算**

$\triangle$ 期待解决的问题：首先是线性度的问题，其次是低功耗高精度的模数转换电路，最后RRAM存在电阻曲线漂移的问题。



## 本章小结