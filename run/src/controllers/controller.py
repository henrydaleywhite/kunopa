from flask import Blueprint,redirect,render_template,request,session,url_for

controller = Blueprint('fb',__name__)

@controller.route('/', methods=['GET','POST'])
def frontpage():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if request.form['button'] == 'Full Application':
            session['app_use'] = 'full'
            return redirect(url_for('fb.ingredient_selection'))
        elif request.form['button'] == 'Ingredient Selection Only':
            session['app_use'] = 'ingredients'
            return redirect(url_for('fb.ingredient_selection'))
        elif request.form['button'] == 'API Only':
            session['app_use'] = 'search'
            return redirect(url_for('fb.api_search_input'))
        elif request.form['button'] == 'View Ingredient Information':
            return redirect(url_for('fb.ingredient_info'))


@controller.route('/ingredient_selection', methods=['GET','POST'])
def ingredient_selection():
    if request.method == 'GET':
        return session['app_use']
    elif request.method == 'POST':
        pass


@controller.route('/api_input', methods=['GET','POST'])
def api_search_input():
    if request.method == 'GET':
        return session['app_use']
    elif request.method == 'POST':
        pass


@controller.route('/ingredient_info', methods=['GET','POST'])
def ingredient_info():
    if request.method == 'GET':
        return 'info list'
    elif request.method == 'POST':
        pass