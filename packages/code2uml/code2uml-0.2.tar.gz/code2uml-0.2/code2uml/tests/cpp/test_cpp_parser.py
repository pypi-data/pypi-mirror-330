import unittest
from code2uml.parser.cpp_parser import CppParser

class TestCppParser(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(True)

    def testCppClass(self):
        code = '''
        class MyClass {
        private:
            int myVar;
        public:
            void myMethod();
        };
        '''
        parser = CppParser()
        result = parser.parse(code)
        self.assertEqual(len(result.classes), 1)
        self.assertEqual(result.classes[0].name, "MyClass")
        self.assertEqual(len(result.classes[0].methods), 1)
        self.assertEqual(result.classes[0].methods[0].name, "myMethod")

    def testCppClassInheritance(self):
        code = '''
        class Base {
        public:
            virtual void baseMethod();
        };

        class Derived : public Base {
        public:
            void derivedMethod();
        };
        '''
        parser = CppParser()
        result = parser.parse(code)
        self.assertEqual(len(result.classes), 2)
        self.assertEqual(result.classes[1].name, "Derived")
        self.assertEqual(len(result.classes[1].base_classes), 1)
        self.assertEqual(result.classes[1].base_classes[0], "Base")

    def testClassMethods(self):
        code = '''
        class MathUtils {
        public:
            int add(int a, int b) { return a + b; }
            int subtract(int a, int b) { return a - b; }
        };
        '''
        parser = CppParser()
        result = parser.parse(code)
        self.assertEqual(len(result.classes[0].methods), 2)
        self.assertEqual(result.classes[0].methods[0].name, "add")
        self.assertEqual(result.classes[0].methods[1].name, "subtract")

    def testNamespace(self):
        code = '''
        namespace MyNamespace {
            class MyClass {
            public:
                void myMethod();
            };
        }
        '''
        parser = CppParser()
        result = parser.parse(code)
        self.assertEqual(len(result.namespaces), 1)
        self.assertEqual(result.namespaces[0].name, "MyNamespace")
        self.assertEqual(len(result.namespaces[0].classes), 1)
        self.assertEqual(result.namespaces[0].classes[0].name, "MyClass")

if __name__ == '__main__':
    unittest.main()
