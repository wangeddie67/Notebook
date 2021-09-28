; Command:

; Ex 1-9
; 下面几个过程各定义了一种加两个正整数的方法，他们都基于过程inc和dec。

(define (+ a b)
    (if (= a 0)
        b
        (inc (+ (dec a) b)))

(define (+ a b)
    (if (= a 0)
        b
        (+ (dec a) (inc b))))

; 请用代换模型展示这两个过程在求值(+ 4 5)时所产生的计算过程。这些计算过程是递归的或者迭代
; 的吗？

(+ 4 5)
(inc (+ (dec 4) 5))
(inc (+ 3 5))
(inc (inc (+ (dec 3) 5)))
(inc (inc (+ 2 5)))
(inc (inc (inc (+ (dec 2) 5))))
(inc (inc (inc (+ 1 5))))
(inc (inc (inc (inc (+ (dec 1) 5)))))
(inc (inc (inc (inc (+ 0 5)))))
(inc (inc (inc (inc 5))))
(inc (inc (inc 6)))
(inc (inc 7))
(inc 8)
9   ; 递归过程

(+ 4 5)
(+ (dec 4) (inc 5))
(+ 3 6)
(+ (dec 3) (inc 6))
(+ 2 7)
(+ (dec 2) (inc 7))
(+ 1 8)
(+ (dec 1) (inc 8))
(+ 0 9)
9   ; 迭代过程
