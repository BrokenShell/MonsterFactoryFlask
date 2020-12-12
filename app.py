import re
from collections import deque
from flask import Flask, render_template, request
import Fortuna
import csv


app = Flask(__name__)
rand_type_id = Fortuna.truffle_shuffle(range(15))


@app.route("/")
@app.route("/index")
@app.route("/factory")
def factory():
    random_cr = Fortuna.distribution_range(Fortuna.front_linear, -3, 30)
    return render_template(
        "factory.html",
        type_id=rand_type_id(),
        rand_cr=random_cr,
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


@app.route('/summon', methods=['POST'])
def summon():
    damage_lookup = (
        (1, 2), (2, 3), (4, 5), (6, 8),
        (9, 14), (15, 20), (21, 26), (27, 32), (33, 38),
        (39, 44), (45, 50), (51, 56), (57, 62), (63, 68),
        (69, 74), (75, 80), (81, 86), (87, 92), (93, 98),
        (99, 104), (105, 110), (111, 116), (117, 122), (123, 140),
        (141, 158), (159, 176), (177, 194), (195, 212), (213, 230),
        (231, 248), (249, 266), (267, 284), (285, 302), (303, 320),
    )
    health_lookup = (
        (1, 7), (7, 36), (36, 50), (50, 71),
        (71, 86), (86, 101), (101, 116), (116, 131), (131, 146),
        (146, 161), (161, 176), (176, 191), (191, 206), (206, 221),
        (221, 236), (236, 251), (251, 266), (266, 281), (281, 296),
        (296, 311), (311, 326), (326, 341), (341, 356), (356, 401),
        (401, 446), (446, 491), (491, 536), (536, 581), (581, 626),
        (626, 671), (671, 716), (716, 761), (761, 806), (806, 851),
    )
    xp_lookup = (
        10, 25, 50, 100,
        200, 450, 700, 1100, 1800,
        2300, 2900, 3900, 5000, 5900,
        7200, 8400, 10000, 11500, 13000,
        15000, 18000, 20000, 22000, 25000,
        33000, 41000, 50000, 62000, 155000,
        155000, 155000, 155000, 155000, 155000,
        155000, 155000, 155000, 155000, 155000,
    )
    cr_lookup = (
        '0', '1/8', '1/4', '1/2',
    )
    name = re.sub(
        r'[^A-ZÀ-Ýa-zà-ý 0-9$]', '', request.form.get("monsterName")
    ).strip()
    if name.lower() == name or name.upper() == name:
        name = name.title()
    if not name:
        return monsters()
    cr_val = int(request.form.get("cr"))
    cr_key = cr_val + 3
    cr_str = cr_lookup[cr_key] if cr_key < 4 else str(cr_val)
    monster = {
        "Name": name,
        "Type": request.form.get("type"),
        "CR": cr_str,
        "Armor Class": int(request.form.get("ac")),
        "Attack Bonus": int(request.form.get("att")),
        "Save DC": int(request.form.get("dc")),
        "Health": Fortuna.distribution_range(
            Fortuna.middle_gauss, *health_lookup[cr_key])(),
        "Damage": Fortuna.distribution_range(
            Fortuna.middle_gauss, *damage_lookup[cr_key])(),
        "XP": xp_lookup[cr_key] + Fortuna.random_below(cr_key * 5),
    }
    with open("data/monsters.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow(monster.values())
    return monsters()


if __name__ == '__main__':
    app.run()
