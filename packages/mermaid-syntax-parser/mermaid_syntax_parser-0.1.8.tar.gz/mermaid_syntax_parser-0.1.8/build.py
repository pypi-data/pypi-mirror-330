def copy_js_lib():
    import shutil
    shutil.copyfile("../dist/mermaid_syntax_parser.cjs", "src/mermaid_parser/lib/mermaid_syntax_parser.cjs")


if __name__ == "__main__":
    copy_js_lib()
