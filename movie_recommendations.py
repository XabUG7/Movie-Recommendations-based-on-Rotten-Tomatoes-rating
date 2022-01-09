import requests
import json

#Given a list of movies, get recommended more movies based on their Rotten Tomatoes rating

def get_movies_from_tastedive(title, title_type = "movies", limit = "5" ): #gets related movies to a
    baseURL = "https://tastedive.com/api/similar"                          #input movie title 
    params = {"q":title,"type":title_type, "limit": limit}                 #tastedive web
    api_resp = requests.get(baseURL, params)
    
    return json.loads(api_resp.text)

def extract_movie_titles(title_name):                      #Extracts the titles from the information 
    title_list = []                                        #given by tastedive web
    titles_dict = get_movies_from_tastedive(title_name)
    for title_data in titles_dict["Similar"]["Results"]:
        title_list.append(title_data["Name"])
        
    return title_list

def get_related_titles(title_list):                       #creates a list of recommended movies 
    related_titles_list = []                              #with one movie title as an input
    for title in title_list:
        titles_related_to_1 = extract_movie_titles(title)
        for name in titles_related_to_1:
            if name not in related_titles_list:
                related_titles_list.append(name)            
 
    return related_titles_list


def get_movie_data(title, r = "json"):   #gets information of a movie in a dictionary
    baseURL = "http://www.omdbapi.com/"  #including Rotten Tomatoes rating
    params = {"t":title, "r":r}
    api_resp = requests.get(baseURL, params)
    
    return json.loads(api_resp.text)

def get_movie_rating(title):    #get the Rotten Tomatoes rating of a movie
    movie_data_dict = get_movie_data(title)
    for ratings in movie_data_dict["Ratings"]:
        if ratings["Source"] == "Rotten Tomatoes":
            return int(ratings["Value"][:2])
    return 0


def get_sorted_recommendations(title_list):          #movie recommendations sorted by 
    rel_title_list = get_related_titles(title_list)  #Rotten Tomatoes rating with 
    sorted_list_alf = sorted(rel_title_list)         #a list of movies as input
    sorted_list_by_rating = sorted(sorted_list_alf, key=get_movie_rating, reverse = True)
    
    return sorted_list_by_rating




