from src import saveData
import sqlite3
from random import randint
from time import sleep
import requests as rq
from bs4 import BeautifulSoup

# Need header to disguise https requests to avoid rejection 
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

my_path_to_db = 'Master_Actor_database.db'
db = sqlite3.connect(my_path_to_db)
cursor = db.cursor()

MainPageURL = "/list/ls053501318/"
awardsURL = "awards"
baseURL = "http://www.imdb.com"

def getActorList():
    rqMainPageList = rq.get(baseURL + MainPageURL, headers=HEADERS)  # request the website
    soup = BeautifulSoup(rqMainPageList.text, 'lxml')

    top50page = soup.find('div', class_ ="lister-list")
    allmyActors_images = top50page.find_all('div', class_= 'lister-item mode-detail')

    # go through each actor
    for eachActorImage in allmyActors_images:

        # extract name of actor being scrubbed
        allActors_images_exact = eachActorImage.find('div', class_= 'lister-item-image')
        img = allActors_images_exact.find('img', alt=True)
        img_string = str(img['alt'])   
        print("Begin initial biography scrubbing on", img_string)     # this is my actor page

        # extract about info on actor being scrubbed
        each_actor_info = eachActorImage.find('div', class_='lister-item-content')
        each_actor_info_pTAG = each_actor_info.find('p', class_=False, id=False)
        actor_info_for_db = str(each_actor_info_pTAG.text)
        actor_info_strip_db = actor_info_for_db.strip()

        # save actorpage_URL and actorawar_url to database 
        myActorImageLink = allActors_images_exact.a['href']
        actorpage = baseURL+myActorImageLink
        actorpage_str = str(actorpage)
        actorpage_str_no_lastslash = actorpage_str.rfind('/')
        result_actorpage_noslash = actorpage_str[:actorpage_str_no_lastslash + 1]
        actor_award_page = result_actorpage_noslash + awardsURL

        # pass information to save an actor in the 'actor' table of DB
        saveData.saveNewActor(img_string,actor_info_strip_db, result_actorpage_noslash, actor_award_page)

        # print statements for feedback in the terminal
        print("\n**************************** NEW ACTOR *******************************")
        print("Begin scrubbing for awards on actor:", img_string)
        print("-----------------------------------------------------------------------")
        print("-----------------------------------------------------------------------\n")
        # call function to get films
        getAllAwardsOfActor(actor_award_page)
        print("Scrubing for Awards complete")
        print("-----------------------------------------------------------------------\n")

        print("\nBegin scrubbing movies for actor:", img_string)
        print("-----------------------------------------------------------------------")
        print("-----------------------------------------------------------------------\n")
        # call function to get films
        getAllFilmsofActor(result_actorpage_noslash)
        print("Scrub complete --> Actor finished! Going to next actor:", img_string)
        print("-----------------------------------------------------------------------\n")


def getAllFilmsofActor(link_to_actor):
    MyActorPageRequest = rq.get(link_to_actor, headers=HEADERS)
    MyActorSoup = BeautifulSoup(MyActorPageRequest.text, 'lxml')
    print("access following webpage to get list of films ", link_to_actor)
    # Randomize speed of searching to avoid detection by website
    print("\n-----------------------------------------------------------------------")
    print("****Sleeping to allow data extraction..")
    sleep(randint(1,2))
    print("****Sleeping is over")   
    print("-----------------------------------------------------------------------\n")   

    # get actor name
    #myActorName = MyActorSoup.find('span', class_ = 'sc-7f1a92f5-1 benbRT').string
    myActorName = MyActorSoup.find('span', class_ = 'hero__primary-text').string
    print("did it work?: ", myActorName)
    # section on html page where films are located
    AllFimsbyActor = MyActorSoup.find('div', class_='ipc-accordion__item ipc-accordion__item--expanded accordion-item')
    
    # select in section where individual films are found
    ListofFilms = AllFimsbyActor.find_all('div', class_ = 'ipc-metadata-list-summary-item__c')

    # go through each movie
    for each_ListofFilms in ListofFilms:
        print("Searching in next movie within same actor....")
        each_FilmYear = ""
        each_FilmGenre = ""
        each_FilmRating = 0.0
        each_FilmTitle = ""

        # GET FILM TITLE
        myActorFilm_solo_title = each_ListofFilms.find("a", class_= "ipc-metadata-list-summary-item__t")
        each_FilmTitle = myActorFilm_solo_title.string #the title
        movie_url = each_ListofFilms.a['href']
        print("visting URL:", baseURL + movie_url)
        myActorFilm_solo_year = each_ListofFilms.find("span", class_ = 'ipc-metadata-list-summary-item__li')
        each_FilmYear = myActorFilm_solo_year.string #film year

        ### GET FILM RATING
        myFilm_rating = each_ListofFilms.find("span", class_ = 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ipc-rating-star-group--imdb')
        if myFilm_rating:
            each_FilmRating = myFilm_rating.text # film rating
        else:
            each_FilmRating = 0.0
        print("Extracted Film Rating:", each_FilmRating)

        ### GET URL to find FILM GENRE
        rqMyFilm = rq.get(baseURL + movie_url, headers=HEADERS)
        print("Page where genre is extracted:", baseURL + movie_url)
        ### GET FILM GENRE
        soupMyFilm = BeautifulSoup(rqMyFilm.text, 'lxml')
        myGenres = soupMyFilm.find("a", class_  = "ipc-chip ipc-chip--on-baseAlt")
        if myGenres != None:
            each_FilmGenre = str(myGenres.text)
        else:
            each_FilmGenre = "no genre available"
        print("\nExtracted Film Genre:", each_FilmGenre)
        print("***********************************Saving in DB*************************************\n")
            # PRINT TO CONSOLE
        print("NEW saved movie from " + myActorName + " called " + each_FilmTitle)
        saveData.saveNewFilm(myActorName, each_FilmTitle, each_FilmYear, each_FilmGenre, each_FilmRating)

def getAllAwardsOfActor(Link_To_ActorsAwards):
    print("accessing webpage to scrub awards: ", Link_To_ActorsAwards)
    rqMyAwards = rq.get(Link_To_ActorsAwards, headers=HEADERS)  # request the actor URL
    # select whole page
    soupMyAwards = BeautifulSoup(rqMyAwards.text, 'lxml')

    # we need to randomize speed of searching to avoid being detected by website
    print("\n-----------------------------------------------------------------------")
    print("****Sleeping to allow data extraction..")
    sleep(randint(1,2))
    print("****Sleeping is over")   
    print("-----------------------------------------------------------------------\n")  

    # select the one place, where the categories for awards are located
    myAwards_all = soupMyAwards.find('div', class_ = "sc-a83bf66d-1 gYStnb ipc-page-grid__item ipc-page-grid__item--span-2")
    # select all categories where several awards are located
    myAward_categories = myAwards_all.find_all('section', class_ = "ipc-page-section ipc-page-section--base")
    # Grab the name of the actor for our Database Primary Key   
    myActorName_h2 = soupMyAwards.find('h2', class_ = 'sc-a885edd8-9 dcErWY')
    myActorName = myActorName_h2.string

    for EachAwardCategory in myAward_categories: # find each category of awards
        # now we must find each individual awards in each award category
        AllAwardsinCategory = EachAwardCategory.find_all('li', class_ = 'ipc-metadata-list-summary-item sc-15fc9ae6-1 kZSOHj')

        for EachAward in AllAwardsinCategory:
            # Get award name
            EachAwardName_tag = EachAward.find('span', class_ = 'ipc-metadata-list-summary-item__li awardCategoryName')
            #print(EachAwardName_tag)
            #print("aaand")
            if EachAwardName_tag != None:
                award_name = str(EachAwardName_tag.text)
            else:
                award_name = "no description available"

            #Get award year
            award_yea_tag = EachAward.find('a', class_ = "ipc-metadata-list-summary-item__t")
            award_year = str(award_yea_tag.text)
            award_description = "N/A"

             # grab just the first word---> which is the year of the award
            words = award_year.split()
            first_word = words[0]

            #print(myActorName + " has won the award " + award_name)

            # Function call to get each award
            saveData.saveNewAward(first_word, award_name, award_description, myActorName)