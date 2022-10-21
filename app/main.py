from pydantic import BaseModel
from fastapi import FastAPI
import http3, requests
import dotenv, os

#TODO: Add services hostname and port as env variables
#TODO: Add health check of all services
#TODO: Make parallel calls to the services

class InputText(BaseModel):
    text: str

dotenv.load_dotenv()
client = http3.AsyncClient()

# Trends Innovations Service
trends_innovations_host = os.environ.get('TRENDS_INNOVATIONS_HOST')
trends_innovations_port = os.environ.get('TRENDS_INNOVATIONS_PORT')
trends_service = trends_innovations_host + ':' + trends_innovations_port

# Article Sentiment Service
article_sentiment_host = os.environ.get('ARTICLE_SENTIMENT_HOST')
article_sentiment_port = os.environ.get('ARTICLE_SENTIMENT_PORT')
sentiment_service = article_sentiment_host + ':' + article_sentiment_port

# Article Entities Service
article_entities_host = os.environ.get('ARTICLE_ENTITIES_HOST')
article_entities_port = os.environ.get('ARTICLE_ENTITIES_PORT')
entities_service = article_entities_host + ':' + article_entities_port

app = FastAPI()

@app.get("/predictions-example")
async def get_predictions():

    response = await client.get(trends_service + "/predictions-example", timeout=30)   

    if(response.status_code == 200):
        return {"output": response.json()}

    else:
        return {"Hello": "Error"}


@app.get("/sentiment-example")
async def get_sentiment():

    response = await client.get(sentiment_service +"/sentiment-example", timeout=30)   
    if(response.status_code == 200):
        return {"output": response.json()}

    else:
        return {"Hello": "Error"}

@app.get("/entities-example")
async def get_entities():

    response = await client.get(entities_service + "/entities-example", timeout=30)   
    if(response.status_code == 200):
        return {"output": response.json()}

    else:
        return {"Hello": "Error"}


@app.post("/trends")
def process_trends(input_text:InputText):

    data = {"text":input_text.text}
    # 1 - Get Trend predictions

    r_trends = requests.post(trends_service + "/predictions", json=data, timeout=30)  
    
    # 2 - Get Sentiment analysys
    r_sentiment = requests.post(sentiment_service + "/sentiment", json=data, timeout=30) 
    
    # 3 - Get Entities
    r_entities = requests.post(entities_service + "/entities", json=data, timeout=30)  

    trend_results = r_trends.json()
    sentiment = r_sentiment.json()
    entities = r_entities.json()

    '''
    # 4 - Get Sentiment from trends
    r_sents = requests.post(sentiment_service + "/batch-sentiment", json={"trends":trend_results}, timeout=30)

    # 5 - Get entities from trends
    r_ents = requests.post(entities_service + "/batch-entities", json={"trends":trend_results}, timeout=30)

    # 6 - Add sentiment and entities for each trend
    size = len(trend_results)
    trend_sents = r_sents.json()
    trend_ents = r_ents.json()

    for i in range(0, size):
        trend_results[i]['extract_sentiment'] = trend_sents[i]['extract_sentiment']
        trend_results[i]['extract_entities'] = trend_ents[i]['extract_entities']
    '''


    results = {'trend_extractions': trend_results,
                   'article_sentiment': sentiment,
                   'article_entities': entities}

    return results

