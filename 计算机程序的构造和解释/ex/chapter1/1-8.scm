; Command:
; mit-scheme < 1-8.scm 

; Ex 1-8
; 求立方根的牛顿法基于如下事实，如果y是x的立方根的一个近似值，那么下式将给出一个更好的近似值：

; 请利用这一公式实现一个类似平方根过程的求立方根的过程。

(define (average x y)
    (/ (+ x y) 2))

(define (improve guess x)
    (/ (+ (/ x (square guess)) (* 2 guess)) 3))

(define (good-enough? guess x)
    (< (abs (- (square guess) x)) 0.001))

(define (sqrt-iter guess x)
    (if (good-enough? guess x)
        guess
        (sqrt-iter (improve guess x)
                   x)))

(sqrt-iter 1 4)

