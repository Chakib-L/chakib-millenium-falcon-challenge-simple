import pytest
from pathlib import Path
from main import C3PO

@pytest.mark.parametrize(
    "example_folder_name",
    [
        Path("examples/example1"),
        Path("examples/example2"),
        Path("examples/example3"),
        Path("examples/example4"),
    ],
)
def test_main(example_folder_name: Path):
    milleniumFalconJsonFilePath = example_folder_name / "millennium-falcon.json"
    empireJsonFilePath = example_folder_name / "empire.json"
    resolver = C3PO(milleniumFalconJsonFilePath)
    solution = resolver.giveMeTheOdds(empireJsonFilePath)
    
    match example_folder_name.as_posix():
        case "examples/example1":
            assert solution == 0, f"Example 1 should return 0, got {solution}"
        case "examples/example2":
            assert solution == 0.81, f"Example 2 should return 0.81, got {solution}"
        case "examples/example3":
            assert solution == 0.9, f"Example 3 should return 0.9, got {solution}"
        case "examples/example4":
            assert solution == 1, f"Example 4 should return 1, got {solution}"
        case _:
            raise ValueError("Impossible value of example_folder_name")
        
    