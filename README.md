# Stream 25_percentile, 50_percentile, 75_percentile

## Run:

```bash
cd docker
docker-compose up -d

docker exec stream run_stream_generator
```

## In repo:
- endpoint (receive UDP stream)
- stream generator (generate random number and send it with some delay by UDP)
- postgresql for storing values
