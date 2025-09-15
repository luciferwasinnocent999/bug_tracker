class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/bugtracker'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = 'supersecret'
    SECRET_KEY = 'supersecret-session' 