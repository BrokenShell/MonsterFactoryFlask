import csv
import re
from collections import deque

from Fortuna import distribution_range, random_below, middle_gauss, \
    truffle_shuffle, front_poisson
from flask import Flask, render_template, request

from monster_data import damage_lookup, health_lookup, xp_lookup

app = Flask(__name__)
rand_type_id = truffle_shuffle(range(15))


@app.route("/")
@app.route("/index")
@app.route("/factory")
def factory():
    return render_template(
        "factory.html",
        type_id=rand_type_id(),
        rand_cr=distribution_range(front_poisson, -3, 24)(),
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/monsters")
def monsters():
    monster_data = deque(maxlen=20)
    with open("data/monsters.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            monster_data.append(row)
    return render_template(
        "monsters.html",
        monster_data=reversed(monster_data),
        toggle_more=True
    )


@app.route("/archive")
def archive():
    monster_data = deque()
    with open("data/monsters.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            monster_data.append(row)
    return render_template(
        "monsters.html",
        monster_data=reversed(monster_data),
        toggle_more=False
    )


def get_cr_str(cr: int) -> str:
    cr_lookup = ('1/16', '1/8', '1/4', '1/2')
    return str(cr) if cr > 0 else cr_lookup[cr + 3]


def create_monster(cr: int) -> tuple:
    cr_key = cr + 3
    name = re.sub(
        r'[^A-ZÀ-Ýa-zà-ý 0-9$]', '', request.form.get("monsterName")
    ).strip()
    if name.lower() == name or name.upper() == name:
        name = name.title()
    if not name:
        return monsters()
    return (
        name,
        request.form.get("type"),
        get_cr_str(cr),
        int(request.form.get("ac")),
        int(request.form.get("att")),
        int(request.form.get("dc")),
        distribution_range(
            middle_gauss, *health_lookup[cr_key])(),
        distribution_range(
            middle_gauss, *damage_lookup[cr_key])(),
        xp_lookup[cr_key] + random_below(cr_key * 5),
    )


@app.route('/summon', methods=['POST'])
def summon():
    cr = int(request.form.get("cr"))
    with open("data/monsters.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow(create_monster(cr))
    return monsters()


if __name__ == '__main__':
    app.run()
