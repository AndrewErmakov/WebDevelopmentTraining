from flask import Flask, render_template, request, redirect

from parser_job_site import get_jobs

app = Flask('JobScrapper')

db = {}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/report')
def contact():
    keyword = request.args.get('keyword')

    if keyword is not None:
        keyword = keyword.lower()

        get_db = db.get(keyword)
        if get_db:
            jobs = get_db
        else:
            jobs = get_jobs(keyword)
            db[keyword] = jobs
        print(jobs)
    else:
        return redirect('/')

    return render_template('report.html', searchBy=keyword, count=len(jobs), jobs=jobs)


@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            raise Exception()
        jobs = db.get(keyword.lower())
        if not jobs:
            raise Exception()
        return f'Генерация csv по запрос {keyword}'
    except Exception as e:
        print(e)
        return redirect('/')


app.run(host='127.0.0.1', debug=True)
