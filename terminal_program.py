import sqlite3
from src import webscraping_MINE as ws
from src import mainWindow as mw
from src import makeDB
from src import obj_actor
from src import obj_film
from src import obj_award
from datetime import datetime
path_to_databaseeee = 'actual_Master_Actor_database.db'


# done
def About_Actor_ID(user_input_ID):
    db = sqlite3.connect(path_to_databaseeee)
    cursor = db.cursor()
    cursor.execute('SELECT About_info FROM actor WHERE ActorID=?', (user_input_ID,))
    first_row = cursor.fetchall()
    for result in first_row:
        print(result[0])
    db.close()

# done
def All_time_movies_ID(user_input_ID):
    db = sqlite3.connect(path_to_databaseeee)
    cursor = db.cursor()
    cursor.execute('SELECT Title, Year FROM film WHERE ActorID=? ORDER BY YEAR DESC', (user_input_ID,))
    title_and_year = cursor.fetchall()
    
    if title_and_year:
        #print("printing results for", GetOneActor(user_input_ID))
        for each_title_and_year in title_and_year:
            print(f"Movie Title: {each_title_and_year[0]}\nReleased in {each_title_and_year[1]}\n")



  #  print("incomming...")
  #  print(title_and_year[3][0], "from year", title_and_year[3][1])
  #  for result in title_and_year:
  #      print(result[0][0])
    db.close()

# done
def Awards_to_Actor_ID(user_input_ID):
    db = sqlite3.connect(path_to_databaseeee)
    cursor = db.cursor()
    cursor.execute('SELECT Name, Year FROM award WHERE ActorID=? ORDER BY YEAR DESC', (user_input_ID,))
    award_and_year = cursor.fetchall()
    
    if award_and_year:
        for each_award_and_year in award_and_year:
            print(f"In the year, {each_award_and_year[1]}, the following award was won: {each_award_and_year[0]}")
    db.close()

# done
def Movie_genres_ID(user_input_ID):
    db = sqlite3.connect(path_to_databaseeee)
    cursor = db.cursor()
    cursor.execute('''SELECT DISTINCT G.Description
            FROM actor AS N
            JOIN film AS F ON N.ActorID = F.ActorID
            JOIN filmgenres AS FG ON F.FilmID = FG.FilmID
            JOIN genre AS G ON FG.GenreID = G.GenreID
            WHERE N.ActorID = ?
        ''', (user_input_ID,))
        
    first_row = cursor.fetchall()
    for result in first_row:
        print(result[0])
    db.close()

# not done
def Average_movie_rating_ID(user_input_ID):
    db = sqlite3.connect(path_to_databaseeee)
    cursor = db.cursor()
    cursor.execute('SELECT About_info FROM actor WHERE ActorID=?', (user_input_ID,))
    db.close()   

# not done
def Top_5_movies_ID(user_input_ID):
    db = sqlite3.connect(path_to_databaseeee)
    cursor = db.cursor()
    cursor.execute('SELECT About_info FROM actor WHERE ActorID=?', (user_input_ID,))
    db.close()

# done
def GetOneActor(actorID):
    db = sqlite3.connect(path_to_databaseeee)
    cursor = db.cursor()
    cursor.execute('SELECT Firstname_Surname FROM actor WHERE ActorID=?', (actorID,))
    first_row = cursor.fetchall()
    for result in first_row:
        #print(result[0])
        return result[0]
    db.close()

# done
def getAllActors():
    db = sqlite3.connect(path_to_databaseeee)
    cursor = db.cursor()
    cursor.execute('SELECT Firstname_Surname FROM actor ORDER BY ActorID ASC')
    result_ALLActors = cursor.fetchall()
    idx = 1
    for each_Actor in result_ALLActors:
        print("ID:", idx, each_Actor[0])
        idx = idx + 1
    db.close()


def main():
    while True:
        # this prints sylvester sallone as a test
        #GetOneActor(int(13))

        print('''
              Welcome to my program. You have two options:
              (1) Type and enter 1 to list of all available actors and actresses and their IDs")
              (2) Type and enter 2 to do something with the data''')
        
        ############# first user_input #############

        user_input_first = input()
        number1 = int(user_input_first)
        if user_input_first.lower() == 'q':
           print("Exiting the program. Goodbye!")
           break
        elif number1 == 1:
            print("You entered 1. Returning a list of all actors/actresses:")
            getAllActors()
        elif number1 == 2:
            print("You entered 2. Showing you a list of commands:")
            print('''
            Type and enter 2 for following function: About the actor/actresses
            Type and enter 3 for following function: All time movie names and years
            Type and enter 4 for following function: Awards to actor/actresses in different years
            Type and enter 5 for following function: Movie genre of actor/actresses
            Type and enter 6 for following function: Average rating of their movies (overall and each year)
            Type and enter 7 for following function: Top 5 movies, their respective years and genre
            ''')

            ############# second user input #############

            user_input_second = input()
            number2 = int(user_input_second)
            if user_input_second.lower() == 'q':
                print("Exiting the program. Goodbye!")
                break

            elif number2 == 2:
                print("You entered 2. Type and enter the actor/actress ID you wish to know more about")
                user_input_ID = input()
                About_Actor_ID(user_input_ID)
                print("\n########### Enquiry Complete. Returning to beginning page ###########\n")

            elif number2 == 3:
                print("You entered 3. Type and enter the actor/actress ID you wish to see all time movies and years for")
                user_input_ID = input()
                print("\n",GetOneActor(int(user_input_ID)), "has acted in the following movies:")
                All_time_movies_ID(user_input_ID)
                print("\n########### Enquiry Complete. Returning to beginning page ###########\n")

            elif number2 == 4:
                print("You entered 4. Type and enter the actor/actress ID you wish to see all awards for including years")
                user_input_ID = input()
                print("\n",GetOneActor(int(user_input_ID)), "has won the following awards:")
                Awards_to_Actor_ID(user_input_ID)
                print("\n########### Enquiry Complete. Returning to beginning page ###########\n")

            elif number2 == 5:
                print("You entered 5. Type and enter the actor/actress ID you wish to see genres of movies they acted in")
                user_input_ID = input()
                print("\n",GetOneActor(int(user_input_ID)), "has acted in movies of the follow genres:")
                Movie_genres_ID(user_input_ID)
                print("\n########### Enquiry Complete. Returning to beginning page ###########\n")

            elif number2 == 6:
                print("You entered 6. Type and enter the actor/actress ID you wish to see the average rating of their movies (overall and each year)")
                user_input_ID = input()
                print("\nThe average rating of moves, that", GetOneActor(int(user_input_ID)), " has acted in:")
                Average_movie_rating_ID(user_input_ID)
                print("\n########### Enquiry Complete. Returning to beginning page ###########\n")

            elif number2 == 7:
                print("You entered 7. Type and enter the actor/actress ID you wish to the top 5 movies for, including its year of release and genre")
                user_input_ID = input()
                print("\n",GetOneActor(int(user_input_ID)),"'s top five movies:")
                Top_5_movies_ID(user_input_ID)
                print("\n########### Enquiry Complete. Returning to beginning page ###########\n")

            else:
                print("something went wrong pal")
        else:
            print("returning to beginning")

        #Choose a number between 1 and 7, or 'q' to quit:")
        #user_input = input()
        #number = int(user_input)
        #print("calling function to return just 1 actor....")
        #GetOneActor(number)

if __name__ == "__main__":
    main()