# insights-backend


## Run mongodb

```bash
docker run --rm -it --name mongodb -p 27016:27017 -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=user -v $PWD/mongodb_data:/data/db mongo
```

```bash
pip install flask pymongo python-dotenv
```