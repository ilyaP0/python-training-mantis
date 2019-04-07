from model.project import Project
from model.project import Project
import string
import random
import pytest

def random_username(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

Testdata = [Project(name=random_username("project", 10))]

@pytest.mark.parametrize("project", Testdata, ids=[repr(x) for x in Testdata])

def test_add_project_soap(app, project):
    old_list_project = app.soap.get_user_projects("administrator", "root")
    if len(old_list_project) == 0:
        app.project.create_new_project(project)
    app.project.create_new_project(project)
    new_list_project = app.soap.get_user_projects("administrator", "root")
    assert len (old_list_project) + 1 == len (new_list_project)
    old_list_project.append(project)
    assert sorted(old_list_project, key=Project.sorted_key) == sorted(new_list_project, key=Project.sorted_key)
