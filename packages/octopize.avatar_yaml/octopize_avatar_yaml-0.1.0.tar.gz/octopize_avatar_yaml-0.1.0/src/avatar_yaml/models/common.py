from dataclasses import dataclass
from enum import StrEnum


@dataclass
class Metadata:
    name: str


class ModelKind(StrEnum):
    VOLUME = "AvatarVolume"
    SCHEMA = "AvatarSchema"
    PARAMETERS = "AvatarParameters"
    PRIVACY_METRICS = "AvatarPrivacyMetricsParameters"
    SIGNAL_METRICS = "AvatarSignalMetricsParameters"
    REPORT = "AvatarReportParameters"
    ADVICE = "AvatarAdviceParameters"
