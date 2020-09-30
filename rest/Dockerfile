FROM python:3.7-slim
WORKDIR /secaid
ADD . /secaid
RUN pip install -r requirements.txt
EXPOSE 5000
ARG keycloak_setting=/secaid/app/main/util/local_settings.py
ENV KEYCLOAK_FLASK_SETTINGS=${keycloak_setting}
CMD ["python", "manage.py", "run"]