import requests
import json
import csv
import sqlite3

url = "https://api.graphql.imdb.com/?operationName=TMD_Storyline&variables=%7B%22locale%22%3A%22en-US%22%2C%22titleId%22%3A%22tt0111161%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%2278f137c28457417c10cf92a79976e54a65f8707bfc4fd1ad035da881ee5eaac6%22%2C%22version%22%3A1%7D%7D"

payload = {}
headers = {
  'content-type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

# Load the JSON data
data = json.loads(response.text)

# Extract the relevant information
title = data['data']['title']['summaries']['edges'][0]['node']['plotText']['plaidHtml']
outline = data['data']['title']['outlines']['edges'][0]['node']['plotText']['plaidHtml']
synopsis = data['data']['title']['synopses']['edges'][0]['node']['plotText']['plaidHtml']
keywords = [edge['node']['legacyId'] for edge in data['data']['title']['storylineKeywords']['edges']]
tagline = data['data']['title']['taglines']['edges'][0]['node']['text']
genre = data['data']['title']['genres']['genres'][0]['text']
certificate = data['data']['title']['certificate']['rating']
certificate_reason = data['data']['title']['certificate']['ratingReason']
certificate_body = data['data']['title']['certificate']['ratingsBody']['id']

conn = sqlite3.connect('imdb.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS movie(MovieID TEXT PRIMARY KEY, title TEXT, plot TEXT, genre TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY, title TEXT, MovieID TEXT)""")

# Save the data to a CSV file
with open('shawshank_redemption.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Outline', 'Synopsis', 'Keywords', 'Tagline', 'Genre', 'Certificate', 'Certificate Reason', 'Certificate Body'])
    writer.writerow([title, outline, synopsis, ', '.join(keywords), tagline, genre, certificate, certificate_reason, certificate_body])
