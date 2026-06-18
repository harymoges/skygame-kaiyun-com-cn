from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

SAMPLE_URL = "https://www.skygame-kaiyun.com.cn"
SAMPLE_KEYWORD = "开云体育"


@dataclass
class KeywordNote:
    keyword: str
    source_url: str
    content: str
    tags: List[str]
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def short_summary(self, max_length: int = 60) -> str:
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "…"


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote]

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag.lower() in [t.lower() for t in n.tags]]

    def all_keywords(self) -> List[str]:
        return list({n.keyword for n in self.notes})

    def all_tags(self) -> List[str]:
        all_tags = []
        for n in self.notes:
            all_tags.extend(n.tags)
        return list(set(all_tags))

    def count(self) -> int:
        return len(self.notes)


def format_note_single(note: KeywordNote) -> str:
    lines = [
        f"关键字：{note.keyword}",
        f"来源：{note.source_url}",
        f"时间：{note.created_at}",
        f"标签：{', '.join(note.tags)}",
        f"内容：{note.content}",
        "---",
    ]
    return "\n".join(lines)


def format_notes_brief(notes: List[KeywordNote]) -> str:
    if not notes:
        return "（无记录）"
    result_parts = []
    for idx, note in enumerate(notes, start=1):
        line = f"{idx}. [{note.keyword}] {note.short_summary(45)}"
        result_parts.append(line)
    return "\n".join(result_parts)


def format_notes_detailed(notes: List[KeywordNote]) -> str:
    if not notes:
        return "（无记录）"
    parts = [f"共 {len(notes)} 条笔记：\n"]
    for note in notes:
        parts.append(format_note_single(note))
    return "\n".join(parts)


def build_demo_collection() -> KeywordNoteCollection:
    sample_notes = [
        KeywordNote(
            keyword=SAMPLE_KEYWORD,
            source_url=SAMPLE_URL,
            content="开云体育提供多种体育赛事在线观看与互动服务。",
            tags=["体育", "在线平台"],
        ),
        KeywordNote(
            keyword="电竞",
            source_url=SAMPLE_URL,
            content="热门电竞赛事直播与数据分析。",
            tags=["电竞", "直播"],
        ),
        KeywordNote(
            keyword="赛事",
            source_url=SAMPLE_URL,
            content="每日更新最新体育赛事时间安排。",
            tags=["赛事", "日程"],
        ),
    ]
    return KeywordNoteCollection(notes=sample_notes)


def main():
    collection = build_demo_collection()
    print("=== 简要输出 ===")
    print(format_notes_brief(collection.notes))
    print("\n=== 详细输出（第一条） ===")
    print(format_note_single(collection.notes[0]))
    print("\n=== 按关键字过滤（开云体育） ===")
    filtered = collection.filter_by_keyword(SAMPLE_KEYWORD)
    print(format_notes_detailed(filtered))
    print("\n=== 全部标签 ===")
    print(collection.all_tags())
    print("\n=== 全部关键字 ===")
    print(collection.all_keywords())


if __name__ == "__main__":
    main()