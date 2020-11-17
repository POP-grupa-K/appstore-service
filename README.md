# appstore-service

appstore-service component of our system

## Installation

Clone repository to your machine.

```bash
git clone https://github.com/POP-grupa-K/appstore-service.git
```

## Usage

Enter repo root directory and run:

```bash
docker-compose up
```

Container should run on localhost on port (current 8005) pointed in:
```bash
docker-compose.yml
```

### Endpoints
```bash
GET	appstore/rating/app/{app_uid} -> ratingi apliakcji
DELETE  appstore/rating/{rating_id}   -> usun rating
PUT 	appstore/rating/{rating_id}   -> update ratingu
GET 	appstore/rating/{rating_id}   -> pobierz po id
POST	appstore/{id_app}/rate	      -> dodaj rating
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)