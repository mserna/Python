import json, os, requests

# ## GLOBALS ##

HOST = 'http://localhost:3000'
headers = {'Authorization': 'Bearer %s' % (KEY,)}

old_datasource = ""
old_title = ""
new_targets = []
old_thresholds = []
old_json = []
new_json = []
skip = []
counter = 0
old_panel = 'btplc-status-dot-panel'
new_panel = 'blackmirror1-singlestat-math-panel'
str_thresholds = ''

## LOAD GRAFANA INSTANCE ##
try:
    request = requests.get('%s/api/search?query=&' % (HOST,), headers=headers)
    print request # Will get 200 if successful
except Exception:
    import traceback
    print("traceback: " + traceback.format_exc())

dashboards = request.json()

for dashboard in dashboards:
  if dashboard['type'] == '"btplc-status-dot-panel"' or dashboard['uid'] in skip:
    continue
  counter += 1
  new_request = requests.get('%s/api/dashboards/uid/%s' % (HOST, dashboard['uid']), headers=headers)
  dash_json = json.loads(new_request.text.encode('utf-8'))
  new_counter = 1
  if "message" in dash_json:
    print dash_json
    continue
  if dashboard['uid'] == 'e5eEliWik':
    if 'panels' in dash_json['dashboard']:
      for field in dash_json['dashboard']['panels']:
        new_thresholds = []
        new_color_array = []
        if field['title'] == "":
          continue
        if field['type'] == old_panel:
          print "Yea, duh! Type is on " + str(new_counter) + ": " + dashboard['uid']
          new_counter += 1
          field['type'] = new_panel
          field['colorBackground'] = True
          field['circleBackground'] = True
          field['valueName'] = "current"
          field['defaultColor'] = field['defaultColor']
          print(field['defaultColor'])
          if len(str(field['format'])) > 7:
            print field['format']
            field['format'] = 'none'
    dash_json['message'] = 'Status Dot panel changed to SingleStat Math panel'
    dash_json['folderId'] = dash_json['meta']['folderId']
    dash_json['overwrite'] = True
    res = requests.post('%s/api/dashboards/db' % HOST, headers=headers, json=dash_json)