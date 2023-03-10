from langchain.document_loaders import YoutubeLoader

loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=20iV7caN3rc", add_video_info=True)
doc = loader.load()
print(doc)
