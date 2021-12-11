FROM postgres:latest
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_USER=parrot
ENV POSTGRES_DB=parrot
COPY structure.sql /docker-entrypoint-initdb.d/structure.sql
