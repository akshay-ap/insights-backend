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