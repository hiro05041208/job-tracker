from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(companies):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)

def next_id(companies):
    return max((c['id'] for c in companies), default=0) + 1

def days_until(deadline_str):
    """締切までの日数を返す。締切なしはNone、過去はマイナス"""
    if not deadline_str:
        return None
    try:
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        return (deadline - datetime.now()).days
    except ValueError:
        return None

def deadline_urgency(deadline_str):
    """締切の緊急度を返す: 'danger', 'warning', 'normal', None"""
    days = days_until(deadline_str)
    if days is None:
        return None
    if days < 0:
        return 'past'
    if days <= 3:
        return 'danger'
    if days <= 7:
        return 'warning'
    return 'normal'

@app.route('/')
def index():
    companies = load_data()
    status_filter = request.args.get('status', 'all')
    sort = request.args.get('sort', 'default')

    if status_filter != 'all':
        filtered = [c for c in companies if c['status'] == status_filter]
    else:
        filtered = companies

    # 締切順ソート
    if sort == 'deadline':
        filtered = sorted(filtered, key=lambda c: c['deadline'] if c['deadline'] else '9999')

    # 各企業に緊急度と残り日数を付加
    for c in filtered:
        c['urgency'] = deadline_urgency(c['deadline'])
        c['days_left'] = days_until(c['deadline'])

    counts = {
        'total': len(companies),
        'es': sum(1 for c in companies if c['status'] == 'ES提出'),
        'interview': sum(1 for c in companies if c['status'] == '面接'),
        'offer': sum(1 for c in companies if c['status'] == '内定'),
    }
    return render_template('index.html', companies=filtered, counts=counts,
                           status_filter=status_filter, sort=sort)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        companies = load_data()
        company = {
            'id': next_id(companies),
            'name': request.form['name'],
            'status': request.form['status'],
            'deadline': request.form['deadline'],
            'memo': request.form['memo'],
        }
        companies.append(company)
        save_data(companies)
        return redirect(url_for('index'))
    return render_template('form.html', company=None, action='add')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    companies = load_data()
    company = next((c for c in companies if c['id'] == id), None)
    if not company:
        return redirect(url_for('index'))
    if request.method == 'POST':
        company['name'] = request.form['name']
        company['status'] = request.form['status']
        company['deadline'] = request.form['deadline']
        company['memo'] = request.form['memo']
        save_data(companies)
        return redirect(url_for('index'))
    return render_template('form.html', company=company, action='edit')

@app.route('/delete/<int:id>')
def delete(id):
    companies = load_data()
    companies = [c for c in companies if c['id'] != id]
    save_data(companies)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
