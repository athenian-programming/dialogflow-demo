# DialogFlow Demo

## Helpful Links
* [DialogFlow Tutorial](https://dialogflow.com/docs/getting-started/building-your-first-agent)
* [WebhookRequest](https://dialogflow.com/docs/reference/api-v2/rest/Shared.Types/WebhookRequest)
* [WebhookResponse](https://dialogflow.com/docs/reference/api-v2/rest/Shared.Types/WebhookResponse)
* [Docker Tutorial](https://hackernoon.com/docker-tutorial-getting-started-with-python-redis-and-nginx-81a9d740d091)


## Setup

Install the required python packages with:
```bash
pip install -r requirements.txt
```

## Server Execution

### Local dev

Run 'webhook.py' with:
```bash
python3 webhook.py
```

Run [redis](https://redis.io) with:
```bash
docker run -p 6379:6379 -d redis
```

### ngrok

Run [ngrok](https://ngrok.com) with:
```bash
ngrok http 5000
```

### Docker
Build the *dialogflow-webhook* container with:

```bash
docker build -t $(USER)/dialogflow-webhook:1.0 .
```

Run a Redis server with:
```bash
docker run -p 6379:6379 -d redis
```

Run the *dialogflow-webhook* container with:
```bash
docker run -p 8080:8080 $(USER)/dialogflow-webhook:1.0
```

## Heroku

Add a remote repo with:
```bash
heroku git:remote -a {heroku-app-name}
```

Provision a Redis server on Heroku with:
```bash
heroku addons:create heroku-redis:hobby-dev
```

Deploy the DialogFlow server to heroku with:
```bash
git push heroku master
```

The deployed app's URL will be: https://{heroku-app-name}.herokuapp.com

## Docker Compose

Use [Docker Compose](https://docs.docker.com/compose/) to deploy the *dialogflow-webhook* container and Redis server together with:
```bash
docker-compose -f docker-compose.yml up
```