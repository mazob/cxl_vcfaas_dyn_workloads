FROM python:3

WORKDIR /usr/src/app
COPY * ./

#COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN ls -latr
#COPY * ./

CMD [ "python", "/usr/src/app/vmscheduler.py" ]
