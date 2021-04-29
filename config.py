import os

secrets = {}

if 'MODE_ACCESS_KEY' in os.environ and 'MODE_ACCESS_SECRET' in os.environ and 'MODE_TEAM' in os.environ and 'TOKEN' in os.environ:
    secrets['mode_access_key'] = os.getenv('MODE_ACCESS_KEY')
    secrets['mode_access_secret'] = os.getenv('MODE_ACCESS_SECRET')
    secrets['mode_team'] = os.getenv('MODE_TEAM')
    secrets['access_token'] = os.getenv('TOKEN')
else:
    print("The following environment variables must be present: MODE_ACCESS_KEY, MODE_ACCESS_SECRET, MODE_TEAM and TOKEN")
    exit(1)

reports = {
    'account': {
        'mode_report': '3a56c4ec192c',
        'param_name': 'param_account_id',
        'param_default_value': '0011N00001g3ns7QAA',
    },
    'opportunity': {
        'mode_report': '2cfd0c546cec',
        'param_name': 'param_team_id',
        'param_default_value': '110',
    }
}

listen_port = 8080
if 'PORT' in os.environ:
    listen_port = int(os.getenv('PORT'))
