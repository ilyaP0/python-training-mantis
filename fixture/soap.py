from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper:

    def __init__(self, app):
        self.app = app


    def can_login(self, username, password):
        client = Client("http://localhost:8080/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False


    def get_user_projects(self, username, password):
        client = Client("http://localhost:8080/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            return [Project(project.name, project.description)
                    for project in client.service.mc_projects_get_user_accessible(username, password)]
        except WebFault:
            return []