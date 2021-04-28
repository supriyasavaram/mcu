from bs4 import BeautifulSoup
import requests
import json

mcu_list_url = 'https://www.imdb.com/list/ls066946827/'
res = requests.get(mcu_list_url)
mcu_soup = BeautifulSoup(res.text, features="html.parser")

movie_details = mcu_soup.select(".mode-detail")

all_directors = {'Jon Favreau': 1, 'Louis Leterrier': 2, 'Kenneth Branagh': 3, 'Joe Johnston': 4, 'Joss Whedon': 5, 'Shane Black': 6, 'Alan Taylor': 7, 'Anthony Russo': 8, 'Joe Russo': 9, 'James Gunn': 10,
                 'Peyton Reed': 11, 'Scott Derrickson': 12, 'Jon Watts': 13, 'Taika Waititi': 14, 'Ryan Coogler': 15, 'Anna Boden': 16, 'Ryan Fleck': 17, 'Cate Shortland': 18, 'Chloé Zhao': 19, 'Destin Daniel Cretton': 20, 'Sam Raimi': 21}
all_stars = {'Robert Downey Jr.': 1, 'Gwyneth Paltrow': 2, 'Terrence Howard': 3, 'Jeff Bridges': 4, 'Edward Norton': 5, 'Liv Tyler': 6, 'Tim Roth': 7, 'William Hurt': 8, 'Mickey Rourke': 9, 'Don Cheadle': 10, 'Chris Hemsworth': 11, 'Anthony Hopkins': 12, 'Natalie Portman': 13, 'Tom Hiddleston': 14, 'Chris Evans': 15, 'Hugo Weaving': 16, 'Samuel L. Jackson': 17, 'Hayley Atwell': 18, 'Scarlett Johansson': 19, 'Jeremy Renner': 20, 'Guy Pearce': 21, 'Stellan Skarsgård': 22, 'Joe Russo': 23, 'Robert Redford': 24, 'Chris Pratt': 25, 'Vin Diesel': 26, 'Bradley Cooper': 27, 'Zoe Saldana': 28, 'Mark Ruffalo': 29, 'Paul Rudd': 30, 'Michael Douglas': 31, 'Corey Stoll': 32, 'Evangeline Lilly': 33, 'Sebastian Stan': 34, 'Benedict Cumberbatch': 35,
             'Chiwetel Ejiofor': 36, 'Rachel McAdams': 37, 'Benedict Wong': 38, 'Dave Bautista': 39, 'Tom Holland': 40, 'Michael Keaton': 41, 'Marisa Tomei': 42, 'Cate Blanchett': 43, 'Chadwick Boseman': 44, 'Michael B. Jordan': 45, "Lupita Nyong'o": 46, 'Danai Gurira': 47, 'Michael Peña': 48, 'Walton Goggins': 49, 'Ryan Fleck': 50, 'Brie Larson': 51, 'Ben Mendelsohn': 52, 'Jude Law': 53, 'Jake Gyllenhaal': 54, 'Pom Klementieff': 55, 'Elizabeth Debicki': 56, 'Karen Gillan': 57, 'Florence Pugh': 58, 'David Harbour': 59, 'Rachel Weisz': 60, 'Angelina Jolie': 61, 'Salma Hayek': 62, 'Gemma Chan': 63, 'Richard Madden': 64, 'Martin Freeman': 65, 'Simu Liu': 66, 'Awkwafina': 67, 'Tony Chiu-Wai Leung': 68, 'Fala Chen': 69, 'Elizabeth Olsen': 70}

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
        fields['runtime'] = ''

    # director(s)
    directors = movie.select(
        ".text-small a:nth-child(2) , .text-muted a:nth-child(1)")
    if directors:
        # for director in directors:
        #     director = director.text.strip()
        #     if director not in all_directors:
        #         all_directors.append(director)
        d = []
        for director in directors:
            director = all_directors[director.text.strip()]
            d.append(director)
        fields['directors'] = d
    else:
        fields['directors'] = ''

    # # stars
    stars = movie.select(".text-small a+ a , .ghost+ a")
    if stars:
        # for star in stars:
        #     star = star.text.strip()
        #     if star not in all_stars:
        #         all_stars.append(star)
        s = []
        for star in stars:
            star = star.text.strip()
            s.append(all_stars[star])
        fields['actors'] = s
    else:
        fields['actors'] = ''

    cur_movie['fields'] = fields

    all_movies.append(cur_movie)

j = json.dumps(all_movies)
print(j)

# print(all_stars)
