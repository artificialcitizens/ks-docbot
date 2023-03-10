`docker build --tag docbotapi .` - builds tag from docker file
`docker run -d --name docbotapi docbotapi:latest` - runs container
`docker tag docbotapi artificialcitizens.azurecr.io/docbotapi` - copies tag to azure
`docker push artificialcitizens.azurecr.io/docbotapi` - pushes to image repo


## install locally

`pip install -r requirements.txt`
`python doc_bot_api.py`