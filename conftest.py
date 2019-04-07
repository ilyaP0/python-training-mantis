from fixture.application import Application
import pytest
import json
import os.path
import importlib
import jsonpickle
import ftputil


fixture = None
target = None

def load_config(file):
   global target
   if target is None:
      config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
      with open(config_file) as f:
         target = json.load(f)
   return target

@pytest.fixture
def app(request, config):
   global fixture
   browser = request.config.getoption("--browser")
   if fixture is None or not fixture.is_valid():
      fixture = Application(browser=browser, config=config)
   fixture.session.ensure_Login(username=config['webadmin']["username"], password=config['webadmin']["password"])
   return fixture

@pytest.fixture(scope="session")
def config(request):
   return load_config(request.config.getoption("--target"))



@pytest.fixture (scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
   with ftputil.FTPHost(host, username, password) as remote:
      if remote.path.isfile("config_inc.php.back"):
         remote.remove("config_inc.php.back")
      if remote.path.isfile("config_inc.php"):
         remote.rename("config_inc.php", "config_inc.php.back")
      remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
   with ftputil.FTPHost(host, username, password) as remote:
      if remote.path.isfile("config_inc.php.back"):
         if remote.path.isfile("config_inc.php"):
            remote.remove("config_inc.php")
            remote.rename("config_inc.php.back", "config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
   def fin():
      fixture.session.ensure_Logout()
      fixture.destroy()
   request.addfinalizer(fin)
   return fixture


def pytest_addoption(parser):
   parser.addoption("--browser", action="store", default="firefox")
   parser.addoption("--target", action="store", default="target.json")
   parser.addoption("--check_ui", action="store_true")


def pytest_generate_tests(metafunc):
   for fixture in metafunc.fixturenames:
      if fixture.startswith("data_"):
         Testdata = load_from_module(fixture[5:])
         metafunc.parametrize(fixture, Testdata, ids=[str(x) for x in Testdata])
      elif fixture.startswith("json_"):
         Testdata = load_from_json(fixture[5:])
         metafunc.parametrize(fixture, Testdata, ids=[str(x) for x in Testdata])

def load_from_module(module):
   return importlib.import_module("data.%s" % module).Testdata

@pytest.fixture
def check_ui(request):
   return request.config.getoption("--check_ui")

def load_from_json(file):
   with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
      return jsonpickle.decode(f.read())

