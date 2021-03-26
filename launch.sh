docker build -t candy-api .
docker run --rm --name candy -p 8080:8080 candy-api
