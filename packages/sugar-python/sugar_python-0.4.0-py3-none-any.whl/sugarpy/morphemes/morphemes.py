from sugarpy.config import SM_MODEL_NAME
from sugarpy.morphemes.utils import match_case, find_LCS
from sugarpy.morphemes.rules import morpheme_rules
from spacy.tokens.token import Token
from nltk.corpus import words
from typing import Tuple, List, Union
from pydantic import BaseModel
import spacy
import nltk
import inspect
import re


class WordWithPrefix(BaseModel):
    base: str
    prefix: str

    def join(self):
        return self.prefix + " " + self.base


class WordWithSuffix(BaseModel):
    base: str
    suffix: str

    def join(self):
        return self.base + " " + self.suffix


class MorphologyCounter:
    marker_start = "<mark>"
    marker_end = "</mark>"

    def __init__(self, model_name=None):
        self.nlp = spacy.load(model_name or SM_MODEL_NAME)
        nltk.download("words")
        self.words = set(words.words())

    def endswith(suffix):
        """
        TODO: document
        """

        def decorator(method):
            def wrapper(cls, token):
                b = method(cls, token) and token.text.lower().endswith(suffix)
                split = None
                if b:
                    baseword = token.text[: -len(suffix)]
                    suff = match_case(suffix, token.text[-len(suffix) :])
                    split = WordWithSuffix(base=baseword, suffix=suff)
                return b, split

            return wrapper

        return decorator

    def startswith(prefix):
        """
        TODO: document
        """

        def decorator(method):
            def wrapper(cls, token):
                b = method(cls, token) and token.text.lower().startswith(prefix)
                split = None
                if b:
                    baseword = token.text[len(prefix) :]
                    pref = match_case(prefix, token.text[: len(prefix)])
                    split = WordWithPrefix(base=baseword, prefix=pref)
                return b, split

            return wrapper

        return decorator

    def count(self, s: str, debug: bool = False) -> list:
        """
        Main counting method.
        """
        s = self.preprocess(s)
        num_words = len(s.split(" "))

        # Build lookup table for string index to token
        token_locator = {}
        for token in self.nlp(s):
            for i in range(token.idx, token.idx + len(token.text)):
                token_locator[i] = token

        # Iterate through whitespace words, collecting tokens for each word
        # Count morphemes on each word and space out the word as well.
        s_processed = ""
        morpheme_count = 0

        str_idx = 0
        while str_idx < len(s):
            lookup = 0
            current_tokens = []
            while str_idx + lookup < len(s) and s[str_idx + lookup] != " ":
                t = token_locator[str_idx + lookup]
                if t not in current_tokens:
                    current_tokens.append(t)
                lookup += 1

            full_word = s[str_idx : str_idx + lookup]
            if full_word.strip() in morpheme_rules:
                # Handle execeptional/manual cases
                processed_word = " " + morpheme_rules[full_word.strip()].processed
                morphemes_in_word = morpheme_rules[full_word.strip()].score
            else:
                processed_word, morphemes_in_word = self.count_tokens(current_tokens)

            s_processed += processed_word
            morpheme_count += morphemes_in_word

            str_idx += lookup + 1

        s_processed = s_processed.strip()

        return s_processed, morpheme_count, num_words

    def count_tokens(self, tokens: List[Token]) -> Tuple[str, int]:
        """
        Get the processed string and morpheme count from a list of tokens
        associated to the same whitespace delimited word.
        """

        total_score = 0
        s_added = ""
        for token in tokens:
            count, spaced = self.count_on_token(token)
            total_score += count
            if count:
                s_added += " "
            s_added += spaced

        if total_score > 1:
            s_processed = " " + self.marker_start + s_added.strip() + self.marker_end
        else:
            s_processed = s_added

        return s_processed, total_score

    def preprocess(self, s: str) -> str:
        """
        Preprocess the string.
        """

        # remove newlines and extra spaces
        s = s.replace("\n", ". ")
        s = re.sub(r"\s+", " ", s)
        s = s.replace("’", "'")

        # remove hyphens in ritualized reduplications
        words = []
        for word in s.split(" "):
            if "-" in word and len(set(word.lower().split("-"))) == 1:
                words += [word.replace("-", "")]
            else:
                words += [word]
        s = " ".join(words)
        s = s.strip()

        return s

    def count_on_token(self, token: Token, debug: bool = False) -> Tuple[int, str]:
        """
        Count morphemes present in a single token. Also return the
        token text with spaces inserted between distinct morphemes.
        """

        # Tokens that don't independently count as a morpheme
        skip_tokens = ["'", "-", "’", "."]

        if token.text in skip_tokens or token.is_punct:
            return 0, token.text

        count = 1
        morph_identifying_methods = [
            m
            for m in inspect.getmembers(self, predicate=inspect.ismethod)
            if m[0].startswith("_count")
        ]

        splits = []
        for method, _ in morph_identifying_methods:
            val, split = getattr(self, method)(token)
            if split is not None:
                splits.append(split)

            if val and debug:
                print(token.text, method)
            count += val

        if splits:
            token_str = self.join_splits(splits)
        else:
            token_str = token.text
        return count, token_str

    def join_splits(self, splits: List[Union[WordWithPrefix, WordWithSuffix]]) -> str:
        """
        Not convinced this is the best way.
        """
        if len(splits) == 1:
            return splits[0].join()
        elif len(splits) > 1:
            suff = [s for s in splits if isinstance(s, WordWithSuffix)]
            pref = [s for s in splits if isinstance(s, WordWithPrefix)]
            if len(suff) != 1 or len(pref) != 1:
                raise ValueError(
                    "Can only join a single WordWithSuffix and a single WordWithPrefix."
                )

            middle = find_LCS(suff[0].base, pref[0].base)
            return pref[0].prefix + " " + middle + " " + suff[0].suffix

    def is_word(self, word: str) -> bool:
        return word in self.words

    @endswith("s")
    def _count_plural_noun(self, token: Token) -> int:
        return token.tag_ == "NNS"

    @endswith("s")
    def _count_third_person_singular_present_tense_verb(self, token: Token) -> int:
        return token.tag_ == "VBZ" and len(token.text) > 2

    @endswith("ed")
    def _count_regular_past_tense_verb(self, token: Token) -> int:
        return token.tag_ == "VBD"

    @endswith("ing")
    def _count_present_progressive_verb(self, token: Token) -> int:
        return token.tag_ == "VBG"

    """
    def _count_proper_noun(self, token: Token) -> Tuple[int, None]:
        return token.pos_ == "PROPN" and token.text[0].isupper(), None
    """

    @endswith("ed")
    def _count_endswith_ed_adj(self, token: Token) -> int:
        return token.pos_ == "ADJ"

    @endswith("er")
    def _count_endswith_er_comp(self, token: Token) -> int:
        return token.tag_ == "JJR"

    @endswith("y")
    def _count_endswith_y_adj_adv(self, token: Token) -> int:
        """
        Not perfect. For example 'many` satisfies all conditions
        but should not get an extra morpheme.
        """
        base_word = re.sub("y$", "", token.text.lower())
        return (token.pos_ == "ADJ" or token.pos_ == "ADV") and self.is_word(base_word)

    @endswith("est")
    def _count_endswith_est_sup(self, token: Token) -> int:
        return token.tag_ == "JJS"

    @endswith("tion")
    def _count_endswith_tion(self, token: Token) -> int:
        return True

    @endswith("sion")
    def _count_endswith_sion(self, token: Token) -> int:
        return True

    @endswith("ment")
    def _count_endswith_ment(self, token: Token) -> int:
        """
        Not perfect, for example "parchment" satisfies all conditions
        but should not get an extra morpheme.
        """
        base_word = re.sub("ment$", "", token.text.lower())
        return len(token.text) >= 6 and self.is_word(base_word)

    @endswith("ful")
    def _count_endswith_ful(self, token: Token) -> int:
        """
        No short words (<6) count.
        """
        return len(token.text) >= 6

    @endswith("ish")
    def _count_endswith_ish(self, token: Token) -> int:
        """
        Not perfect, for example "garish", "radish" satisfy all conditions
        but should not get an extra morpheme.
        """
        base_word = re.sub("ish$", "", token.text.lower())
        return len(token.text) >= 6 and self.is_word(base_word)

    @startswith("dis")
    def _count_startswith_dis(self, token: Token) -> int:
        """
        Not perfect, for example "disease" satisfies all conditions
        but should not get an extra morpheme.
        """
        base_word = re.sub("^dis", "", token.text.lower())
        return len(token.text) >= 7 and self.is_word(base_word)

    @startswith("re")
    def _count_startswith_re(self, token: Token) -> int:
        """
        Not perfect, for example "regal" satisfies all conditions
        but should not get an extra morpheme.
        """
        base_word = re.sub("^re", "", token.text.lower())
        return len(token.text) >= 5 and self.is_word(base_word)

    @startswith("un")
    def _count_startswith_re(self, token: Token) -> int:
        base_word = re.sub("^un", "", token.text.lower())
        return len(token.text) >= 5 and self.is_word(base_word)
