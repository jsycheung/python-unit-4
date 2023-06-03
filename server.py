from flask import Flask, render_template, redirect, url_for
from forms import TeamForm, DeleteTeamForm, ProjectForm, DeleteProjectForm, UpdateTeamForm, UpdateProjectForm
from model import db, User, Team, Project, connect_to_db

user_id = 1 #hard code user id

app = Flask(__name__)
app.secret_key = "keep this secret"

def get_team_project_list():
    team_list = User.query.get(user_id).teams
    project_list = []
    for team in team_list:
        for project in team.projects:
            project_list.append(project)
    return team_list, project_list


@app.route("/")
def home():
    team_form = TeamForm()
    delete_team_form = DeleteTeamForm()
    update_team_form = UpdateTeamForm()
    project_form = ProjectForm()
    delete_project_form = DeleteProjectForm()
    update_project_form = UpdateProjectForm()
    delete_team_form.update_delete_teams(User.query.get(user_id).teams)
    update_team_form.update_team_names(User.query.get(user_id).teams)
    project_form.update_teams(User.query.get(user_id).teams)
    _, project_list = get_team_project_list()
    delete_project_form.update_projects(project_list)
    update_project_form.update_projects(project_list)
    return render_template("home.html", team_form=team_form, delete_team_form=delete_team_form, update_team_form=update_team_form, project_form=project_form, delete_project_form=delete_project_form, update_project_form=update_project_form)

@app.route("/info")
def info():
    team_list, project_list = get_team_project_list()
    return render_template("info.html", team_list=team_list, project_list=project_list)

@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()
    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Team(team_name, user_id)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/update-team", methods=["POST"])
def update_team():
    update_team_form = UpdateTeamForm()
    update_team_form.update_team_names(User.query.get(user_id).teams)
    if update_team_form.validate_on_submit():
        new_team_name = update_team_form.new_team_name.data
        team_id = update_team_form.team_selection.data
        team_to_update = Team.query.filter_by(id=team_id).first()
        team_to_update.team_name = new_team_name
        db.session.add(team_to_update)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/delete-team", methods=["POST"])
def delete_team():
    delete_team_form = DeleteTeamForm()
    delete_team_form.update_delete_teams(User.query.get(user_id).teams)
    if delete_team_form.validate_on_submit():
        delete_team_id = delete_team_form.team_delete_selection.data
        team_to_delete = Team.query.filter_by(id=delete_team_id).first()
        db.session.delete(team_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

    

@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_selection.data

        new_project = Project(project_name, completed, team_id, description = description)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/update-project", methods=["POST"])
def update_project():
    update_project_form = UpdateProjectForm()
    _, project_list = get_team_project_list()
    update_project_form.update_projects(project_list)

    if update_project_form.validate_on_submit():
        project_id = update_project_form.project_selection.data
        project_to_update = Project.query.filter_by(id=project_id).first()
        project_to_update.completed = update_project_form.completed.data
        db.session.add(project_to_update)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/delete-project", methods=["POST"])
def delete_project():
    delete_project_form = DeleteProjectForm()
    team_list, project_list = get_team_project_list()
    delete_project_form.update_projects(project_list)

    if delete_project_form.validate_on_submit():
        project_id = delete_project_form.project_selection.data
        project_to_delete = Project.query.filter_by(id=project_id).first()
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)