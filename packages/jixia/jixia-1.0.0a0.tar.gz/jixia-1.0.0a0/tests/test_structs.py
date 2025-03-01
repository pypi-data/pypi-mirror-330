from jixia.structs import Declaration


def test_declaration():
    declarations = Declaration.from_json_file("/Users/mac1/work/jixia-stuff/jixia_py/tests/Example.decl.json")
    print(declarations)
