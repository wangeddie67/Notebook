; Command:
; mit-scheme < 1-6.scm 

; Ex 1-6
; Alyssa P. Hacker看不出为什么需要将if提供为一种特殊形式，她问：“为什么我不能直接通过cond将它定义为一个常规过程呢？” Alysssa的朋友Eva Lu Ator断言确实可以这样做，并定义了if的一个新版本

(define (new-if predicate then-clause else-clause)
    (cond (predicate then-clause)
          (else else-clause)))

; Eva给Alyssa演示她的程序

(new-if (= 2 3) 0 5)

(new-if (= 1 1) 0 5)

; 她很高兴地用自己的new-if重写了求平方根的程序：

(define (average x y)
    (/ (+ x y) 2))

(define (improve guess x)
    (average guess (/ x guess)))

(define (good-enough? guess x)
    (< (abs (- (square quess) x)) 0.001))

(define (sqrt-iter guess x)
    (new-if (good-enough? guess x)
            guess
            (sqrt-iter (improve guess x)
                       x)))

; 当Alyssa试着用这个过程去计算平方根时会发生什么事情呢？请给出解释。

(sqrt-iter 1 4)

; 如果程序采用正则序，程序运行会死机。原因在于求值过程会反复求解then-clause和else-clause的值，从而进入死循环。
