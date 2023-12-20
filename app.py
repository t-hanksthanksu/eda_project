import streamlit as st
import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt





def get_movie_data(api_key, movie_title):
    base_url = "http://www.omdbapi.com/"
    params = {
        "apikey": api_key,
        "t": movie_title,  
        "type": "movie",
        "plot": "short",
        "tomatoes": "true",  
        "r": "json",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return data
    else:
        return None

def extract_movie_info(movie):
    return {
        "Title": movie.get("Title", ""),
        "Year": movie.get("Year", ""),
        "IMDbRating": movie.get("imdbRating", ""),
        "TomatoRating": next(
            (rating["Value"] for rating in movie.get("Ratings", []) if rating["Source"] == "Rotten Tomatoes"),
            "N/A"
        ),
    }

def save_to_csv(data, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["Title", "Year", "IMDbRating", "TomatoRating"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

st.title("Leonardo DiCaprio vs. Brad Pitt Movie Ratings Comparison")
st.sidebar.title("User Input")

with open("api_key_omdb.txt", "r") as key_file:
    api_key = key_file.read().strip()


# Movies for Leonardo DiCaprio and Brad Pitt
movies_leo = [
    "Killers of the Flower Moon", "Don't Look Up", "Once Upon a Time in Hollywood",
    "The Revenant", "The Audition", "The Wolf of Wall Street", "The Great Gatsby",
    "Titanic: Deleted Scenes", "Django Unchained", "J. Edgar", "Inception: The Cobol Job",
    "Inception", "Shutter Island", "Revolutionary Road", "Body of Lies", "Blood Diamond",
    "The Departed", "The Aviator", "Catch Me If You Can", "Gangs of New York", "Don's Plum",
    "The Beach", "Celebrity", "The Man in the Iron Mask", "Titanic", "Marvin's Room",
    "Romeo + Juliet", "Total Eclipse", "The Quick and the Dead", "The Basketball Diaries",
    "The Foot Shooting Party", "What's Eating Gilbert Grape", "This Boy's Life"
]
movies_brad = [
    "World War Z", "Wolves", "War Machine", "Voyage of Time", "Untitled Joseph Kosinski film",
    "True Romance", "Troy", "The Tree of Life", "Thelma & Louise", "The Lost City",
    "The Counselor", "The Big Short", "The Audition", "Spy Game", "Snatch",
    "Sleepers", "Sinbad: Legend of the Seven Seas", "Seven Years in Tibet", "Seven",
    "A River Runs Through It", "Once Upon a Time in Hollywood", "Ocean's Twelve",
    "Ocean's Eleven", "Ocean's Thirteen", "No Way Out", "No Man's Land", "Mr. & Mrs. Smith",
    "Moneyball", "The Mexican", "Megamind", "Meet Joe Black", "Less than Zero",
    "Legends of the Fall", "Killing Them Softly", "Kalifornia", "Johnny Suede",
    "Interview with the Vampire", "Inglourious Basterds", "Hunk", "Happy Together",
    "Happy Feet Two", "Fury", "Fight Club", "The Favor", "The Devil's Own",
    "Deadpool 2", "The Dark Side of the Sun", "Cutting Class", "The Curious Case of Benjamin Button",
    "Cool World", "Contact", "Confessions of a Dangerous Mind", "By the Sea",
    "Burn After Reading", "Bullet Train", "Being John Malkovich", "Babylon",
    "Babel", "The Assassination of Jesse James by the Coward Robert Ford", "Allied",
    "Ad Astra", "Across the Tracks", "12 Years a Slave", "12 Monkeys"
]

# Leo
leo_movies_info = []
for movie_title in movies_leo:
    movie_data = get_movie_data(api_key, movie_title)
    if movie_data:
        leo_movies_info.append(extract_movie_info(movie_data))

# Brad
brad_movies_info = []
for movie_title in movies_brad:
    movie_data = get_movie_data(api_key, movie_title)
    if movie_data:
        brad_movies_info.append(extract_movie_info(movie_data))

all_movies_info = leo_movies_info + brad_movies_info

save_to_csv(all_movies_info, "movies_ratings_comparison.csv")

print("Data successfully saved to movies_ratings_comparison.csv")

#finding avergaes
def calculate_average_scores(data):
    imdb_scores = [float(movie["IMDbRating"]) if movie["IMDbRating"] != "N/A" else 0 for movie in data]
    tomato_scores = [float(movie["TomatoRating"].rstrip('%')) if movie["TomatoRating"] != "N/A" else 0 for movie in data]

    average_imdb = sum(imdb_scores) / len(imdb_scores) if imdb_scores else 0
    average_tomato = sum(tomato_scores) / len(tomato_scores) if tomato_scores else 0

    return average_imdb, average_tomato

#calculate averages
average_imdb_leo, average_tomato_leo = calculate_average_scores(leo_movies_info)
average_imdb_brad, average_tomato_brad = calculate_average_scores(brad_movies_info)

# # Plotting bar graphs
# def create_bar_graph(labels, scores, xlabel, ylabel, title):
#     x = range(len(labels))

#     plt.bar(x, scores, color='blue')
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title)
#     plt.xticks(x, labels)
#     plt.show()

# Plotting bar graphs
st.subheader("Average IMDb Scores")
st.bar_chart({f"Average IMDb Score - {labels_imdb[i]}": average_imdb_scores[i] for i in range(len(labels_imdb))})
st.pyplot()

st.subheader("Average Rotten Tomatoes Scores")
st.bar_chart({f"Average Rotten Tomatoes Score - {labels_tomato[i]}": average_tomato_scores[i] for i in range(len(labels_tomato))})
st.pyplot()


# # IMDb Scores
# labels_imdb = ['Leonardo DiCaprio', 'Brad Pitt']
# average_imdb_scores = [average_imdb_leo, average_imdb_brad]
# create_bar_graph(labels_imdb, average_imdb_scores, 'Actor', 'Average IMDb Score', 'Average IMDb Scores for Leonardo DiCaprio and Brad Pitt Movies')

# # Rotten Tomatoes Scores
# labels_tomato = ['Leonardo DiCaprio', 'Brad Pitt']
# average_tomato_scores = [average_tomato_leo, average_tomato_brad]
# create_bar_graph(labels_tomato, average_tomato_scores, 'Actor', 'Average Rotten Tomatoes Score', 'Average Rotten Tomatoes Scores for Leonardo DiCaprio and Brad Pitt Movies')

