from flask import Flask, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

ITEMS_PER_PAGE = 10

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


'''
VIEWS
'''

@app.route('/minions/')
@app.route('/minions/page')
@app.route('/minions/page/<int:page>')
def minion_list(page=1):
    minions = Returns.query.order_by('id').distinct('id').paginate(page, ITEMS_PER_PAGE, False)
    return render_template('minions.html', minions=minions, page=page)

@app.route('/minions/<minion_id>')
@app.route('/minions/<minion_id>/page')
@app.route('/minions/<minion_id>/page/<int:page>')
def minion_detail(minion_id, page=1):
    returns = Returns.query.order_by(Returns.jid.desc()).filter(Returns.id==minion_id).paginate(page, ITEMS_PER_PAGE, False)
    return render_template('minion.html', id=minion_id, returns=returns, page=page)

@app.route('/jobs/')
@app.route('/jobs/page')
@app.route('/jobs/page/<int:page>')
def job_list(page=1):
    jids = Jids.query.order_by(Jids.jid.desc()).paginate(page, ITEMS_PER_PAGE, False)
    return render_template('jobs.html', jids=jids, page=page)

@app.route('/jobs/<jid>')
def job_detail(jid):
    job = Jids.query.get(jid)
    returns = Returns.query.filter(Returns.jid==jid)
    return render_template('job.html', job=job, returns=returns)

@app.route('/returns/')
@app.route('/returns/page')
@app.route('/returns/page/<int:page>')
def return_list(page=1):
    returns = Returns.query.order_by(Returns.jid.desc()).paginate(page, ITEMS_PER_PAGE, False)
    return render_template('returns.html', returns=returns, page=page)

@app.route('/returns/<id>')
def return_detail(id):
    return_data = Returns.query.get(id)
    return render_template('return.html', id=id, return_data=return_data)

@app.route('/')
@app.route('/changes/')
@app.route('/changes/page')
@app.route('/changes/page/<int:page>')
def change_list(page=1):
    returns = Returns.query.filter(Returns.changes==True).order_by(Returns.alter_time.desc()).paginate(page, ITEMS_PER_PAGE, False)
    return render_template('changes.html', returns=returns, page=page)

if __name__ == '__main__':
    app.run(debug=True)
