
;; test.lisp

(test-report

    (define x 10)
    (define s "str")
    (define (square x) (* x x))


    (eq? null ())
    (eq? () null)
    (eq? null 'null)
    (eq? () '())

    (eq? x 10)
    (eq? x x)
    (eq? s "str")
    (eq? s s)
    (eq? 10.1 10.1)

)

