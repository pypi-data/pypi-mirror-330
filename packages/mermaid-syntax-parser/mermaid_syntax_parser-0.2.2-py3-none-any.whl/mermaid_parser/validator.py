import multiprocessing
from multiprocessing import Pipe, Process
from pathlib import Path
from typing import Any

multiprocessing.set_start_method("spawn", force=True)


def _validate_mermaid(mermaid_diagram: str, conn: Any) -> None:
    try:
        import pythonmonkey as pm

        lib_path = (Path(__file__).parent / "lib/mermaid_syntax_parser.cjs").resolve()
        lib = pm.require(str(lib_path))
        result: bool = lib.ValidateMermaid(mermaid_diagram)
        conn.send(result)
    except Exception as e:
        print("Error in validating mermaid diagram", str(e))
        conn.send(False)
    finally:
        conn.close()


# pythonmonkey does not work in multitheaded environments, so we use multiprocessing to wrap the function
def validate_mermaid(mermaid_diagram: str) -> bool:
    parent_conn, child_conn = Pipe()
    process = Process(target=_validate_mermaid, args=(mermaid_diagram, child_conn))
    process.start()
    process.join()

    result = parent_conn.recv()
    if isinstance(result, Exception):
        raise result
    return result  # type: ignore[no-any-return]


if __name__ == "__main__":
    result = validate_mermaid("graph TD; A-->B;")
    print("Valid Graph returns -", result)  # Should print True
    result = validate_mermaid("graph TD; A-/->B;")  # Invalid graph
    print("Invalid Graph returns -", result)  # Should print False
