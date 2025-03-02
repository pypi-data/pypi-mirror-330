from enum import Enum


class MetricName(str, Enum):
    MLU = "mlu"
    WPS = "wps"
    CPS = "cps"
    TNW = "tnw"
