# 递推

$\triangle$ *递推*（recurrence）和递归算法（recursive algorithm）。

$\triangle$ *猜测-验证法*（guess-and-verify）和*扩充-化简法*（plug-and-chug）。



# 第22章 递推

## 22.1 汉诺塔

$\triangle$ 求解递推方程的方法有很多。最简单的办法是*猜测*（guess）一个方案，再用归纳证明法*验证*（Verify）这个猜测是否正确。

$\triangle$ **断言 22.1.1** $T_n=2^n-1$满足递推：
$$
\begin{array}{l} T_1 = 1 \\ T_n=2T_{n-1} + 1 \end{array}
$$

$T_n$表示$n$个盘子的汉诺塔的移动次数。

### 22.1.1 上界陷阱

本节的中心意思是：如果一个递推的解过于复杂，可以尝试证明某个简单的表达式是递推解的上界。但是上界有可能无法用归纳证明法证明。

### 22.1.2 扩充-化简法

$\triangle$ 扩充-化简法（plug-and-chug），有时也称为”扩展“（expansion）或者”迭代“（iteration）。

$\triangle$ 步骤：

- 步骤1：扩充和化简直到规律出现。
- 步骤2：验证规律。
- 步骤3：用已知的前几项重写通项公式。

## 22.2 归并排序

$\triangle$ *归并排序*（Merge Sort）

- 如果输入只有1个数字，算法什么也不做。
- 否则，分别对列表的前一半和后一半进行排序。然后将两部分合并。

### 22.2.1 寻找递推

$\triangle$ $T_n$表示对$n$个数字进行归并排序所需要的比较次数的最大值。
$$
\begin{array}{ll} T_1=0 \\ T_n=2T_{n/2}+n-1 & n\geq2 \end{array}
$$

## 22.3 线性递推

### 22.3.1 爬楼梯

$\triangle$ *齐次线性递推*（homogeneous linear recurrence）：形如
$$
f(n)=a_1f(n-1)+a_2f(n-2)+\dots+a_df(n-d)
$$
其中$a_1,a_2,\dots,a_d$和$d$是常量。$d$是递推的*阶*（order）。通常，函数$f$的值落在若干个点上，称为*边界条件*（boundary condition）。

$\triangle$ **定理 22.3.1** 如果$f(n)$和$g(n)$是齐次线性递推的两个解，那么对所有$s,t \in \mathbb{R}$，$h(n)=sf(n)+tg(n)$也是这个递推的解。

$\triangle$ 解的线性组合也是解。

### 22.3.2 求解齐次线性递推

$\triangle$ *特征方程*（characteristic equation）。特征方程的根就是线性递推的解。如果不考虑边界条件：

- 如果$r$是特征方程的非重根，则$r^n$是递推的一个解。
- 如果$r$是特征方程的$k$重根，则$r^n,nr^n,n^2r^n,\dots,n^{k-1}r^n$都是递推的解。

### 22.3.3 求解一般线性递推

$\triangle$ *非齐次线性递推*（inhomogeneous linear recurrence）：
$$
f(n)=a_1f(n-1)+a_2f(n-2)+\dots+a_df(n-d)+g(n)
$$

$\triangle$ 求解步骤：

- 用0代替$g(n)$，得到一个齐次线性递推。如同之前一样，得到特征方程的根。
- 计算齐次递推的解，但是不要用边界条件去确定常量，这称之为*齐次解*（homogeneous solution）。
- 恢复$g(n)$，忽略边界条件，确定一个递推解，称为*特解*（particular solution）。
- 将齐次解和特解加起来得到*通解*（general solution）。
- 使用边界条件，求解线性方程组确定常量。

### 22.3.4 如何猜测特解

## 22.4 分治递推

$\triangle$ 分治算法（divide-and-conquer algorithm）和*分治递推*（divide-and-conquer recurrences）：
$$
T_n=\sum^k_{i=1}a_iT\left(b_in\right)+g\left(n\right)
$$

其中$a_i,\dots,a_k$是正常数，$b_i,\dots,b_k$是0到1之间的常数，$g(n)$是一个非负函数。

### 22.4.1 Akra-Bazzi公式

$\triangle$ 一般分治递推的渐进解（asymptotic solution）是
$$
T\left(n\right)=\Theta\left(n^p\left(1+\int_1^n\frac{g\left(u\right)}{u^{p+1}}du\right)\right)
$$
其中$p$满足
$$
\sum_{i=1}^k a_ib_i^p = 1
$$

### 22.4.2 两个技术问题

$\triangle$ 首先，Akra-Bazzi公式不能处理边界条件。然后，分治递推不产生线性递推。

$\triangle$ 分治递推的近似解与边界条件无关。

$\triangle$ 分治递推的近似解不受向上取整和向下取整操作的影响。

### 22.4.3 Akra-Bazzi定理

$\triangle$ **定理22.4.1（Akra-Bazzi） **设函数$T: \mathbb{R} \rightarrow \mathbb{R}$是非负的，当$0\leq x \leq x_0$时有界，且满足递推
$$
T\left(x\right)=\sum_{i=1}^k a_iT\left(b_ix+h_i\left(x\right)\right)+g\left(n\right)\space\space\space\space x > x_0
$$
其中：

1. $x_0$足够大，$T$是严格定义的。
2. $a_1,\dots,a_k$是大于0的常数。
3. $b_1,\dots,b_k$是0到1之间的常数。
4. $g\left(x\right)$是非负函数，且$\left|g'\left(x\right)\right|$有多项式界。
5. $\left|h_i\left(x\right)\right|=O\left(x/log^2x\right)$

那么
$$
T\left(n\right)=\Theta\left(n^p\left(1+\int_1^n\frac{g\left(u\right)}{u^{p+1}}du\right)\right)
$$
其中$p$满足
$$
\sum_{i=1}^k a_ib_i^p = 1
$$

### 22.4.4 主定理

$\triangle$ **定理22.4.2（主定理） **对于如下形式的递归$T$
$$
T\left(n\right)=aT\left(\frac{n}{b}\right)+g\left(n\right)
$$
**情况1：**如果存在常数$\epsilon > 0$使$g\left(n\right)=O\left(n^{log_b\left(a\right)-\epsilon}\right)$成立，则
$$
T\left(n\right)=\Theta\left(n^{log_b\left(a\right)-\epsilon}\right)
$$
**情况2：**如果存在常数$k\geq 0$使$g\left(n\right)=\Theta\left(n^{log_b\left(a\right)}log^k\left(n\right)\right)$成立，则
$$
T\left(n\right)=\Theta\left(n^{log_b\left(a\right)}log^{k+1}\left(n\right)\right)
$$
**情况3：**如果存在常数$\epsilon > 0$使$g\left(n\right)=\Omega\left(n^{log_b\left(a\right)-\epsilon}\right)$成立，其中$ag\left(n/b\right)<cg\left(n\right)$对常数$c<1$成立，且$n$足够大，则
$$
T\left(n\right)=\Theta\left(g\left(n\right)\right)
$$

## 22.5 进一步探索