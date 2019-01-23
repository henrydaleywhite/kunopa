from flask import Blueprint,redirect,render_template,request,session,url_for

from ..models.spoonacular_api import *
from ..models.model import get_base_ingredient_list, get_current_ingredient_list, ParentIngredient, ChildIngredient

controller = Blueprint('main',__name__)

@controller.route('/', methods=['GET','POST'])
def frontpage():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if request.form['button'] == 'Full Application':
            session['app_use'] = 'full'
            session['api_key'] = get_api_key('spoonacular_key.txt')
            return redirect(url_for('main.ingredient_selection'))
        elif request.form['button'] == 'Ingredient Selection Only':
            session['app_use'] = 'ingredients'
            return redirect(url_for('main.ingredient_selection'))
        elif request.form['button'] == 'API Only':
            session['app_use'] = 'search'
            session['api_key'] = get_api_key('spoonacular_key.txt')
            return redirect(url_for('main.api_search_input'))
        elif request.form['button'] == 'View Ingredient Information':
            return redirect(url_for('main.ingredient_info'))


@controller.route('/ingredient_selection', methods=['GET','POST'])
def ingredient_selection():
    if request.method == 'GET':
        return session['app_use']
        return render_template('ingredient_selection.html')
    elif request.method == 'POST':
        pass


@controller.route('/api_input', methods=['GET','POST'])
def api_search_input():
    if request.method == 'GET':
        # return session['app_use']
        return render_template('api_input.html')
    elif request.method == 'POST':
        ingredient_inputs = ['ing_1', 'ing_2', 'ing_3', 'ing_4', 'ing_5']
        search_terms = []
        session['num_results'] = request.form['num_results']
        for item in ingredient_inputs:
            if request.form[item] != "":
                search_terms.append(request.form[item])
        session['api_ingred'] = format_ingred_list(search_terms)
        return redirect(url_for('main.search_results'))


@controller.route('/ingredient_info', methods=['GET','POST'])
def ingredient_info():
    ingredients = get_base_ingredient_list()
    return render_template('ingredient_info.html', ingredients=ingredients)


@controller.route('/results', methods=['GET','POST'])
def search_results():
    # results_dict = api_call(session['api_key'], session['api_ingred'], session['num_results'])
    # TODO parse resulting json to work with JINJA in an html file
    return 'results displayed here'