import config as config
from app import db, create_app
import os
from app.utils import write_indexes


app = create_app(os.getenv('FLASK_ENV') or 'config.DevelopementConfig')

write_indexes()


if __name__ == '__main__':
    app.run()