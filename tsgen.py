import docxtpl
from tsconfig import TSConfig

from tsmenu import menus

def main():
    TSConfig.load("config.json")
    try:
        while True:
            menus.menu_main()

    except KeyboardInterrupt:
        print("Aborting...")
    

if __name__ == "__main__": main()