#import sqlite3
from src import webscraping_MINE

def makeDB():
    # Enable foreign key support
    webscraping_MINE.cursor.execute('''PRAGMA foreign_keys = 1''')
    webscraping_MINE.db.commit()

    webscraping_MINE.cursor.execute('''
    CREATE TABLE IF NOT EXISTS actor (
        'ActorID'               INTEGER UNIQUE,
        `Firstname_Surname`	    TEXT,
        `About_info`	        TEXT,
        `Actorpage_URL`	        TEXT,
        `actoraward_url`	    TEXT,                    
        PRIMARY KEY(Firstname_Surname)
    ) ''')
    webscraping_MINE.db.commit()

    webscraping_MINE.cursor.execute('''
        CREATE TABLE if not exists film
            (
            'FilmID'    INTEGER UNIQUE,
            'ActorID'   INTEGER,
            `Title`	    TEXT,
            `Year`	    INTEGER,
            `Rating`	FLOAT,
            PRIMARY KEY(Title,Year),
            FOREIGN KEY(`ActorID`) REFERENCES `actor`(`ActorID`) ON UPDATE CASCADE ON DELETE SET NULL
	)
        ''')
    webscraping_MINE.db.commit()

    webscraping_MINE.cursor.execute('''
           CREATE TABLE if not exists genre
            (
            GenreID INTEGER UNIQUE,
            Description TEXT,
			PRIMARY KEY(Description))
            ''')
    webscraping_MINE.db.commit()

    webscraping_MINE.cursor.execute('''
               CREATE TABLE if not exists filmgenres
                ('FilmID'    INTEGER,
                 'GenreID'    INTEGER,
                  FOREIGN KEY(`FilmID`) REFERENCES `film`(`FilmID`) ON DELETE CASCADE
                  FOREIGN KEY(`GenreID`) REFERENCES `genre`(`GenreID`) ON DELETE CASCADE
                )''')
    webscraping_MINE.db.commit()

    webscraping_MINE.cursor.execute('''
            CREATE TABLE if not exists award
            (
            AwardID INTEGER UNIQUE,
            `Description`	TEXT,
            'Name'          TEXT,
            `Year`	        INTEGER,
            `ActorID`	    INTEGER,
            PRIMARY KEY(Description,Year,ActorID),
            FOREIGN KEY(`ActorID`) REFERENCES `actor`(`ActorID`) ON UPDATE CASCADE ON DELETE SET NULL
            )''')
    webscraping_MINE.db.commit()
