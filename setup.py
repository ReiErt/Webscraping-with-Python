from src import webscraping_MINE
from src import makeDB

def main():
    # make database
    makeDB.makeDB()


    webscraping_MINE.getActorList()
    print("\nif you see this. we finished successfully\n")




main()
webscraping_MINE.db.close()

