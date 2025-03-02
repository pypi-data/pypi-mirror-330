"""File utilities for the c3po package."""

import json
from pathlib import Path
from typing import List, Dict, Any, Union, Tuple, Optional


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure that a directory exists, creating it if necessary.
    
    Args:
        path: Path to the directory
        
    Returns:
        Path object for the directory
    """
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def read_text_file(file_path: Union[str, Path], encoding: str = "utf-8") -> List[str]:
    """Read a text file and return a list of lines.
    
    Args:
        file_path: Path to the text file
        encoding: Encoding of the text file
        
    Returns:
        List of lines from the file
    """
    with open(file_path, "r", encoding=encoding) as f:
        return [line.strip() for line in f]


def write_text_file(
    lines: List[str],
    file_path: Union[str, Path],
    encoding: str = "utf-8"
) -> None:
    """Write a list of lines to a text file.
    
    Args:
        lines: List of lines to write
        file_path: Path to the text file
        encoding: Encoding of the text file
    """
    # Ensure the parent directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "w", encoding=encoding) as f:
        for line in lines:
            f.write(f"{line}\n")


def read_parallel_files(
    source_file: Union[str, Path],
    target_file: Union[str, Path],
    encoding: str = "utf-8"
) -> Tuple[List[str], List[str]]:
    """Read parallel text files and return lists of lines.
    
    Args:
        source_file: Path to the source language file
        target_file: Path to the target language file
        encoding: Encoding of the text files
        
    Returns:
        Tuple of (source lines, target lines)
    """
    source_lines = read_text_file(source_file, encoding)
    target_lines = read_text_file(target_file, encoding)
    
    if len(source_lines) != len(target_lines):
        raise ValueError(
            f"Source and target files have different numbers of lines: "
            f"{len(source_lines)} vs {len(target_lines)}"
        )
    
    return source_lines, target_lines


def write_parallel_files(
    source_lines: List[str],
    target_lines: List[str],
    source_file: Union[str, Path],
    target_file: Union[str, Path],
    encoding: str = "utf-8"
) -> None:
    """Write parallel text files from lists of lines.
    
    Args:
        source_lines: List of source language lines
        target_lines: List of target language lines
        source_file: Path to the source language file
        target_file: Path to the target language file
        encoding: Encoding of the text files
    """
    if len(source_lines) != len(target_lines):
        raise ValueError(
            f"Source and target lists have different numbers of lines: "
            f"{len(source_lines)} vs {len(target_lines)}"
        )
    
    write_text_file(source_lines, source_file, encoding)
    write_text_file(target_lines, target_file, encoding)


def read_json(file_path: Union[str, Path], encoding: str = "utf-8") -> Any:
    """Read a JSON file and return the parsed data.
    
    Args:
        file_path: Path to the JSON file
        encoding: Encoding of the JSON file
        
    Returns:
        Parsed JSON data
    """
    with open(file_path, "r", encoding=encoding) as f:
        return json.load(f)


def write_json(
    data: Any,
    file_path: Union[str, Path],
    encoding: str = "utf-8",
    indent: int = 2,
    ensure_ascii: bool = False
) -> None:
    """Write data to a JSON file.
    
    Args:
        data: Data to write
        file_path: Path to the JSON file
        encoding: Encoding of the JSON file
        indent: Number of spaces for indentation
        ensure_ascii: Whether to escape non-ASCII characters
    """
    # Ensure the parent directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "w", encoding=encoding) as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)


def write_parallel_json(
    source_lines: List[str],
    target_lines: List[str],
    output_file: Union[str, Path],
    instruction: Optional[str] = None,
    encoding: str = "utf-8"
) -> None:
    """Write parallel text data to a JSON file in a format suitable for fine-tuning.
    
    Args:
        source_lines: List of source language lines
        target_lines: List of target language lines
        output_file: Path to the output JSON file
        instruction: Optional instruction to include in each example
        encoding: Encoding of the JSON file
    """
    if len(source_lines) != len(target_lines):
        raise ValueError(
            f"Source and target lists have different numbers of lines: "
            f"{len(source_lines)} vs {len(target_lines)}"
        )
    
    data = []
    for src, tgt in zip(source_lines, target_lines):
        example = {
            "instruction": instruction or "",
            "input": src,
            "target": tgt
        }
        data.append(example)
    
    write_json(data, output_file, encoding) 