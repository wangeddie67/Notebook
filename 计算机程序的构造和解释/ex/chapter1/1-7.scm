; Command:
; mit-scheme < 1-7.scm 

; Ex 1-7
; 对于确定很小的数的平方根而言，在计算平方根中使用的检测good-enough?是很不好的。还有，
; 在现实的计算机里，算术运算总是以一定的有限精度进行的。这也会使我们的检测不适合非常大的数的计算。
; 请解释上述论断，用例子说明对很小和很大的数，这种检测都可能失败。实现good-enough的
; 另一个策略是监视猜测值在从一次迭代到下一次的变化情况，当改变值相对于猜测值的比率很小时就结束，
; 请设计一个采用这种终止测试方式的平方根过程。对于很大和很小的数。这一方式都能工作吗？

(define (average x y)
    (/ (+ x y) 2))

(define (improve guess x)
    (average guess (/ x guess)))

(define (good-enough? guess preguess)
    (< (abs (- guess preguess)) 0.001))

(define (sqrt-iter guess preguess x)
    (if (good-enough? guess preguess)
        guess
        (sqrt-iter (improve guess x)
                   guess
                   x)))

(sqrt-iter 1 0 4)

