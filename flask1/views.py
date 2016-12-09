"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from flask1 import app
from pcftemplate import pcftemplate
from pattern import Pattern
from products import product_to_business, environments

view_model = {}
nextid = 0

envs = environments.items() # [
    #('P', 'Production'),
    #('B', 'Beta'),
    #('U', 'UAT'),
    #('Q', 'QA')
#]

product_names = product_to_business.keys()

patterns = Pattern.pattern_fields.keys() # (
    # 'Solo', 'Alias', 'Point to Point', 
    # 'Router', 'Sender-Receiver', 'Client'
# )


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET','POST'])
@app.route('/template', methods=['GET','POST'])
def template():
    """ render the new template page depending on form input """
    if(request.method == 'POST'):

        # A new message pattern appears!
        if ('pattern' in request.form 
            and 'add' in request.form
            and request.form['pattern'] in Pattern.pattern_fields):

            # We're going to write to this, so it needs to be marked global
            global nextid 

            # Clear edit state of existing patterns, if any
            for k in view_model.keys():
                view_model[k]['edit'] = 0

            # initialize a new state blob with the right fields for the
            # requested pattern
            new_pattern = Pattern.Get(
                                request.form['pattern'],
                                request.form['product'],
                                request.form['envs'])
            view_model[nextid] = {
                'id' : nextid,
                'edit' : 1, # new patterns start in edit mode
                'pattern' : new_pattern
             }
            nextid += 1

        # We're working with individual patterns here
        elif 'id' in request.form:
            # Delete this pattern from the list
            if 'delete' in request.form:
                try:
                    del view_model[int(request.form['id'])]
                except (KeyError, ValueError):
                    pass # ok to delete non-existent item

            # A pattern has been selected for editing. 
            # Un-set edit state of other patterns and flag this one
            elif 'edit' in request.form:
                try:
                    requested_id = int(request.form['id'])
                    if requested_id in view_model:
                        for pattern_id in view_model.keys():
                            view_model[pattern_id]['edit'] = 0
                        view_model[requested_id]['edit'] = 1
                except ValueError: # bogus pattern id. Ignore and move on
                    pass

            # Cancel editing
            elif 'cancel' in request.form:
                try:
                    requested_id = int(request.form['id'])
                    view_model[requested_id]['edit'] = 0
            
                except (KeyError, ValueError): # ignore bad input
                    pass

            # Accept updated data
            elif 'ok' in request.form:
                try:
                    requested_id = int(request.form['id'])
                    view_model[requested_id]['edit'] = 0
                    fields = view_model[requested_id]['pattern'].pattern_fields

                    # update each field in the pattern
                    for field_name in fields.keys():
                        try:
                            pattern = view_model[requested_id]['pattern']
                            pattern.pattern_fields[field_name] = request.form[field_name]
                        except KeyError:
                            pass

                    # update the note last in case it throws
                    view_model[requested_id]['pattern'].note = request.form['note']
                except (KeyError, ValueError):
                    pass

        # User thinks they're done
        elif 'save' in request.form:
            pcf = pcftemplate(view_model)
            if pcf.is_valid:
                pass # eventually render pcf from xml template
            else:
                return render_template('templ.html', 
                            state = view_model.values(), 
                            envs = envs, 
                            products = product_names,
                            patterns = patterns,
                            error = pcf.error)
  
    return render_template('templ.html', 
                            state = view_model.values(), 
                            envs = envs, 
                            products = product_names,
                            patterns = patterns)
