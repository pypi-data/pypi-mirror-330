class APIConfig:
    BASE_URL = "http://localhost:8080"
    VERSION = "v1"
    
    @classmethod
    def get_url(cls, endpoint):
        return f"{cls.BASE_URL}/{cls.VERSION}/{endpoint}"