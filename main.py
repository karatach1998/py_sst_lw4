from dataclasses import dataclass, field


@dataclass
class Node:
    leaf: bool = field(default=True)
    n: int = field(default=0)


@dataclass
class BTree:
    root: Node = field(default_factory=Node)
