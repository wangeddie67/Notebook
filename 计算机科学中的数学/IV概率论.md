# 引言

$\triangle$ 概率论（Probability）



# 第17章 事件和概率空间

## 17.1 做个交易吧

$\triangle$ *蒙特霍尔*问题。

### 17.1.1 理清问题

本节的主要内容是用假设描述蒙特霍尔问题。

## 17.2 四步法

本节的主要内容是利用四步法分析蒙特霍尔问题。

### 17.2.1 步骤一：找到样本空间

$\triangle$ 随机确定的量的每一种可能的组合称为*一次结果*（outcome）。所有可能结果的集合称为实验的*样本空间*（sample space）。

$\triangle$ *树状图*（tree diagram）。

### 17.2.2 步骤二：确定目标事件

$\triangle$ 结果的集合称为*事件*（event）。

### 17.2.3 步骤三：确定结果的概率

### 17.2.4 步骤四：计算事件的概率

计算的结果是，交换后获胜的概率是2/3，所以应该交换。

### 17.2.5 蒙特霍尔问题的另一种解释

本节的主要内容是解释为什么蒙特霍尔问题可能是错的。

## 17.3 奇怪的骰子

本节的主要内容是分析均匀事件模型。

### 17.3.1 骰子A vs. 骰子B

### 17.3.2 骰子A vs. 骰子C

### 17.3.3 骰子B vs. 骰子C

### 17.3.4 掷两次

## 17.4 生日原理

本节的主要内容是分析生日原理

$\triangle$ 生日原理 如果一年中有$d$天，一个房间有$\sqrt{2d}$个人，那么房间中有两人生日相同的概率约为$1-1/e \approx 0.632$。

## 17.5 集合论和概率

### 17.5.1 概率空间

$\triangle$ **定义17.5.1** 一个可数的*样本空间*$\varsigma$是可以非空可数集。样本空间中的元素$\omega\in\varsigma$称为*结果*（outcome），$\varsigma$的子集称为*事件*（event）。

$\triangle$ **定义17.5.2** 在样本空间$\varsigma$上的*概率函数*（probablity function）是一个全函数（total function）$Pr:\varsigma\rightarrow\mathbb{R}$，其满足：

- $Pr[\omega]\geq0,\forall\omega\in\varsigma$，且
- $\sum_{\omega\in\varsigma}Pr[\omega]=1$。

$\triangle$ 样本空间和概率函数一起称为*概率空间*（probablity space）。对于任意事件$E\subseteq\varsigma$，$E$的*概率*定义为其中结果的概率之和：
$$
Pr[E]::=\sum_{\omega\in\varsigma}Pr[E]
$$

### 17.5.2 集合论的概率法则

$\triangle$ 由两个*不相交*（disjoint）事件$E$和$F$的事件概率定义，
$$
Pr[E\cup F] = Pr[E] + Pr[F]
$$
$\triangle$ **法则17.5.3**（加和法则，Sum Rule） 设$E_0,E_1,\dots,E_n,\dots$是两两不相交的时间，那么：
$$
Pr\left[\bigcup_{n\in\mathbb{N}}E_n\right]=\sum_{n\in\mathbb{N}}Pr[E_n]
$$
$\triangle$

- 互补法则（Complement Rule） $Pr[\overline{A}]=1-Pr[A]$
- 减法法则（Difference Rule） $Pr[B-A]=Pr[B]-Pr[A\cap B]$
- 容斥原则（Includison-Exclusion） $Pr[A\cup B] = Pr[A] + Pr[B] - Pr[A\cap B]$
- 布尔不等式（Boole's Inequality） $Pr[A\cup B]\leq Pr[A] + Pr[B]$
- 单调性原理（Monotonicity Rule） 如果$A \subseteq B$，那么$Pr[A]\leq Pr[B]$

$\triangle$ **法则17.5.4**（并集的上界，Union Bound）
$$
Pr[E_1\cup\cdots\cup E_n\cup\cdots]\leq Pr[E_1]+\cdots + Pr[E_n] + \cdots
$$

### 17.5.3 均匀概率空间

$\triangle$ **定义17.5.5** 给定有限的概率空间$\varsigma$，如果对每个$\omega\in\varsigma$来说，$Pr[\omega]$都相等，那么这个概率空间是*均匀的*（uniform）。

$\triangle$ 对于任何事件$E\subseteq\varsigma$，都有
$$
Pr[E]=\frac{\left|E\right|}{\left|\varsigma\right|}
$$

### 17.5.4 无穷概率空间

$\triangle$ 无穷概率空间（Infinite probability space）

本节介绍无穷概率空间的定义。



# 第18章 条件概率

## 18.1 蒙特霍尔困惑

本节介绍在考虑条件的情况下，蒙特霍尔问题的结果。

### 18.1.1 帷幔之后

## 18.2 定义和标记

$\triangle$ **定义18.2.1** 设$X$和$Y$是事件，且$Y$具有非零概率，那么，
$$
Pr[X|Y]::=\frac{Pr[X\cap Y]}{Pr[Y]}
$$


###  18.2.1 问题所在

本节解释为什么用条件概率分析蒙特霍尔问题是错误的。

## 18.3 条件概率四步法

本节利用四步法分析锦标赛获胜概率。

## 18.4 为什么树状图有效

$\triangle$ **法则**（条件概率的乘法法则：两个事件）
$$
Pr[E_1\cap E_2] = Pr[E_1]\cdot Pr[E_2|E_1]
$$
$\triangle$ **法则**（条件概率的乘法法则：三个事件）
$$
Pr[E_1\cap E_2\cap E_3]=Pr[E1]\cdot Pr[E_2|E_1]\cdot Pr[E_3|E_1\cap E_2]
$$

### 18.4.1 大小为k的子集的概率

本节利用条件概率推导大小为k的子集个数。

### 18.4.2 医学检测

利用条件概率解释医学检测准确率的含义。

### 18.4.3 四步分析法

本节用四步分析法计算医学检测结果的正确概率。

### 18.4.4 固有频率

本节阐述固有频率。

### 18.4.5 后验概率

$\triangle$ **定理18.4.1**（贝叶斯公式）
$$
Pr[B|A] = \frac{Pr[A|B]\cdot Pr[B]}{Pr[A]}
$$

### 18.4.6 概率的哲学

本节阐述贝叶斯派和频率论者。

## 18.5 全概率定理

$\triangle$ **法则18.5.1**（全概率定理：单一事件）
$$
Pr[A]=Pr[A|E]\cdot Pr[E] + Pr[A|\overline{E}]\cdot Pr[\overline{E}]
$$
$\triangle$ **法则18.5.2**（全概率公式：三个事件） 若$E_1,E_2$和$E_3$是不相交的，且$Pr[E_1\cup E_2\cup E_3]=1$，那么$Pr[A]=Pr[A|E_1]\cdot Pr[E_1]+Pr[A|E_2]\cdot Pr[E_2]+Pr[A|E_3]\cdot P[E_3]$

$\triangle$ **法则**（贝叶斯法则：三个事件）
$$
Pr[E_1|A]=\frac{Pr[A|E_1]\cdot Pr[E_1]}{Pr[A|E_1]\cdot Pr[E_1]+Pr[A|E_2]\cdot Pr[E_2]+Pr[A|E_3]\cdot P[E_3]}
$$

### 18.5.1 以单一事件为条件

17.5.2节中的概率法则也适用于以单一事件为条件的条件概率。

## 18.6 辛普森悖论

辛普森悖论：多个数据组呈现出类似的趋势，而这些数据组集合起来呈现相反的趋势。

## 18.7 独立性

$\triangle$ **定义18.7.1** 概率为0的事件是指独立于所有事件（包括它自己）的事件。如果$Pr[B]\neq0$，那么事件A独立于事件B当且仅当
$$
Pr[A|B]=Pr[A]
$$
$\triangle$ 不相交的时间不可能是独立的。

### 18.7.1 另一个公式

$\triangle$ **定理18.7.2** A独立于B，当且仅当
$$
Pr[A\cap B] = Pr[A]\cdot Pr[B]
$$
$\triangle$ **推论18.7.3** A独立于B当且仅当B独立于A。

### 18.7.2 独立性是一种假设

## 18.8 相互独立性

$\triangle$ 相互独立，即两两独立。

### 18.8.1 DNA检测

### 18.8.2 两两独立

$\triangle$ **定义18.8.1** 一个事件集合$A_1,A_2,\cdots$是*k-次独立的*（k-way independent），当且仅当其中$k$个事件构成在子集是相互独立的。这个事件集合是*两两独立的*（pairwise independent），当且仅当它是2-次独立的。

## 18.9 概率vs.置信度

### 18.9.1 肺结核测试

本节分析一个肺结核测试问题。

$\triangle$ **引理18.9.1** 你能够99%地确信测试结果是正确的。

$\triangle$ **推论18.9.1** 如果检测结果是阳性，那么要么患有肺结核，要么发生了某件很不可能的事情（概率为1/100）。

### 18.9.2 可能性修正

$\triangle$ **引理18.9.2**
$$
\text{Odds}(H|E) = \text{Bayes-factor}(E,H)\cdot \text{Odds}(H)
$$
其中，
$$
\text{Bayes-factor}(E,H)::=\frac{Pr[E|H]}{Pr[E|\overline{H}]}
$$

### 18.9.3 很可能正确的事实

### 18.9.4 极端事件

本节分析连续50次正面的硬币是一种极端事件。

### 18.9.5 下一次抛掷的置信度



# 第19章 随机变量

## 19.1 随机变量示例

$\triangle$ **定理19.1.1** 概率空间上的*随机变量*（random variable）$R$是域等于样本空间的全函数。

### 19.1.1 指示器随机变量

$\triangle$ *指示器随机变量*（indicator random variable）是将每个结果映射成0或1的随机变量。又称*伯努利变量*（Bernoulli variable）。

### 19.1.2 随机变量和事件

本节解释随机变量和事件的密切联系。

## 19.2 独立性

$\triangle$ 随机变量$R_1$和$R_2$是*独立的*（independent），当且仅当两个事件$[R_1=x_1]$和$[R_2=x_2]$对于所有的$x_1,x_2$是独立的。

$\triangle$ **引理19.2.1** 两个事件独立，当且仅当这两个事件的指示器变量是独立的。

$\triangle$ **引理19.2.2** 设$R$和$S$是两个独立的随机变量，$f$和$g$是两个函数，其中$\text{域}(f)=\text{培域}(R)$且$\text{域}(g)=\text{培域}(S)$。那么$f(R)$和$g(S)$是独立随机变量。

$\triangle$ **定义19.2.3** 随机变量$R_1,R_2,\cdots,R_n$是*相互独立的*（mutually independent）当且仅当对所有$x_1,x_2,\cdots,x_n$，$n$个事件
$$
[R_1=x_1],[R_2=x_2],\cdots,[R_n=x_n]
$$
是相互独立的。他们是*k-次独立*（k-way independent）的当且仅当他们的任意k元素子集是相互独立的。

## 19.3 分布函数

$\triangle$ **定义19.3.1** 设$R$是一个随机变量，陪域为$V$。$R$的*概率密度函数*（Probability density function）为$\text{PDF}_R:V\rightarrow [0,1]$，定义如下：
$$
\text{PDF}_R(X)=\left\{\begin{array}{ll}Pr[R=x] & 若\in\text{range}(R) \\ 0 & 若\notin\text{range}(R)\end{array}\right.
$$
如果陪域是实数的子集，那么*累计分布函数*（cumulative distribution function）为$\text{CDF}_R:\mathbb{R}\rightarrow[0,1]$，定义如下：
$$
CDF_R(x)::=Pr[R\leq x]
$$

### 19.3.1 伯努利分布

$\triangle$ *伯努利分布*（Bernoulli distribution）的概率密度函数为
$$
f_p(0)=p, f_p(1)=1-p
$$
累积分布函数为
$$
F_p(x)::=\left\{\begin{array}{ll}0 & x<0 \\ p & 0\leq x<1 \\ 1 & 1\leq x \end{array}\right.
$$

### 19.3.2 均匀分布

$\triangle$ *均匀分布*（uniform distribution）的概率密度函数为
$$
f(v)=\frac{1}{n}
$$
累积分布函数为
$$
F_p(x)::=\left\{\begin{array}{ll}0 & x<a_1 \\ k/n & a_k\leq x<a_{k+1}， 1\leq k<n \\ 1 & a_n\leq x \end{array}\right.
$$

### 19.3.3 数字游戏

分析猜数字游戏的策略和概率模型

### 19.3.4 二项分布

$\triangle$ *二项分布*（binomial distribution）

$\triangle$ *无偏二项分布*（unbiased binomial distribution）的概率密度函数为
$$
f_n(k)::=\left(\begin{array}{c} n \\ k \end{array}\right)2^{-n}
$$
$\triangle$ *广义二项分布*（general binomial distribution）的概率密度函数为
$$
f_n(k)::=\left(\begin{array}{c} n \\ k \end{array}\right)p^k\left(1-p\right)^{n-k}
$$

## 19.4 期望

$\triangle$ *期望*（expectation）或*期望值*（expected value），又称*均值*（mean）或*平均值*（average）。

$\triangle$ **定义19.4.1** 如果$R$是定义在样本空间$S$的随机变量，那么$R$的期望是
$$
Ex[R]::=\sum_{\omega\in S}R\left(\omega\right)Pr[\omega]
$$

### 19.4.1 均匀随机变量的期望值

### 19.4.2 随机变量的倒数的期望

随机变量倒数的期望不等于随机变量期望的倒数。

### 19.4.3 指示器随机变量的期望

$\triangle$ **引理19.4.2** 如果$I_A$是事件A的指示器随机变量，那么$Ex[I_A]=Ex[A]$。

### 19.4.4 期望的另一种定义

$\triangle$ **定理19.4.3** 对任意的随机变量$R$，
$$
Ex[R]=\sum_{x\in\text{range}(R)}x\cdot Pr[R=x]
$$

### 19.4.5 条件期望

$\triangle$ **定义19.4.4** 对定事件A的条件下，随机变量$R$的*条件期望*（conditional expectation）$Ex[R|A]$是
$$
Ex[R|A]::=\sum_{r\in\text{range}(R)}r\cdot Pr[R=r|A]
$$
$\triangle$ **定理19.4.5**（全期望定理，Law of Total Exception） 设$R$是样本空间$S$上的一个随机变量，并且$A_1,A_2,\dots$是对$S$的划分，那么
$$
Ex[R]=\sum_i Ex[R|A_i]P[A_i]
$$

### 19.4.6 平均故障时间

$\triangle$ 假设系统在各个时间周期内独立运行，如果系统在每一个时间周期发生故障的概率为$p$，那么系统第一次出现故障所需的时间期望是$1/p$。

$\triangle$ **定义19.4.6** 随机变量$C$服从参数为$p$的*几何分布*（geometric distribution），当且仅当$陪域(C)=\mathbb{Z}^+$且
$$
Pr[C=i]=(1-p)^{i-1}p
$$
$\triangle$ **引理19.4.7** 如果随机变量$C$服从参数为$p$的几何分布，那么
$$
Ex[C]=1/p
$$

### 19.4.7 赌博游戏的预期收益

本节分析赌博游戏、国家彩票的期望。分析了有意识合谋和无意识合谋现象。

## 19.5 期望的线性性质

$\triangle$ 期望的线性性质（Linearity of Expectation）。

$\triangle$ **定理19.5.1** 对于任意随机变量$R_1$和$R_2$，有：
$$
Ex[R_1+R_2]=Ex[R_1]+Ex[R_2]
$$
$\triangle$ **定理19.5.2** 对于任意随机变量$R_1$和$R_2$和常数$a_1,a_2\in\mathbb{R}$，有：
$$
Ex[a_1R_1+a_2R_2]=a_1Ex[R_1]+a_2Ex[R_2]
$$
$\triangle$ **推论19.5.3**（期望的线性性质） 对于任意随机变量$R_1,\cdots,R_k$和常数$a_1,\cdots,a_k\in\mathbb{R}$，有：
$$
Ex\left[\sum_{i=1}^{k}a_iR_i\right]=\sum_{i=1}^ka_iEx[R_i]
$$

### 19.5.1 两个骰子的期望

### 19.5.2 指示器随机变量的和

$\triangle$ **定理19.5.4** 给定任意一系列事件$A_i,A_2,\cdots,A_n$，将要发生的事件数目的期望是
$$
\sum_{i=1}^{n}Pr[A_i]
$$

### 19.5.3 二项分布的期望

$\triangle$ 二项分布的期望$Ex[J]=pn$。

### 19.5.4 赠券收集问题

$\triangle$ 赠券收集问题的期望$Ex[T]=nH_n\sim n\ln n$。

### 19.5.5 无限和

$\triangle$ **定理19.5.5**（期望的线性性质） 设$R_0,R_1,\dots$为随机变量，且有
$$
\sum_{l=0}^\infin Ex\left[\left|R_i\right|\right]
$$
收敛，则
$$
Ex\left[\sum_{i=0}^{\infin}R_i\right]=\sum_{i=0}^{\infin}Ex\left[R_i\right]
$$

### 19.5.6 赌博悖论

本节阐述轮盘赌的悖论。

### 19.5.7 悖论的解答

本节解释轮盘赌悖论产生的原因。

### 19.5.8 乘积的期望

$\triangle$ **定理19.5.6** 对任意两个独立的随机变量$R_1,R_2$，$Ex[R_1\cdot R_2]=Ex[R_1]\cdot Ex[R_2]$

$\triangle$ **推论19.5.7**[独立乘积的期望] 如果随机变量$R_1,R_2,\cdots,R_k$是相互独立的，那么
$$
Ex\left[\prod_{i=1}^k R_i\right]=\prod_{i=1}^k Ex[R_i]
$$


# 第20章 离差

$\triangle$ 置信度（confidence）和置信水平（confidence level）。

$\triangle$ *噪声*（noise）和*偏离*（deviate）。

$\triangle$ *离差*（deviation from the mean，又称偏离平均数）。

## 20.1 马尔科夫定理

$\triangle$ **定理20.1.1**（马尔科夫定理） 如果$R$是一个非负随机变量，那么对任意$x>0$
$$
Pr[R\geq x]\leq\frac{Ex[R]}{x}
$$
$\triangle$ **推论20.1.2** 如果$R$是一个非负随机变量，那么对任意$c\geq1$
$$
Pr\left[R\geq c\cdot Ex[R]\right]\leq\frac{1}{c}
$$

### 20.1.1 应用马尔科夫定理

马尔科夫可以给出正确的上界，但是有时上界过大。

### 20.1.2 有界变量的马尔科夫定理

马尔科夫过程也可以应用于随机变量的变形（如$R-b$或$S-b$），要求变形后的随机变量也是非负的。

## 20.2 切比雪夫定理

$\triangle$ **引理20.2.1** 对任意随机变量$R$和正实数$x,z$，
$$
Pr[\left|R\right|\geq x] \leq \frac{Ex\left[\left|R\right|^z\right]}{x^z}
$$
用离差$\left|R-Ex[R]\right|$重写引理，可得
$$
Pr[\left|R-Ex[R]\right|\geq x] \leq \frac{Ex\left(\left[\left|R-Ex[R]\right|\right)^z\right]}{x^z}
$$
$\triangle$ **定义20.2.2** 随机变量$R$的**方差**（variance）为
$$
Var[R]::=Ex\left[\left(R-Ex[R]\right)^2\right]
$$
方差也被称为*均方差*（mean square deviation）。

$\triangle$ **定理20.3.3**（切比雪夫） 设计随机变量$R$以及$x\in\mathbb{R}^+$，那么
$$
Pr\left[\left|R-Ex[R]\right|\geq x\right]\leq\frac{Var[R]}{x^2}
$$

### 20.2.1 两个赌博游戏的方差

大方差往往与高风险相关联。

### 20.2.2 标准差

$\triangle$ **定义20.2.4** 随机变量$R$的*标注差*$\sigma_R$等于方差的平方根：
$$
\sigma_R::=\sqrt{Var[R]}=\sqrt{Ex\left[(R-Ex[R])^2\right]}
$$
简称*均方根*（root mean square）。

$\triangle$ **推论20.2.6** 设随机变量$R$和正实数$c$，
$$
Pr\left[\left|R-Ex[R]\right|\geq c\sigma_R\right]\leq\frac{1}{c^2}
$$

## 20.3 方差的性质

### 20.3.1 方差公式

$\triangle$ **引理20.3.1** 
$$
Var[R]=Ex[R^2]-Ex^2[R]
$$
对任意随机变量$R$成立。

$\triangle$ **推论20.3.2** 如果B是一个伯努利变量，其中$p::=Pr[B=1]$，那么
$$
Var[B]=p-p^2=p\left(1-p\right)
$$

### 20.3.2 故障时间的方差

$\triangle$ **推论20.3.3** 如果每一步发生故障的概率为$p$，且相互独立，$C$为第一次故障发生时的步数，那么
$$
Var[C]=\frac{1-p}{p^2}
$$

### 20.3.3 常数的处理

$\triangle$ **定理20.3.4**[方差的平方多重法则，Square Multiple Rule] 令$R$为随机变量，$a$为常数。那么，
$$
Var[aR]=a^2Var[R]
$$
$\triangle$ **定理20.3.5** 令$R$为随机变量，$b$为常数，那么
$$
Var[R+b]=Var[R]
$$
$\triangle$ **推论20.3.6**
$$
\sigma\left(aR+b\right)=\left|a\right|\sigma R
$$

### 20.3.4 和的方差

$\triangle$ **定理20.3.7** 如果$R$和$S$是独立的随机变量，那么
$$
Var[R+S]=Var[R]+Var[S]
$$
$\triangle$ **定理20.3.8**[方差的两两独立可加性] 如果$R_1,R_2,\dots,R_n$是两两独立的随机变量，那么
$$
Var[R_1+R_2+\dots+R_n]=Var[R_1]+Var[R_2]+\dots+Var[R_n]
$$
$\triangle$ **引理20.3.9**（二项分布的方差）如果$J$满足参数为$\left(n,p\right)$的二项分布，那么
$$
Var[J]=nVar[I_k]=np\left(1-p\right)
$$

### 20.3.5 生日匹配

假设有$n$个学生，一年有$d$天，设$M$为生日匹配的学生对的数量。令$B_1,B_2,\dots,B_n$是$n$个独立的人的生日，令$E_{i,j}$表示第$i$个人和第$j$个人有相同生日。那么
$$
Ex[M]=\sum_{1\leq i\leq j\leq n}Ex[E_{i,j}]=\left(\begin{array}{c}n \\ 2\end{array}\right)\cdot\frac{1}{d} \\
$$

$$
Var[M]=\sum_{1\leq i\leq j\leq n}Var[E_{i,j}]=\left(\begin{array}{c}n \\ 2\end{array}\right)\cdot\frac{1}{d}\left(1-\frac{1}{d}\right)
$$

## 20.4 随机抽样估计

### 20.4.1 选民投票

$\triangle$ 我们将使用样本值$S_n/n$作为$p$的*统计估计*（statistical estimate）。

已知概率分布，可以根据切比雪夫公式得到需要的样本大小。

### 20.4.2 两两独立采样

$\triangle$ **定理20.4.1**（两两独立采样） 假设$G_1,\dots,G_n$是两两独立的变量，就有相同的均值$\mu$和方差$\sigma$。定义
$$
S_n::=\sum_{i=1}^{n}G_i
$$
那么，
$$
Pr\left[\left|\frac{S_n}{n}-\mu\right|\geq x\right]\leq \frac{1}{n}\left(\frac{\sigma}{x}\right)^2$
$$
$\triangle$ **推论20.4.2**[弱大数定理，Weak Law of Large Number] 假设$G_1,\dots,G_n$为两两独立的变量，具有相同的均值$\mu$以及相同的有限偏差，令
$$
S_n::=\frac{\sum_{i=1}^n G_i}{n}
$$
那么对于任意$\epsilon>0$，
$$
\lim_{n\rightarrow\infty} Pr\left[\left|S_n-\mu\right| \leq \epsilon\right] = 1
$$

## 20.5 估计的置信度

$\triangle$ 置信水平（confidence level）指的是，真实量的估计过程结果。

## 20.6 随机变量的和

### 20.6.1 引例

本节介绍Fussbook的服务器负载均衡问题背景。

### 20.6.2 切诺夫界

$\triangle$ 切诺夫界指出很多小的、独立的随机变量的和，不大可能显著超过他们和的均值。

$\triangle$ **定理20.6.1**（切诺夫界） 设$T_1,\dots,T_n$为相互独立的随机变量，满足$0\leq T_i \leq 1$对任意$i$成立。令$T=T_1+T_2+\dots+T_n$，那么对所有$c\geq 1$，
$$
Pr\left[T\geq cEx[T]\right] leq e^{-\beta\left(c\right)Ex[T]}
$$
其中$\beta\left(c\right)::= c \ln c - c +1$。

### 20.6.3 二项式尾的切诺夫界

本节分析抛硬币过程的切诺夫界。偏离程度越大，边界越强。

### 20.6.4 彩票游戏的切诺夫界

本节分析选4彩票的切诺夫界。

### 20.6.5 随机负载均衡

本节分析Fussbook的服务器负载均衡问题的切诺夫界，计算所需要的服务器数量。

### 20.6.6 切诺夫界的证明

$\triangle$ **引理20.6.2** 
$$
Ex[c^T]\leq e^{\left(c-1\right)Ex[T]}
$$
$\triangle$ **引理20.6.3**
$$
Ex[c^{T_i}] \leq e^{\left(c-1\right)Ex[T_i]}
$$

### 20.6.7 边界的比较

针对独立事件，比较马尔科夫定理、切比雪夫定理和切诺夫界，切诺夫界最强。

### 20.6.8 墨菲定律

$\triangle$ **定理20.6.4**（墨菲定律） 设$A_1,A_2,\dots,A_n$为相互独立的事件。令$T_i$为$A_i$的指示器随机变量并定义
$$
T::=T_1+T_2+\dots+T_n
$$
为发生的事件个数。那么
$$
Pr[T=0]\leq e^{-Ex[T]}
$$

## 20.7 大期望

### 20.7.1 重复你自己

本节分析一个抛硬币赌博问题，证明在获胜之前需要给出无穷多次钱。



# 第21章 随机游走

$\triangle$ *随机游走*（random walk）的建模场景是某个对象按照随机选择的方向行走一个步数序列。

## 21.1 赌徒破产

$\triangle$ 赌徒手上的现金称为*资本*（capital）。

$\triangle$ 目标金额为$T$，定义$T-n$为*预期利润*（intended profit）。

$\triangle$ 如果赢得逾期利润，成为*全场总冠军*（overall winner）。如果在到达目标之前自资本变为零，损失$n$美元，称为*破产*（broke/ruined）。

$\triangle$ *无偏博弈*（unbiased game）中，每次赌博都是公平的，即$p=1/2$。如果$p>1/2$或者$p<1/2$，随机游走是*有偏的*（biased）。

$\triangle$ 以$n$美元开始，以$T \geq n$为目标，赌徒在破产前到达目标的概率是$n/T$。

### 21.1.1 避免破产的概率

$\triangle$ **定理21.1.1** 在赌徒破产博弈中，初始资本为$n$，目标为$T$，每一局获胜的概率为$p$，
$$
Pr[赌徒赢]=\left\{\begin{array}{ll}\frac{n}{T} & 对于p=\frac{1}{2} \\ \frac{r^n-1}{r^T-1} & 对于p\neq\frac{1}{2}\end{array}\right.
$$
其中$r::=q/p$。

### 21.1.2 获胜概率递推

### 21.1.3 有偏情况的简单解释

$\triangle$ **推论21.1.2** 在初始资本为$n$、目标为$T$、单次获胜概率为$p<1/2$的赌徒破产博弈中，
$$
Pr[赌徒赢]<\left(\frac{1}{r}\right)^{T-n}
$$
其中$r::=q/p>1$。

$\triangle$ 运气好坏导致赌徒的资本随机上下*波动*（swing）。赌徒的资本有一个稳定的向下*漂移*（drift）。

### 21.1.4 步长多长

### 21.1.5 赢了就退出

$\triangle$ 不管任何目标$T$，一定一直玩到彻底破产，称为*无限赌徒破产博弈*（unbounded Gambler's ruin game）。

$\triangle$ **引理21.1.4** 如果赌徒以1美元或更多钱开始，进行无限赌徒破产博弈，那么他将以概率1破产。

$\triangle$ **引理21.1.5** 如果赌徒以1美元或更多钱开始进行无限公平博弈，那么他能玩的预期次数是无限的。

## 21.2 图的随机游走

### 21.2.1 网页排名初探

$\triangle$ 将*网页排名*（page rank）定义为$indegree(x)$。

### 21.2.2 网页图的随机游走

$\triangle$ *超点*（supervertex）。

### 21.2.3 平稳分布与网页排名

$\triangle$ **定义21.2.1** 有向图的顶点概率的一个*平稳分布*（stationary distribution），如果对所有顶点$x$
$$
Pr[在x]=Pr[下一步到x]
$$
