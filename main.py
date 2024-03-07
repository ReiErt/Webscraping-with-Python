from src import webscraping_MINE
from src import makeDB

def main():
    # Create db
    makeDB.dataconnect()


main()

# Close the db connection!
webscraping_MINE.db.close()

