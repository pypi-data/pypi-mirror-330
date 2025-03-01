import os
import concurrent.futures
from antlr4 import *

if "__main__" == __name__:
    from antlr.java import JavaLexer, JavaParser, JavaParserListener
else:
    from .antlr.java import JavaLexer, JavaParser, JavaParserListener
import json

def get_before_equal(s):
    if '=' in s:
        index = s.index('=')
        return s[:index]
    return s


class JavaClassListener(JavaParserListener.JavaParserListener):
    def __init__(self, parsed_data):
        self.parsed_data = parsed_data
        self.current_class = None
        self.current_method = None
        self.package_name = ""
        self.classes = []
        self.permission = "package"
    
    def enterPackageDeclaration(self, ctx: JavaParser.JavaParser.PackageDeclarationContext):
        self.package_name = ctx.qualifiedName().getText()
        print("enterPackageDeclaration package_name:", self.package_name)
    
    def enterClassOrInterfaceModifier(self, ctx: JavaParser.JavaParser.ClassOrInterfaceModifierContext):
        self.permission = ""
        if ctx.STATIC():
            self.permission = "static"
        if ctx.FINAL():
            self.permission = "final"
        if ctx.PUBLIC():
            self.permission += "public"
        elif ctx.PROTECTED():
            self.permission += "protected"
        elif ctx.PRIVATE():
            self.permission += "private"
        else:
            self.permission += "package"
            
        print("enterClassOrInterfaceModifier permission:", self.permission)

    def enterClassDeclaration(self, ctx: JavaParser.JavaParser.ClassDeclarationContext):
        class_name = ctx.identifier().getText()
        print("enterClassDeclaration class_name:", class_name)
        class_type = "class" if ctx.CLASS() else "interface"

        bases = []
        if ctx.typeType():
            bases.append(ctx.typeType().getText())

        if ctx.typeList():
            for type_list in ctx.typeList():
                for interface_type in type_list.typeType():
                    interface_name = interface_type.getText()
                    bases.append(interface_name)

        package_name = self.get_current_package()

        if class_name not in self.parsed_data['classes']:
            self.parsed_data['classes'][class_name] = {
                'package' : package_name,
                'methods': [],
                'fields': [],
                'bases': bases
            }
        else:
            self.parsed_data['classes'][class_name]['bases'] = bases

        self.current_class = class_name
        self.classes.append(class_name)
        self.permission = "package"

    def exitClassDeclaration(self, ctx: JavaParser.JavaParser.ClassDeclarationContext):
        self.current_class = None
        self.classes.pop()

        if self.classes:
            self.current_class = self.classes[-1]

    def enterMethodDeclaration(self, ctx: JavaParser.JavaParser.MethodDeclarationContext):
        if not self.current_class:
            return
        
        method_name = ctx.identifier().getText()
        print("method_name:", method_name)
        
        if "public" not in self.permission:
            return


        # return_type = ctx.typeType().getText() if ctx.typeType() else "void"
        return_type = self.get_return_type(ctx)
        # print("return_type:", return_type)
        
        parameters = self.getMethodParamters(ctx)
        
  
        # print("parameters:", parameters)
        # formalParameter
        
        # parameters = self._get_parameters(ctx.formalParameters().formalParameterList())
        
        # # print(f"Method: {method_name} ({return_type})")
        # # print(f"Parameters: {parameters}")

        self.current_method = method_name
        # print("method:", method_name)
        # print("methodBody:", ctx.methodBody().getText())
        self.parsed_data['classes'][self.current_class]['methods'].append(f'{return_type} {self.current_method}({parameters});')

    def get_current_package(self):
        package = self.package_name
        if self.classes:
            for index in range(0, len(self.classes), 1):
                if package:
                    package +=  '.' + self.classes[index]
                else:
                    package = self.classes[index]
        return package

    def enterInterfaceDeclaration(self, ctx: JavaParser.JavaParser.InterfaceDeclarationContext):
        class_name = ctx.identifier().getText()
        bases = []
        if ctx.typeList() is not None:
            for type_list in ctx.typeList():
                for interface_type in type_list.typeType():
                    # # print("interface_type", interface_type)
                    interface_name = interface_type.getText()
                    bases.append(interface_name)
                    # # print(f"Implements: {interface_name}")

        package_name = self.get_current_package()

        if class_name not in self.parsed_data['classes']:
            self.parsed_data['classes'][class_name] = {
                'package' : package_name,
                'methods': [],
                'fields': [],
                'bases': bases
            }
        else:
            self.parsed_data['classes'][class_name]['bases'] = bases
        # print("interface body:", ctx.interfaceBody().getText())
        self.current_class = class_name
        self.classes.append(class_name)
        
    def enterInterfaceMethodDeclaration(self, ctx: JavaParser.JavaParser.InterfaceMethodDeclarationContext):
        method_name = ctx.interfaceCommonBodyDeclaration().identifier().getText()
        return_type = self.get_return_type(ctx.interfaceCommonBodyDeclaration())
        parameters = self.getMethodParamters(ctx.interfaceCommonBodyDeclaration())
        self.parsed_data['classes'][self.current_class]['methods'].append(f'{return_type} {method_name}({parameters});')
        
    def exitInterfaceMemberDeclaration(self, ctx: JavaParser.JavaParser.InterfaceMethodDeclarationContext):
        self.current_method = None
        
    def exitInterfaceDeclaration(self, ctx: JavaParser.JavaParser.InterfaceDeclarationContext):
        self.current_class = None
        self.classes.pop()
        if len(self.classes) != 0:
            self.current_class = self.classes[-1]

    def getMethodParamters(self, ctx):
        parameters = ""
        if ctx.formalParameters().formalParameterList() is not None:
            for formalParameter in ctx.formalParameters().formalParameterList().formalParameter():
                if formalParameter.typeType().classOrInterfaceType() is not None:
                    parameter_type = formalParameter.typeType().classOrInterfaceType().getText()
                else:
                    parameter_type = formalParameter.typeType().primitiveType().getText()
                if formalParameter.variableDeclaratorId() is not None:
                    parameter_name = formalParameter.variableDeclaratorId().identifier().getText()
                    parameters += f"{parameter_type} {parameter_name}, "
            parameters = parameters[:-2]
        return parameters

    def get_return_type(self, ctx):
        return_type = ""
        if ctx.typeTypeOrVoid().VOID() is not None:
            return_type = "void"
        else:
            if ctx.typeTypeOrVoid().typeType().classOrInterfaceType() is not None:
                return_type = ctx.typeTypeOrVoid().typeType().classOrInterfaceType().typeIdentifier().IDENTIFIER().getText()
            elif ctx.typeTypeOrVoid().typeType().primitiveType() is not None:
                return_type = ctx.typeTypeOrVoid().typeType().primitiveType().getText()
            else:
                return_type = "constructor"
        return return_type
        

    def exitMethodDeclaration(self, ctx: JavaParser.JavaParser.MethodDeclarationContext):
        self.current_method = None

    def enterFieldDeclaration(self, ctx: JavaParser.JavaParser.FieldDeclarationContext):
        if not self.current_class:
            return
        
        if "static" in self.permission or "final" in self.permission:
            return
        

        field_type = ctx.typeType().getText()
        print("field_type:", field_type)
        field_names = [id.getText() for id in ctx.variableDeclarators().variableDeclarator()]
        
        # 避免出现 int a = 1;
        # HashMap<String, Integer> map = new HashMap<>();的情况
        for name in field_names:
            name = get_before_equal(name)
            field = {
                'name': name,
                'type': field_type
            }
            self.parsed_data['classes'][self.current_class]['fields'].append(field)

def parse_java(code, line_numbers = 0):
    input_stream = InputStream(code)
    lexer = JavaLexer.JavaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = JavaParser.JavaParser(stream)
    tree = parser.compilationUnit()
    parsed_data = {'classes': {}, 'lines': line_numbers}
    listener = JavaClassListener(parsed_data)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    return parsed_data

def process_single_file(file_path):
    """
    处理单个 Java 文件，返回解析后的数据。
    """
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        with open(file_path, 'r') as file:
            line_count = len(file.readlines())
        return parse_java(code, line_count)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def merge_results(results):
    """
    合并多个解析结果字典。
    """
    merged_data = {'classes': {}, 'lines': 0}
    for result in results:
        if result is not None:
            merged_data['lines'] += result['lines']
            for class_name, class_data in result['classes'].items():
                merged_data['classes'][class_name] = class_data  # 或者进行更复杂的合并，例如处理同名类的情况
    return merged_data

def parse_java_files(files):
    """
    优化后的 Java 文件解析函数，使用线程池处理。
    """
    num_files = len(files)

    if num_files == 0:
        print("No code found in the files.")
        return None  # 或者返回一个空的解析结果

    # 使用线程池
    cpu_count = os.cpu_count()
    max_workers = int(min(cpu_count / 2, 32))  # 限制最大线程数，防止资源耗尽, 32是一个经验值，根据实际情况调整
    print(f"Using thread pool with {max_workers} workers.")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_file, file_path) for file_path in files]
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error in thread: {e}")
                # Handle thread exception.  Maybe re-raise, log and continue, or exit.
                # Decide based on the severity of the error.
                # For example:
                #import traceback
                #traceback.print_exc()
                results.append(None)  # Add a None if a future fails

    # 合并结果
    merged_data = merge_results(results)
    return merged_data


if __name__ == '__main__':
    # Example Java code to parse
    java_code = """
    package com.example;
    public class Example extends BaseClass implements Interface1, Interface2 {
        private int field1;
        protected static final String field2 = "value";

        public Example() {
        }

        public int method1(int param1, String param2) {
            return 0;
        }

        protected T method2(T param1, T param2) {
        }

        static void method3() {
        }
        
        interface ILove {
            void foo();
            void love();
            default int testAdd(int x, int y) { return 0;}
        }

        class Love implements ILove {
            class Inner {
                int x;
                public void foo(int x) {
                    System.out.println("Inner.foo" + x + " this:" + this.x);
                }
                
                class TestInner {
                    int y;
                    public void foo(int x) {
                        System.out.println("TestInner.foo" + x + " y:" + y);
                    }
                }
            }
            @Override
            public void foo() {
                System.out.println("foo");
            }

            @Override
            public void love() {
                System.out.println("love");
            }
        }
    }
    public class Example1 extends Example {
        public Example1() {
        }
        public void method4() {
        }
        int x;
    }
    """
    parsed_data = parse_java(java_code)
    str = json.dumps(parsed_data, indent=4)
    print(str)
