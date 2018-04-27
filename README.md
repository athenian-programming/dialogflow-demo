# dialogflow-demo

## DialogFlow Tutorial
https://dialogflow.com/docs/getting-started/building-your-first-agent


## Setup

Install the required python packages with:
```bash
pip install -r requirements.txt
```

## Execution

### Standalone

Run 'webhook.py' with:
```bash
python webhook.py
```

### ngrok

Run [ngrok](https://ngrok.com) with:
```bash
ngrok http 5000
```

### docker
Build the *dialogflow-webhook* container with:

```bash
docker build -t dialogflow-webhook .
```

Run the *dialogflow-webhook* container with:

```bash
docker run -p 8080:8080 dialogflow-webhook
```

## Heroku

Add a remote repo with:
```bash
heroku git:remote -a {heroku-app-name}
```

Deploy to heroku with:
```bash
git push heroku master
```

Reach the deployed app at https://{heroku-app-name}.herokuapp.com