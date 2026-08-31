#!/usr/bin/env python3

"""将 SRT 字幕机械清洗为原始纯文字稿。

语义分段和字幕纠错由调用本 skill 的 AI 在此脚本之后完成。
"""

import argparse
import html
import re
from pathlib import Path


INDEX_RE = re.compile(r"^\s*\d+\s*$")
TIMESTAMP_RE = re.compile(
    r"^\s*\d{1,2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*"
    r"\d{1,2}:\d{2}:\d{2}[,.]\d{3}(?:\s+.*)?$"
)
TAG_RE = re.compile(r"<[^>]+>")
ASS_STYLE_RE = re.compile(r"\{\\[^}]*\}")
CJK_RE = re.compile(r"[\u3400-\u9fff]")


def read_text(path: Path) -> str:
    """按常见字幕编码读取文件。"""
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"无法识别文件编码：{path}")


def clean_line(line: str) -> str:
    """删除字幕标记并规范行首尾空白。"""
    line = html.unescape(line)
    line = TAG_RE.sub("", line)
    line = ASS_STYLE_RE.sub("", line)
    line = re.sub(r"[ \t]+", " ", line)
    return line.strip()


def join_multiline_text(lines: list[str]) -> str:
    """合并同一字幕块中的多行，避免中文行之间出现多余空格。"""
    result = ""

    for raw_line in lines:
        line = clean_line(raw_line)
        if not line:
            continue

        if not result:
            result = line
            continue

        left = result[-1]
        right = line[0]

        if CJK_RE.match(left) and CJK_RE.match(right):
            separator = ""
        elif right in "，。！？；：、）》）】」』,.!?;:)]}":
            separator = ""
        else:
            separator = " "

        result += separator + line

    return result


def convert_srt(source: Path, target: Path) -> None:
    """将 SRT 转换为每条字幕一行的原始文字稿。"""
    content = read_text(source).replace("\r\n", "\n").replace("\r", "\n")
    blocks = re.split(r"\n\s*\n", content)
    transcript: list[str] = []

    for block in blocks:
        lines = block.split("\n")

        if lines and lines[0].strip().upper() == "WEBVTT":
            lines = lines[1:]

        if lines and INDEX_RE.fullmatch(lines[0]):
            lines = lines[1:]

        lines = [
            line for line in lines
            if not TIMESTAMP_RE.fullmatch(line.strip())
        ]

        text = join_multiline_text(lines)
        if text:
            transcript.append(text)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "\n".join(transcript) + ("\n" if transcript else ""),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="将 SRT 字幕转换为原始 TXT 文字稿")
    parser.add_argument("source", type=Path, help="输入 SRT 文件")
    parser.add_argument("-o", "--output", type=Path, help="输出 TXT 文件")
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"输入文件不存在：{args.source}")

    target = args.output or args.source.with_suffix(".txt")
    convert_srt(args.source, target)
    print(f"已生成：{target}")


if __name__ == "__main__":
    main()
