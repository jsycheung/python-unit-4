from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

class TeamForm(FlaskForm):
    team_name = StringField("team name", validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("submit")

class DeleteTeamForm(FlaskForm):
    team_delete_selection = SelectField("team to delete", validators=[DataRequired()])
    submit = SubmitField("delete team")
    def update_delete_teams(self, teams):
        self.team_delete_selection.choices = [(team.id, team.team_name) for team in teams]

class UpdateTeamForm(FlaskForm):
    team_selection = SelectField("team to update", validators=[DataRequired()])
    new_team_name = StringField("new team name", validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("update team")
    def update_team_names(self, teams):
        self.team_selection.choices = [(team.id, team.team_name) for team in teams]

class ProjectForm(FlaskForm):
    project_name = StringField("project name", validators=[DataRequired(), Length(min=4, max=255)])
    description = TextAreaField("description")
    completed = BooleanField("completed?")
    team_selection = SelectField("team")
    submit = SubmitField("submit")
    def update_teams(self, teams):
        self.team_selection.choices = [(team.id, team.team_name) for team in teams]

class UpdateProjectForm(FlaskForm):
    project_selection = SelectField("project name", validators=[DataRequired()])
    completed = BooleanField("completed?")
    submit = SubmitField("update project")
    def update_projects(self, projects):
        self.project_selection.choices = [(project.id, project.project_name) for project in projects]

class DeleteProjectForm(FlaskForm):
    project_selection = SelectField("project to delete", validators=[DataRequired()])
    submit = SubmitField("delete project")
    def update_projects(self, projects):
        self.project_selection.choices = [(project.id, project.project_name) for project in projects]
