# 开发者

安装antlr4, antlr4是一个语法解析器，能够支持很多的语法，目前支持的语言可以在这个库中找到
[https://github.com/antlr/grammars-v4/tree/master](https://github.com/antlr/grammars-v4/tree/master)

```sh
pip install antlr4-python3-runtime
```

```sh
antlr4 -Dlanguage=Python3 javaantlr/JavaLexer.g4 javaantlr/JavaParser.g4
antlr4 -Dlanguage=Python3 code2uml/antlr/cpp/CPP14Lexer.g4
antlr4 -Dlanguage=Python3 code2uml/antlr/cpp/CPP14Parser.g4
```

生成python的解析器

```sh
.
├── JavaLexer.g4
├── JavaLexer.interp
├── JavaLexer.py
├── JavaLexer.tokens
├── JavaParser.g4
├── JavaParser.interp
├── JavaParserListener.py
├── JavaParser.py
└── JavaParser.tokens
```

C++解析器存在问题:

1. 如果只使用这个lex和parser, 没有形成完整的语义树, 无法生成AST, 无法识别字段, 需要将python中的代码连接起来，需要从[https://github.com/antlr/grammars-v4/tree/master](https://github.com/antlr/grammars-v4/tree/master)中导入`CPP14ParserBase.py`和`transformGrammar.py`

transformGrammar.py是用于生成CPP14Parser.g4和CPP14Lexer.g4的工具，如果之前已经有现成的，可以不用执行
CPP14ParserBase.py只需要和生成后的文件集成在一起即可.

![alt text](img/develop/image.png)

2. 字段识别存在问题，无法识别成员变量

## 设计思路
再利用antlr解析完成后，需要构建一个默认的中间语言，用于转换
综合C++/Java 类的声明和定义, 产生如下一个中间结构, 对于python而言是dict字典，也可以是数据结构
```json
{
  "classes" : {
    "class_name" : {
       "method" : [
         {
           "permission" : "private/protected/public/package",
           "name" : "MethodName"
         }
       ],
       "fields" : [
         {
           "permission" : "private/protected/public/package",
           "name" : "fieldName"
         }
       ]
    }
  },
  "lines" : 10
}
```
* classes 用于定义总体的管理结构
* className 类名
  * method 方法集合
    * permission 权限问题
    * name 方法名
  * fields 字段集合
    * permission 权限问题
    * name 字段名
* lines 文件的行数，用于统计处理效率

建议的逻辑:
将单个文件的处理作为一个任务，如果任务长度小于8，则直接处理
如果总体超过10个任务，则启用线程池，线程池大小根据机器的cpu多少，运行不超过CPU 2/3的线程
处理后，将相关的结果dict进行合并操作, 最终合并后再进行转换


