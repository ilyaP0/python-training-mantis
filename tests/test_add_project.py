import string
import random
from model.project import Project



def test_add_project(app):
     if len(app.project.get_project_list()) == 0:
         app.project.create_new_project(Project(name="NewProject6"))
     old_list_project = app.project.get_project_list()
     project = Project(name="NewProject2")
     app.project.create_new_project(project)
     new_list_project = app.project.get_project_list()
     assert len (old_list_project) + 1 == len (new_list_project)
     old_list_project.append(project)
     assert sorted(old_list_project, key=Project.sorted_key) == sorted(new_list_project, key=Project.sorted_key)