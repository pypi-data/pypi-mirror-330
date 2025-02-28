from os import chdir, getenv, system, path
import logging
import tomllib
from datetime import datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Dict, List

from wallman.wallman_classes import ConfigError, ConfigGeneral, ConfigFile

# Setup Logging. NOTE: Declaration as a global variable is necessary to ensure correct functionality across multiple modules.
global logger
logger = logging.getLogger("wallman")

class _Config:
    # Initializes the most important config values.
    def __init__(self) -> None:
        # Config file
        self.config_file: ConfigFile = self._initialize_config() # Full config
        # Config general
        valid_general: bool = self._initialize_general()
        if not valid_general:
            logger.critical("The general dictionary was not found or contains errors")
            print("CRITICAL: The general dictionary was not found or contains errors")
            raise ConfigError("The general dictionary was not found or contains errors")
        # Changing times
        valid_changing_times: bool = self._initialize_changing_times()
        if not valid_changing_times:
            logger.critical("The amount of provided changing times does not match the amount of wallpapers per set, or the dictionary has not been found in the config file.")
            print("CRITICAL: The amount of provided changing times does not match the amount of wallpapers per set, or the dictionary has not been found in the config file.")
        self.config_total_changing_times: int = len(self.config_changing_times)
        # Wallpaper sets
        valid_wallpaper_amount: bool = self._check_wallpaper_amount()
        if not valid_wallpaper_amount:
            raise ConfigError("The amount of wallpapers in a set does not match the amount of wallpapers_per_set provided in general.")

    # Read config
    def _initialize_config(self) -> ConfigFile:
        chdir(str(getenv("HOME")) + "/.config/wallman/")
        try:
            with open("wallman.toml", "rb") as config_file:
                data: ConfigFile = tomllib.load(config_file) #pyright:ignore
                return data
        except FileNotFoundError:
            raise FileNotFoundError("No config file could be found in ~/.config/wallman/wallman.toml")
        except tomllib.TOMLDecodeError as e:
            print("ERROR: Config could not be parsed: Invalid TOML Syntax")
            raise e

    def _verify_systray_deps(self):
        from importlib import util
        if util.find_spec("pystray") is None or util.find_spec("PIL") is None:
            logger.error("systray is enabled, but dependencies for the systray couldn't be found. Are pystray and pillow installed?")
            logger.info("Setting self.config_systray to false.")
            print("ERROR: systray is enabled, but dependencies for the systray couldn't be found. Are pystray and pillow installed?")
            self.config_systray = False

    def _set_log_level(self):
        global logging
        global logger
        chdir("/var/log/wallman/")
        numeric_level: int = getattr(logging, self.config_log_level, logging.INFO)
        logger.setLevel(numeric_level)
        if not path.exists("wallman.log"):
            system("touch wallman.log")
        logging.basicConfig(filename="wallman.log", encoding="utf-8", level=numeric_level)

    def _set_behavior(self) -> str:
        try:
            behavior = self.config_general["behavior"]
        except KeyError:
            logger.warning("There is no wallpaper behavior specified in general, defaulting to fill...")
            print("WARNING: There is no wallpaper behavior specified in general, defaulting to fill...")

        human_behaviors: List[str] = ["plain", "tile", "center", "fill", "max", "scale"]
        machine_behaviors: List[str] = ["--bg", "--bg-tile", "--bg-center", "--bg-fill", "--bg-max", "--bg-scale"]
        behavior: str = self.config_general.get("behavior", "--bg-fill").lower()
        if behavior not in human_behaviors and behavior not in machine_behaviors:
            logging.error(f"The value provided for behaviors, {behavior}, is not valid. Defaulting to fill...")
            print(f"ERROR: The value provided for behaviors, {behavior}, is not valid. Defaulting to --bg-fill...")

        if behavior not in machine_behaviors:
            match behavior:
                case "plain":
                    behavior = "--bg"
                case "tile":
                    behavior = "--bg-tile"
                case "center":
                    behavior = "--bg-center"
                case "max":
                    behavior = "--bg-max"
                case "scale":
                    behavior = "--bg-scale"
                case _:
                    behavior = "--bg-fill"

        logger.info(f"The wallpaper behavior '{behavior}' has been set.")
        return behavior

    def _set_fallback_wallpaper(self) -> None:
        if self.config_fallback_wallpaper:
            successfully_set: int = system(f"feh {self.config_behavior} --no-fehbg {self.config_fallback_wallpaper}")
            if successfully_set == 0:
                logger.info("The fallback Wallpaper has been set.")
            else:
                logger.critical("An Error occured and no fallback wallpaper was provided, exiting...")
                raise ConfigError("An error occured and no fallback wallpaper has been set, exiting...")

    def _initialize_general(self) -> bool:
        # Create Config General Dict
        try:
            self.config_general: ConfigGeneral = self.config_file["general"]
        except KeyError:
            print("CRITICAL: No general dictionary found in Config file.")
            raise ConfigError("The general dictionary could not be found in the config, exiting!")
        # Set up logger.
        self.config_log_level = self.config_general.get("log_level", "INFO").upper()
        self._set_log_level()
        logger.debug(f"Log level has been set to {self.config_log_level}")
        logger.debug("Logger initialized successfully")
        # Set up fallback wallpaper
        self.config_fallback_wallpaper: str = self.config_general.get("fallback_wallpaper", "/etc/wallman/DefaultFallbackWallpaper.jpg")
        logger.debug(f"Set fallback wallpaper: {self.config_fallback_wallpaper}")
        # Wallpapers per set
        try:
            self.config_wallpapers_per_set: int = self.config_general["wallpapers_per_set"]
            logger.debug(f"Set config_wallpapers_per_set to {self.config_wallpapers_per_set}")
        except KeyError:
            print("CRITICAL: No option wallpapers_per_set provided in the general dictionary. Attempting to set the fallback wallpaper")
            logger.critical("No option wallpapers_per_set provided in the general dictionary. Attempting to set the fallback wallpaper")
            self._set_fallback_wallpaper()
            return False
        # Are wallpaper sets enabled to begin with?
        try:
            self.config_wallpaper_sets_enabled: bool = self.config_general["enable_wallpaper_sets"]
            logger.debug(f"Set config_wallpaper_sets_enabled to {self.config_wallpaper_sets_enabled}")
        except KeyError:
            logger.critical("No option enable_wallpaper_sets provided in the general dictionary. Attempting to set the fallback wallpaper")
            print("CRITICAL: No option enable_wallpaper_sets provided in the general dictionary. Attempting to set the fallback wallpaper")
            self._set_fallback_wallpaper()
            return False
        # Configure used sets
        if self.config_wallpaper_sets_enabled:
            try:
                self.config_used_sets: List[str] = self.config_general["used_sets"]
                logger.debug(f"These wallpaper sets are in use: {self.config_used_sets}")
            except KeyError:
                print("CRITICAL: No array used_sets provided in the general dictionary. Attempting to set the fallback wallpaper.")
                logger.critical("No array used_sets provided in the general dictionary. Attempting to set the fallback wallpaper.")
                self._set_fallback_wallpaper()
                return False
        # Systray
        try:
            self.config_systray: bool = self.config_general["systray"]
            logger.debug(f"config_systray has been set to: {self.config_systray}")
        except KeyError:
            self.config_systray: bool = True
            logger.warning("No option systray found in general. Defaulting to true...")
        if self.config_systray:
            self._verify_systray_deps()
        # Wallpaper behavior
        self.config_behavior = self._set_behavior()
        # Notifications
        try:
            self.config_notify: bool = self.config_general["notify"]
            logger.debug(f"Set config_notify to {self.config_notify}.")
        except KeyError:
            self.config_notify: bool = False
            logger.warning("notify is not set in dictionary general in the config file, defaulting to 'false'.")

        return True

    def _initialize_changing_times(self) -> bool:
        try:
            self.config_changing_times: Dict[str, str] = self.config_file["changing_times"]
            logger.debug(f"Changing times are {self.config_changing_times}")
        except KeyError:
            logger.critical("No dictionary called changing_times has been found in the config file.")
            print("CRITICAL: No dictionary called changing_times has been found in the config file.")
            return False
        return self._wallpapers_per_set_and_changing_times_match()

    def _wallpapers_per_set_and_changing_times_match(self) -> bool:
        # Check if the amount of wallpapers_per_set and given changing times match
        if self.config_total_changing_times == self.config_wallpapers_per_set:
            logger.debug("The amount of changing times and wallpapers per set is set correctly")
            return True
        else:
            try:
                self._set_fallback_wallpaper()
                logger.critical("The amount of changing_times and the amount of wallpapers_per_set does not match, the fallback wallpaper has been set.")
                print("CRITICAL: The amount of changing_times and the amount of wallpapers_per_set does not match, the fallback wallpaper has been set.")
                return False
            except ConfigError:
                logger.critical("The amount of changing times and the amount of wallpapers per set does not match, exiting...")
                print("CRITICAL: The amount of changing times and the amount of wallpapers per set does not match, exiting...")
                raise ConfigError("The amount of changing times and the amount of wallpapers per set does not match.")

    def _check_wallpaper_amount(self) -> bool:
        # This block checks if if each wallpaper set dictionary provides enough wallpapers to satisfy wallpapers_per_set
        for wallpaper_set in self.config_used_sets:
            if len(self.config_file[wallpaper_set]) == self.config_wallpapers_per_set:
                logger.debug(f"Dictionary {wallpaper_set} has sufficient values.")
                return True
            else:
                try:
                    self._set_fallback_wallpaper()
                    logger.error(f"The Dictionary {wallpaper_set} does not have sufficient entries, the fallback wallpaper has been set.")
                    print(f"ERROR: The Dictionaty {wallpaper_set} does not have sufficient entries, the fallback wallpaper has been set.")
                    return False
                except ConfigError:
                    logger.critical(f"Dictionary {wallpaper_set} does not have sufficient entries, exciting...")
                    print(f"Dictionary {wallpaper_set} does not have sufficient entries, exciting...")
        return False


# TODO: Improve modularity. See notes inside the class for more details.
# TODO: Ensure functionality and if needed add handling for the 1 wallpaper per set case.
class WallpaperLogic(_Config):
    def __init__(self) -> None:
        super().__init__()
        self.wallpaper_list: List[str] = None # pyright: ignore
        self.chosen_wallpaper_set: str = None # pyright: ignore

    # NOTE: This function could be in a different file because it's not needed in the case only 1 wallpaper per set is needed.
    # Returns a list of a split string that contains a changing time from the config file
    def _clean_times(self, desired_time: int) -> List[str]:
        unclean_times: str = list(self.config_changing_times.values())[desired_time]
        return unclean_times.split(":")

    # NOTE: This could be in a different file because it's not needed in the "Only one wallpaper set" case.
    def _choose_wallpaper_set(self) -> None:
        from random import choice as choose_from
        self.chosen_wallpaper_set = choose_from(self.config_used_sets)
        self.wallpaper_list: List[str] = list(self.config_file[self.chosen_wallpaper_set].values())
        logger.debug(f"Chose wallpaper set {self.chosen_wallpaper_set}")

    # NOTE: Same as _clean_times()
    # Verify if a given time is in a given range
    def _time_in_range(self, start: time, end: time, x: time) -> bool:
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x < end

    # NOTE: Potentially add handling for this to be also usable for notify_user and add logging if notify_user fails. Consider adding an argument that is where it's called from and handle accordingly.
    def _check_system_exitcode(self, code: int) -> bool:
        if code != 0:
            try:
                self._set_fallback_wallpaper()
                logger.error(f"The wallpaper {self.wallpaper_list[self.current_time_range]} has not been found, the fallback wallpaper has been set. Future wallpapers will still attempted to be set.")
                print(f"ERROR: The wallpaper {self.wallpaper_list[self.current_time_range]} has not been found, the fallback wallpaper has been set. Future wallpapers will still attempted to be set.")
                return False
            except ConfigError:
                logger.error(f"The wallpaper {self.wallpaper_list[self.current_time_range]} has not been found and no fallback wallpaper has been set. Future wallpapers will still attempted to be set.")
                print(f"ERROR: The wallpaper {self.wallpaper_list[self.current_time_range]} has not been found and no fallback wallpaper has been set. Future wallpapers will still attempted to be set.")
                return False
        else:
            logger.info(f"The wallpaper {self.wallpaper_list[self.current_time_range]} has been set.")
            return True

    # NOTE: Add error handling in case libnotify is not installed or notify-send fails for any other reason.
    # TODO: Add a check whether config[notify] is true or not.
    def _notify_user(self):
        system("notify-send 'Wallman' 'A new Wallpaper has been set.'")
        logger.debug("Sent desktop notification.")

    # TODO: Clean this up. It's way too large and way too intimidating.
    # NOTE: This could be in a different for the case that the user only wants 1 wallpaper per set.
    # TODO: Add an way for the user to choose if the wallpaper should scale, fill or otherwise. This needs to be editable in the config file.
    def set_wallpaper_by_time(self) -> bool:
        # Ensure use of a consistent wallpaper set
        if not self.chosen_wallpaper_set:
            self._choose_wallpaper_set()
        for time_range in range(self.config_total_changing_times - 1):
            self.current_time_range = time_range # Store current time for better debugging output
            clean_time: List[str] = self._clean_times(time_range)
            clean_time_two: List[str] = self._clean_times(time_range + 1)
            # HACK on this to make it more readable. This function call is way too long. Consider storing these in a bunch of temporary variables, though keep function length in mind.
            # HACK on this to see if this logic can be simplified. It's very ugly to check it that way.
            # Check if the current time is between a given and the following changing time and if so, set that wallpaper. If not, keep trying.
            if self._time_in_range(time(int(clean_time[0]), int(clean_time[1]), int(clean_time[2])), time(int(clean_time_two[0]), int(clean_time_two[1]), int(clean_time_two[2])), datetime.now().time()):
                exitcode: int = system(f"feh {self.config_behavior} --no-fehbg --quiet {self.wallpaper_list[time_range]}")
                has_wallpaper_been_set: bool = self._check_system_exitcode(exitcode)
                # TODO: Add this check to _notify_user.
                if self.config_notify:
                    self._notify_user()
                return has_wallpaper_been_set
            else:
                continue

        exitcode: int = system(f"feh {self.config_behavior} --no-fehbg {self.wallpaper_list[-1]}")
        has_wallpaper_been_set: bool = self._check_system_exitcode(exitcode)
        if self.config_notify:
            self._notify_user()
        return has_wallpaper_been_set

    # NOTE: Consider avoiding nested functions.
    def schedule_wallpapers(self) -> None:
        def _schedule_background_wallpapers() -> BackgroundScheduler:
            from apscheduler.schedulers.background import BackgroundScheduler
            scheduler = BackgroundScheduler()
            # Create a scheduled job for every changing time
            # NOTE: This should be a function.
            for changing_time in range(len(self.config_changing_times)):
                clean_time = self._clean_times(changing_time)
                scheduler.add_job(self.set_wallpaper_by_time, trigger=CronTrigger(hour=clean_time[0], minute=clean_time[1], second=clean_time[2]))
            scheduler.start()
            logger.info("The background scheduler has been started.")
            return scheduler

        def _schedule_blocking_wallpapers() -> None:
            from apscheduler.schedulers.blocking import BlockingScheduler
            scheduler = BlockingScheduler()
            # Create a scheduled job for every changing time
            # NOTE: Thisshould be a function.
            for changing_time in range(len(self.config_changing_times)):
                clean_time = self._clean_times(changing_time)
                scheduler.add_job(self.set_wallpaper_by_time, trigger=CronTrigger(hour=clean_time[0], minute=clean_time[1], second=clean_time[2]))
            logger.info("The blocking scheduler has been started.")
            scheduler.start()

        if self.config_systray:
            import wallman.wallman_systray as systray
            from functools import partial

            scheduler: BackgroundScheduler = _schedule_background_wallpapers()
            menu: systray.Menu = systray.Menu (
                systray.item("Re-Set Wallpaper", partial(systray.set_wallpaper_again, wallpaper_setter=self.set_wallpaper_by_time)),
                systray.item("Reroll Wallpapers", partial(systray.reroll_wallpapers, wallpaper_chooser=self._choose_wallpaper_set, wallpaper_setter=self.set_wallpaper_by_time)),
                systray.item("Quit", partial(systray.on_quit, shutdown_scheduler=scheduler.shutdown))
            )
            icon = systray.Icon("wallman_icon", systray.icon_image, "My Tray Icon", menu)
            icon.run()
        else:
            _schedule_blocking_wallpapers()
