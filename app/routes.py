import requests
from requests.exceptions import Timeout, ConnectionError
from re import findall
from datetime import datetime
from dill import dumps
from flask import render_template, request, redirect, flash
from app import app, db, celery
from .models import Results, Tasks
from .forms import WebsiteForm

nsq_address = app.config['NSQHTTP_ADDRESS']
nsq_topic = app.config['NSQ_TOPIC']

class NSQD:
    def __init__(self, server):
        self.server= "http://{server}/pub".format(server=server)

    def send(self, topic, msg):
        res = requests.post(self.server, params={"topic": topic}, data=msg)
        if res.ok:
            return res

nsqd = NSQD(nsq_address)

def millis(start_time):
   dt = datetime.now() - start_time
   ms = round((dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0)
   return ms

def create_task(address, status):
    print(status)
    task = Tasks(address=address,
                 create_time=datetime.now(),
                 task_status=status)
    db.session.add(task)
    db.session.commit()
    return task

def set_task_status(_id, status):
    print(status)
    task = Tasks.query.get(_id)
    task.task_status = status
    db.session.add(task)
    db.session.commit()
    return task

def set_result(address, word_count, create_time, status_code, status):
    elapsed_time = millis(create_time)
    result = Results(address=address,
                     word_count=word_count,
                     elapsed_time=elapsed_time,
                     create_time=create_time,
                     http_status_code=status_code,
                     status=status)
    db.session.add(result)
    db.session.commit()
    return result

@celery.task
def parse_webpage(_id):
    task = set_task_status(_id, 'PENDING')
    url = task.address
    try:
        res = requests.get(url, timeout=10) 
        if res.ok:
            word_count = len(findall(r'[P,p]ython', res.text))
            task = set_task_status(_id, 'FINISHED')
            set_result(url, word_count, task.create_time, res.status_code, 'Расчёт произведён')
        else:
            raise Exception()
    except Timeout as ex:
        task = set_task_status(_id, 'FINISHED')
        set_result(url, 0, task.create_time, 404, 'Превышен интервал ожидания')
    except ConnectionError as ex:
        task = set_task_status(_id, 'FINISHED')
        set_result(url, 0, task.create_time, 404, 'Ошибка http-соединения')
    except Exception:
        task = set_task_status(_id, 'FINISHED')
        set_result(url, 0, task.create_time, 404, 'Неизвестная ошибка')
    else:
        try:
            print('NSQD address = {}'.format(nsq_address))
            print('NSQD topic = {}'.format(nsq_topic))
            data = {'address': url,
                    'word_count': word_count,
                    'create_time': task.create_time,
                    'status_code': res.status_code,
                    'status': 'Расчёт произведён'
                   }
            nsqd.send(nsq_topic, dumps(data))
        except:
            pass

@app.route('/', methods=['POST', 'GET'])
@app.route('/add_website', methods=['POST', 'GET'])
def website():
    website_form = WebsiteForm()
    if request.method == 'POST':
        if website_form.validate_on_submit():
            url = request.form.get('address')
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'http://' + url
            task = create_task(url, 'UNSTARTED')
            parse_webpage.delay(task._id)
            flash('Успех: задание отправлено на анализ')
            return redirect('/')
        flash('Ошибка: неверный формат ввода данных')
    return render_template('add_website.html', form=website_form)

@app.route('/results')
def get_results():
    results = Results.query.all()
    return render_template('results.html', results=results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404