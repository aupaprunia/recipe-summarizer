import os

from dotenv import load_dotenv

from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4o", api_key=api_key)

def get_transcript(url):

    loader = YoutubeLoader.from_youtube_url(url, language = ["en-IN"], translation="en")
    transcript_doc = loader.load()

    if transcript_doc != []:
        transcript = transcript_doc[0].page_content
        return transcript
    
    return None

def get_result(video_link):

    transcript = get_transcript(video_link)
    
    if not transcript:
        return "No transcript"

    template = """
    Here is the attached transcript from a youtube video for a recipe. Create a well-formatted recipe from the transcript. Include the following sections:
    1) Ingredients
    2) Serving Size
    3) Step by Step instructions

    Here is the transcript:{transcript}
    """

    prompt = PromptTemplate(
        input_variables=["transcript"],
        template=template,
    )

    parser = StrOutputParser()

    chain = prompt | model | parser

    result = chain.invoke({"transcript": transcript})

    return result
