#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate a Dataset (TMDb Movies)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# >### **Overview**
# >Using TMDb movies dataset to complete my Data Analysis project. 
# 
# >This data set contains information about 10 thousand movies collected from The Movie Database (TMDb), including user ratings and revenue. It consist of 21 columns.   
# 
# >#### **Question that can analyised from this data set**
# > 1. Movies which had most and least profit
# 
# >----------------------------------------------------------------------
# > 2. Successful genres (with respect to the successful movies).
# > 3. Most frequent cast  (with respect to the successful movies).
# > 4. What is the best budget to acheive the most profit(relation between budget & profit).
# > 5. Does the cinema production increases by the time? (no. of movies increases each year?).
# > 6. Average budget  (with respect to the successful movies)
# > 7. Average revenue  (with respect to the successful movies)
# > 8. Average duration  (with respect to the successful movies)

# In[1]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > reading dataset from csv file and cleaning it by deleting unused data.
# 
# ### General Properties

# In[2]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.

#reading data in dataframe object "df"
df = pd.read_csv('tmdb-movies.csv')
#showing data first 5 rows
df.head()


# ### info about columns and their datatypes.

# In[3]:


#showind info about data 
df.info()


# >**observation:**
# from data head and info we see that many columns is not neccessary in our analysis,
# some columns not in the suitable data type for analysis

# In[4]:


df.describe()


# >budget, revenue and runtime columns has many 0's

# 
# ### Data Cleaning (removing unused rows and columns)
# 
# > **removing unused columns**: *('id', 'imdb_id', 'popularity', 'budget_adj', 'revenue_adj', 'homepage', 'keywords', 'overview', 'production_companies', 'vote_count', 'vote_average')*
# 
# > **replacing zero's by NaN.**
# 
# > **removing duplicate rows.**
# 
# > **removing rows with null values.**

# ### deleting unused cols.

# In[5]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.
cols_to_delete = [ 'id', 'imdb_id', 'popularity', 'budget_adj', 'revenue_adj', 'homepage', 'keywords', 'overview', 'production_companies', 'vote_count', 'vote_average']

df.drop(cols_to_delete, axis=1, inplace=True)


# **showing head of dataframe after deleting columns**

# In[6]:


df.head()


# > ***columns deleted successfully***

# ### deleting 0's in budget, revenue and runtime cols.

# In[7]:


df[['budget', 'revenue', 'runtime']] = df[['budget', 'revenue', 'runtime']].replace(0, np.NAN)


# In[8]:


df.describe()


# > *zero's deleted successfully*

# ### deleting duplicate rows

# In[9]:


rows_before = df.shape[0]

#removing duplicated rows
df.drop_duplicates(inplace=True)

print("{} duplicate rows removed successfully".format(rows_before-df.shape[0]))


# ### deleting null values

# In[10]:


#removing null values from budget and revenue cols.
df.dropna(subset=['budget', 'revenue'], inplace=True)


# In[11]:


#changing formats of cols.
df.release_date = pd.to_datetime(df.release_date)

df[['budget', 'revenue']] = df[['budget', 'revenue']].astype(int)


# In[12]:


df.dtypes


# <a id='eda'></a>
# ## Exploratory Data Analysis

# ### profit of each movie

# In[13]:


#insert new column in dataframe after budget and revenue columns
df.insert(2, 'profit', df['revenue']- df['budget'])

df.head(3)


# In[14]:


#movies with highest profit
df.original_title[df.profit.sort_values(ascending=False).index[:5]]


# from the list above:
# >*Avatar is the movie with highest profits*

# ## creating data frame "successful movies" (the movies with high profits)

# In[15]:


#subsetting dataframe to take movies with high profits only (movies with profit > profits median)
successful_movies = df[df['profit']> df.profit.median()]


# ### Successful genres (with respect to the profitable movies).

# In[16]:


#freq function takes a column name and return the count of each value in this column
def freq(col):
    data = successful_movies[col].dropna()
    l = []
    for row in data:
        l.extend(row.split('|'))
    
    l = pd.Series(l)
    return l.value_counts(ascending=False)


# In[17]:


freq('genres').head()


# > **most successful genres is (Drama, Comedy, Action, Thriller, Adventure)**

# In[18]:


y_label="Genre"
p = freq('genres').sort_values(ascending=True).plot.barh(ylabel=y_label)
p.set_title('Most common genres', fontsize=15)
p.set_xlabel('Number of movies', fontsize=12)
p.set_ylabel('Genre', fontsize=12)
plt.show()


# > **bar plot to visualize the successful genres**

# In[19]:


freq_cast = freq('cast')
freq_cast.head(8)


# > **showing top actors:**(Tom Cruise, Brad Pitt, Tom Hanks, Robert De Niro, Bruce Willis)

# In[20]:


freq_cast.sort_values(ascending=True, inplace=True)


# In[21]:


c = freq_cast.tail(10).plot.barh()
c.set_title('Most successful actors', fontsize=15)
c.set_xlabel('Number of movies', fontsize=12)
c.set_ylabel('Actor', fontsize=12)
plt.show()


# > **using barplot to show the most 10 successful actors**

# ### relation between budget & profit.

# In[43]:


#making scatter plot to visualize the relation
plt.figure(figsize=(12,6))
plt.scatter(successful_movies['budget'], successful_movies['profit'])
plt.xlabel('budget', fontsize=15)
plt.ylabel('profit', fontsize=15)
plt.show()


# > **it seems like by increasing the budget the profit increases, but at a point where the budget=225million the profit decreases**

# ### count of movies in each year.
# > histogram displays the relation between time and the number of movies.

# In[66]:


years = successful_movies['release_year']

plt.hist(years, bins=20)
plt.xlabel('year', fontsize=12)
plt.ylabel('number of movies', fontsize=12)
plt.show()


# > **the histogram skewed to the left, so we conclude that the number of movies in year increases by the time.**

# #### finding average budget of successful movies:

# In[22]:


#finding average budget of successful movies
print(successful_movies['budget'].mean())


# ### finding average revenue of successful movies:

# In[23]:


print(successful_movies.revenue.mean())


# ### Average duration time of successful movies:

# In[24]:


print(successful_movies['runtime'].mean(), 'Minute')


# <a id='conclusions'></a>
# ## Conclusions
# 
# > **Movie to be in successful criteria**
# > 1. Average Budget must be around 50 millon dollar
# > 2. Average duration of the movie must be 112 minutes 
# > 3. Any one of these should be in the cast :Tom Cruise, Brad Pitt, Tom Hanks, Sylvester Stallone,Bruce Willis.
# > 4. Best budget to make most profit is about 225 million.
# > 5. By the time the number of movies in year increases, (concluded from the histogram).
# > 6. Genre must be : Drama, Comedy, Action, Thriller, Adventure.
# >
# > By doing all this the movie might be one of the hits and hence can earn an average revenue of around 192 million  dollar.
# >
# >**Limitations: **We are not sure if the data provided to us is completel corect and up-to-date. As mentioned before the budget and revenue column do not have currency unit, it might be possible different movies have budget in different currency according to the country they are produce in. So a disparity arises here which can state the complete analysis wrong. Dropping the rows with missing values also affected the overall analysis.

# In[ ]:




