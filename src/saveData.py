from src import webscraping as ws

def saveNewActor(Firstname_Surname, About_info, Actorpage_URL, actoraward_url):
    # save new actor
    ws.cursor.execute('''INSERT OR IGNORE INTO actor (ActorID, Firstname_Surname, About_info, Actorpage_URL,actoraward_url)
                    VALUES ((SELECT COALESCE(MAX(ActorID), 0)+1 FROM ACTOR),?,?,?,?)''',
                   (Firstname_Surname,
                    About_info,
                    Actorpage_URL,
                    actoraward_url)
                  )
    ws.db.commit()

    ws.cursor.execute('''SELECT Max(ActorID) from actor''')
    myActorID = ws.cursor.fetchone()[0]

    # PRINT TO CONSOLE
    print("Saved new actor: " + Firstname_Surname)

    if myActorID == None:
        return 0
    else:
        return myActorID

def saveNewAward(year, name, description, actorName):
    # Get the actor ID
    use_me1 = actorName
    myActorName_List = actorName.split(' ', 1)
    myActorPrename = myActorName_List[0]
    myActorSurname = myActorName_List[1]

    ws.cursor.execute('''SELECT ActorID from actor WHERE Firstname_Surname = ?''', (use_me1,))
    result_award = ws.cursor.fetchone()
    if result_award != None:
        myActorID = int(result_award[0])
    else:
        myActorID = 0

    ws.cursor.execute('''INSERT OR IGNORE INTO Award (AwardID, year, name, description, actorID)
        VALUES ((SELECT COALESCE(MAX(AwardID), 0)+1 FROM Award),?,?,?,?)''',
                   (year,
                    name,
                    description,
                    myActorID))

    ws.db.commit()

    # PRINT TO CONSOLE
    print(actorName + " has won the award " + name)

def saveNewFilmGenre(FilmID, GenreID):
    ws.cursor.execute('''INSERT OR IGNORE INTO filmgenres (FilmID, GenreID)
                    VALUES (?,?)''',(FilmID, GenreID,))
    ws.db.commit()

def saveNewGenre(myGenreDescription):
    ws.cursor.execute('''INSERT OR IGNORE INTO genre (GenreID, description)
         VALUES ((SELECT COALESCE(MAX(GenreID), 0)+1 FROM genre),?)''',
                   (myGenreDescription,))
    ws.db.commit()

    ws.cursor.execute('''SELECT GenreID from genre WHERE description = ?''', (myGenreDescription,))
    myGenreID = ws.cursor.fetchone()[0]

    if myGenreID == None: return 0
    else: return myGenreID

def saveNewFilm(actorName, title, year, genreDescription, rating):
    # Get the actor ID
    use_me = actorName
    myActorName_List = actorName.split(' ', 1)
    myActorPrename = myActorName_List[0]
    myActorSurname = myActorName_List[1]
    ws.cursor.execute('''SELECT ActorID from actor WHERE Firstname_Surname = ?''', (use_me,))
    result_newFilm = ws.cursor.fetchone()
    if result_newFilm != None:
        myActorID = int(result_newFilm[0])
    else:
        myActorID = 0

    ws.cursor.execute('''INSERT OR IGNORE INTO film (FilmID, actorID, title, year, rating)
        VALUES ((SELECT COALESCE(MAX(FilmID), 0)+1 FROM film),?,?,?,?)''',
                   (myActorID,
                    title,
                    year,
                    rating
                   ))
    ws.db.commit()

    # Get the new film ID
    ws.cursor.execute('''SELECT FilmID from film WHERE TITLE = ? AND YEAR = ?''', (title, year,))
    result_newFilm = ws.cursor.fetchone()
    if result_newFilm != None:
        myFilmID = int(result_newFilm[0]) # get latest FilmID
    else:
        myFilmID = 0

    # Save new genre(s) and filmgenre(s)
    myGenreList = genreDescription.split()
    for eachGenre in myGenreList:
        myGenreID = saveNewGenre(eachGenre) # save single genre
        saveNewFilmGenre(myFilmID, myGenreID)  # save single filmgenre

    if myFilmID == None:
        print ("Warning: No FilmID was generated!")
        return 0
    else:
        return myFilmID