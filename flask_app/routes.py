from flask_app import app, db

@app.route("/")
def index():
    return "Hello, World!"


@app.route("/cfb", methods=['GET'])
def getGameData():
    url = "https://www.espn.com/college-football/scoreboard"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    score_cells = []
    games_cards = soup.find_all('section', class_='Scoreboard')

    for i in games_cards:
        away_rank = None
        home_rank = None
        try:
            away_rank = i.find('li', class_='ScoreboardScoreCell__Item--away').find('div', class_='ScoreCell__Rank').text
            home_rank = i.find('li', class_='ScoreboardScoreCell__Item--home').find('div', class_='ScoreCell__Rank').text
        except:
            pass
            
        score_cell = {
            'status': i.find('div', class_='ScoreCell__Time').text,
            'away': {
                'img': i.find('li', class_='ScoreboardScoreCell__Item--away').find('img')['src'],
                'rank': away_rank,
                'team_name': i.find('li', class_='ScoreboardScoreCell__Item--away').find('div', class_='ScoreCell__TeamName').text,
                'record': i.find('li', class_='ScoreboardScoreCell__Item--away').find('div', class_='ScoreboardScoreCell__RecordContainer').text,
                'score': i.find('li', class_='ScoreboardScoreCell__Item--away').find('div', class_='ScoreCell__Score').text

            },
            'home': {
                'img': i.find('li', class_='ScoreboardScoreCell__Item--home').find('img')['src'],
                'rank': home_rank,
                'team_name': i.find('li', class_='ScoreboardScoreCell__Item--home').find('div', class_='ScoreCell__TeamName').text,
                'record': i.find('li', class_='ScoreboardScoreCell__Item--home').find('div', class_='ScoreboardScoreCell__RecordContainer').text,
                'score': i.find('li', class_='ScoreboardScoreCell__Item--home').find('div', class_='ScoreCell__Score').text
            },
        }
        score_cells.append(score_cell)
    return score_cells
