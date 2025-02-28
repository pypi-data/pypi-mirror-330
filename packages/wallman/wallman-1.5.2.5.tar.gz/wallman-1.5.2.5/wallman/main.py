#!/usr/bin/env python3
from wallman.wallman_lib import ConfigValidity, WallpaperLogic

def main():
    validator: ConfigValidity = ConfigValidity()
    logic: WallpaperLogic = WallpaperLogic()
    validator.validate_config()
    logic.set_wallpaper_by_time()
    logic.schedule_wallpapers()

if __name__ == "__main__":
    main()
