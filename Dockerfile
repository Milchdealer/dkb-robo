FROM python:3.8-slim
LABEL MAINTAINER="Milchdealer/Teraku"

WORKDIR /usr/src/app

RUN pip install --no-cache-dir dkb_robo

COPY src/main.py .

CMD ["python", "./main.py", "--secret_file", "./.secrets/dkb", "--out_folder", "./out"]
