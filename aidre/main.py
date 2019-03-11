from flask import (
    Flask, redirect, url_for, render_template, request
    )
import polib

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


@app.route('/')
def index():
    return render_template('index.html', menus=MENUS, errors=['fwefwwgw', 'wgeweg'])


@app.route('/editor', methods=['GET', 'POST'])
def list_strings():
    global path_now
    errors = []
    translated = ''
    if request.method == 'POST':
        try:
            strings = []
            fpath = request.form['fpath']
            path_now = fpath
            po = polib.pofile(fpath)
            translated = po.percent_translated()
            for i, entry in enumerate(po):
                strings.append([entry.msgid, entry.msgstr, i+1])
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
    return render_template('stats.html')

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
