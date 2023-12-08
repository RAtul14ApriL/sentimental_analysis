import praw
import pandas as pd
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()


#User agent
user_agent = "praw_scraper_1.0"

#Creating instance of reddit class
reddit = praw.Reddit(username=os.getenv("USERNAME"),
                     password=os.getenv("PASSWORD"),
                     client_id=os.getenv("CLIENTID"),
                     client_secret=os.getenv("CLIENTSECRET"),
                     user_agent=user_agent
                     )

#Getting reddit posts based on keyword
submissions=praw.models.Submission

reddit_posts=pd.DataFrame()

post_obj={
  "titles":[],
  "ids":[],
  "ups":[],
  "downs":[],
  "upvote_ratio":[],
  "posted_on":[],
  "num_comments":[]
}


for submission in reddit.subreddit("all").search("artificial intelligence"):
  post_obj['titles'].append(submission.title)
  post_obj['ids'].append(submission.id)
  post_obj['ups'].append(submission.ups)
  post_obj['downs'].append(submission.downs)
  post_obj['posted_on'].append(date.fromtimestamp(submission.created_utc))
  post_obj['upvote_ratio'].append(submission.upvote_ratio)


reddit_posts['title'] =post_obj['titles']
reddit_posts['id'] =post_obj['ids']
reddit_posts['upvotes']=post_obj['ups']
reddit_posts['downs']=post_obj['downs']
reddit_posts['upvote_ratio']=post_obj['upvote_ratio']
reddit_posts['posted_on']=post_obj['posted_on']

reddit_posts.to_csv('reddit_posts.csv')

#Getting the reddit comments
reddit_comments=pd.DataFrame()
all_posts=[]
comments=[]
comment_ids=[]

for id in post_obj['ids']:
  posts = reddit.submission(id=id)
  all_posts.append(posts)

for post in all_posts:
  for comment in post.comments.list():
    if type(comment).__name__ == 'Comment':
      comments.append(comment.body)
      comment_ids.append(post.id)

reddit_comments['id']=comment_ids
reddit_comments['comments']=comments

reddit_comments.to_csv('reddit_comments.csv')