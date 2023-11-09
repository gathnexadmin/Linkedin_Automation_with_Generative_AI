import re
from openai import OpenAI

class llm_auto:

    def __init__(self, prompt, openai_api):
        self.prompt = prompt
        self.openai_api = openai_api

    
    def intent_indentifier(self):
      model = "gpt-3.5-turbo"
      client = OpenAI(api_key = self.openai_api)
      DEFAULT_SYSTEM_PROMPT = '''You are a prompt classification assistant. Your role is to recognize prompts where the user intends to create and post content on LinkedIn. If the user clearly indicates the intent to 'post it on LinkedIn with a web URL,' classify it as #Post. If there are no indications of publishing or posting, classify the prompt as #Decline. For all other prompts without publishing intent, classify them as #Decline.
       Your task is to distinguish prompts based on their intention to publish content on LinkedIn or not.
       Sample prompts:
       1. create a content about this page 'www.xxx.com - #Decline
       2. create a content and  post this is web url 'www.xxx.com' - #Post
       3. 'www.xxx.com' create a content to post on linkedin - #Decline
       4. create and publish the content about in this page 'www.xxx.com' - #Post
       '''
      response = client.chat.completions.create(
          model= model,
      messages=[
            {f"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {f"role": "user", "content":  "Classify the prompt in the following '#Post' or '#Decline' :" + self.prompt},
          ]
          )
      return response.choices[0].message.content
    
    
    def normal_gpt(self):
      model = "gpt-3.5-turbo"
      client = OpenAI(api_key = self.openai_api)
      DEFAULT_SYSTEM_PROMPT = "You are Gathnex, an intelligent assistant dedicated to providing effective solutions. Your responses will include emojis to add a friendly and engaging touch. 😊 Analyze user queries and provide clear and practical answers, incorporating emojis to enhance the user experience. Focus on delivering solutions that are accurate, actionable, and helpful. If additional information is required for a more precise solution, politely ask clarifying questions. Your goal is to assist users by providing effective and reliable solutions to their queries. 🌟"
      response = client.chat.completions.create(
          model= model,
      messages=[
            {f"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {f"role": "user", "content": self.prompt},
          ]
          )
      return response.choices[0].message.content
    
    
    def prompt_link_capturer(self):
        url_pattern = r'https?://\S+|www\.\S+'
        urls = re.findall(url_pattern, self.prompt)
        return urls[0]
    
    def posted_or_not(self, y):
       client = OpenAI(api_key = self.openai_api)
       model = "gpt-3.5-turbo"
       DEFAULT_SYSTEM_PROMPT = "your a assistance just inform the user the linkedin post."
       if y == "<Response [201]>":
            response1 = client.chat.completions.create(
            model= model,
            messages=[
                    {f"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                    {f"role": "user", "content": "Tell the user in friendly manner the linked post is succesefully posted with emoji's"},
                ]
                )
            return response1.choices[0].message.content
       else:
            response2 = client.completions.create(
            model= model,
                messages=[
                        {f"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                        {f"role": "user", "content": "Tell the user in friendly manner the linked post is not succesefully posted and check the access tokens and hyperparamters correctly with sad emoji's"},
                    ]
                    )
            return response2.choices[0].message.content
            
