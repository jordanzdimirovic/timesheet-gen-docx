import docxtpl
from tsconfig import TSConfig
from tsdef.definitions import Collection

from tsmenu import menus

def main():
    TSConfig.load("config.json")
    try:
        collection: Collection = menus.menu_collection()
        while True:
            menus.menu_main(collection)

    except KeyboardInterrupt:
        print("Aborting...")
    

if __name__ == "__main__": main()