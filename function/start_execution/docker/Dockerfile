FROM public.ecr.aws/lambda/python:3.8

COPY /src/app.py ./
COPY /src/lib ./lib
COPY /src/requirements.txt ./

RUN ["pip", "install", "-r", "./requirements.txt"]

RUN ["ls"]

CMD ["app.handler"]