import re, requests, json, os, openai
from bs4 import BeautifulSoup
from openai import OpenAI

class LinkedinAutomate:
    def __init__(self, access_token, medium_url, openai_api):
        self.access_token = access_token
        self.openai_api = openai_api
        #self.yt_url = yt_url
        self.medium_url = medium_url
        self.python_group_list = []
        self.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

    def get_page_content(self):
      response = requests.get(self.medium_url)
      soup = BeautifulSoup(response.text, 'html.parser')
      for script in soup(["script", "style"]):
          script.extract()
      text = soup.get_text()
      text = '\n'.join(line.strip() for line in text.split('\n'))
      text = '\n'.join(line for line in text.split('\n') if line)
      return text

    def get_title_description(self):
        def extract_title_and_description(input_text):
            title_pattern = r"Title:(.+?)(?=Description:)"
            description_pattern = r"Description:(.+)"
            title_match = re.search(title_pattern, input_text, re.DOTALL)
            description_match = re.search(description_pattern, input_text, re.DOTALL)
            if title_match and description_match:
                title = title_match.group(1).strip()
                description = description_match.group(1).strip()
                return title, description
            else:
                return None, None
        x = self.get_page_content()
        client = OpenAI(api_key = self.openai_api)
        DEFAULT_SYSTEM_PROMPT = '''You are a content title and description generator. Your task is to create a captivating title and a concise short description for a given content. Provide one compelling title and a informative short description that clearly conveys the main points of the content.
         response should be in this format. for example.
         Title: Title Content
         Description: Description Content
         Aim for creativity and clarity in your creations, ensuring that both the title and description are attention-grabbing and informative. make a description short don't give too long'''
        response = client.chat.completions.create(
        model= "gpt-3.5-turbo-0613",
        messages=[
                    {f"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                    {f"role": "user", "content": "[" + x + "].Create one title and description of the content"},
                ]
                )
        mod_output = response.choices[0].message.content
        title, description = extract_title_and_description(mod_output)
        return title, description

    def common_api_call_part(self, feed_type = "feed", group_id = None):
        x, y = self.get_title_description()
        payload_dict = {
            "author": f"urn:li:person:{self.user_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": y
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                        {
                        "status": "READY",
                        "description": {
                            "text": y
                        },
                        "originalUrl": self.medium_url,
                        "title": {
                            "text": x
                        },
                        "thumbnails": [
                                {
                                "url": self.extract_medium_thumbnail()
                                }
                            ]
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" if feed_type == "feed" else "CONTAINER"
            }
        }
        if feed_type == "group":
            payload_dict["containerEntity"] = f"urn:li:group:{group_id}"

        return json.dumps(payload_dict)

    #Extract the thumbnail of youtube video
    def extract_thumbnail_url_from_YT_video_url(self):
        exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
        s = re.findall(exp,self.yt_url)[0][-1]
        return  f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"


    #Extract the thumbnail of medium blog
    def fetch_blog_html(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def extract_medium_thumbnail(self):
        def extract_thumbnail_url_from_medium_blog(blog_html):
            soup = BeautifulSoup(blog_html, 'html.parser')
            thumbnail_meta_tag = soup.find('meta', property='og:image')
            if thumbnail_meta_tag:
                thumbnail_url = thumbnail_meta_tag['content']
                return thumbnail_url
            return None

        blog_html = self.fetch_blog_html(self.medium_url)
        if blog_html:
            thumbnail_url = extract_thumbnail_url_from_medium_blog(blog_html)
            return thumbnail_url
        else:
            return None
    def get_user_id(self):
        url = "https://api.linkedin.com/v2/userinfo"
        response = requests.request("GET", url, headers=self.headers)
        jsonData = json.loads(response.text)
        return jsonData["sub"]

    def feed_post(self):
        url = "https://api.linkedin.com/v2/ugcPosts"
        payload = self.common_api_call_part()

        return requests.request("POST", url, headers=self.headers, data=payload)

    def group_post(self, group_id):
        url = "https://api.linkedin.com/v2/ugcPosts"
        payload = self.common_api_call_part(feed_type = "group", group_id=group_id)

        return requests.request("POST", url, headers=self.headers, data=payload)


    def main_func(self):
        self.user_id = self.get_user_id()
        #print(self.user_id)

        feed_post = self.feed_post()
        print(feed_post)
        for group_id in self.python_group_list:
            print(group_id)
            group_post = self.group_post(group_id)
            print(group_post)
        return str(feed_post)
