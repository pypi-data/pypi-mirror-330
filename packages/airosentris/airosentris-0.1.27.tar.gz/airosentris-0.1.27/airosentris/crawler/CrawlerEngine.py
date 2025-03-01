import os
import time
from dotenv import load_dotenv
from airosentris.crawler.apify.ApifyCrawler import ApifyCrawler
from airosentris.crawler.httprequest.HttpRequestCrawler import HttpRequestCrawler
from airosentris.crawler.tweepy.TweepyCrawler import TweepyCrawler
from airosentris.logger.Logger import Logger

# Load environment variables
load_dotenv()

class CrawlerEngine:
    _instances = {}

    def __init__(self, method: str = 'http', apify_token: str = None, twitter_bearer_token: str = None):
        
        self.logger = Logger(__name__)

        self.method = method
        self.apify_token = apify_token or os.getenv('APIFY_TOKEN')
        self.twitter_bearer_token = twitter_bearer_token or os.getenv('TWITTER_BEARER_TOKEN')

        if not self.apify_token and method == 'apify':
            raise ValueError("APIFY_TOKEN is required for ApifyCrawler.")
        if not self.twitter_bearer_token and method == 'tweepy':
            raise ValueError("TWITTER_BEARER_TOKEN is required for TweepyCrawler.")

        self.crawler = self._get_or_create_instance(method)
        # self.logger.info(f"Initialized CrawlerEngine with method: {method}")

    def _get_or_create_instance(self, method: str):
        if method not in self._instances:
            try:
                if method == 'apify':
                    self._instances[method] = ApifyCrawler(self.apify_token)
                elif method == 'tweepy':
                    self._instances[method] = TweepyCrawler(bearer_token=self.twitter_bearer_token)
                elif method == 'graphapi':
                    raise NotImplementedError("GraphAPI method is not implemented yet.")
                elif method == 'instaloader':
                    raise NotImplementedError("Instaloader method is not implemented yet.")
                elif method == 'selenium':
                    raise NotImplementedError("Selenium method is not implemented yet.")
                elif method == 'http':
                    self._instances[method] = HttpRequestCrawler()
                else:
                    raise ValueError(f"Unsupported crawling method: {method}")

                # self.logger.info(f"Created new instance for method: {method}")
            except Exception as e:
                self.logger.exception(f"Error initializing crawler for method: {method}")
                raise e

        return self._instances[method]

    def change_method(self, method: str):
        """Change the crawling method dynamically."""
        self.method = method
        self.crawler = self._get_or_create_instance(method)
        self.logger.info(f"Switched crawling method to: {method}")

    def crawl_from_cis(self):
        """
        Crawling data from CIS, processing it, and posting it to the server.
        """
        limit = 10

        while True:
            try:
                last_sequence = self.crawler.get_last_sequence()
                self.logger.info(f"🔢 Last sequence before fetching: {last_sequence}")

                # Fetch comments from CIS
                result = self.crawler.get_cis_comments(last_sequence + 8, last_sequence + limit)

                if not result or 'data' not in result:
                    self.logger.warning("⚠️ Warning: No 'data' key in response from CIS")
                    continue

                total_comments = len(result['data'])
                self.logger.info(f"📊 Total comments retrieved: {total_comments}")

                if total_comments == 0:
                    self.logger.info("🔄 No new comments to process.")
                    time.sleep(10)
                    continue

                for comment in result['data']:
                    try:
                        last_sequence = self.crawler.get_last_sequence()

                        pengaduan_text = comment.get('pengaduan', 'Unknown')
                        pengaduan_short = (pengaduan_text[:37] + "...") if len(pengaduan_text) > 40 else pengaduan_text

                        data = [{
                            "sequence": last_sequence + 1,
                            "nopel": comment.get('nopel', 'Unknown'),
                            "tgl_pengaduan": comment.get('tgl_pengaduan', 'Unknown'),
                            "jns_pengaduan": comment.get('jns_pengaduan', 'Unknown'),
                            "pengaduan": pengaduan_text,
                        }]

                        self.logger.info(f"📝 Pengaduan: {pengaduan_short}")

                        self.crawler.post_comments(data)
                        self.logger.info(f"✅ Posted comment sequence: {last_sequence + 1}")

                    except Exception as e:
                        self.logger.exception(f"❌ Error while processing comment: {e}")

                last_sequence = self.crawler.get_last_sequence()
                self.logger.info(f"🔄 Last sequence after processing: {last_sequence}")

            except Exception as e:
                self.logger.exception("🔥 Error during crawling process")

            time.sleep(10)


    def get_instagram_post(self, username: str, date: str, limit: int):
        """
        Retrieves Instagram posts for a given username.

        Parameters:
        username (str): The Instagram username to fetch posts for.
        date (str): The date to filter posts.
        limit (int): The maximum number of posts to retrieve.

        Returns:
        list: A list of Instagram posts.
        """
        self.logger.info(f"Fetching Instagram posts for user: {username} from {date} with limit {limit}")
        return self.crawler.get_instagram_post(username, date, limit)

    def get_instagram_comment(self, post_short_code: str, include_reply: bool):
        """
        Retrieves comments for a given Instagram post.

        Parameters:
        post_short_code (str): The short code of the Instagram post.
        include_reply (bool): Whether to include replies to comments.

        Returns:
        list: A list of Instagram comments.
        """
        self.logger.info(f"Fetching Instagram comments for post: {post_short_code}, include replies: {include_reply}")
        return self.crawler.get_instagram_comment(post_short_code, include_reply)

    def get_twitter_post(self, username: str, date: str, limit: int):
        """
        Retrieves Twitter posts for a given username.

        Parameters:
        username (str): The Twitter username to fetch posts for.
        date (str): The date to filter posts.
        limit (int): The maximum number of posts to retrieve.

        Returns:
        list: A list of Twitter posts.
        """
        self.logger.info(f"Fetching Twitter posts for user: {username} from {date} with limit {limit}")
        return self.crawler.get_twitter_post(username, date, limit)
