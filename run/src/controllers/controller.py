from flask import Blueprint,redirect,render_template,request,session,url_for

from ..models.spoonacular_api import *
from ..models.model import *

controller = Blueprint('main',__name__)

@controller.route('/', methods=['GET','POST'])
def frontpage():
    if request.method == 'GET':
        clear_results()
        to_del = []
        session.clear()
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
        if 'num' in session.keys():
            session['num'] += 1
            if session['num'] == 2:
                new_ingred = ParentIngredient(pk=session['pk'])
            else:
                new_ingred_child = ChildIngredient(pk=session['pk'])
                new_ingred = new_ingred_child.get_parent()
            new_ingred_par_pk = new_ingred.pk
            update_data_post_selection(new_ingred_par_pk)
            to_update = new_ingred.get_children()
            new_ingred.update_weightings(to_update, session['num']-1)
            populate_full_selection()
            cur = get_selected_ingredient_list()
            # weights = get_ingredient_weights()
            ingred = get_available_ingredient_list()
        else:
            session['num'] = 1
            cur = []
            ingred = get_base_ingredient_list()
            weights = ''
        return render_template('ingredient_selection.html',app_use=session['app_use'],ingred=ingred,num=session['num'], cur=cur)
    elif request.method == 'POST':
        if request.form['button'] == 'API Search':
            session['api_ingred'] = get_selected_ingredient_list()
            session['num_results'] = 2
            return redirect(url_for('main.search_results'))
        elif request.form['button'] == 'Back to Homepage':
            return redirect(url_for('main.frontpage'))
        else:
            child_pk = request.form['button'].split()[1]
            session.pop('pk', None)
            session['pk'] = child_pk
            return redirect(url_for('main.ingredient_selection'))


@controller.route('/api_input', methods=['GET','POST'])
def api_search_input():
    if request.method == 'GET':
        # return session['app_use']
        return render_template('api_input.html')
    elif request.method == 'POST':
        if request.form['button'] == 'Back to Homepage':
            return redirect(url_for('main.frontpage'))
        else:
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
    if request.method == 'GET':
        ingredients = get_base_ingredient_list()
        return render_template('ingredient_info.html', ingredients=ingredients)
    else:
        if request.form['button'] == 'Back to Homepage':
            return redirect(url_for('main.frontpage'))


@controller.route('/results', methods=['GET','POST'])
def search_results():
    if request.method == 'GET':
        api_key = session['api_key']
        ingredients = session['api_ingred']
        num_results = session['num_results']
        results_list = api_call(api_key, ingredients, num_results)
        print(results_list)
        return render_template('results.html', result=results_list)
        # TODO parse resulting json to work with JINJA in an html file
        # return "endpoint"
        # print_str = ""
        # for element in session['api_ingred']:
        #     print_str += element + ", "
        # return print_str
    else:
        if request.form['button'] == 'Back to Homepage':
            return redirect(url_for('main.frontpage'))
    
    
@controller.route('/about')
def about():
    pass