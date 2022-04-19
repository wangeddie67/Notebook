; Command:
; mit-scheme < 1-12.scm 

; Ex 1-12
; 下面数值模式成为帕斯卡三角形：
; 三角形边界上的数都是1，内部的每个数是位于它上面的两个数之和。请写一个过程，它采用递归计算过程计算帕斯卡三角形。

(define (pascal row col)
    (cond ((< col 0) 0)
          ((= col 0) 1)
          ((= col row) 1)
          ((< col row) (+ (pascal (- row 1) (- col 1)) (pascal (- row 1) col)))
          (else 0)))

(pascal 0 0)
(pascal 1 0)
(pascal 1 1)
(pascal 2 0)
(pascal 2 1)
(pascal 2 2)
(pascal 3 0)
(pascal 3 1)
(pascal 3 2)
(pascal 3 3)
(pascal 4 0)
(pascal 4 1)
(pascal 4 2)
(pascal 4 3)
(pascal 4 4)

