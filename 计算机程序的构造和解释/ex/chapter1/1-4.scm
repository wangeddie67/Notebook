; Command:
; mit-scheme < 1-4.scm 

; Ex 1-4
; 请仔细考察上面给出的允许运算符为符合表达式组合的求值模型，根据对这一模型的认识描述下面过程的行为。

(define (a-plus=abs-b a b)
    ((if (> b 0) + -) a b))

