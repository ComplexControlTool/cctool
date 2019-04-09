from enum import Enum


class classproperty(object):
    def __init__(self, getter):
        self.getter= getter
    def __get__(self, instance, owner):
        return self.getter(owner)


class CustomEnum(Enum):
    @classproperty
    def __values__(cls):
        return [m.value for m in cls]


# Analysis
class AnalysisOption(CustomEnum):
    CONTROLLABILITY_ANALYSIS = 'Controllability'
    UP_STREAM_ANALYSIS = 'Up stream'
    DOWN_STREAM_ANALYSIS = 'Down stream'
    SUBJECTIVE_LOGIC_ANALYSIS = 'Subjective logic'
    XCS_ANALYSIS = 'XCS classifier'


class AnalysisShortcode(CustomEnum):
    CONTROLLABILITY_ANALYSIS = 'CA'
    UP_STREAM_ANALYSIS = 'USA'
    DOWN_STREAM_ANALYSIS = 'DSA'
    SUBJECTIVE_LOGIC_ANALYSIS = 'SLA'
    XCS_ANALYSIS = 'XCS'


class AnalysisDescription(CustomEnum):
    CONTROLLABILITY_ANALYSIS = 'Description here for Controllability Analysis'
    UP_STREAM_ANALYSIS = 'Description here for Controllability Analysis'
    DOWN_STREAM_ANALYSIS = 'Description here for Controllability Analysis'
    SUBJECTIVE_LOGIC_ANALYSIS = 'Description here for Controllability Analysis'
    XCS_ANALYSIS = 'Description here for Controllability Analysis'


# Function
class FunctionOption(CustomEnum):
    LINEAR_FUNCTION = 'Linear'


class FunctionShortcode(CustomEnum):
    LINEAR_FUNCTION = 'L'


# Controllability
class ControllabilityOption(CustomEnum):
    NEUTRAL_CONTROLLABILITY = 'Neutral'
    EASY_CONTROLLABILITY = 'Easy'
    MEDIUM_CONTROLLABILITY = 'Medium'
    HARD_CONTROLLABILITY = 'Hard'


class ControllabilityShortcode(CustomEnum):
    NEUTRAL_CONTROLLABILITY = 'N'
    EASY_CONTROLLABILITY = 'E'
    MEDIUM_CONTROLLABILITY = 'M'
    HARD_CONTROLLABILITY = 'H'


class ControllabilityWeight(CustomEnum):
    NEUTRAL_CONTROLLABILITY = 0
    EASY_CONTROLLABILITY = 1
    MEDIUM_CONTROLLABILITY = 2
    HARD_CONTROLLABILITY = 3


# Vulnerability
class VulnerabilityOption(CustomEnum):
    NO_VULNERABILITY = 'None'
    LOW_VULNERABILITY = 'Low'
    MEDIUM_VULNERABILITY = 'Medium'
    HIGH_VULNERABILITY = 'High'


class VulnerabilityShortcode(CustomEnum):
    NO_VULNERABILITY = 'N'
    LOW_VULNERABILITY = 'E'
    MEDIUM_VULNERABILITY = 'M'
    HIGH_VULNERABILITY = 'H'


class VulnerabilityWeight(CustomEnum):
    NO_VULNERABILITY = 0
    LOW_VULNERABILITY = -1
    MEDIUM_VULNERABILITY = -2
    HIGH_VULNERABILITY = -3


# Importance
class ImportanceOption(CustomEnum):
    NO_IMPORTANCE = 'None'
    LOW_IMPORTANCE = 'Low'
    HIGH_IMPORTANCE = 'High'


class ImportanceShortcode(CustomEnum):
    NO_IMPORTANCE = 'N'
    LOW_IMPORTANCE = 'L'
    HIGH_IMPORTANCE = 'H'


class ImportanceWeight(CustomEnum):
    NO_IMPORTANCE = 0
    LOW_IMPORTANCE = 1
    HIGH_IMPORTANCE = 2


# Connection
class ConnectionOption(CustomEnum):
    NEUTRAL_CONNECTION = 'Neutral'
    POSITIVE_WEAK_CONNECTION = 'Positive Weak'
    POSITIVE_MEDIUM_CONNECTION = 'Positive Medium'
    POSITIVE_STRONG_CONNECTION = 'Positive Strong'
    NEGATIVE_WEAK_CONNECTION = 'Negative Weak'
    NEGATIVE_MEDIUM_CONNECTION = 'Negative Medium'
    NEGATIVE_STRONG_CONNECTION = 'Negative Strong'


class ConnectionShortcode(CustomEnum):
    NEUTRAL_CONNECTION = 'N'
    POSITIVE_WEAK_CONNECTION = '+W'
    POSITIVE_MEDIUM_CONNECTION = '+M'
    POSITIVE_STRONG_CONNECTION = '+S'
    NEGATIVE_WEAK_CONNECTION = '-W'
    NEGATIVE_MEDIUM_CONNECTION = '-M'
    NEGATIVE_STRONG_CONNECTION = '-S'


class ConnectionWeight(CustomEnum):
    NEUTRAL_CONNECTION = 0
    POSITIVE_WEAK_CONNECTION = 1
    POSITIVE_MEDIUM_CONNECTION = 2
    POSITIVE_STRONG_CONNECTION = 3
    NEGATIVE_WEAK_CONNECTION = -1
    NEGATIVE_MEDIUM_CONNECTION = -2
    NEGATIVE_STRONG_CONNECTION = -3
