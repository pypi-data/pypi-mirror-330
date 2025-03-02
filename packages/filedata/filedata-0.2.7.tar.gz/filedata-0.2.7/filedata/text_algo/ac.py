import weakref
from typing import Dict, Collection, Tuple, List

from pydantic import BaseModel


class ACNode:
    def __init__(self, ch: str = None, is_root: bool = False):
        self.ch = ch
        self.is_root = is_root

        self.next: Dict[str, ACNode] = {}
        self.fail = None
        self.parent = None
        self.words = []

    def keys(self):
        return self.next.keys()

    def __contains__(self, item):
        return item in self.next

    def __getitem__(self, item):
        return self.next[item]

    def __setitem__(self, key, value):
        self.next[key] = value
        value.parent = weakref.ref(self)

    def add_word(self, word: str):
        self.words.append(word)


class MatchResult(BaseModel):
    word: str
    position: Tuple[int, int]


class ACAutomaton:
    def __init__(self, words: Collection[str]):
        _word_set = set(words)
        self.words = [i for i in _word_set if i]
        self._root = ACNode(is_root=True)
        self._all_nodes = [(0, self._root)]

        for w in self.words:
            self._add_word(w)
        self._build()

    def _add_word(self, word: str):
        current_node: ACNode = self._root
        for i, ch in enumerate(word):
            if ch not in current_node:
                node = ACNode(ch=ch)
                self._all_nodes.append((i + 1, node))
                current_node[ch] = node
            current_node = current_node[ch]
        current_node.add_word(word)

    def _build(self):
        self._all_nodes.sort(key=lambda x: x[0])
        for level, node in self._all_nodes:
            if level <= 1:
                node.fail = weakref.ref(self._root)
            else:
                p: ACNode = node.parent().fail()
                while True:
                    if node.ch in p:
                        node.fail = weakref.ref(p[node.ch])
                        node.words.extend(node.fail().words)
                        break
                    else:
                        if p.is_root:
                            node.fail = weakref.ref(self._root)
                            break
                        p = p.fail()

    def find_all(self, content: str, from_start: bool = False):
        result: List[MatchResult] = []
        if not content:
            return result

        current_node: ACNode = self._root
        for i, ch in enumerate(content):
            while True:
                if ch not in current_node:
                    if from_start:
                        result.sort(key=lambda x: x.position)
                        return result

                    if current_node.is_root:
                        break
                    current_node = current_node.fail()
                else:
                    current_node = current_node[ch]
                    for w in current_node.words:
                        idx = i - len(w) + 1
                        if from_start and idx != 0:
                            continue

                        result.append(
                            MatchResult(
                                word=w,
                                position=(idx, i + 1)
                            )
                        )
                    break
        result.sort(key=lambda x: x.position)
        return result

    def find_all_from_segments(self, segments: List[str]):
        result: List[MatchResult] = []
        if not segments:
            return result

        current_node: ACNode = self._root
        for i, seg in enumerate(segments):
            for ch in seg:
                while True:
                    if ch not in current_node:
                        if current_node.is_root:
                            break
                        current_node = current_node.fail()
                    else:
                        current_node = current_node[ch]
                        break
            if not current_node.is_root:
                for w in current_node.words:
                    n = len(w)
                    k = i
                    while k >= 0:
                        n -= len(segments[k])
                        if n == 0:
                            result.append(
                                MatchResult(
                                    word=w,
                                    position=(k, i + 1),
                                )
                            )
                            break
                        if n < 0:
                            break
                        k -= 1
        return result
