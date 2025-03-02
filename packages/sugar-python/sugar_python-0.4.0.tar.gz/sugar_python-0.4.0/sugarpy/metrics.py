from sugarpy import MorphologyCounter
from sugarpy import SentenceCounter
from sugarpy.norms import norms
from sugarpy.config import DEFAULT_MODEL
from pydantic import BaseModel
from typing import List
import numpy as np
import json


class SugarMetrics(BaseModel):
    sample: str
    morpheme_split_sample: str
    utterances: int
    morphemes: int
    words: int
    words_in_sentences: int
    sentences: int
    clauses: int

    @property
    def mlu(self):
        if self.utterances:
            return self.morphemes / self.utterances
        else:
            return np.inf

    @property
    def tnw(self):
        return self.words

    @property
    def wps(self):
        if self.sentences:
            return self.words_in_sentences / self.sentences
        else:
            return np.inf

    @property
    def cps(self):
        if self.sentences:
            return self.clauses / self.sentences
        else:
            return np.inf


def consolidate_metrics(metrics: List[SugarMetrics]):
    total = SugarMetrics(
        sample="\n".join(m.sample for m in metrics),
        morpheme_split_sample="\n".join(m.morpheme_split_sample for m in metrics),
        utterances=sum([m.utterances for m in metrics]),
        morphemes=sum([m.morphemes for m in metrics]),
        words=sum([m.words for m in metrics]),
        words_in_sentences=sum([m.words_in_sentences for m in metrics]),
        sentences=sum([m.sentences for m in metrics]),
        clauses=sum([m.clauses for m in metrics]),
    )
    return total


def get_metrics(input_samples: List[str], consolidate=True):
    """
    Main metrics function.
    """
    cm = MorphologyCounter(model_name=DEFAULT_MODEL)
    cs = SentenceCounter(nlp=cm.nlp)
    computed_metrics = []

    for utterance in input_samples:
        if utterance.strip():
            morph_line, num_morph, num_words = cm.count(utterance.strip())
            num_sent, num_clauses, num_words, words_in_sentences = cs.count(
                utterance.strip()
            )

            m = SugarMetrics(
                sample=utterance.strip(),
                morpheme_split_sample=morph_line,
                utterances=1,
                morphemes=num_morph,
                words=num_words,
                sentences=num_sent,
                words_in_sentences=words_in_sentences,
                clauses=num_clauses,
            )
            computed_metrics.append(m)

    if consolidate:
        return consolidate_metrics(computed_metrics)
    return computed_metrics
