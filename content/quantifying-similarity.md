Title: Quantifying Similarity
Date: 2016-10-26 18:32
Tags: Mathematics, Programming, Python, Similarity, Recommendations



## Problem Statement

I want to compare my last.fm dataset with that of my friend's and arrive at a metric that quantifies the similarity between us in terms of musical preferences. I'm looking at just one variable here, the number of times a particular artist is played and will approach this problem using basic Mathematics and Python. Nothing fancy.

The dataset I'm comparing mine with is about 9 times more voluminous - 9000 vs 80000 plays. I used to listen to my music primarily on my iPod so unfortunately, all that I have to show on last.fm is the music I played on my laptop and about an year of data scrobbled from Rdio. So the data I have there, though is reflective of the kind of music I listen to - post punk, indie, experimental, noise etc, it is not reflective of *all the artists* I've been listening to over the years. Luckily enough, after about an hour of frantic searching, I managed to find a backup of my ipod stats for the years 2005 - 09. *Pats past-self on his back* Now we are looking at a more respectable 34000 vs 80000

## Naive Solution

1. Find the artists present in both the datasets.
2. Taking these *n* artists as base vectors, our listening habits can then be described as vectors in this n-dimensional space, with the number of times an artist was played represented as magnitude of the component along that artist's base vector.
3. Calculate the cosine of angle between these two vectors (dot product divided by product of magnitudes) and now we have a number in the range $[0,1]$. 0 in case of no common artists at all and 1 in case of the ratio of number of plays of every common artist across the both sets is a constant.



# Thoughts
1. Using *common artists* doesn't look like a good idea. Consider this trivial edge case. A and B listen to 1000 bands each, of which 10 are common. If their playing habits were similar for these 10 bands, does that mean their music tastes are similar? Of course not. One thing that comes at the top of my head is to multiply the cosine value with a function that quantifies the magnitude of common artists relative to the total number. Some thing like proportion of common artists to the total number of artists - $\frac{n(X\cap Y)}{n(X\cup Y)}$ Alternatively, take the union of artists from both the data sets and take them as base vectors. If a user hasn't heard a particular band, his component along the base vector would be zero, thereby contributing nothing to the numerator (Dot Product) but contributing to the denominator (Product of Magnitudes) and thus decreasing the compatibility value.


2. Why dot product? How about a custom function say 1 upon 1 + Euclidean distance between the vector coordinates? How about using other metrics for distance like Minkowski distance? How about using Pearson Correlation Score? I could think of a simpler function where there is no need to bother about the concept of distance at all. Let $   a\_1, a\_2, a\_3,......, a\_n  $ be the union of artists present in both the sets and let $a\_{m}^{x}, a\_{m}^{y}$ represent the play counts of artist $a\_m $ by $X$ and $Y$ respectively. Now consider the function $$s(x) = \frac{\sum\_{i\in X \cap Y } \frac{min(a\_{i}^{x},a\_{i}^{y} )}{max(a\_{i}^{x},a\_{i}^{y} )}}{n(X \cap Y)}$$ with a range $[0,1]$. How effective would this be in quantifying what we want? It churns out 1 if and only if the play counts of all the respective common artists are exactly the same across both the users, as opposed to the naive approach where it is 1 in case of the ratio of number of plays of each artist across the both sets is constant. That can however be taken care of by normalizing the data sets before the computation.

# Results
(computed in Common Artists Mode with and without ipod data)

1. Pearson Correlation Score - 0.314 & 0.114
2. Dot Product Cosine  -  0.416 & **0.2815**
3. $ s(x) $ score - 0.296 & 0.2633

That function I created out of thin air appears to be more consistent! And also pretty close to the **29%** similarity we seem to have according to last.fm! **Whoa!** I'm assuming it's just a coincidence. Will run this function over other data sets and see how it fares.

So, in conclusion, last.fm's similarity metric is most likely based on cosine similarity among common artists.
# Code

Used [this](https://gist.github.com/bitmorse/5201491) script to download last.fm data to a text file. Removed the data that isn't relevant to the task at hand - artist, album, song ids at musicbrainz. The data set I downloaded for my user profile was unfortunately missing values(Song and Album names) at many places. Had to fix that first. Then I had to clean up my ipod data and merge it with the last.fm data. Duplication due to wrong capitalization, Spellings, 'The' issues. *Fun times.*

<br>

    from __future__ import division
    import sys
    import math


    def filedata(file):
        a = open(file, 'rw')
        b = a.readlines()
        return b


    def lastfmfreq(filedatas):
        artdict = {}
        for line in filedatas:
            first_tab = line.index('\t')
            second_tab = line.index('\t', first_tab + 1)
            art_name = line[first_tab + 1 : second_tab]
            if art_name in artdict.keys():
                artdict[art_name] += 1
            else:
                artdict[art_name] = 1
        return artdict


    def commonartists(artdict1, artdict2):
        comartdict = {}
        for artist in artdict1.keys():
            if artist in artdict2.keys():
                comartdict[artist] = (artdict1[artist], artdict2[artist])
        return comartdict

    class Vector(object):
        def __init__(self, components):
            self.components = components


        def dot_product(self, vektor):
            dimension = len(self.components)
            self_size = math.sqrt(sum([(component)**2 for component in self.components]))
            vektor_size = math.sqrt(sum([(component)**2 for component in vektor.components]))
            comp_product = [(self.components[i]) * (vektor.components[i]) for i in range[dimension]]
            magnitude_product = self_size * vektor_size
            return comp_product / magnitude_product

        def pearson(self, vektor):
            dimension = len(self.components)
            self_mean = sum(self.components)/dimension
            vektor_mean = sum(vektor.components)/dimension
            self_size = math.sqrt(sum([(component-self_mean)**2 for component in self.components]))
            vektor_size = math.sqrt(sum([(component-vektor_mean)**2 for component in vektor.components]))
            dot_product = sum([(self.components[i]-self_mean)*(vektor.components[i]-vektor_mean) for i in range(dimension)])
            magnitude_product = self_size * vektor_size
            return dot_product/magnitude_product

        def sx(self, vektor):
            dimension = len(self.components)
            numerator = sum([min(self.components[i], vektor.components[i])/max(self.components[i], vektor.components[i])
                            for i in range(dimension)])
            return (numerator/dimension)    



    if __name__ == "__main__":
        common_artists = commonartists(lastfmfreq(filedata(sys.argv[1])), lastfmfreq(filedata(sys.argv[2]))).items()
        vector1 = Vector([element[1][0] for element in common_artists])
        vector2 = Vector([element[1][1] for element in common_artists])
        print vector1.dot_product(vector2)
        print vector1.pearson(vector2)
        print vector1.sx(vector2)
<br>

# More Thoughts

1. Data of tracks that were skipped could add an extra dimension (metaphorical i.e.) to the users' perception of artists. 

2. Does the similarity function need to be symmetric?

**Update** : [Tversky index](https://en.wikipedia.org/wiki/Tversky_index) explores the notion of *asymmetric similarity*. It is *not* a similarity metric in the traditional sense, by virtue of it being asymmetric but I will dig more into the notion of asymmetric similarity anyway, may be a dedicated post sometime on how it could possibly make sense, with the help of a real world example I have in mind.

 ![](https://wikimedia.org/api/rest_v1/media/math/render/svg/593c9e7d96dc41cc82abdb13d3efb9b3b4d6cb51)
# What Next

Need to refer to literature on this and learn more about various similarity metrics. Will also be exploring the humongous user-generated-tags data released by last.fm and see if I can come up with anything interesting.

**Update**: [WOW!](http://www.iiisci.org/journal/CV$/sci/pdfs/GS315JG.pdf)


# Common Artists' Data

For those who are interested

1.    The Clash    (404, 2689)
2.    Pixies    (834, 1757)
3.    Bloc Party    (91, 1341)
4.    Wire    (79, 1331)
5.    Deerhoof    (561, 1295)
6.    Blur    (506, 1280)
7.    The Dead Milkmen    (34, 1176)
8.    Joy Division    (93, 1149)
9.    Spoon    (489, 1035)
10.    Modest Mouse    (885, 906)
11.    Gang of Four    (17, 794)
12.    The Undertones    (20, 725)
13.    Melt-Banana    (2, 676)
14.    Franz Ferdinand    (46, 666)
15.    New Order    (28, 611)
16.    Talking Heads    (70, 608)
17.    Minutemen    (1187, 587)
18.    Siouxsie and the Banshees    (35, 545)
19.    The Dandy Warhols    (74, 507)
20.    Interpol    (128, 493)
21.    Urinals    (22, 492)
22.    The Rakes    (126, 443)
23.    Sonic Youth    (215, 401)
24.    Pulp    (22, 326)
25.    Swell Maps    (3, 325)
26.    Primus    (13, 309)
27.    The Smiths    (278, 308)
28.    Glaxo Babies    (4, 306)
29.    The Fall    (279, 305)
30.    New York Dolls    (14, 305)
31.    Happy Mondays    (56, 282)
32.    Arctic Monkeys    (79, 273)
33.    The Breeders    (262, 272)
34.    The Ex    (12, 272)
35.    The Shins    (387, 259)
36.    Graham Coxon    (5, 252)
37.    Stephen Malkmus    (21, 213)
38.    Pavement    (1196, 211)
39.    Japanther    (38, 210)
40.    Kraftwerk    (73, 201)
41.    Daft Punk    (62, 200)
42.    Liars    (38, 200)
43.    Weezer    (60, 189)
44.    Kaiser Chiefs    (6, 188)
45.    The Futureheads    (9, 181)
46.    Beck    (466, 172)
47.    The Fiery Furnaces    (29, 170)
48.    The Strokes    (256, 155)
49.    Young Knives    (2, 152)
50.    Fugazi    (28, 135)
51.    Buzzcocks    (19, 124)
52.    The Feelies    (9, 123)
53.    Ratatat    (180, 116)
54.    Public Image Ltd.    (5, 110)
55.    The Rapture    (24, 108)
56.    Au Pairs    (3, 104)
57.    Health    (11, 97)
58.    OOIOO    (1, 96)
59.    Delta 5    (1, 95)
60.    Two Door Cinema Club    (26, 94)
61.    Nirvana    (83, 92)
62.    The Yardbirds    (21, 88)
63.    Merzbow    (2, 86)
64.    Big Black    (7, 84)
65.    Tokyo Police Club    (19, 84)
66.    The New Pornographers    (1775, 83)
67.    The Wombats    (3, 82)
68.    Stereophonics    (11, 80)
69.    Fountains of Wayne    (54, 79)
70.    Liliput    (1, 78)
71.    Butthole Surfers    (156, 76)
72.    Editors    (28, 75)
73.    Bauhaus    (13, 73)
74.    Gorillaz    (125, 72)
75.    Chicks On Speed    (88, 70)
76.    Negativland    (40, 68)
77.    Battles    (242, 68)
78.    Metronomy    (2, 64)
79.    The Kooks    (19, 63)
80.    Blonde Redhead    (6, 60)
81.    Mystery Jets    (16, 56)
82.    Caravan Palace    (3, 56)
83.    Marnie Stern    (2, 54)
84.    Chuck Berry    (60, 53)
85.    Lou Reed    (13, 52)
86.    MGMT    (215, 50)
87.    Bright Eyes    (88, 48)
88.    Stereolab    (27, 46)
89.    Tom Waits    (153, 44)
90.    XTC    (1, 44)
91.    Built to Spill    (403, 42)
92.    The Stranglers    (57, 42)
93.    Louis XIV    (1, 40)
94.    Vampire Weekend    (260, 40)
95.    The Mekons    (5, 40)
96.    The Naked and Famous    (13, 40)
97.    Sex Pistols    (12, 38)
98.    Yeah Yeah Yeahs    (119, 38)
99.    Flogging Molly    (20, 37)
100.    Pere Ubu    (34, 37)
101.    Digitalism    (3, 36)
102.    Good Shoes    (1, 36)
103.    The Spinto Band    (180, 34)
104.    Television    (8, 33)
105.    The Stone Roses    (8, 32)
106.    Klaxons    (5, 32)
107.    The Libertines    (105, 29)
108.    Neu!    (25, 28)
109.    1990s    (2, 27)
110.    The Vaselines    (109, 26)
111.    Mission of Burma    (117, 26)
112.    The View    (1, 24)
113.    The Modern Lovers    (1, 23)
114.    Tapes 'n Tapes    (43, 23)
115.    Jeff Beck    (57, 23)
116.    Angry Samoans    (5, 22)
117.    Josef K    (10, 22)
118.    The Jesus and Mary Chain    (119, 21)
119.    Muddy Waters    (8, 21)
120.    We Are Scientists    (5, 21)
121.    Madness    (1, 21)
122.    Poison Girls    (21, 20)
123.    The Killers    (56, 20)
124.    Parov Stelar    (7, 20)
125.    Black Randy & the Metrosquad    (1, 19)
126.    The Drums    (4, 19)
127.    The Offspring    (2, 18)
128.    The Raincoats    (6, 18)
129.    Deep Wound    (8, 18)
130.    The Velvet Underground    (581, 18)
131.    Radiohead    (569, 18)
132.    Original Soundtrack, Mulatu Astatqe    (1, 17)
133.    LCD Soundsystem    (86, 17)
134.    Blurt    (5, 16)
135.    Johnny Cash    (5, 16)
136.    Wavves    (1, 16)
137.    Lesbians On Ecstasy    (8, 16)
138.    Cabaret Voltaire    (8, 16)
139.    Cansei de Ser Sexy    (86, 16)
140.    The Postal Service    (49, 15)
141.    Drive Like Jehu    (21, 15)
142.    Tilly and the Wall    (1, 15)
143.    Rapeman    (5, 14)
144.    Sleater-Kinney    (127, 14)
145.    Wipers    (2, 14)
146.    British Sea Power    (1, 14)
147.    A Certain Ratio    (31, 14)
148.    The Evolution Control Committee    (34, 14)
149.    The Brian Jonestown Massacre    (21, 14)
150.    Ludus    (1, 13)
151.    This Heat    (5, 12)
152.    The Danse Society    (4, 12)
153.    Bérurier Noir    (2, 12)
154.    The Raveonettes    (119, 10)
155.    Boredoms    (5, 10)
156.    Dinosaur Jr.    (84, 10)
157.    Norah Jones    (16, 10)
158.    Ringo Deathstarr    (5, 10)
159.    The Whitest Boy Alive    (2, 10)
160.    The Kills    (4, 10)
161.    Red Hot Chili Peppers    (53, 9)
162.    PJ Harvey    (174, 9)
163.    The Monochrome Set    (7, 8)
164.    Iggy Pop    (4, 8)
165.    Pink Floyd    (442, 8)
166.    NoMeansNo    (6, 8)
167.    Unwound    (2, 8)
168.    The Decemberists    (103, 7)
169.    The Slits    (92, 7)
170.    Suicide    (4, 6)
171.    Jefferson Airplane    (62, 6)
172.    My Dad Is Dead    (1, 6)
173.    Beat Happening    (5, 6)
174.    Jello Biafra    (2, 6)
175.    Bombay Bicycle Club    (28, 6)
176.    Black Flag    (13, 6)
177.    The Names    (6, 6)
178.    Donovan    (1, 6)
179.    My Bloody Valentine    (457, 6)
180.    The Durutti Column    (2, 5)
181.    Hard-Fi    (3, 5)
182.    Nada Surf    (21, 5)
183.    Duke Ellington    (2, 5)
184.    No Age    (7, 4)
185.    The Cure    (430, 4)
186.    Violent Femmes    (78, 4)
187.    Liquid Liquid    (1, 4)
188.    Queen    (316, 4)
189.    A Place to Bury Strangers    (6, 4)
190.    AC/DC    (14, 4)
191.    Death from Above 1979    (15, 4)
192.    Arcade Fire    (432, 4)
193.    Chrome    (6, 4)
194.    Friendly Fires    (14, 4)
195.    Half Japanese    (5, 4)
196.    The Vaccines    (7, 4)
197.    Kent    (8, 3)
198.    KT Tunstall    (26, 3)
199.    Neko Case    (209, 3)
200.    Kasabian    (15, 3)
201.    LOVE PSYCHEDELICO    (9, 3)
202.    Kool & The Gang    (7, 3)
203.    R.E.M.    (192, 2)
204.    The Royal Family And The Poor    (6, 2)
205.    The Glitch Mob    (11, 2)
206.    Jens Lekman    (67, 2)
207.    Nick Cave & The Bad Seeds    (176, 2)
208.    Janis Joplin    (2, 2)
209.    The Black Keys    (55, 2)
210.    Röyksopp    (28, 2)
211.    Tortoise    (3, 2)
212.    Naked Raygun    (4, 2)
213.    Datarock    (2, 2)
214.    23 Skidoo    (6, 2)
215.    The Jesus Lizard    (2, 2)
216.    The Rolling Stones    (85, 2)
217.    Le Tigre    (2, 2)
218.    Siege    (2, 2)
219.    The Kinks    (74, 2)
220.    Led Zeppelin    (445, 2)
221.    The Staple Singers    (9, 2)
222.    The Residents    (118, 2)
223.    Flipper    (13, 2)
224.    The Smashing Pumpkins    (39, 2)
225.    Rogue Wave    (5, 2)
226.    The Horrors    (11, 2)
227.    fIREHOSE    (16, 2)
228.    Washed Out    (47, 2)
229.    The Replacements    (32, 2)
230.    The Homosexuals    (3, 2)
231.    Justice    (12, 2)
232.    Sigur Rós    (151, 2)
233.    Five Or Six    (6, 2)
234.    The Pop Group    (83, 2)
235.    Passion Pit    (14, 2)
236.    Boris    (2, 2)
237.    Barenaked Ladies    (2, 2)
238.    Broken Bells    (8, 2)
239.    Van Halen    (2, 2)
240.    Sly & The Family Stone    (3, 2)
241.    Casiotone for the Painfully Alone    (7, 2)
242.    The xx    (107, 2)
243.    The dB's    (7, 2)
244.    Electrelane    (46, 2)
245.    Foster the People    (48, 2)
246.    SBTRKT    (7, 2)
247.    Les Savy Fav    (8, 2)
248.    Ladytron    (22, 2)
249.    The Centurians    (5, 2)
250.    PJ Harvey, PJ Harvey    (10, 2)
251.    Dead Kennedys    (7, 2)
252.    Frank Sinatra    (16, 2)
253.    Sebadoh    (7, 2)
254.    !!!    (3, 2)
255.    Phoenix    (45, 2)
256.    Yo La Tengo    (876, 2)
257.    Epic45    (9, 2)
258.    Colin Newman    (5, 2)
259.    Elliott Smith    (340, 2)
260.    Clap Your Hands Say Yeah    (54, 2)
261.    Bonobo    (16, 2)
262.    Swirlies    (6, 2)
263.    Pretty Lights    (10, 2)
264.    Shpongle    (1, 2)
265.    Brendan Benson    (2, 1)
266.    Shinedown    (1, 1)
267.    James Brown    (12, 1)
268.    The Servant    (1, 1)
269.    Grandaddy    (5, 1)
270.    Switchfoot    (1, 1)
271.    Matt Costa    (1, 1)
272.    Ray Charles    (3, 1)
273.    Marvin Gaye    (14, 1)
274.    Coldplay    (94, 1)
275.    Captain Beefheart & His Magic Band    (10, 1)
276.    Neutral Milk Hotel    (207, 1)
277.    The Magic Numbers    (62, 1)
278.    Can    (151, 1)
