#!/usr/bin/env python3
from wallman.wallman_lib import WallpaperLogic

def main():
    logic: WallpaperLogic = WallpaperLogic()
    logic.set_wallpaper_by_time()
    logic.schedule_wallpapers()

if __name__ == "__main__":
    main()
