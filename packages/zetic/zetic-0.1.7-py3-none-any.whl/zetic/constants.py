# Create a new env.py during build process
ENV = "production"  # This will be replaced during build


class Constants:
    API_URL = "https://api.zetic.ai" if ENV == "production" else "http://localhost:8000"
    WEB_URL = "https://mlange.zetic.ai" if ENV == "production" else "http://localhost:3000"


constants = Constants()
