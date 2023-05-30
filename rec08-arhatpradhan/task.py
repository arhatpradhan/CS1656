import json
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Task(object):
    def __init__(self, data):
        self.df = pd.read_csv(data)

    def t1(self, name):
        result = []
        weight_dictionary = {}
        #calculating weights for all the users relative to the name given
        for user in self.df.columns:
            if user == 'Alias' or user == name:
                continue
            #create a subset of the target user and everyone else who has watched the same movie
            df_subset = self.df[[name,user]][self.df[name].notnull() & self.df[user].notnull()]
            #calculate the cosine similarity
            dist = cosine(df_subset[name], df_subset[user])
            #store the weights of the individual users in a dictionary
            weight_dictionary[user] = dist

        # iterating over all the missing values in the specified user's row
        for movie in self.df.index:
            movie_name = self.df.iloc[movie , 0]
            if pd.isnull(self.df.loc[movie, name]):
                # finding the set of users who have rated this movie
                users = self.df.columns[self.df.loc[movie].notnull() & (self.df.columns != 'Alias') & (self.df.columns != name)]
                if len(users) > 0:
                    # calculating the weighted average of the ratings given by those users
                    weighted_sum = 0.0
                    weight_sum = 0.0
                    for user in users:
                        weighted_sum += weight_dictionary[user] * self.df.loc[movie, user]
                        weight_sum += weight_dictionary[user]
                    # adding the movie name and the predicted rating to the result list
                    result.append((movie_name, weighted_sum / weight_sum))
        return result
        #result with all the weights calculated 
        

    def t2(self, name):
        result = []
        movie_similarity = {}

        # calculating similarities between movies
        for movie1 in self.df.index:
            movie1_name = self.df.iloc[movie1, 0]
            similarity_scores = {}
            for movie2 in self.df.index:
                movie2_name = self.df.iloc[movie2,0]
                #calculating similarites for only movies that the user has watched
                if movie1 == movie2 or pd.isnull(self.df.loc[movie2, name]):
                    continue
                
                # calculate the cosine similarity
                similarity = cosine(self.df.loc[movie1].notnull(), self.df.loc[movie2].notnull())
                similarity_scores[movie2_name] = similarity
            # sort the movies by similarity score in descending order
            sorted_similarities = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
            movie_similarity[movie1] = sorted_similarities
        print(movie_similarity)

        # iterating over all the missing values in the specified user's row
        for movie in self.df.index:
            movie_name = self.df.iloc[movie , 0]
            if pd.isnull(self.df.loc[movie, name]):
                # calculating the weighted average of the ratings for the similar movies
                weighted_sum = 0.0
                weight_sum = 0.0
                for similar_movie, similarity_score in movie_similarity[movie]:

                    #user ratings for the most similar movie
                    user_ratings = None
                    movie_number = 0
                    for movies in self.df.index:
                        if similar_movie == self.df.iloc[movies, 0]:
                            movie_number = movies
                            user_ratings = self.df.loc[movie_number, name]
                            break

                    weighted_sum += similarity_score * user_ratings
                    weight_sum += similarity_score
                    prediction = weighted_sum/weight_sum
                    # adding the movie name and the predicted rating to the result list
                    if weight_sum > 0:
                        result.append((movie_name, prediction))
                        print(result)
                    break

        return result

    
    def t3(self, name):
        result = []
        weight_dictionary = {}

        # Calculating weights for top 10 most similar users
        for user in self.df.columns:
            if user == 'Alias' or user == name:
                continue
            # Create a subset of the target user and everyone else who has watched the same movie
            df_subset = self.df[[name, user]][self.df[name].notnull() & self.df[user].notnull()]
            # Calculate the cosine similarity
            dist = cosine(df_subset[name], df_subset[user])
            # Store the weights of the individual users in a dictionary
            weight_dictionary[user] = dist

        # Sort the dictionary by weights and pick the top 10 most similar users
        top_10 = dict(sorted(weight_dictionary.items(), key=lambda x: x[1], reverse=True)[:10])

        # Iterating over all the missing values in the specified user's row
        for movie in self.df.index:
            movie_name = self.df.iloc[movie, 0]
            if pd.isnull(self.df.loc[movie, name]):
                # Finding the set of users who have rated this movie
                users = self.df.columns[self.df.loc[movie].notnull() & (self.df.columns != 'Alias') & (self.df.columns != name)]
                if len(users) > 0:
                    # Calculating the weighted average of the ratings given by those users
                    weighted_sum = 0.0
                    weight_sum = 0.0
                    for user in users:
                        if user in top_10:
                            weighted_sum += top_10[user] * self.df.loc[movie, user]
                            weight_sum += top_10[user]
                    # Adding the movie name and the predicted rating to the result list
                    result.append((movie_name, weighted_sum / weight_sum))
        return None
        
if __name__ == "__main__":
    # using the class movie ratings data we collected in http://data.cs1656.org/movie_class_responses.csv
    t = Task('http://data.cs1656.org/movie_class_responses.csv')
    print(t.t1('BabyKangaroo'))
    print('------------------------------------')
    print(t.t2('BabyKangaroo'))
    print('------------------------------------')
    print(t.t3('BabyKangaroo'))
    print('------------------------------------')