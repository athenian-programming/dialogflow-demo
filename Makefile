
list-containers:
	docker ps -a

rm-containers:
	docker ps -q -a | xargs docker rm

build:
	docker build -t $(USER)/dialogflow-webhook:1.0 .

docker-run:
	docker run -p 8080:8080 $(USER)/dialogflow-webhook:1.0

docker-push:
	docker push $(USER)/dialogflow-webhook:1.0

heroku-push:
	git push heroku master