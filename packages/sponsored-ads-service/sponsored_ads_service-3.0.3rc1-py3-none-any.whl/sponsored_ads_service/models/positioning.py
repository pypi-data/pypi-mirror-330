from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Breakpoints:
    sm: list[int] = field(default_factory=list)
    medium: list[int] = field(default_factory=list)


@dataclass
class Positions:
    apps: Breakpoints = field(default_factory=Breakpoints)
    web: Breakpoints = field(default_factory=Breakpoints)

    @classmethod
    def create_basic(cls, positions: list[int]) -> Positions:
        return cls(
            web=Breakpoints(sm=positions, medium=positions),
            apps=Breakpoints(sm=positions, medium=positions),
        )
