from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
import plotly.express as px
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    frequency = db.Column(db.String(20), default='daily')
    
@app.route('/')
def index():
    habits = Habit.query.all()
    return render_template('index.html', habits=habits)

@app.route('/add', methods=['POST'])
def add_habit():
    name = request.form.get('name')
    frequency = request.form.get('frequency', 'daily')
    if name:
        new_habit = Habit(name=name, frequency=frequency)
        db.session.add(new_habit)
        db.session.commit()
        flash('Habit added successfully!', 'success')
    else:
        flash('Habit name cannot be empty!', 'error')
    return redirect(url_for('index'))

@app.route('/complete/<int:habit_id>')
def complete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if habit:
        habit.completed = True
        habit.completed_at = datetime.utcnow()
        db.session.commit()
        flash('Habit marked as completed!', 'success')
    return redirect(url_for('index'))

@app.route('/reset/<int:habit_id>')
def reset_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if habit:
        habit.completed = False
        habit.completed_at = None
        db.session.commit()
        flash('Habit reset successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:habit_id>')
def delete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if habit:
        db.session.delete(habit)
        db.session.commit()
        flash('Habit deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/plot')
def plot():
    habits = Habit.query.all()
    data = {
        'Habit': [habit.name for habit in habits],
        'Status': ['Completed' if habit.completed else 'Not Completed' for habit in habits],
        'Date': [habit.created_at.strftime('%Y-%m-%d') for habit in habits]
    }
    df = pd.DataFrame(data)
    fig = px.line(df, x='Date', y='Status', color='Habit', title='Evolution des Habitudes', markers=True)
    fig.update_layout(xaxis_title='Date', yaxis_title='Statut', legend_title='Habitude')
    graph_html = fig.to_html(full_html=False)
    return render_template('plot.html', graph_html=graph_html)

def send_daily_reminders():
    with app.app_context():
        habits = Habit.query.filter_by(frequency='daily').all()
        for habit in habits:
            if not habit.completed:
                # Simuler l'envoi d'un email (remplacez par votre logique d'envoi d'email)
                print(f"Reminder: {habit.name}")
scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_reminders, 'interval', days=1, start_date=datetime.now() + timedelta(seconds=10))
scheduler.start()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    


