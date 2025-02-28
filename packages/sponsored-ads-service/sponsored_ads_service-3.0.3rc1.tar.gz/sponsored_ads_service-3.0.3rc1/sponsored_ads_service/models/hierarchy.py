from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    id: int
    name: str
    department_id: int
    slug: str
    parent_id: int | None = None


@dataclass(frozen=True)
class Department:
    id: int
    name: str
    slug: str


Node = Department | Category
