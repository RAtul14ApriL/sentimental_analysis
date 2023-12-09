import praw
import pandas as pd
from datetime import date
from dotenv import load_dotenv
import os
from tqdm import tqdm
import time

load_dotenv()


starttime = time.time()
#User agent
user_agent = "praw_scraper_1.0"

#Creating instance of reddit class
reddit = praw.Reddit(username=os.getenv("PRAW_USERNAME"),
                     password=os.getenv("PRAW_PASSWORD"),
                     client_id=os.getenv("PRAW_CLIENTID"),
                     client_secret=os.getenv("PRAW_CLIENTSECRET"),
                     user_agent=user_agent
                     )

#Getting reddit posts based on keyword
submissions=praw.models.Submission

reddit_posts=pd.DataFrame()

comments_objs={
  "post_id":[],
  "id":[],
  "comments":[], 
  "author":[],
  "score":[],
  "ups":[],
  "downs":[],
  "posted_on":[],
  "controversiality":[]
  }
post_obj={
  "titles":[],
  'post_text':[],
  "ids":[],
  "ups":[],
  "downs":[],
  "upvote_ratio":[],
  "posted_on":[],
  "num_comments":[],
  "author":[],
  "score":[],
  "subreddit":[],
}

reddit_comments=pd.DataFrame()
search_query=input("Enter search query: ")

for submission in reddit.subreddit("all").search(search_query if search_query else "artificial intelligence"):
  post_obj['titles'].append(str(submission.title).strip().replace(',',' '))
  post_obj['ids'].append(submission.id)
  post_obj['ups'].append(submission.ups)
  post_obj['downs'].append(submission.downs)
  post_obj['posted_on'].append(date.fromtimestamp(submission.created_utc))
  post_obj['upvote_ratio'].append(submission.upvote_ratio)
  post_obj['score'].append(submission.score)
  post_obj['num_comments'].append(submission.num_comments)
  post_obj['author'].append(str(submission.author.name).strip().replace(',',''))
  post_obj['subreddit'].append(submission.subreddit.display_name)
  post_obj['post_text'].append(str(submission.selftext).strip().replace(',',' '))
  print("Getting comments for post: ",submission.id , " with title: ",submission.title)
  for i in tqdm(submission.comments.list()):
    if type(i).__name__ == 'Comment' and i.author is not None and i.body is not None and i.body != '[deleted]':
      comments_objs['post_id'].append(submission.id)
      comments_objs['id'].append(i.id)
      comments_objs['comments'].append(str(i.body).strip().replace(',',' '))
      comments_objs['author'].append(str(i.author.name).strip().replace(',',''))
      comments_objs['score'].append(i.score)
      comments_objs['ups'].append(i.ups)
      comments_objs['downs'].append(i.downs)
      comments_objs['posted_on'].append(date.fromtimestamp(i.created_utc))
      comments_objs['controversiality'].append(i.controversiality)

for i in list(post_obj.keys()):
  print("Filling column in post DF: ",i)
  reddit_posts[i]=post_obj[i]

for i in list(comments_objs.keys()):
  print("Filling column in comments DF: ",i)
  reddit_comments[i]=comments_objs[i]

print("Time taken to extract data: ",time.time()-starttime," seconds")
reddit_posts.to_csv(f'reddit_posts-{search_query.replace(" ","_")}.csv')
reddit_comments.to_csv(f'reddit_comments-{search_query.replace(" ","_")}.csv')