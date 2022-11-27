FROM python:3.5-alpine

WORKDIR /app

ENV REPOSITORY_ZIP=vandal-master

COPY . .

RUN unzip ${REPOSITORY_ZIP}.zip -d /tmp
RUN mkdir /app/vandal
RUN cp -r /tmp/${REPOSITORY_ZIP}/* /app/vandal
RUN rm ${REPOSITORY_ZIP}.zip

RUN pip install -r ./vandal/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 3000

CMD [ "python", "main.py"]