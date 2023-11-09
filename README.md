# Linkedin_Automation_with_Generative_AI

This tool leverages the power of artificial intelligence and machine learning to automate the process of creating and posting high-quality content on LinkedIn. It utilizes Gen AI, a large language model, to generate engaging text and Information Ratri to extract relevant information from provided links.

## Features

- Automated content creation: Generate compelling LinkedIn posts based on your intent and provided links.
- Intelligent posting: Determine the optimal time to post your content for maximum engagement.
- Image capturing: Automatically find and include relevant images to accompany your posts.
- Time-saving efficiency: Streamline your LinkedIn posting process and save valuable time.

## Prerequisites

- Python 3.x 🐍
- Pip package installer 📦
- Valid LinkedIn account 💼
- Installation 🎯
- Clone or download the repository 🚀

## Quickstart

### **Python installation**
Install our linkedin_automation psi repo 
```python
pip install -q git+https://github.com/gathnexadmin/Linkedin_Automation_with_Generative_AI.git
````
- Import files and setup the credentials
- To know more about how to create linkedin access toked checkout previous blog : https://medium.com/@gathnex/automating-the-linkedin-posts-using-generative-ai-llm-part-1-how-to-create-linkedin-api-e5f77fa46e5f
```python
#import this two files contain PSI automation system
from psi import llm_automation, Linkedin_post
#setup your credentials
OPENAI_API_KEY = "openai key"
access_token = "linkedin access token"
```
PSI function
```python
def psi(prompt):
    llm = llm_automation.llm_auto(prompt, OPENAI_API_KEY)
    if llm.intent_indentifier() == "#Post":
        url = llm.prompt_link_capturer()
        res = Linkedin_post.LinkedinAutomate(access_token, url, OPENAI_API_KEY).main_func()
        return llm.posted_or_not(res)
    else:
        return llm.normal_gpt()
```
Now, you're read to use Genrative AI with PSI tool
```python
psi("create content about my new medium blog post https://medium.com/@gathnex/new-generative-ai-course-by-deeplearning-ai-daf34e24e9c8 and post it on my linkedin")
```

## Contributing

We welcome contributions to this project. Please feel free to open issues or pull requests with your suggestions or code improvements.

## License

This project is licensed under the MIT License.
