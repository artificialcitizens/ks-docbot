## Docker/Azure
`docker build --tag docbot .` - builds tag from docker file
`docker run -d --name -p 5000:5000 docbot docbot:latest` - runs container
`docker tag docbot artificialcitizens.azurecr.io/docbot` - copies tag to azure
`docker push artificialcitizens.azurecr.io/docbot` - pushes to image repo

Todo: https://stackoverflow.com/questions/49796968/update-docker-image-in-azure-container-instances