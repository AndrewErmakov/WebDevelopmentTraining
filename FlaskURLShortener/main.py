from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    session,
    jsonify)

import json
import os.path

app = Flask(__name__)
app.secret_key = 'shtopor'


@app.route('/')
def index():
    return render_template('index.html', codes=session.keys())


@app.route('/your-url', methods=['POST', 'GET'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as file:
                urls = json.load(file)

        if request.form['code'] in urls.keys():
            flash('That short name has already been taken')
            return redirect(url_for('index'))

        urls[request.form.get('code')] = {'url': request.form['url']}
        with open('urls.json', 'w') as file:
            json.dump(urls, file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form.get('code'))
    else:
        return redirect(url_for('index'))


@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as file:
            urls = json.load(file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])

    return abort(404)


# custom handler 404 error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


if __name__ == "__main__":
    app.run()
