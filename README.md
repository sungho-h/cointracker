# Cointracker
project for cointracker


simple flask web app wrapped with a docker container for simple demo

build docker image `docker image build -t docker-flask-test .`

run docker container `docker run -p 5000:5000 -d docker-flask-test`

to stop the container run `docker kill $(docker ps -q)`
