import json

class DiagramConverter:
    def __init__(self, json_data):
        self.data = json.loads(json_data) if isinstance(json_data, str) else json_data
        self.pre_package = ""

    def need_plantuml_package(self, package_name):
        """
        检查是否需要 PlantUML 包。
    
        根据给定的包名，判断是否需要引入 PlantUML 包。
        如果包名的第一个部分在类数据中存在，则返回 False，
        否则返回 True。
    
        参数:
            package_name (str): 要检查的包名。
    
        返回:
            bool: 如果需要 PlantUML 包则返回 True，否则返回 False。
        """
        split_package_name = package_name.split('.')
        if len(split_package_name) >= 1:
            if self.data['classes'].get(split_package_name[-1]):
                return False
        return True

    def to_plantuml(self):
        """Convert JSON data to PlantUML class diagram format"""
        result = ["@startuml"]
        self.pre_package = ""

        # Add classes
        for class_name, class_data in self.data['classes'].items():
            package_name = class_data.get('package', '')
            if package_name != '':
                if self.need_plantuml_package(package_name):
                    if self.pre_package != package_name:
                        if self.pre_package:
                            result.append('}')
                        result.append(f'package \"{package_name}\" {{')
                        self.pre_package = package_name
            result.append(f"class {class_name} {{")
            for method in class_data['methods']:
                result.append(f"  {method}")
            for field in class_data['fields']:
                result.append(f"  {field['type']} {field['name']};")
            result.append("}")
        
        if self.pre_package:
            result.append('}')

        # Add inheritance relationships
        for class_name, class_data in self.data['classes'].items():
            for base_class in class_data['bases']:
                if base_class in self.data['classes']:
                    result.append(f"{base_class} <|-- {class_name}")

        # Add relationships based on method parameters
        # for class_name, class_data in self.data['classes'].items():
        #     for field in self.data['classes'][class_name]['fields']:
        #         for class_internal_name, class_intenal_data in self.data['classes'].items():
        #             if field == class_internal_name:
        #                 result.append(f"{class_name} --> {class_internal_name}")

        result.append("@enduml")
        return "\n".join(result)

    def to_mermaid(self):
        """Convert JSON data to Mermaid class diagram format"""
        result = ["classDiagram"]

        # Add classes
        for class_name, class_data in self.data['classes'].items():
            result.append(f"class {class_name} {{")
            for method in class_data['methods']:
                result.append(f"  {method}")
            for field in class_data['fields']:
                result.append(f"  {field['type']} {field['name']};")
            result.append("}")

        # Add inheritance relationships
        for class_name, class_data in self.data['classes'].items():
            for base_class in class_data['bases']:
                if base_class in self.data['classes']:
                    result.append(f"{class_name} --|> {base_class}")

        # Add relationships based on method parameters
        # for class_name, class_data in self.data['classes'].items():
        #     for field in self.data['classes'][class_name]['fields']:
        #         for class_internal_name, class_intenal_data in self.data['classes'].items():
        #             if field == class_internal_name:
        #                 result.append(f"{class_name} --> {class_internal_name}")

        return "\n".join(result)
    
    def to_dot(self):
        """Convert JSON data to Graphviz DOT format (string only)"""
        result = [
            'digraph G {',
            '  node [shape=record, fontname="Arial", fontsize=10];'  # 统一节点样式
        ]
        self.pre_package = ""
        
        # 添加类和子图（包）
        for class_name, class_data in self.data['classes'].items():
            # 处理包结构为子图 [3,6](@ref)
            package_name = class_data.get('package', '')
            if package_name:
                subgraph_name = package_name.replace('.', '_')
                result.append(f'  subgraph {subgraph_name} {{ ')
                result.append(f'    label = "{package_name}";')
                result.append('    style=filled; color=lightgrey;')  # 子图样式
            
            # 构建类节点内容（字段+方法）
            fields = '|'.join([f'+ {field["name"]} : {field["type"]}' for field in class_data['fields']])
            methods = '|'.join([f'+ {method}' for method in class_data['methods']])
            label = f'{{ {class_name}|{fields}|{methods} }}'
            result.append(f'    {class_name} [label="{label}"];')
            
            if package_name:
                result.append('  }')  # 关闭子图
        
        # 添加继承关系 [6](@ref)
        for class_name, class_data in self.data['classes'].items():
            for base_class in class_data['bases']:
                if base_class in self.data['classes']:
                    result.append(f'  {base_class} -> {class_name} [arrowhead=empty];')  # 空心箭头表示继承
        
        result.append('}')
        return '\n'.join(result)

def save_diagrams(json_data, base_filename):
    print("jsonData:", json.dumps(json_data, indent=4))
    converter = DiagramConverter(json_data)

    # Save PlantUML
    with open(f"{base_filename}.puml", "w") as f:
        f.write(converter.to_plantuml())

    # Save Mermaid
    with open(f"{base_filename}.mmd", "w") as f:
        f.write(converter.to_mermaid())
    
    dot_source = converter.to_dot()
    with open(f"{base_filename}.dot", "w") as f:
        f.write(dot_source)


if __name__ == "__main__":
    # Example JSON data
    example_data = {
        "classes": {
            "A": {
                "methods": ["int testAdd(int x, int y)"],
                "fields": [],
                "bases": []
            },
            "B": {
                "methods": ["void useA(A a)"],
                "fields": [],
                "bases": []
            },
            "E": {
                "methods": ["int testAdd(int x, int y)"],
                "fields": [],
                "bases": ["A"]
            }
        }
    }

    save_diagrams(example_data, "example_diagram")