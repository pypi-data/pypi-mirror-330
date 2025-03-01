from diagram_converter import DiagramConverter, save_diagrams

example_data = {
    "classes": {
        "A": {
            "methods": [
                "int testAdd(intx,inty)",
                "int testDiv(intx,inty)",
                "int testMul(intx,inty)",
                "int testSub(intx,inty)"
            ],
            "fields": [],
            "bases": []
        },
        "B": {
            "methods": [
                "int testAdd(intx,inty)",
                "int testDiv(intx,inty)",
                "int testMul(intx,inty)",
                "int testSub(intx,inty)"
            ],
            "fields": [],
            "bases": []
        },
        "C": {
            "methods": [
                "T testAdd(Tx,Ty)",
                "T testDiv(Tx,Ty)",
                "T testMul(Tx,Ty)",
                "T testSub(Tx,Ty)"
            ],
            "fields": [],
            "bases": []
        },
        "E": {
            "methods": [
                "int testAdd(intx,inty)",
                "int testSub(intx,inty)",
                "int testMul(intx,inty)",
                "int testDiv(intx,inty)"
            ],
            "fields": [],
            "bases": [
                "A"
            ]
        },
        "D": {
            "methods": [
                "void addA(Aa)",
                "void addB(Bb)",
                "void addC(C<int>c)"
            ],
            "fields": [],
            "bases": []
        }
    }
}

# Create converter instance
converter = DiagramConverter(example_data)

# Print both diagram formats
print("PlantUML:")
print(converter.to_plantuml())

print("\nMermaid:")
print(converter.to_mermaid())

# Save diagrams to files
save_diagrams(example_data, "example_diagram")
