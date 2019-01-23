from flask import Blueprint,redirect,render_template,request,session,url_for

controller = Blueprint(__name__)

@controller.route('/', methods=['GET','POST'])
def frontpage():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if request.form['button'] == 'Full Application':
            session['app_use'] = 'full'
            return redirect(url_for('ingredient_selection'))
        elif request.form['button'] == 'Ingredient Selection Only':
            session['app_use'] = 'ingredients'
            return redirect(url_for('ingredient_selection'))
        elif request.form['button'] == 'API Only':
            session['app_use'] = 'search'
            return redirect(url_for('api_search_input'))
        elif request.form['button'] == 'View Ingredient Information':
            return redirect(url_for('ingredient_info'))


@controller.route('ingredient_selection', methods=['GET','POST'])
def ingredient_selection():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass