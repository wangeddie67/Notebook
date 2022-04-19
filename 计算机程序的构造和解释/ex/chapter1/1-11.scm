; Command:
; mit-scheme < 1-11.scm 

; Ex 1-11
; 函数f由如下的规则定义：如果n<3，那么f(n)=n；如果n>=3，那么f(n)=f(n-1)+2f(n-2)+3f(n-3)。
; 请写一个采用递归计算过程计算f的过程。在写一个采用迭代计算过程计算f的过程。

(define (f1 n)
    (cond ((< n 3) n)
          (else (+ (f1 (- n 1)) 
                   (* 2 (f1 (- n 2)))
                   (* 3 (f1 (- n 3)))))))

(f1 1)
(f1 2)
(f1 3)
(f1 4)
(f1 5)
(f1 6)
(f1 7)
(f1 8)
(f1 9)
(f1 10)

(define (f2 n)
    (cond ((< n 3) n)
          (else (f-iter 1 2 4 n))))
    

(define (f-iter a b c count)
    (cond ((= count 3) c)
          (else (f-iter b c (+ c (* 2 b) (* 3 a)) (- count 1)))))

(f2 1)
(f2 2)
(f2 3)
(f2 4)
(f2 5)
(f2 6)
(f2 7)
(f2 8)
(f2 9)
(f2 10)
