from model.project import Project
import random

def test_delete_some_project(app):
    if len(app.project.get_project_list()) == 0:
        app.project.create_new_project(Project(name="test4"))
    old_list_project = app.project.get_project_list()
    project = random.choice(old_list_project)
    app.project.delete_project(project)
    new_list_project = app.project.get_project_list()
    assert len(old_list_project) - 1 == len(new_list_project)
    old_list_project.remove(project)
    assert sorted(old_list_project, key=Project.sorted_key) == sorted(new_list_project, key=Project.sorted_key)