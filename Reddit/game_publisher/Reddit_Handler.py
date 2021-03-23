import praw

import constants


class RedditHandler:
    def __init__(self):
        user_agent = 'GamePublisher by u/Patrick_k'
        self.reddit = praw.Reddit(user_agent=user_agent)

    def create_post(self, title, body):
        subreddit = self.reddit.subreddit(constants.SUBREDDIT)
        return subreddit.submit(title=title, selftext=body)

    def remove_post(self, submission_id):
        self.reddit.submission(submission_id).delete()
