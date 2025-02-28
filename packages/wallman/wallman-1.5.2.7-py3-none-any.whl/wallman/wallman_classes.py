from typing import TypedDict, List, Dict

"""
This is where library classes, like the config error
And other utility things like TypedDicts for better
linting and type checking go. I should also consider
to move some other import here
"""

class ConfigError(Exception):
    pass

class ConfigGeneral(TypedDict):
    enable_wallpaper_sets: bool
    used_sets: List[str]
    wallpapers_per_set: int
    notify: bool
    fallback_wallpaper: str
    log_level: str
    systray: bool
    behavior: str

class ConfigFile(TypedDict):
    general: ConfigGeneral
    changing_times: Dict[str, str]
