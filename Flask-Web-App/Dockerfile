# start by pulling the python image
FROM python:3.9

# copy the requirements file into the image
COPY ./requirements.txt /Flask-Web-App/requirements.txt

# switch working directory
WORKDIR /Flask-Web-App

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt

# copy every content from the local file to the image
COPY . /Flask-Web-App

# configure the container to run in an executed manner

CMD [ "python", "main.py" ]