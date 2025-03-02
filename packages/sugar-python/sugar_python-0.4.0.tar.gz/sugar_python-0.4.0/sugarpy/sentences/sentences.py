from sugarpy.config import SM_MODEL_NAME
from spacy.tokens.span import Span
from typing import Tuple, List
import re
import spacy
import sugarpy.claucy as claucy


class SentenceCounter:
    def __init__(self, model_name=None, nlp=None):
        if nlp is not None:
            self.nlp = nlp
        else:
            self.nlp = spacy.load(model_name or SM_MODEL_NAME)
        claucy.add_to_pipe(self.nlp)

    def is_sentence(self, s: str) -> bool:
        """
        A sentence is defined as an utterance with at least one
        verb (auxillary verbs included) and a subject.

        TODO: count imperatives
        """
        verbs = [t.pos_ == "VERB" or t.pos_ == "AUX" for t in self.nlp(s)]

        subj_types = ["nsubj", "csubj", "nsubjpass", "csubjpass"]
        subjs = [t.dep_ in subj_types for t in self.nlp(s)]
        if sum(verbs) and sum(subjs):
            return True
        return False

    def preprocess(self, s: str) -> str:
        # remove newlines and extra spaces
        s = s.replace("\n", ". ")
        s = re.sub(r"\s+", " ", s)
        s = s.replace("’", "'")
        s = s.strip()

        return s

    def count_sentences(self, s: str) -> Tuple[List[Span], int]:
        sentences = []
        total_words = 0
        for sent in self.nlp(s).sents:
            if self.is_sentence(sent.text):
                sentences.append(sent)
                total_words += len(sent.text.split(" "))
        return sentences, total_words

    def count_clauses(self, sentence: str) -> int:
        """
        Count the clauses in a sentence. Assumes that the
        input is a complete sentence (and hence there must
        be at least one clause).
        """
        doc = self.nlp(sentence)
        clauses = doc._.clauses
        return max(len(clauses), 1)

    def count(self, s: str) -> Tuple[int, int, int]:
        """
        Main counting method. Returns number of sentences,
        number of clauses, and number of words in an utterance.
        """
        s = self.preprocess(s)

        total_words = len(s.split(" "))
        sentences, words_in_sentences = self.count_sentences(s)
        total_clauses = 0
        for sent in sentences:
            total_clauses += self.count_clauses(sent.text)

        return len(sentences), total_clauses, total_words, words_in_sentences
