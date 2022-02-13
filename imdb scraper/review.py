import requests
from bs4 import BeautifulSoup
import json
import re

def clean_data(data):
    regex=re.compile("\n{1,}(\s+)?")
    new_data=re.sub(regex,"",data)
    return new_data

class Movie:
    def __init__(self,title,year,rating,user_reviews,rated,hours,genre,rdate,summary,cast):
        self.title=title
        self.year=year
        self.rating=rating
        self.user_reviews=user_reviews
        self.rated=rated
        self.hours=hours
        self.genre=genre
        self.rdate=rdate
        self.summary=summary
        self.cast=cast
    
    def __str__(self):
        string="title:{}\n year:{}\n rating:{}\n user_reviews:{}\n rated:{}\n hours:{}\n genre:{}\n release-date:{}\n summary:{}\n\n cast:\n".format(self.title,self.year,self.rating,self.user_reviews,self.rated,self.hours,self.genre,self.rdate,self.summary)
        
        for item in self.cast:
            string+= item + " : " + self.cast[item] + "\n"
        
        return string

def scrape_movie(movie):
    movie_json="https://v2.sg.media-imdb.com/suggestion/{}/{}.json".format(movie[0].lower(),movie)
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}

    data_json=requests.get(movie_json).content
    data=json.loads(data_json)
    #getting the movie title for scraping data
    id_movie=data["d"][0]["id"]
    url="https://imdb.com/title/{}".format(id_movie)
    html=requests.get(url,headers=headers).content

    #creating the soup
    soup=BeautifulSoup(html,'html.parser')

    #getting title and year
    title_wrapper=soup.find(class_="title_wrapper")
    title,year=title_wrapper.h1.text.split("(")

    #removing unwanted parts from year
    year=re.sub(r"[()]","",year)

    #rating and no. of users reviewed
    rating=soup.find(class_="ratingValue")
    rating_value=rating.text.strip("\n")
    user_reviews=rating.strong['title']

    #rated, length , genre and release date of the movie
    other_info=soup.find(class_="subtext").text
    rated,hours,genre,release_date=list(map(str.strip,other_info.split("|")))

    #removing unwanted spaces from genre
    genre=genre.replace("\n","")

    #summary of the movie
    summary=clean_data(soup.find(class_="summary_text").text)

    #cast of the movie
    cast_list=soup.find(class_="cast_list")
    cast_mem=cast_list.findAll("td",class_='')
    character=cast_list.findAll("td",class_="character")

    mem_and_char={}
    for mem,char in zip([i.text for i in cast_mem],[i.text for i in character]):
        
        #removing unwanted spaces and newlines from the data
        mem=clean_data(mem)
        char=clean_data(char)

        #adding to dictionary
        mem_and_char[mem]=char

    # final_data={
    #     "title":title,
    #     "year":year,
    #     "rating":rating_value,
    #     "user_reviews":user_reviews,
    #     "rated":rated,
    #     "hours":hours,
    #     "genre":genre,
    #     "rdate":release_date,
    #     "summary":summary,
    #     "cast":mem_and_char,
    # }
    movie=Movie(title,year,rating_value,user_reviews,rated,hours,genre,release_date,summary,mem_and_char)
    return movie

print(scrape_movie("Harry Potter and the golbet of fire"))