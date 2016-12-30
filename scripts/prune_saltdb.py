#!/usr/bin/env python

import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://salt:salt@127.0.0.1:5432/salt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
meta = db.metadata
engine = db.engine
db.Model.metadata.reflect(db.engine)

class Jids(db.Model):
    __table__ = db.Model.metadata.tables['jids']

class Returns(db.Model):
    __table__ = db.Model.metadata.tables['salt_returns']

keepdays = 10

def clean(keepdays):
    old_returns = Returns.query.filter(Returns.alter_time < datetime.datetime.utcnow() - datetime.timedelta(days=keepdays))
    try:
        o = old_returns[0]
        tzinfo = o.alter_time.tzinfo
        old_returns = Returns.query.filter(Returns.alter_time < datetime.datetime.now(tzinfo) - datetime.timedelta(days=keepdays))
        jids = set([Jids.query.filter(Jids.jid == o.jid) for o in old_returns])
        print("Pruning {0} old jobs and {1} old returns".format(len(jids), old_returns.count()))
        for job in jids:
            job.delete()
        old_returns.delete()
        db.session.commit()
    except IndexError:
        pass

if __name__=='__main__':
    clean(keepdays)
