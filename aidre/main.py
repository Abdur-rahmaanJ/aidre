from flask import (
    Flask, redirect, url_for, render_template, request
    )
import polib
from github import Github
from translate import Translator
import urllib

app = Flask(__name__)

path_now = ''

# name, description, link, font-awesome class
MENUS = [
    ['EDITOR', 'edit any .po file', '/editor', 'fas fa-pencil-alt'],
    ['ADD FORK', 'add fork to software', '#', 'fas fa-plus-square'],
    ['BROWSE FORK', 'browse added forks', '#', 'fas fa-ship'],
    ['SYNCHRONISE FORK', 'update from original repo', '#', 'fas fa-sync'],
    ['STATS', 'stats for translation repo', '/stats', 'fas fa-chart-pie'],
]

def check_internet(): 
    errors.append('internet not available')
    try :
        url = "https://www.google.com"
        urllib.urlopen(url)
        return 0
    except:
        return -1

@app.route('/')
def index():
    return render_template('index.html', menus=MENUS, errors=['fwefwwgw', 'wgeweg'])


@app.route('/editor', methods=['GET', 'POST'])
def list_strings():
    global path_now
    global errors
    errors = []
    if check_internet() == -1:
        errors.append('internet not available')
        return render_template(
            'editor.html', errors=['internet not available'])
    if request.method == 'POST':
        try:
            strings = []
            fpath = request.form['fpath']
            path_now = fpath
            po = polib.pofile(fpath)
            translated = po.percent_translated()
            translator = Translator(to_lang="ar")
            for i, entry in enumerate(po):
                suggest = translator.translate(entry.msgid)
                strings.append([entry.msgid, entry.msgstr, i+1, suggest])
        except OSError:
            errors.append('wrong path')
        except Exception as e:
            errors.append(e)
        return render_template(
            'editor.html', strings=strings, path=fpath,
            translated=translated, errors=errors)
    return render_template(
        'editor.html', strings=[], path='', translated='---', errors=[])


@app.route('/stats')
def stats():

    num_open = 210
    num_closed = 10
    num_issues = num_open + num_closed
    percent_open = (num_open/num_issues) * 100
    percent_closed = (num_closed/num_issues) * 100
    return render_template('stats.html',
        issues=['Issue1', 'Issue2','Issue3'],
        num_open=num_open,
        num_closed=num_closed,
        num_issues=num_issues,
        percent_open=percent_open,
        percent_closed=percent_closed)

@app.route('/modify', methods=['GET', 'POST'])
def modify_id():
    global path_now
    if request.method == 'POST':
        strings = []

        fpath = path_now  # request.form['fpath']
        msg_id = request.form['msg_id']
        modified_str = request.form['modified_str']

        po = polib.pofile(fpath)
        translated = po.percent_translated()
        entry = po.find(msg_id, by='msgid')
        entry.msgstr = modified_str
        po.save(path_now)

        for i, entry in enumerate(po):
            strings.append([entry.msgid, entry.msgstr, i+1])

        return render_template(
            'editor.html', strings=strings, path=fpath,
            translated=translated, errors=[])
    return ''
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
