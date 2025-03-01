import os
import time
import argparse
if __name__ == "__main__":
    from parser.cpp_parser import parse_cpp_files, parse_cpp
    from parser.java_parser import parse_java_files, parse_java
    from graph.diagram_converter import save_diagrams
else:
    from .parser.cpp_parser import parse_cpp_files, parse_cpp
    from .parser.java_parser import parse_java_files, parse_java
    from .graph.diagram_converter import save_diagrams

def parse_file_with_metadata(file_path):
    """解析单个文件并收集元数据"""
    file_ext = os.path.splitext(file_path)[1].lower()
    java_data = {}
    cpp_data = {}
    if file_ext == ".java":
        java_data = parse_java_files([file_path])
        save_diagrams(java_data, file_path + "_java")
    elif file_ext in ['.cpp', '.h', '.hpp', '.cc']:
        cpp_data = parse_java_files([file_path])
        save_diagrams(cpp_data, file_path + "_cpp")
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    return {
        'java': java_data,
        'cpp': cpp_data
    }

def handle_multiple_inputs(input_paths):
    """
    处理多个输入路径（文件和/或目录）。

    该函数接收一个路径列表，遍历每个路径，判断其是文件还是目录，并相应地处理。对于目录，调用 `handle_directory` 函数；对于文件，调用 `handle_file` 函数。最终返回一个包含 Java 和 C++ 结果的字典。

    参数：
        input_paths (list): 输入路径列表，可以是文件或目录的路径。
        focus (str): 关注的内容（未在函数中使用，可能用于扩展功能）。

    返回：
        dict: 包含 Java 和 C++ 结果的字典，格式为 {"java": java_results, "cpp": cpp_results}。

    异常：
        ValueError: 如果输入路径无效，则抛出异常。
    """
    java_results = {}
    cpp_results = {}
    for path in input_paths:
        if os.path.isdir(path):
            dir_results = handle_directory([path]) # Pass each directory as a list
            if dir_results['java']:
                java_results.update(dir_results['java'])
            if dir_results['cpp']:
                cpp_results.update(dir_results['cpp'])
        elif os.path.isfile(path):
            file_results = handle_file(path)
            if file_results['java']:
                java_results.update(file_results['java'])
            if file_results['cpp']:
                cpp_results.update(file_results['cpp'])
        else:
            raise ValueError(f"Invalid input path: {path}")
    
    return { "java": java_results, "cpp": cpp_results }

def handle_directory(directories):
    """处理目录输入，按语言类型分线程解析"""
    java_files = []
    cpp_files = []
    hasDirectory = False

    # 遍历获取java和cpp文件
    for directory in directories:
        for root, _, files in os.walk(directory):
            hasDirectory = True
            for file in files:
                if file.endswith(".java"):
                    print(f"Processing file: {file}")
                    java_files.append(os.path.join(root, file))
                elif file.endswith(".cpp") or file.endswith(".h") or file.endswith(".hpp") or file.endswith(".cc"):
                    print(f"Processing file: {file}")
                    cpp_files.append(os.path.join(root, file))

    if not hasDirectory:
        print("error input directories:", directories)
        exit()

    cpp_results = {}
    java_results = {}

    if len(java_files) != 0:
        java_results = parse_java_files(java_files)
        save_diagrams(java_results, directories[0] + "/code2uml_java")
    if len(cpp_files) != 0:
        cpp_results = parse_cpp_files(cpp_files)
        save_diagrams(cpp_results, directories[0] + "/code2uml_cpp")
    
    return {
        "java": java_results,
        "cpp": cpp_results
    }

def handle_file(file_path):
    """处理文件输入，按文件类型解析"""
    return parse_file_with_metadata(file_path)



def main():
    parser = argparse.ArgumentParser(description='Generate UML diagrams from source code')
    parser.add_argument('--input', help='Input file, directory', default=".", nargs="*")
    # parser.add_argument('--focus', help='Focus on a specific class name', default="")
    args = parser.parse_args()
    
    print("path:", args.input)
    
    total_lines = 0
    total_time = time.time()
    
    results = handle_multiple_inputs(args.input)
    if 'java' in results:
        if 'lines' in results['java']:
            total_lines += results['java']['lines']
    if 'cpp' in results:
        if 'lines' in results['cpp']:
            total_lines += results['cpp']['lines']

    total_time = time.time() - total_time
    # 打印统计信息
    print(f"\n=== Parsed Summary ===")
    print(f"Total Lines: {total_lines}")
    print(f"Total Time: {total_time:.2f}s")

if __name__ == "__main__":
    main()