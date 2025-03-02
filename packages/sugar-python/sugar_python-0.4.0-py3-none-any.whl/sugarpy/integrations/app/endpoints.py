from sugarpy import get_metrics, get_norms
import matplotlib.pyplot as plt
import math
import numpy as np
import tempfile
import os


def html_mlu_response(input_str: str):
    scores = get_metrics(input_str.split("\n"))
    morph_lines = scores.morpheme_split_sample
    morph_lines = morph_lines.replace("\n", "<br>")
    mlu_score = round(scores.mlu, 2)
    # todo: make this a template
    resp = f"""<center><b><p style="font-size:20px">Total utterances: {scores.utterances}, morphemes: {scores.morphemes}, MLU: {mlu_score}</p></b></center><br>"""
    resp += "<p>" + morph_lines + "</p>"

    return resp


def create_labels(ticks):
    strs = ["\u03bc-2\u03c3", "\u03bc-\u03c3", "\u03bc"]
    return [str(round(t, 2)) + f"\n({g})" for t, g in zip(ticks, strs)]


def draw_bellcurves(scores, age_y, age_m):
    plt.clf()

    figure, axis = plt.subplots(4, 1, figsize=(8, 12.8))
    norms = get_norms(age_y, age_m, "tnw")
    mean, sd = norms["mean_score"], norms["sd"]

    x = np.linspace(mean - 4 * sd, mean + 4 * sd, 200)
    y = 1 / (sd * math.sqrt(2 * math.pi)) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
    score = scores.tnw
    title = f"TNW: {scores.tnw}"
    axis[0].fill_between(x, y, color="b", alpha=0.2)
    axis[0].tick_params(left=False, labelleft=False)
    ticks = [mean - 2 * sd, mean - sd, mean]
    axis[0].set_xticks(ticks, labels=create_labels(ticks))
    axis[0].axvline(x=score, color="r", label=str(score))
    axis[0].title.set_text(title)
    [s.set_visible(False) for s in axis[0].spines.values()]

    norms = get_norms(age_y, age_m, "mlu")
    mean, sd = norms["mean_score"], norms["sd"]
    x = np.linspace(mean - 4 * sd, mean + 4 * sd, 200)
    y = 1 / (sd * math.sqrt(2 * math.pi)) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
    score = round(scores.mlu, 2)
    title = f"MLU: {score}"
    axis[1].fill_between(x, y, color="b", alpha=0.2)
    axis[1].tick_params(left=False, labelleft=False)
    ticks = [mean - 2 * sd, mean - sd, mean]
    axis[1].set_xticks(ticks, labels=create_labels(ticks))
    axis[1].axvline(x=score, color="r", label=str(score))
    axis[1].title.set_text(title)
    [s.set_visible(False) for s in axis[1].spines.values()]

    if scores.wps != np.inf:
        norms = get_norms(age_y, age_m, "wps")
        mean, sd = norms["mean_score"], norms["sd"]
        x = np.linspace(mean - 4 * sd, mean + 4 * sd, 200)
        y = 1 / (sd * math.sqrt(2 * math.pi)) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
        score = round(scores.wps, 2)
        title = f"WPS: {score}"
        axis[2].fill_between(x, y, color="b", alpha=0.2)
        axis[2].tick_params(left=False, labelleft=False)
        ticks = [mean - 2 * sd, mean - sd, mean]
        axis[2].set_xticks(ticks, labels=create_labels(ticks))
        axis[2].axvline(x=score, color="r", label=str(score))
        axis[2].title.set_text(title)
        [s.set_visible(False) for s in axis[2].spines.values()]
    else:
        figure.delaxes(axis[2])

    if scores.cps != np.inf:
        norms = get_norms(age_y, age_m, "cps")
        mean, sd = norms["mean_score"], norms["sd"]
        x = np.linspace(mean - 4 * sd, mean + 4 * sd, 200)
        y = 1 / (sd * math.sqrt(2 * math.pi)) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
        score = round(scores.cps, 2)
        title = f"CPS: {score}"
        axis[3].fill_between(x, y, color="b", alpha=0.2)
        axis[3].tick_params(left=False, labelleft=False)
        ticks = [mean - 2 * sd, mean - sd, mean]
        axis[3].set_xticks(ticks, labels=create_labels(ticks))
        axis[3].axvline(x=score, color="r", label=str(score))
        axis[3].title.set_text(title)
        [s.set_visible(False) for s in axis[3].spines.values()]
    else:
        figure.delaxes(axis[3])

    figure.subplots_adjust(hspace=1)
    plt.savefig("curves.svg", bbox_inches="tight")
    svg_str = open("curves.svg", "r").read()
    os.remove("curves.svg")

    return svg_str


def metrics_table(scores, age_y, age_m, num_sd_criteria=2):
    table = "<table><thead><tr>"
    for r in ["Metric", "Raw Score", "Mean", "Meets criteria"]:
        table += f"<th>{r}</th>"
    table += "</tr></thead><tbody>"

    metrics = [
        ("tnw", "Total number of words (TNW)"),
        ("mlu", "Mean length of utterance (MLU)"),
        ("wps", "Words per sentence (WPS)"),
        ("cps", "Clauses per sentence (CPS)"),
    ]
    for metric, name in metrics:
        norms = get_norms(age_y, age_m, metric)
        mean, sd = norms["mean_score"], norms["sd"]
        meets_criteria = "Yes" if score > mean - num_sd_criteria * sd else "No"
        if score == np.inf:
            meets_criteria = "N/A"
        raw = round(score, 2)
        if raw == np.inf:
            raw = "N/A"
        table += f"<tr><td>{name}</td><td>{raw}</td><td>{mean}</td><td>{meets_criteria}</td></tr>"

    table += "</tbody></table>"
    return table


def html_metrics_response(input_str: str, age_y: int, age_m: int):
    scores = get_metrics(input_str.split("\n"))
    curves_svg = draw_bellcurves(scores, age_y, age_m)

    rval = '<div style="text-align: center"> '
    rval += "<br>" + metrics_table(scores, age_y, age_m) + "<br>"
    rval += curves_svg
    if scores.sentences == 0:
        rval += "<p><i><b>Note:</b></i> There were no complete sentences detected, so Words per sentence (WPS) and Clauses per sentence (CPS) could not be calculated</p>"
    rval += "</div>"

    return rval
