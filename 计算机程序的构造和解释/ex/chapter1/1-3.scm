; Command:
; mit-scheme < 1-3.scm 

; Ex 1-3
; 请定义一个过程，它以三个数为参数，返回其中较大的两个数之和。

(define (major-sum a b c)
    (cond ((and (> b a) (> c a)) (+ b c))
          ((and (> a b) (> c b)) (+ a c))
          (else (+ a b))))

(major-sum 1 2 3)

(major-sum 3 1 2)

(major-sum 2 3 1)
