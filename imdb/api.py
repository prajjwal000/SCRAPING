from curl_cffi import requests
from json import loads
import sqlite3
from random import uniform
from time import sleep


def getPlot(movieID: str, min_rate_limit: float = 3, max_rate_limit: float = 6):
    url = "https://api.graphql.imdb.com/?operationName=TMD_Storyline&variables=%7B%22locale%22%3A%22en-US%22%2C%22titleId%22%3A%22"+movieID + \
        "%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2278f137c28457417c10cf92a79976e54a65f8707bfc4fd1ad035da881ee5eaac6%22%2C%22version%22%3A1%7D%7D"

    payload = {}
    headers = {
        'content-type': 'application/json'
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload)

    data = loads(response.text)

    title = data['data']['title']['summaries']['edges'][0]['node']['plotText']['plaidHtml']
    outline = data['data']['title']['outlines']['edges'][0]['node']['plotText']['plaidHtml']
    synopsis = data['data']['title']['synopses']['edges'][0]['node']['plotText']['plaidHtml']
    keywords = [edge['node']['legacyId']
                for edge in data['data']['title']['storylineKeywords']['edges']]
    tagline = data['data']['title']['taglines']['edges'][0]['node']['text']
    genre = data['data']['title']['genres']['genres'][0]['text']
    certificate = data['data']['title']['certificate']['rating']
    certificate_reason = data['data']['title']['certificate']['ratingReason']
    certificate_body = data['data']['title']['certificate']['ratingsBody']['id']

    conn = sqlite3.connect('imdb.db')
    cursor = conn.cursor()
    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS movie_plot
                     (movieid TEXT PRIMARY KEY,title TEXT, outline TEXT, synopsis TEXT, keywords TEXT, tagline TEXT, genre TEXT, certificate TEXT, certificate_reason TEXT, certificate_body TEXT)''')

    # Insert the data into the table
    try:
        cursor.execute("INSERT INTO movie_plot VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)", (movieID, title, outline,
                       synopsis, ', '.join(keywords), tagline, genre, certificate, certificate_reason, certificate_body))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: Error inserting data for movie ID {movieID}: {e}")
    conn.close()
    delay = uniform(min_rate_limit, max_rate_limit)
    sleep(delay)


def getReview(movieID: str, no: int = 25, min_rate_limit: float = 3, max_rate_limit: float = 6):
    url = "https://api.graphql.imdb.com/?operationName=TitleReviewsRefine&variables=%7B%22const%22%3A%22" + movieID + "%22%2C%22filter%22%3A%7B%7D%2C%22first%22%3A" + \
        str(no) + "%2C%22locale%22%3A%22en-US%22%2C%22sort%22%3A%7B%22by%22%3A%22TOTAL_VOTES%22%2C%22order%22%3A%22DESC%22%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2289aff4cd7503e060ff1dd5aba91885d8bac0f7a21aa1e1f781848a786a5bdc19%22%2C%22version%22%3A1%7D%7D"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'application/graphql+json, application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'content-type': 'application/json'
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, impersonate="chrome")
    data = loads(response.text)

    headers = ['Review ID', 'Author', 'Author Rating',
               'Submission Date', 'Review Text', 'Upvotes', 'Downvotes']
    conn = sqlite3.connect('imdb.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS movie_reviews
                     (movieid TEXT, reviewid TEXT PRIMARY KEY, author TEXT, author_rating INTEGER, submission_date TEXT, review_text TEXT, upvotes INTEGER, downvotes INTEGER)''')
    # Insert the data into the table
    for review in data['data']['title']['reviews']['edges']:
        try:
            cursor.execute("INSERT INTO movie_reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
                movieID,
                review['node']['id'],
                review['node']['author']['nickName'],
                review['node']['authorRating'],
                review['node']['submissionDate'],
                review['node']['text']['originalText']['plaidHtml'],
                review['node']['helpfulness']['upVotes'],
                review['node']['helpfulness']['downVotes']
            ))
        except sqlite3.Error as e:
            print(f"Error: Error inserting data for movie ID {
                  movieID}, review ID {review['node']['id']}: {e}")

    conn.commit()
    conn.close()

    delay = uniform(min_rate_limit, max_rate_limit)
    sleep(delay)


def getTrivia(movieID: str, no: int = 25, min_rate_limit: float = 3, max_rate_limit: float = 6):
    url = "https://api.graphql.imdb.com/?operationName=TitleTriviaPagination&variables={\"const\":\""+movieID + "\",\"filter\":{\"categories\":[\"uncategorized\"],\"spoilers\":\"EXCLUDE_SPOILERS\"},\"first\":"+str(
        no)+",\"locale\":\"en-US\",\"originalTitleText\":false}&extensions={\"persistedQuery\":{\"sha256Hash\":\"16fe8948f4489e0d7f45641919c9b36a7cfb29faeace1910d34f463a0efd973d\",\"version\":1}}"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': 'application/graphql+json, application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://www.imdb.com/',
        'content-type': 'application/json',
        'x-imdb-user-language': 'en-US',
        'x-imdb-user-country': 'US'
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, impersonate="chrome")
    data = loads(response.text)
    conn = sqlite3.connect('imdb.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS movie_trivia
                     (movieid TEXT, id TEXT PRIMARY KEY, body TEXT, interest_score_users_voted INTEGER, interest_score_users_interested INTEGER, category_id TEXT, category_text TEXT)''')

    # Insert the data into the table
    for trivia in data['data']['title']['trivia']['edges']:
        try:
            cursor.execute("INSERT INTO movie_trivia VALUES (?, ?, ?, ?, ?, ?, ?)", (
                movieID,
                trivia['node']['id'],
                trivia['node']['displayableArticle']['body']['plaidHtml'],
                trivia['node']['interestScore']['usersVoted'],
                trivia['node']['interestScore']['usersInterested'],
                trivia['node']['category']['id'],
                trivia['node']['category']['text']
            ))
        except sqlite3.Error as e:
            print(f"Error: Error inserting data for movie ID {
                  movieID}, trivia ID {trivia['node']['id']}: {e}")

    conn.commit()
    conn.close()
    delay = uniform(min_rate_limit, max_rate_limit)
    sleep(delay)


getPlot("tt7131622")
getReview("tt7131622", 50)
getTrivia("tt7131622", 50)
