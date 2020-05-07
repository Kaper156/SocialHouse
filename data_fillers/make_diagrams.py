from data_fillers.helpers import *

FOLDER = '../docs/diagrams/'

args = f'graph_models %s -g -o {FOLDER}%s.png'
# args = 'graph_models %s -g -o %s.png -n' # In russian
# args_exclude = args.replace('-g', '-g -X %s')
args_exclude = args + ' -X %s'
exclude = {
    # 'people': 'User',
}

# apps = {app.__name__: app for app in apps.get_app_configs()}

apps = [app for app in set(settings.MY_APPLICATIONS)
        # if not app.startswith("django.")
        # or not app.startswith('admin_tools.')
        # or not app.startswith('slugify')
        # or not app.startswith('crispy_forms')
        # or not app.startswith('formtools')
        ]

# # Make diagramm of all
# app_names = (app.split('.')[-1] for app in apps)
# arguments = args % (' '.join(app_names), '!all')
# management.call_command(*arguments.split(' '))
#
# # Make diagramm for each app
# for app_path in apps:
#     app_name = app_path.split('.')[-1]
#     app_path = FOLDER + app_path.replace('applications.', '')
#     print(f"{app_name}\t:{app_path}")
#
#     if exclude.get(app_name):
#         arguments = (args_exclude % (app_name, app_path, exclude.get(app_name)))
#     else:
#         arguments = (args % (app_name, app_path))
#     arguments = arguments.split(' ')
#     print(arguments)
#     management.call_command(*arguments)

# Make diagram for main apps
keys = (app_path.split('.')[-2] for app_path in apps if app_path.count('.') == 2)
main_apps = {key: list(filter(lambda a: key in a, apps)) for key in keys}
for main_app_name, sub_apps in main_apps.items():
    print(f"{main_app_name}\t:{sub_apps}")
    excluded = []
    for app in sub_apps:
        if exclude.get(app):
            excluded += exclude.get(app)

    sub_apps = list(map(lambda app: app.split('.')[-1], sub_apps))
    if excluded:
        excluded = ','.join(excluded)
        arguments = (args_exclude % (','.join(sub_apps), main_app_name, excluded))
    else:
        arguments = (args % (' '.join(sub_apps), main_app_name))
    arguments = arguments.split(' ')
    print(arguments)
    management.call_command(*arguments)
