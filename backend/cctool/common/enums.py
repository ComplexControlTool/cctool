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
    CONTROLLABILITY_ANALYSIS = 'Controllability Analysis'
    INTERVENTION_ANALYSIS = 'Intervention Analysis'
    NETWORK_ANALYSIS = 'Network Analysis'
    OUTCOME_ANALYSIS = 'Outcome Analysis'
    XCS_ANALYSIS = 'XCS classifier'


class AnalysisShortcode(CustomEnum):
    CONTROLLABILITY_ANALYSIS = 'CA'
    INTERVENTION_ANALYSIS = 'IA'
    NETWORK_ANALYSIS = 'NA'
    OUTCOME_ANALYSIS = 'OA'
    XCS_ANALYSIS = 'XCS'


class AnalysisDescription(CustomEnum):
    CONTROLLABILITY_ANALYSIS = 'Controllability Analysis Description'
    INTERVENTION_ANALYSIS = 'Intervention Analysis Description'
    NETWORK_ANALYSIS = 'Network Analysis Description'
    OUTCOME_ANALYSIS = 'Outcome Analysis Description'
    XCS_ANALYSIS = 'XCS Analysis Description'


# Function
class FunctionOption(CustomEnum):
    LINEAR_FUNCTION = 'Linear'


class FunctionShortcode(CustomEnum):
    LINEAR_FUNCTION = 'L'


# Controllability
class ControllabilityOption(CustomEnum):
    NO_CONTROLLABILITY = 'None'
    LOW_CONTROLLABILITY = 'Low'
    MEDIUM_CONTROLLABILITY = 'Medium'
    HIGH_CONTROLLABILITY = 'High'


class ControllabilityShortcode(CustomEnum):
    NO_CONTROLLABILITY = 'N'
    LOW_CONTROLLABILITY = 'L'
    MEDIUM_CONTROLLABILITY = 'M'
    HIGH_CONTROLLABILITY = 'H'


class ControllabilityWeight(CustomEnum):
    NO_CONTROLLABILITY = 0
    LOW_CONTROLLABILITY = 1
    MEDIUM_CONTROLLABILITY = 2
    HIGH_CONTROLLABILITY = 3


# Vulnerability
class VulnerabilityOption(CustomEnum):
    NO_VULNERABILITY = 'None'
    LOW_VULNERABILITY = 'Low'
    MEDIUM_VULNERABILITY = 'Medium'
    HIGH_VULNERABILITY = 'High'


class VulnerabilityShortcode(CustomEnum):
    NO_VULNERABILITY = 'N'
    LOW_VULNERABILITY = 'L'
    MEDIUM_VULNERABILITY = 'M'
    HIGH_VULNERABILITY = 'H'


class VulnerabilityWeight(CustomEnum):
    NO_VULNERABILITY = 0
    LOW_VULNERABILITY = 1
    MEDIUM_VULNERABILITY = 2
    HIGH_VULNERABILITY = 3


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
    COMPLEX_CONNECTION = 'Complex'
    POSITIVE_WEAK_CONNECTION = 'Positive Weak'
    POSITIVE_MEDIUM_CONNECTION = 'Positive Medium'
    POSITIVE_STRONG_CONNECTION = 'Positive Strong'
    NEGATIVE_WEAK_CONNECTION = 'Negative Weak'
    NEGATIVE_MEDIUM_CONNECTION = 'Negative Medium'
    NEGATIVE_STRONG_CONNECTION = 'Negative Strong'


class ConnectionShortcode(CustomEnum):
    COMPLEX_CONNECTION = 'N'
    POSITIVE_WEAK_CONNECTION = '+W'
    POSITIVE_MEDIUM_CONNECTION = '+M'
    POSITIVE_STRONG_CONNECTION = '+S'
    NEGATIVE_WEAK_CONNECTION = '-W'
    NEGATIVE_MEDIUM_CONNECTION = '-M'
    NEGATIVE_STRONG_CONNECTION = '-S'


class ConnectionWeight(CustomEnum):
    COMPLEX_CONNECTION = 0
    POSITIVE_WEAK_CONNECTION = 1
    POSITIVE_MEDIUM_CONNECTION = 2
    POSITIVE_STRONG_CONNECTION = 3
    NEGATIVE_WEAK_CONNECTION = -1
    NEGATIVE_MEDIUM_CONNECTION = -2
    NEGATIVE_STRONG_CONNECTION = -3


# Colours
class MapColours(CustomEnum):
    HOVER_DEFAULT = '#2B7CE9'

    NODE_BACKGROUND_LOW_IMPORTANCE = '#F8BBD0'
    NODE_BACKGROUND_HIGH_IMPORTANCE = '#F8BBD0'
    NODE_BACKGROUND_INTERVENTION = '#BBDEFB'
    NODE_BACKGROUND_OUTCOME = '#FFFACD'
    NODE_BACKGROUND_FOCUSED = '#FDD835'
    NODE_BACKGROUND_DEFAULT = '#FDFEFE'

    NODE_BORDER_LOW_CONTROLLABILITY = '#D32F2F'
    NODE_BORDER_MEDIUM_CONTROLLABILITY = '#F57C00'
    NODE_BORDER_HIGH_CONTROLLABILITY = '#388E3C'
    NODE_BORDER_DEFAULT = '#333'

    NODE_HIGHLIGHT_BORDER_LOW_CONTROLLABILITY = '#cb181d'
    NODE_HIGHLIGHT_BORDER_MEDIUM_CONTROLLABILITY = '#fd8d3c'
    NODE_HIGHLIGHT_BORDER_HIGH_CONTROLLABILITY = '#238b45'
    NODE_HIGHLIGHT_BORDER_DEFAULT = '#333'

    NODE_HIGHLIGHT_BACKGROUND_DEFAULT = '#D2B4DE'

    NODE_HOVER_BORDER_DEFAULT = '#2B7CE9'

    NODE_HOVER_BACKGROUND_DEFAULT = '#D2E5FF'

    NODE_FONT_BACKGROUND = 'rgba(255,255,255,0.65)'

    EDGE_COLOR_POSITIVE_WEAK_CONNECTION = '#7DCEA0'
    EDGE_COLOR_POSITIVE_MEDIUM_CONNECTION = '#27AE60'
    EDGE_COLOR_POSITIVE_STRONG_CONNECTION = '#1E8449'
    EDGE_COLOR_NEGATIVE_WEAK_CONNECTION = '#D98880'
    EDGE_COLOR_NEGATIVE_MEDIUM_CONNECTION = '#C0392B'
    EDGE_COLOR_NEGATIVE_STRONG_CONNECTION = '#922B21'
    EDGE_COLOR_DEFAULT = '#737373'

    EDGE_HIGHLIGHT_POSITIVE_WEAK_CONNECTION = '#7DCEA0'
    EDGE_HIGHLIGHT_POSITIVE_MEDIUM_CONNECTION = '#27AE60'
    EDGE_HIGHLIGHT_POSITIVE_STRONG_CONNECTION = '#1E8449'
    EDGE_HIGHLIGHT_NEGATIVE_WEAK_CONNECTION = '#D98880'
    EDGE_HIGHLIGHT_NEGATIVE_MEDIUM_CONNECTION = '#C0392B'
    EDGE_HIGHLIGHT_NEGATIVE_STRONG_CONNECTION = '#922B21'
    EDGE_HIGHLIGHT_DEFAULT = '#737373'

class HeatmapColours(CustomEnum):
    ONE = '#1d4877'
    TWO = '#255672'
    THREE = '#29636c'
    FOUR = '#287166'
    FIVE = '#237f5f'
    SIX = '#358c58'
    SEVEN = '#6f9650'
    EIGHT = '#9a9e46'
    NINE = '#c2a63b'
    TEN = '#e8ad2c'
    ELEVEN = '#fbac24'
    TWELVE = '#faa42a'
    THIRTEEN = '#f99b2f'
    FOURTEEN = '#f89333'
    FIFTEEN = '#f68a37'
    SIXTEEN = '#f57e37'
    SEVENTEEN = '#f47036'
    EIGHTEEN = '#f26135'
    NINETEEN = '#f05133'
    TWENTY = '#ee3e32'
    # http://gka.github.io/palettes/#colors=#1d4877,#1b8a5a,#fbb021,#f68838,#ee3e32|steps=20|bez=0|coL=0
