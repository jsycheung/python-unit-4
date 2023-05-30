from flask import Flask, render_template, redirect, url_for
from forms import TeamForm, DeleteTeamForm, ProjectForm
from model import db, User, Team, Project, connect_to_db

user_id = 1 #hard code user id

app = Flask(__name__)
app.secret_key = "keep this secret"


@app.route("/")
def home():
    team_form = TeamForm()
    delete_team_form = DeleteTeamForm()
    project_form = ProjectForm()
    delete_team_form.update_delete_teams(User.query.get(user_id).teams)
    project_form.update_teams(User.query.get(user_id).teams)
    return render_template("home.html", team_form=team_form, delete_team_form=delete_team_form, project_form=project_form)

@app.route("/info")
def info():
    team_list = User.query.get(user_id).teams
    project_list = []
    for team in team_list:
        for project in team.projects:
            project_list.append(project)
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

@app.route("/delete-team")
def delete_team():
    delete_team_form = DeleteTeamForm()
    delete_team_form.update_delete_teams(User.query.get(user_id).teams)
    delete_team_id = delete_team_form.team_delete_selection.data
    team_to_delete = Team.query.filter_by(id=delete_team_id).first()
    db.session.delete(team_to_delete)
    db.session.commit()
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

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)