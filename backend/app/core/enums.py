from enum import Enum


class ContentSource(str, Enum):
    ARTICLE = "article"
    POST = "post"
    VIDEO = "video"
    CAMPAIGN = "campaign"
    EVENT = "event"
    EXHIBITION = "exhibition"
    NEWS = "news"
    OTHER = "other"


class ContentStatus(str, Enum):
    NEW = "new"
    PARSED = "parsed"
    ANALYZED = "analyzed"
    SELECTED = "selected"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ProjectType(str, Enum):
    IN77 = "in77"
    IN88 = "in88"
    OTHER = "other"


class TrendLifecycle(str, Enum):
    RISING = "rising"
    PEAK = "peak"
    DECLINING = "declining"
    OUTDATED = "outdated"


class ScoreLevel(str, Enum):
    IMMEDIATE = "immediate"
    DISCUSS = "discuss"
    BACKUP = "backup"
    HOLD = "hold"
    REJECT = "reject"
