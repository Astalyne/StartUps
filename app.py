from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from startup_setup import Base, Startup, Founder

app = Flask(__name__)

engine = create_engine('sqlite:///startup.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()


@app.route('/')
@app.route('/startups')
def show_startups():
    startups = db_session.query(Startup).all()
    return render_template('startups.html', startups=startups)


@app.route('/startups/<int:startup_id>/')
def show_startup(startup_id):
    startup = db_session.query(Startup).filter_by(id=startup_id).one()
    founders = db_session.query(Founder).filter_by(startup_id=startup_id).all()
    return render_template('startup.html', startup=startup, founders=founders)


@app.route('/startups/<int:startup_id>/founders/new', methods=['GET', 'POST'])
def create_founder(startup_id):
    if request.method == 'POST':
        new_founder = Founder(name=request.form['name'], startup_id=startup_id)
        db_session.add(new_founder)
        db_session.commit()

        return redirect(url_for('show_startup', startup_id=startup_id))
    else:
        # startup = db_session.query(Startup).filter_by(startup_id=startup_id).one()
        return render_template('create_founder.html', startup=startup_id)


@app.route('/startups/<int:startup_id>/founders/<int:founder_id>/edit', methods=['GET', 'POST'])
def edit_founder(startup_id, founder_id):
    founder = db_session.query(Founder).filter_by(id=founder_id).one()
    if request.method == 'POST':
        if request.form['name']:
            founder.name = request.form['name']
        if request.form['bio']:
            founder.bio = request.form['bio']
        db_session.add(founder)
        db_session.commit()
        return redirect(url_for('show_startup', startup_id=startup_id))
    else:
        return render_template('edit_founder.html', startup_id=startup_id, founder_id=founder_id, founder=founder)


@app.route('/startups/<int:startup_id>/founders/<int:founder_id>/delete', methods=['GET', 'POST'])
def delete_founder(startup_id, founder_id):
    founder = db_session.query(Founder).filter_by(id=founder_id).one()
    if request.method == 'POST':
        db_session.delete(founder)
        db_session.commit()
        return redirect(url_for('show_startup', startup_id=startup_id))
    return render_template('delete_founder.html', founder=founder)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
