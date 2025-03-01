#include "a.h"

int A::testAdd(int x, int y) {
    return x + y;
}

int A::testDiv(int x, int y) {
    return x / y;
}

int A::testMul(int x, int y) {
    return x * y;
}

int A::testSub(int x, int y) {
    return x - y;
}

int B::testAdd(int x, int y) {
    return x + y;
}

int B::testDiv(int x, int y) {
    return x / y;
}

int B::testMul(int x, int y) {
    return x * y;
}

int B::testSub(int x, int y) {
    return x - y;
}

template<typename T>
T C<T>::testAdd(T x, T y) {
    return x + y;
}

template<typename T>
T C<T>::testDiv(T x, T y) {
    return x / y;
}

template<typename T>
T C<T>::testMul(T x, T y) {
    return x * y;
}

template<typename T>
T C<T>::testSub(T x, T y) {
    return x - y;
}

class D {
public:
    void addA(A a) {
        a.testAdd(1, 2);
    }

    void addB(B b) {
        b.testAdd(1, 2);
    }

    void addC(C<int> c) {
        c.testAdd(1, 2);
    }

protected:
    A a;
    B b;
    C<int> c;
};