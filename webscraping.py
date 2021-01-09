from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as Ureq
import re

#This code pulls data from IMDB website for movies in genre Comedy (top 10,000) and saves the data in a CSV file.

filename = "Top 10000 Comedy Movies.csv"
f = open(filename, "w")
headers = "Movie, Release Year, Certificate, Runtime, Genre, Rating\n"
f.write(headers)

for i in range(1,10001,50):
    # The For loop runs with page entry. Every page has count of 50 entries (movies or data), and changes with every page, thus the count number is used as a counter to extract data.
    page_url = "https://www.imdb.com/search/title/?genres=comedy&start=" + str(i) + "&explore=title_type,genres&ref_=adv_nxt"
    uclient = Ureq(page_url)
    page_soup = soup(uclient.read(), "html.parser")
    uclient.close()
    containers = page_soup.findAll("div", {"class":"lister-item mode-advanced"})

    for contain in containers:
        title_movie = contain.h3.a.text
        # title
        year_released = contain.findAll("span", {"class": "lister-item-year text-muted unbold"})
        # year_released[0].text
        year_movie = year_released[0].text.strip(" ").strip("(").strip(")")
        # year_released = contain.findAll("span", {"class": "lister-item-year text-muted unbold"})
        # # year_released[0].text
        # year_movie = year_released[0].text.strip(" ").strip("(").strip(")")
        # if year_movie == "":
        #     year_movie = 'NA'
        # else:
        #     # len(year_movie)
        #     year_movie = re.split(r'[–()\s]\s*', year_movie)
        #     if len(year_movie) >= 3:
        #         year_movie = year_movie[2]
        #     else:
        #         year_movie = year_movie[0]
        # year_movie
        # year_released = contain.findAll("span",{"class":"lister-item-year text-muted unbold"})
        # year_movie = year_released[0].text.strip().strip('()').strip('(')
        # year_movie = re.split(r'[–,(]\s*',year_movie)
        # if len(year_movie) == 2:
        #     if year_movie[1] == "":
        #         movie_year = year_movie[0]
        #     else:
        #         year_movie_1 = year_movie[1].strip("()").strip().strip(" ")
        #     movie_year = year_movie[1]
        # else:
        #     movie_year = year_movie[0]

        certificate = contain.findAll("span", {"class": "certificate"})
        if certificate == []:
            certificate = 'NA'
        else:
            certificate = certificate[0].text

        Movie_Runtime = contain.findAll("span",{"class":"runtime"})
        if Movie_Runtime == []:
            Run_Time = 'NA'
        else:
            Run_Time = Movie_Runtime[0].text

        title_movie = title_movie.replace(",", "-")
        Movie_genre = contain.findAll("span",{"class":"genre"})
        Genre = Movie_genre[0].text.strip('\n').strip().replace(",","|")
        if contain.strong is None:
            Rating = 'NA'
        else:
            Rating = contain.strong.text
        # meta_score = contain.findAll("span",{"class":"metascore favorable"})
        # Metascore = meta_score[0].text.strip()
        f.write(title_movie + "," + year_movie + "," + certificate + "," + Run_Time + "," + Genre + "," + Rating + "\n")

f.close()
