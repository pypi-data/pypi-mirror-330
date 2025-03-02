import pylcs


def match_case(s: str, ref: str):
    """
    Change case of each character of s to match
    the case of the corresponding characeter of ref.
    """

    matched = ""
    for c, cr in zip(s, ref):
        if cr.isupper():
            matched += c.upper()
        else:
            matched += c.lower()

    return matched


def find_LCS(s1: str, s2: str):
    res = pylcs.lcs_string_idx(s1, s2)
    return "".join([s2[i] for i in res if i != -1])
