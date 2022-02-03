# Cointracker
project for cointracker


simple flask web app wrapped with a docker container for simple demo


## how to run
go to root directory

build docker image `docker image build -t docker-flask-test .`

run docker container `docker run -p 5000:5000 -d docker-flask-test`

to stop the container run `docker kill $(docker ps -q)`


## part2 fuzzy transfer detection 

located in `/Flask-Web-App/website/detect_transfers.py`

demo without audio: https://youtu.be/gYryF4dHYaw
