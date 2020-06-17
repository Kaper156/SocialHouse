from scripts.helpers import *

ONLY_SHOW_COMMAND = False
FOLDER = '../docs/diagrams/'

# args = f'graph_models %s -g -o {FOLDER}%s.json --theme=original --json --layout=circo'
# args = f'graph_models %s -g -o {FOLDER}%s.png --theme=original --layout=circle'
args = f'graph_models %s -g -o {FOLDER}%s.png --theme=original --layout=circle'
# args = 'graph_models %s -g -o %s.png -n' # In russian
# args_exclude = args.replace('-g', '-g -X %s')
args_exclude = args + ' -X %s'
exclude = {
    # 'people': 'User',
}

DEF_PARAMETERS = '--theme=original --layout=fdp --skip-checks'  #


def graph(models: list or tuple, parameters: list, out_file_name, as_dot=False):
    if not type(models) is str:
        models = ' '.join(models)
    if as_dot:
        graph_arguments = f"graph_models {models} -g  {DEF_PARAMETERS} --dot"
    else:
        graph_arguments = f"graph_models {models} -g -o {FOLDER}{out_file_name}.png {DEF_PARAMETERS}"
    graph_arguments += ' '.join(parameters)
    print(graph_arguments)
    if ONLY_SHOW_COMMAND:
        return graph_arguments
    graph_arguments = graph_arguments.split(' ')
    management.call_command(*graph_arguments)


# adsad=f"graph_models {al11} -e -g --theme=original -X=django*,admin_tools* --disable-abstract-fields --dot"

apps = [app for app in set(settings.MY_APPLICATIONS)]

# Make diagramm of all
all_apps = [app.split('.')[-1] for app in apps]
graph(all_apps, [], '!all')

# # Make diagramm for each app
for app_path in apps:
    app_name = app_path.split('.')[-1]
    app_path = app_path.replace('applications.', '')
    graph(app_name, [], app_path)

# Make diagram for main apps
apps = [app for app in set(settings.MY_APPLICATIONS)]
keys = (app_path.split('.')[-2] for app_path in apps if app_path.count('.') == 2)
main_apps = {key: list(filter(lambda a: key in a, apps)) for key in keys}
for main_app_name, sub_apps in main_apps.items():
    # print(f"{main_app_name}\t:{sub_apps}")
    sub_apps = list(map(lambda app: app.split('.')[-1], sub_apps))
    graph(sub_apps, [], main_app_name)
