from bs4 import BeautifulSoup
import requests
import json

mcu_list_url = 'https://www.imdb.com/list/ls066946827/'
res = requests.get(mcu_list_url)
mcu_soup = BeautifulSoup(res.text, features="html.parser")

movie_details = mcu_soup.select(".mode-detail")

all_movies = []
i = 1
for movie in movie_details:
    cur_movie = {}

    # pk 
    cur_movie['pk'] = i
    i += 1

    # model
    cur_movie['model'] = 'mcu_site.movie'

    fields = {}
    # movie title
    title = movie.select_one(".lister-item-header a").text
    fields['title'] = title

    # synopsis
    synopsis = movie.select_one(".ratings-metascore+ p")
    if synopsis: 
        fields['synopsis'] = synopsis.text.strip()
    else:
        fields['synopsis'] = ''
    
    # date
    date = movie.select_one(".text-muted.unbold")
    if date:
        fields['year'] = date.text.strip()
    else:
        fields['year'] = ''
    
    # runtime
    runtime = movie.select_one(".runtime")
    if runtime:
        fields['runtime'] = runtime.text.strip()
    else:
        fields['runtime']  = ''
    
    cur_movie['fields'] = fields
    # # director(s)
    # directors = movie.select(".text-small a:nth-child(2) , .text-muted a:nth-child(1)")
    # if directors:
    #     d = []
    #     for director in directors:
    #         d.append(director.text.strip())
    #     cur_movie['directors'] = d
    # else:
    #     cur_movie['directors'] = ''
    
    # # stars
    # stars = movie.select(".text-small a+ a , .ghost+ a")
    # if stars:
    #     s = []
    #     for star in stars:
    #         s.append(star.text.strip())
    #     cur_movie['stars'] = s
    # else:
    #     cur_movie['stars'] = ''
    
    all_movies.append(cur_movie)

j = json.dumps(all_movies)
print(j)