from pathlib import Path
import pythonmonkey as pm


def validate_mermaid(mermaid_diagram: str) -> bool:
    lib_path = (Path(__file__).parent / "lib/mermaid_syntax_parser.cjs").resolve()
    print(f"{lib_path=}")
    lib = pm.require(str(lib_path))
    return lib.ValidateMermaid(mermaid_diagram)    # type: ignore[return-any]


if __name__ == "__main__":
    result = validate_mermaid("graph TD; A-->B;")
    print("Valid Graph returns -", result)  # Should print True 
    result = validate_mermaid("graph TD; A-/->B;") # Invalid graph
    print("Invalid Graph returns -", result)  # Should print False
