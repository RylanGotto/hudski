
@app.route("/")
def index():
    return "Hello, world!"


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







# @app.route("/about")
# def about():
#     return render_template("index.html")


# @app.route("/register", methods=['GET', 'POST'])
# def register():

#     if request.method == 'GET':
#         return render_template('register.html')

#     else:
#         # Create user object to insert into SQL
#         passwd1 = request.form.get('password1')
#         passwd2 = request.form.get('password2')

#         if passwd1 != passwd2 or passwd1 == None:
#             flash('Password Error!', 'danger')
#             return render_template('register.html')

#         hashed_pass = sha256_crypt.encrypt(str(passwd1))

#         new_user = User(
#             username=request.form.get('username'),
#             email=request.form.get('username'),
#             password=hashed_pass)

#         if user_exsists(new_user.username, new_user.email):
#             flash('User already exsists!', 'danger')
#             return render_template('register.html')
#         else:
#             # Insert new user into SQL
#             db.session.add(new_user)
#             db.session.commit()

#             login_user(new_user)

#             flash('Account created!', 'success')
#             return redirect(url_for('index'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')

#     else:
#         username = request.form.get('username')
#         password_candidate = request.form.get('password')

#         # Query for a user with the provided username
#         result = User.query.filter_by(username=username).first()

#         # If a user exsists and passwords match - login
#         if result is not None and sha256_crypt.verify(password_candidate, result.password):

#             # Init session vars
#             login_user(result)
#             flash('Logged in!', 'success')
#             return redirect(url_for('index'))

#         else:
#             flash('Incorrect Login!', 'danger')
#             return render_template('login.html')


# @app.route("/logout")
# def logout():
#     logout_user()
#     flash('Logged out!', 'success')
#     return redirect(url_for('index'))


# # Check if username or email are already taken
# def user_exsists(username, email):
#     # Get all Users in SQL
#     users = User.query.all()
#     for user in users:
#         if username == user.username or email == user.email:
#             return True

#     # No matching user
#     return False

# @app.route("/post/new", methods=['GET', 'POST'])
# @login_required
# def new_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(title=form.title.data, content=form.content.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Your post has been created!', 'success')
#         return redirect(url_for('index'))
#     return render_template('create_post.html', title='New Post',
#                            form=form, legend='New Post')


# @app.route("/post/<int:post_id>")
# def post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('post.html', title=post.title, post=post)


# @app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Update Post',
#                            form=form, legend='Update Post')


# @app.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
# def delete_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted!', 'success')
#     return redirect(url_for('index'))
