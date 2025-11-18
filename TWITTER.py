import tweepy
import os
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api_v1 = tweepy.API(auth)
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

def postingtweet(text, imagepath=None, alt_text=None):
    mediaid = None
    if imagepath:
        media = api_v1.media_upload(imagepath)
        mediaid = media.media_id_string
        if alt_text:
            api_v1.create_media_metadata(mediaid, alt_text)
    if mediaid:
        response = client.create_tweet(text=text, media_ids=[mediaid])
    else:
        response = client.create_tweet(text=text)
    print(f"Tweet posted with ID: {response.data['id']}")
    
def replytotweet(tweetid, replytext):
    response = client.create_tweet(
        text=replytext,
        reply_to_tweet_id=tweetid
    )
    print(f"The Reply to the tweet with mentioned tweet id is posted with ID: {response.data['id']}")

def scheduledtweets(Multitexts, Timeinterval):
    for text in Multitexts:
        postingtweet(text)
        print(f"Waiting for {Timeinterval} seconds for tweeting next tweet...")
        time.sleep(Timeinterval)

def deletingtweet(Tweetid):
    try:
        client.delete_tweet(id=Tweetid)
        print(f"Tweet with {Tweetid} id deleted")
    except Exception as e:
        print(f"There is Error deleting tweet: {e}")

def retweet_tweet(tweet_id):
    try:
        response = client.retweet(tweet_id)
        print("Retweet done")
    except tweepy.TweepyException as e:
        print(f"There is error in retweeting tweet: {e}")

if __name__ == "__main__":
    while True:
        print("\nChoose an option for the operation you want to do:")
        print("1 - For Tweeting text only")
        print("2 - For Scheduled text tweets")
        print("3 - For Tweeting Text with image")
        print("4 - For Replying to a tweet")
        print("5 - For Deleting a tweet")
        print("6 - For Retweeting a tweet")
        print("7 - Exit")
        choice = input("Enter Your choice from 1,2,3,4,5,6,7: ").strip()
        match choice:
            case "1":
                tweet= input("Enter your tweet: ")
                postingtweet(tweet)
            case "2":
              print("Enter tweets one by one and type f or F when finished.")
              tweets = []
              while True:
                    text = input("Enter tweet That you want to post: ")
                    if text.lower() == 'f':
                       break
                    tweets.append(text)
              interval = input("Enter Time interval in seconds between tweets: ")
              interval_sec = int(interval)  # Will raise ValueError if invalid input
              scheduledtweets(tweets, interval_sec)
            case "3":
                tweet=input("Enter the text that you want to Tweet: ")
                imagepath = input("Enter the full image file path: ")
                des=input("Do you want to add description for the image? Enter y or Y for yes and any other character for no: ").lower()
                alt_text = ""
                if des in ['y', 'Y']:
                    alt_text = input("Enter alt text (description) for the image: ")
                postingtweet(tweet, imagepath, alt_text or None)
            case "4":
                tweetid = input("Enter Tweet ID to reply to: ")
                replytext = input("Enter your reply to tweet: ")
                replytotweet(tweetid, replytext)
            case "5":
                tweetid = input("Enter Tweet ID to delete: ")
                confirmation = input(f"Are you sure you want to delete tweet ID {tweetid}? Enter y or Y for Yes and any other character for no: ").lower()
                if confirmation in ['y', 'Y']:
                    deletingtweet(tweetid)
                else:
                    print("You entered any other character than Y or y so Tweet Deletion is cancelled")
            case "6":
                tweetid = input("Enter Tweet ID to retweet: ")
                retweet_tweet(tweetid)
            case "7":
                print("Exiting program Thank you for using the bot")
                break    
            case _:
                print("Invalid choice. Please enter a number from 1 to 7.")
