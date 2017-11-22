from flask_sqlalchemy import SQLAlchemy
import logging as lg
import sqlite3
import pandas as pd
import psycopg2
import os

from .views import app

db = SQLAlchemy(app)


def init_db():
    db.drop_all()
    db.create_all()

    if os.environ.get('DATABASE_URL') is None:

        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.executescript('drop table if exists Content;')

        df = pd.read_csv('recommandation_system_light.csv')
        df.to_sql('Content', conn, if_exists='append', index=False)

        db.session.commit()
        lg.warning('Database initialized!')

    else:
        from urllib import parse
        from sqlalchemy import create_engine

        parse.uses_netloc.append("postgres")
        url = parse.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(database=url.path[1:],user=url.username,
        password=url.password,host=url.hostname,port=url.port)

        c = conn.cursor()
        c.execute('drop table if exists Content;')
        db.session.commit()

        df = pd.read_csv('recommandation_system_light.csv')
        engine = create_engine(os.environ["DATABASE_URL"])
        df.to_sql("Content", engine)

        db.session.commit()
        lg.warning('Database initialized!')
