#include <iostream>
#ifndef __A_H__
#define __A_H__

class A {
public:
    int testAdd(int x, int y);
    int testSub(int x, int y);
    int testMul(int x, int y);
    int testDiv(int x, int y);

private:
    int TestA;
    int TestB;
};

struct B {
    public:
    int testAdd(int x, int y);
    int testSub(int x, int y);
    int testMul(int x, int y);
    int testDiv(int x, int y);

private:
    int TestA;
    int TestB;
};

template <typename T>
class C {
public:
    T testAdd(T x, T y);
    T testSub(T x, T y);
    T testMul(T x, T y);
    T testDiv(T x, T y);

private :
    T TestA;
    T TestB;
};

class E : public A {
    public:
    int testAdd(int x, int y) {
        return x + y;
    }
    int testSub(int x, int y) {
        return x - y;
    }
    int testMul(int x, int y) {
        return x * y;
    }
    int testDiv(int x, int y) {
        return x / y;
    }

    private:
    int TestA;
    int TestB;
};

#endif
