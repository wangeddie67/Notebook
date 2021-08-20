# 引言



# 第14章 求和与渐进性

$\triangle$ *闭型*（closed form），没有带上下标的求和或者乘积符号，也没有省略号。

$\triangle$ *几何和*（geometric sum）的闭型：
$$
1+x+x^2+x^3+\cdots+x^n=\frac{1-x^{n+1}}{1-x}
$$
$\triangle$ *阶乘函数*（factorial function）：$n!::=1\cdot 2 \cdot 3 \cdots n$

## 14.1 年金的值

本节阐述年金问题的背景

### 14.1.1 钱未来的价值

$\triangle$ 年金的实际价值为
$$
V=\sum_{i=1}^{n}\frac{m}{\left(1+p\right)^{i-1}}=m\cdot\sum_{j=0}^{n-1}x^j
$$
令$j=i-1$，而且$x=1/(1+p)$。

### 14.1.2 扰动法

$\triangle$ *扰动法*（perturbation method）和*母函数*（generating functions）。

本节个扰动法求几何和。

### 14.1.3 年金价值的闭型

$\triangle$ 年金价值的闭型为
$$
V=m\left(\frac{1+p-(1/(1+p))^{n-1}}{p}\right)
$$

### 14.1.4 无限长的等比数列

$\triangle$ **定理14.1.1** 如果$\left| x \right|<1$，那么
$$
\sum_{i=0}^{\infin}{x^i}=\frac{1}{1-x}
$$

### 14.1.5 示例

$\triangle$ *等比递减*（geometrically decreasing）和*等比递增*（geometrically increasing）。

### 14.1.6 等比数列求和的变化

$\triangle$ 利用扰动法可以求得
$$
\sum_{i=1}^{n-1}ix^{i-1}=\frac{1-nx^{n-1}+(n-1)x^n}{(1-x)^2}
$$
$\triangle$ **定理14.1.2** 如果$\left|x\right|<1$，那么
$$
\sum_{i=1}^{\infin}ix^i=\frac{x}{(1-x)^2}
$$

## 14.2 幂和

$\triangle$
$$
\sum_{i=1}^n i^2 = \frac{(2n+1)(n+1)n}{6}
$$

## 14.3 估算求和式子

$\triangle$ **定义14.3.1** 函数$f:\mathbb{R}^+\rightarrow\mathbb{R}^+$满足下面的条件时是*严格递增/单调递增/绝对递增*（strictly increasing）的，
$$
x<y时，f(x)<f(y)
$$
满足下面的条件是*弱递增/弱增加*（weakly increasing）的，
$$
x<y时，f(x) \leq f(y)
$$
满足下面的条件时是*严格递减/单调递减*（strictly decreasing）的，
$$
x<y时，f(x)>f(y)
$$
满足下面的条件是*弱递减/弱减小*（weakly decreasing）的，
$$
x<y时，f(x) \geq f(y)
$$
$\triangle$ **定理14.3.2** $f:\mathbb{R}^+\rightarrow\mathbb{R}^+$是一个弱递增函数。定义
$$
S::=\sum_{i=1}^n f(i)
$$
和
$$
I::=\int_{1}^n f(x)dx
$$
那么
$$
I+f(1)\leq S \leq I+f(n)
$$
相似地，如果$f$是弱递增的，那么
$$
I+f(n)\leq S \leq 1+f(1)
$$

## 14.4 超出边界

$\triangle$ *图书堆放问题*（book stacking problem）

### 14.4.1 问题陈述

$\triangle$ *稳定堆*（stable stack）和*突出部分/悬垂部分*（overhang）。

本节推导图书堆放问题的求和式子。

### 14.4.2 调和数

$\triangle$ **定义14.4.1** 第$n$个*调和数*（harmonic number）$H_n$是
$$
H_n::=\sum_{i=1}^{n}\frac{1}{n}
$$
$\triangle$ 调和数上下界
$$
\ln(x)+\frac{1}{n}\leq H_n\leq \ln(n)+1
$$
$\triangle$ 调和数近似值
$$
H_n=ln(n)+\gamma+\frac{1}{2n}+\frac{1}{12n^2}+\frac{\varepsilon(n)}{120n^4}
$$

### 14.4.3 渐进等式

$\triangle$ **定义14.4.2** 对于函数$f,g:\mathbb{R}\rightarrow\mathbb{R}$，我们说$f$*渐进相等*（asymptotically equal）于$g$，写成$f(x)\sim g(x)$，当且仅当
$$
\lim_{x\rightarrow\infin}f(x)/g(x)=1
$$

## 14.5 乘积

可以用取自然对数的方法，将乘积式转化为求和式。

$\triangle$ 阶乘的上下界
$$
\frac{n^m}{e^{n-1}}\leq n! \leq \frac{n^{n+1}}{e^{n-1}}
$$

### 14.5.1 斯特林公式

$\triangle$ **定理14.5.1**（斯特林公式，Stirling's Formula） 对于所有$n\geq 1$，满足
$$
n!=\sqrt{2\pi n}\left(\frac{n}{e}\right)^n e^{\epsilon(n)}
$$
其中
$$
\frac{1}{12n+1}\leq \epsilon(n)\leq\frac{1}{12n}
$$
$\triangle$ $n!>\sqrt{2\pi n}\left(\frac{n}{e}\right)^n$

$\triangle$ $n! \sim \sqrt{2\pi n}\left(\frac{n}{e}\right)^n$

$\triangle$ **推论14.5.2**
$$
n! < \sqrt{2\pi n}\left(\frac{n}{e}\right)^n\cdot\left\{\begin{array}{ll}1.09 & n\geq 1 \\ 1.009 & n\geq10 \\ 1.0009 & n\geq100\end{array}\right.
$$

## 14.6 双倍的麻烦

$\triangle$ *二重求和*（double sum）。

$\triangle$ 交换加法式子的前后顺序。

## 14.7 渐近符号

### 14.7.1 小$O$

$\triangle$ **定义14.7.1** 对于函数$f,g:\mathbb{R}\rightarrow\mathbb{R}$，并且$g$是非负函数，我们称$g$渐近小于（asymptotically smaller）$g$，用符号表示，
$$
f(x)=o(g(x))
$$
当且仅当
$$
\lim_{x\rightarrow\infin}f(x)/g(x)=0
$$
$\triangle$ **引理14.7.2** 对于所有的非负常数$a<b$，满足$x^a=o(x^b)$，对于任意$x>1$，$\log x<x$。

$\triangle$ **引理14.7.3** 对于任意$\epsilon>0$，$\log x=o(x^\epsilon)$。

$\triangle$ **推论14.7.4** 对于任意$a,b\in\mathbb{R}$，$a>1$，$x^b=o(a^x)$。

### 14.7.2 大$O$

$\triangle$ **定义14.7.5** 对于函数$f,g:\mathbb{R}\rightarrow\mathbb{R}$，并且$g$是非负函数，我们说
$$
f=O(g)
$$
当且仅当
$$
\lim_{x\rightarrow\infin}\sup|f(x)|/g(x)<\infin
$$
$\triangle$ **定义14.7.6** 如果函数$f:\mathbb{R}\rightarrow\mathbb{R}$，当它的参数趋向无限时，存在有穷或无穷的上极限和下极限时，那么它的极限和上极限是相同的。

$\triangle$ **引理14.7.7** 如果$f=o(g)$或者$f\sim g$，那么$f=O(g)$。

$\triangle$ **引理14.7.8** 如果$f=o(g)$，那么$g=O(f)$是错误的。

$\triangle$ **定义14.7.9** 设函数$f,g:\mathbb{R}\rightarrow\mathbb{R}$，$g$是非负函数，那么$f=O(g)$，当且仅当常量$c\geq0$，并且存在这样的$x_0$，对于任意的$x\geq x_0$，满足$\left|f(x)\right|\leq cg(x)$。

$\triangle$ **命题14.7.10** $100x^2=O(x^2)$。

$\triangle$ **命题14.7.11** $x^2+100x+10=O(x^2)$。

$\triangle$ **命题14.7.12** $a_kx^k+a_{k-1}x^{k-1}+\dots+a_1x+a_0=O(x^k)$。

### 14.7.3 $\theta$

$\triangle$ **定义14.7.13** $f=\theta(g)$当且仅当$f=O(g)$并且$g=O(f)$。

$\triangle$ $f$和$g$的差值是一个常数。

### 14.7.4 渐进符号的误区

渐进符号的误区：指数惨败、常量困惑、等号的误用、运算符适用之错

### 14.7.5 大$\Omega$

$\triangle$ **定义14.7.15** 设函数$f,g:\mathbb{R}\rightarrow\mathbb{R}$，并且$f$是非负函数，定义
$$
f=\Omega(g)
$$
来表示
$$
g=O(f)
$$
$\triangle$ **定义14.7.16** 设函数$f,g:\mathbb{R}\rightarrow\mathbb{R}$，并且$f$是非负函数，定义
$$
f=\omega(g)
$$
来表示
$$
g=o(f)
$$



# 第15章 基数法则

## 15.1 通过其他计数来计算当前计数

$\triangle$ 通过对其他事物进行计数而计算当前计数。

### 15.1.1 双射规则

$\triangle$ **引理15.1.1** 有$k$种口味，选出$n$个甜甜圈的方式的数目，和$n$个0，$(k-1)$个1的序列的数目一样。

## 15.2 序列计数

$\triangle$ *序列*（sequence）

### 15.2.1 乘积法则

$\triangle$ **法则15.2.1**（乘积法则，product rule） 如果$P_1,P_2,\cdots,P_n$是无限集，那么
$$
\left|P_1\times P_2 \times \cdots \times P_n\right|=|P_1| \cdot |P_2| \cdots |P_n|
$$

### 15.2.2 $n$-元素集合的子集

将n元素集合的子集转化为n个比特的0/1字符串数量，进而通过乘法法则得到
$$
|\{0,1\}^n|=2^n
$$

### 15.2.3 加和法则

$\triangle$ **法则15.2.2**（加和法则） 如果$A_1,A_2,\cdots,A_n$是不相交的集合，则：
$$
\left|P_1\cup P_2 \cup \cdots \cup P_n\right|=|P_1| + |P_2| + \cdots + |P_n|
$$

### 15.2.4 密码计数

本节计算密码组合数量。

## 15.3 广义乘积法则

$\triangle$ **法则15.3.1**（广义乘积法则，Generalized Product Rule） 设$S$是长度为$k$的序列构成的集合。如果存在：

- $n_1$个可能的第一项，
- 对每一个第一项来说，有$n_2$个可能的第二项，
- ...
- 对于每一个前$k-1$项构成的序列来说，有$n_k$个可能的第$k$项，那么：

$$
\left|S\right|=n_1 \cdot n_2 \cdot n_3 \cdots n_k
$$

### 15.3.1 有缺陷的美元钞票

本节计算出现重复数字的序号的可能性。

### 15.3.2 一个象棋问题

本节计算象棋不同行/列摆放的组合。

### 15.3.3 排列

$\triangle$ 集合$S$的*排列*（permutations）是指$S$中的每一个元素刚好出现一次而构成的序列。

## 15.4 除法法则

$\triangle$ **法则15.4.1**（除法法则，Division Rule） 如果$f:A\rightarrow B$是$k$对1的，那么$\left|A\right|=k\cdot\left|B\right|$。

### 15.4.1 另一个象棋问题

本节计算两个相同棋子不同行不同列的可能摆放组合，两个棋子调换算作一种。

### 15.4.2 圆桌骑士

本节求解骑士作为的可能性，相同顺序不同起点视为一种。

## 15.5 子集计数

$\triangle$ $\left(\begin{array}{c}n \\ k\end{array}\right)$::= $n$-元素集合包含的$k$-元素自己的个数。

### 15.5.1 子集法则

$\triangle$ **法则15.5.1**（子集法则，Subset Rule） 一个$n$-元素集合包含
$$
\left(\begin{array}{c}n\\k\end{array}\right)=\frac{n!}{k!(n-k)!}
$$
个$k$-元素子集。

### 15.5.2 比特序列

$\triangle$ **推论15.5.2** 恰好包含$k$个1的$n$-比特序列的数目是$\left(\begin{array}{c}n\\k\end{array}\right)$。

$\triangle$ **推论15.5.3** 假定有$k$种口味，选择$n$个甜甜圈的方案个数是$\left(\begin{array}{c}n+(k-1)\\n\end{array}\right)$。

## 15.6 重复序列

### 15.6.1 子集序列

$\triangle$ 设$A$是一个$n$-元素集合，$k_1,k_2,\dots,k_m$都是非负整数且和为$n$。$A$的$(k_1,k_2,\dots,k_m)$-*分割*由以下序列表示：
$$
(A_1,A_2,\dots,A_m)
$$
其中$A_i$是$A$的互不相交的子集，且$\left|A_i\right|=k_i$，$i=1,\dots,m$。

$\triangle$ **定义15.6.1** 对于$n$，$k_1,\dots,k_m\in\mathbb{N}$，有$k_1+k_2+\cdots+k_m=n$，定义*多项式系数*为
$$
\left(\begin{array}{c}n\\k_1,k_2,\dots,k_m\end{array}\right)::=\frac{n!}{k_1!k_2!\cdots k_m!}
$$

### 15.6.2 Bookkeeper法则

$\triangle$ **法则15.6.3**（Bookkeeper法则）设$l_1,\dots,l_m$是不同的元素，$l_1$出现$k_1$次，$l_2$出现$k_2$次，……，$l_m$出现$k_m$次，对应的序列个数是：
$$
\left(\begin{array}{c}k_1k_2\cdots k_m \\ k_1,\cdots,k_m\end{array}\right)
$$
$\triangle$ $k$-组合（k-combinations），重复组合（combinations with repetition），重复排列（permutations with repetition），$r$-排列，和不区分对象的排列（permutations with indistinguishable objects）。

### 15.6.3 二项式定理

$\triangle$ **定理15.6.4**（二项式定理，Binomial Theorem） 对于所有$n\in\mathbb{N}$和$a,b\in\mathbb{R}$：
$$
\left(a+b\right)^n=\sum_{k=0}^n\left(\begin{array}{c}n \\ k\end{array}\right)a^{n-k}b^k
$$
$\triangle$ **定理15.6.5**（多项式定理，Multinomial Theorem） 对于所有$n\in\mathbb{N}$
$$
\left(z_1+z_2+\cdots+z_m\right)^n=\sum_{\begin{array}{c}k_1,\cdots k_m\in\mathbb{N} \\ k_1+\cdots+k_m=n\end{array}}\left(\begin{array}{c}n \\ k_1,k_2,\dots,k_m\end{array}\right)z_1^{k_1}z_2^{k_2}\cdots z_m^{k_m}
$$

## 15.7 计数练习：扑克手牌

本节利用扑克手牌问题进行计算。

### 15.7.1 四条相同点数的手牌

### 15.7.2 葫芦手牌

### 15.7.3 两个对子的手牌

### 15.7.4 花色齐全的手牌

## 15.8 鸽子洞原理

$\triangle$ **法则15.8.1**（鸽子洞原理） 如果$|A|>|B|$，则对于全函数$f:A \rightarrow B$，$A$一定存在两个不同元素通过$f$映射到$B$的同一个元素。

### 15.8.1 头上的头发

$\triangle$ **法则15.8.2**（广义鸽子洞原理） 如果$|A|>k\cdot|B|$，则对于全函数$f:A\rightarrow B$，$A$至少存在$k+1$个不同元素通过$f$映射到$B$的同一个元素。

### 15.8.2 具有相同和的子集

### 15.8.3 魔术

这一节以及后面三节解释魔术师如何猜牌。

### 15.8.4 秘密

### 15.8.5 真正的秘密

### 15.8.6 如果是4张牌呢

## 15.9 容斥原理

### 15.9.1 两个集合的并集

$\triangle$ *容斥原理*（Inclusion-Exclusion Rule）是指他们的并集的大小是：
$$
|S_1\cup S_2|=|S_1|+|S_2|-|S_1\cap S_2|
$$

### 15.9.2 三个集合的并集

$\triangle$ 
$$
|S_1 \cup S_2 \cup S_3|=|S_1|+|S_2|+|S_3|-|S_1 \cap S_2|-|S_1 \cap S_3|-|S_2 \cap S_3|+|S_1 \cap S_2 \cap S_3|
$$

### 15.9.3 42序列、04序列或60序列

### 15.9.4 $n$个集合的并集

$\triangle$ **法则15.9.1**（容斥原理，Inclusion-Exclusion）
$$
|S_1 \cup S_2 \cup\dots\cup S_n|=单个集合的大小之和 减 所有两个集合交集的大小 加 所有三个集合交集的大小 减 所有四个集合交集的大小 加 所有五个集合交集的大小 等等
$$
$\triangle$ **法则**（容斥原理）
$$
\left|\bigcup_{i=1}^{n}S_i\right|=\sum_{i=1}^n\left|S_i\right| - \sum_{1\leq i<j\leq n}\left|S_i\cap S_j\right| + \sum_{1\leq i < j < k \leq n}\left|S_i\cap S_j \cap S_k\right|+\cdots+(-1)^{n-1}\left|\bigcap_{i=1}^{n}S_i\right|
$$
$\triangle$ **法则**（容斥原理-II）
$$
\left|\bigcup_{i=1}^{n}S_i\right|=\sum_{\empty\neq I\subseteq\{1,\cdots,n\}}(-1)^{|I|+1}\left|\bigcap_{i\in I}S_i\right|
$$

### 15.9.5 计算欧拉函数

## 15.10 组合证明

### 15.10.1 帕斯卡三角恒等式

$\triangle$ **引理15.10.1**（帕斯卡三角恒等式，Pascal's Triangle Identity）
$$
\left(\begin{array}{c}n \\ k\end{array}\right)= \left(\begin{array}{c}n-1 \\ k-1\end{array}\right) + \left(\begin{array}{c}n-1 \\ k\end{array}\right)
$$

### 15.10.2 给出组合证明

$\triangle$ *组合证明*（combinatorial proof）是一种依靠技术原理构建代数事实的证明方法。这种证明大多数遵循以下基本框架：

1. 定义一个集合$S$。
2. 通过一种计数方式得出$|S|=n$。
3. 通过另一种计数方式得出$|S|=m$。
4. 得出结论：$n=m$。

### 15.10.3 有趣的组合证明

$\triangle$ **定理15.10.2**
$$
\sum_{r=0}^n\left(\begin{array}{c}n \\ r\end{array}\right)\left(\begin{array}{c}2n \\ n-r\end{array}\right)=\left(\begin{array}{c}3n \\ n\end{array}\right)
$$
