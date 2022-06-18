# insights-backend


## Run mongodb

```bash
docker run --rm -it --name mongodb -p 27016:27017 -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=password -v $PWD/mongodb_data:/data/db mongo
```

```bash
pip install flask pymongo python-dotenv black web3
```

## Bump version

```bash
$ bump2version --current-version 0.0.1 --no-tag patch setup.py 
```

## Docker

### Build container

```bash
docker build . -f Dockerfile -t insights-backend
```

### Run container

```bash
docker run --rm -it --name insights -p 8080:5000 -v $PWD/.env:/home/appuser/app/.env insights-backend
```
