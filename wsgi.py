

from app import create_app


if __name__=="__main__":
    flask_app = create_app("development")
    flask_app.run()
