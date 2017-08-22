#!/usr/bin/env python

import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://salt-admin:salt-passwd@127.0.0.1:5432/salt'
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
    o = Returns.query.filter(Returns.alter_time < datetime.datetime.utcnow() - datetime.timedelta(days=keepdays)).first()
    if o is not None:
        tzinfo = o.alter_time.tzinfo
        old_returns = Returns.query.filter(Returns.alter_time < datetime.datetime.now(tzinfo) - datetime.timedelta(days=keepdays))
        old_jobs = Jids.query.filter(Jids.jid <=o.jid)
        print("Pruning {0} old jobs and {1} old returns".format(old_jobs.count(), old_returns.count()))
        old_returns.delete()
        db.session.commit()

if __name__=='__main__':
    clean(keepdays)
