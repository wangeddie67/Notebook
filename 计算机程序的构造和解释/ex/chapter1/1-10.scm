; Command:
; mit-scheme < 1-10.scm 

; Ex 1-10
; 下面过程计算一个称为Ackermann函数的数学函数：

(define (A x y)
    (cond ((= y 0) 0)
          ((= x 0) (* 2 7))
          ((= y 1) 2)
          (else (A (- x 1) (A x (- y 1))))))

; 下面各表达式的值是什么

(A 1 10)    ; 14

(A 2 4) ; 14

(A 3 3) ; 14

; 请考虑下面的过程，其中的A就是上面定义的过程

(define (f n) (A 0 n))
; (cond ((= n 0) 0)
;       (else 14))

(define (g n) (A 1 n))
; (cond ((= n 0) 0)
;       ((= n 1) 2)
;       (else 14))

(define (h n) (A 2 n))
; (cond ((= n 0) 0)
;       ((= n 1) 2)
;       (else 14))

(define (k n) (* 5 n n))

; 请给出过程f、g和h对给定整数值n所计算的函数的数学定义。例如，(k n)计算的是5n2。
