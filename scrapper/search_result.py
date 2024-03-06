from dataclasses import dataclass


@dataclass
class SearchResult:
    id: int
    label: str
    value: str
