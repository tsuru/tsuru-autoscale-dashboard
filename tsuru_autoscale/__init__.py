from tsuru_dashboard import engine

__version__ = "0.2.1"


class AutoScaleTab(engine.Tab):
    name = 'autoscale'
    url_name = 'autoscale-app-info'

try:
    engine.get('app').register_tab(AutoScaleTab)
except engine.AppNotFound:
    pass
