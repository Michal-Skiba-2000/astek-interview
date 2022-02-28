# Starting application up
To build backend image run below command. It need to be executed only once
```
sudo docker build . --tag emenu-rest-api-image
```

To start up application run command:
```
sudo docker-compose up --no-build
```

To create superuser(admin):
```
sudo docker exec -it emenu-rest-api python manage.py createsuperuser
```
