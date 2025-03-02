from pydantic import BaseModel
from typing import Dict, Any
import json


def capitalize(s: str):
    s_cap = s[0].upper() + s[1:]
    return s_cap


class ManualMorphemeRule(BaseModel):
    processed: str
    score: int


class MorphemeRules:
    def __init__(self, rules: Dict[str, ManualMorphemeRule]):
        self.rules = rules

    @classmethod
    def from_dict(self, d: Dict[str, Any]):
        rules = {}
        for k, v in d.items():
            case_sensitive = v.pop("case_sensitive", True)
            rules[k] = ManualMorphemeRule.parse_obj(v)
            if not case_sensitive:
                v["processed"] = capitalize(v["processed"])
                rules[capitalize(k)] = ManualMorphemeRule.parse_obj(v)
        return MorphemeRules(rules)

    @classmethod
    def from_db(self):
        raise NotImplementedError

    def __contains__(self, key: str):
        return key in self.rules

    def __setitem__(self, key, value):
        raise Exception("Cannot set new rules using an instance")

    def __getitem__(self, key):
        return self.rules[key.lower()]


# Manually curated exceptions. Eventually move this to a db
exceptions = {
    "many": {"processed": "many", "score": 1, "case_sensitive": False},
    "dolly": {"processed": "dolly", "score": 1, "case_sensitive": False},
    "red": {"processed": "red", "score": 1, "case_sensitive": False},
    "until": {"processed": "until", "score": 1, "case_sensitive": False},
    "has": {"processed": "has", "score": 1, "case_sensitive": False},
    "probably": {"processed": "probably", "score": 1, "case_sensitive": False},
    "keeped": {  # This can be removed once we decide how non-words should be handled
        "processed": "keeped",
        "score": 1,
        "case_sensitive": False,
    },
    "shy": {
        "processed": "shy",
        "score": 1,
        "case_sensitive": False,
    },
    "doesn't": {
        "processed": "doesn't",
        "score": 1,
        "case_sensitive": False,
    },
}

morpheme_rules = MorphemeRules.from_dict(exceptions)
