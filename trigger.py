import re
from collections import defaultdict
import copy

import pygtrie
import zhconv

from log import _log

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from service import ServiceFunc


class BaseTrigger:
    def add(self, x, sf: "ServiceFunc"):
        raise NotImplementedError

    def find_handler(self, message) -> list["ServiceFunc"]:
        raise NotImplementedError


class PrefixTrigger(BaseTrigger):
    def __init__(self):
        super().__init__()
        self.trie = pygtrie.CharTrie()

    def add(self, prefix: str, sf: "ServiceFunc"):
        prefix_cht = zhconv.convert(prefix, "zh-hant")
        if prefix in self.trie:
            self.trie[prefix].append(sf)
            if prefix_cht != prefix:
                self.trie[prefix_cht].append(sf)
            _log.warning(f"Prefix trigger `{prefix}` added multiple handlers: {sf.__name__}@{sf.sv.name}")
        else:
            self.trie[prefix] = [sf]
            if prefix_cht != prefix:
                self.trie[prefix_cht] = [sf]
            _log.debug(f"Succeed to add prefix trigger `{prefix}`")

    def find_handler(self, message) -> list["ServiceFunc"]:
        content = message.content
        if content == "":
            return
        content = content.lstrip()
        item = self.trie.longest_prefix(content)
        if not item:
            return

        old_msg = copy.deepcopy(content)
        message.content = content[len(item.key):].lstrip()

        for sf in item.value:
            yield sf

        message.content = old_msg


class SuffixTrigger(BaseTrigger):
    def __init__(self):
        super().__init__()
        self.trie = pygtrie.CharTrie()

    def add(self, suffix: str, sf: "ServiceFunc"):
        suffix_r = suffix[::-1]
        suffix_r_cht = zhconv.convert(suffix_r, "zh-hant")
        if suffix_r in self.trie:
            self.trie[suffix_r].append(sf)
            if suffix_r_cht != suffix_r:
                self.trie[suffix_r_cht].append(sf)
            _log.warning(f"Suffix trigger `{suffix}` added multi handler: `{sf.__name__}`")
        else:
            self.trie[suffix_r] = [sf]
            if suffix_r_cht != suffix_r:
                self.trie[suffix_r_cht] = [sf]
            _log.debug(f"Succeed to add suffix trigger `{suffix}`")

    def find_handler(self, message) -> list["ServiceFunc"]:
        content = message.content
        if content == "":
            return
        content = content.rstrip()
        item = self.trie.longest_prefix(content[::-1])
        if not item:
            return

        old_msg = copy.deepcopy(content)
        message.content = content[: -len(item.key)].rstrip()

        for sf in item.value:
            yield sf

        message.content = old_msg


class KeywordTrigger(BaseTrigger):
    def __init__(self):
        super().__init__()
        self.allkw = {}

    def add(self, keyword: str, sf: "ServiceFunc"):
        if sf.normalize_text:
            keyword = keyword.lower().replace(" ", "")
        if keyword in self.allkw:
            self.allkw[keyword].append(sf)
            _log.warning(f"Keyword trigger `{keyword}` added multi handler: `{sf.__name__}`")
        else:
            self.allkw[keyword] = [sf]
            _log.debug(f"Succeed to add keyword trigger `{keyword}`")

    def find_handler(self, message) -> list["ServiceFunc"]:
        for kw, sfs in self.allkw.items():
            for sf in sfs:
                text = message.content.lower().replace(" ", "") if sf.normalize_text else message.content
                if kw in text:
                    yield sf


class RexTrigger(BaseTrigger):
    def __init__(self):
        super().__init__()
        self.allrex = defaultdict(list)

    def add(self, rex_pattern: re.Pattern, sf: "ServiceFunc"):
        rex = re.compile(rex_pattern)
        self.allrex[rex].append(sf)
        _log.debug(f"Succeed to add rex trigger `{rex.pattern}`")

    def find_handler(self, message) -> "ServiceFunc":
        for rex, sfs in self.allrex.items():
            for sf in sfs:
                text = message.content.lower().replace(" ", "") if sf.normalize_text else message.content
                match = rex.search(text)
                if match:
                    yield sf


class _PlainTextExtractor(BaseTrigger):
    def find_handler(self, message):
        message.content = message.content.strip()
        return []


class _TextNormalizer(_PlainTextExtractor):
    def find_handler(self, message):
        super().find_handler(message)
        message.content = message.content.lower().replace(" ", "")
        return []


prefix = PrefixTrigger()
suffix = SuffixTrigger()
keyword = KeywordTrigger()
rex = RexTrigger()

chain: list[BaseTrigger] = [
    prefix,
    suffix,
    _TextNormalizer(),
    rex,
    keyword,
]
