#!/usr/bin/env python
# coding: utf-8

# ## Building a Basic Recommendation System
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

credits = pd.read_csv("tmdb_5000_credits.csv")
movies_df = pd.read_csv("tmdb_5000_movies.csv")

#https://www.kaggle.com/tmdb/tmdb-movie-metadata




#credits.head()



movies_df.head()




print("Credits:",credits.shape)
print("Movies Dataframe:",movies_df.shape)




credits_column_renamed = credits.rename(index=str, columns={"movie_id": "id"})
movies_df_merge = movies_df.merge(credits_column_renamed, on='id')
#movies_df_merge.head()




movies_cleaned_df = movies_df_merge.drop(columns=['homepage', 'title_x', 'title_y', 'status','production_countries'])
#movies_cleaned_df.head()


#movies_cleaned_df.info()


# ### Using Weighted average for each movie's  Average Rating

# ![image.png](attachment:image.png)
# 
# 
#                   Source: http://trailerpark.weebly.com/imdb-rating.html?source=post_page---------------------------


# Calculate all the components based on the above formula
v=movies_cleaned_df['vote_count']
R=movies_cleaned_df['vote_average']
C=movies_cleaned_df['vote_average'].mean()
m=movies_cleaned_df['vote_count'].quantile(0.70)




movies_cleaned_df['weighted_average']=((R*v)+ (C*m))/(v+m)


#movies_cleaned_df.head()




movie_sorted_ranking=movies_cleaned_df.sort_values('weighted_average',ascending=False)
movie_sorted_ranking[['original_title', 'vote_count', 'vote_average', 'weighted_average', 'popularity']].head(20)

weight_average=movie_sorted_ranking.sort_values('weighted_average',ascending=False)
popularity=movie_sorted_ranking.sort_values('popularity',ascending=False)


# ### Recommendation based on scaled weighted average and popularity score(Priority is given 50% to both)



from sklearn.preprocessing import MinMaxScaler

scaling=MinMaxScaler()
movie_scaled_df=scaling.fit_transform(movies_cleaned_df[['weighted_average','popularity']])
movie_normalized_df=pd.DataFrame(movie_scaled_df,columns=['weighted_average','popularity'])
movie_normalized_df.head()


#

movies_cleaned_df[['normalized_weight_average','normalized_popularity']]= movie_normalized_df


#movies_cleaned_df.head()


movies_cleaned_df['score'] = movies_cleaned_df['normalized_weight_average'] * 0.5 + movies_cleaned_df['normalized_popularity'] * 0.5
movies_scored_df = movies_cleaned_df.sort_values(['score'], ascending=False)
movies_scored_df[['original_title', 'normalized_weight_average', 'normalized_popularity', 'score']].head(20)




scored_df = movies_cleaned_df.sort_values('score', ascending=False)


# ### Content Based Recommendation System
# 
# Now lets make a recommendations based on the movie’s plot summaries given in the overview column. So if our user gives us a movie title, our goal is to recommend movies that share similar plot summaries.



#movies_cleaned_df.head(1)['overview']


from sklearn.feature_extraction.text import TfidfVectorizer

# Using Abhishek Thakur's arguments for TF-IDF
tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

# Filling NaNs with empty string
movies_cleaned_df['overview'] = movies_cleaned_df['overview'].fillna('')


# Fitting the TF-IDF on the 'overview' text
tfv_matrix = tfv.fit_transform(movies_cleaned_df['overview'])


#tfv_matrix.shape



from sklearn.metrics.pairwise import sigmoid_kernel

# Compute the sigmoid kernel
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)



# Reverse mapping of indices and movie titles
indices = pd.Series(movies_cleaned_df.index, index=movies_cleaned_df['original_title']).drop_duplicates()



#indices

def give_rec(title, sig=sig):
    # Get the index corresponding to original_title
    idx = indices[title]

    # Get the pairwsie similarity scores 
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies 
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:11]

    # Movie indices
    movie_indices = [i[0] for i in sig_scores]

    # Top 10 most similar movies
    return movies_cleaned_df['original_title'].iloc[movie_indices]


# Testing our content-based recommendation system with the seminal film Spy Kids
#print(give_rec('Spy Kids'))


# We use weighted avg as well as popularity becz many of the movies which is popular 
# but vewers are not giving any votes so for considering them 

#GUI
from tkinter import *  
import pandas as pd
from sklearn.model_selection import train_test_split

from tkinter import ttk
from tkinter import messagebox



def similar_movie():
    
    sim_str = ''
    sim_list = []
    try:
        movie_name = str(user_id.get())
        if(len(movie_name)<1):
            messagebox.showinfo('Try Again','No Matched Movie Found')
        else:
            sim_list = give_rec(movie_name)
            print(sim_list)
            sim_str = '\n'.join(sim_list)
            lbl['text'] = sim_str
        # print(sim_str)
    except:
        messagebox.showinfo('Try Again','No Matched Movie Found')




omk = Tk()  
omk.title("Movie Recommendation System")
omk.resizable(height = None, width = None)

lbl = Label(omk, text = "Movie Recommender System",font=("Times New Roman", 20))
lbl.grid(row=0,column=0,padx=(10, 10),pady=(10 ,10))


frame = ttk.Frame(omk, padding=10)
frame.grid(row=3,column=0)

global user_id


user_id = None

lbl1 = Label(frame, text = "Enter Movie Name",font=("Times New Roman", 10))
lbl1.grid(row=2,column=0,padx=(10, 0))

entry = Entry(frame, width=25)
entry.grid(row=4,column=0,padx=(10, 0))
user_id = entry





btn2 = ttk.Button(frame,text = 'Similar Movies', command=similar_movie)
btn2.grid(row=5,column=0,padx=(10,0))


omk.mainloop()  








