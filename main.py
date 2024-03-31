from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from forms import CreateCafeForm
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap4

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
ckeditor = CKEditor(app)
bootstrap = Bootstrap4(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self,column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    return render_template("index.html", cafes=all_cafes)

# @app.route('/all')
# def get_all_cafes():
#     result = db.session.execute(db.select(Cafe))
#     all_cafes = result.scalars().all()
#     return render_template("cafes.html", cafes=all_cafes)

@app.route('/<int:cafe_id>',  methods=['GET'])
def cafe(cafe_id):
    cafe =db.session.get(Cafe,cafe_id)
    return render_template('cafe.html', cafe=cafe)

# @app.route('/search')
# def search_cafe():
#     query_location = request.args.get('loc')
#     result = db.session.execute(db.select(Cafe).where( Cafe.location== query_location))
#     #All cafes at that location
#     all_cafes = result.scalars().all()

#     if all_cafes:
#         return jsonify(cafes= [cafe.to_dict() for cafe in all_cafes])
#     else:
#         return jsonify(error = {"NOT FOUND":"sorry there is no cafe for this location in our database"}), 404
    
@app.route("/add", methods=["GET", "POST"])
def post_new_cafe():
    form = CreateCafeForm()
    print(form.validate_on_submit())
    print(form.name.data)
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        # Redirect to the 'all' route after successfully adding a new cafe
        return redirect(url_for('get_all_cafes'))

    return render_template("add.html", form=form)

@app.route('/update-form/<int:cafe_id>', methods=['GET'])
def update_cafe_form(cafe_id):
    cafe =db.session.get(Cafe,cafe_id)
    return render_template('update.html', cafe=cafe)

# Update the route to handle both POST and PATCH
@app.route('/update-price/<int:cafe_id>', methods=['POST', 'PATCH'])
def path_new_price(cafe_id):
    if request.method == 'PATCH' or (request.method == 'POST' and request.form.get('_method') == 'PATCH'):
        new_price = request.args.get('new_price') or request.form.get('new_price')
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            cafe.coffee_price = new_price
            db.session.commit()
            return redirect(url_for('get_all_cafes'))
        else:
            abort(404, description='Cafe not found.')
    else:
        abort(405)  # Method Not Allowed

    
@app.route('/delete-cafe/<int:cafe_id>', methods=['GET'])
def delete_cafe_form(cafe_id):
    cafe = db.session.get(Cafe,cafe_id)
    return render_template('delete.html', cafe=cafe)

    
@app.route('/report-closed/<int:cafe_id>', methods=['POST', 'DELETE'])
def delete_cafe(cafe_id):
    if request.method == 'POST' or request.method == 'DELETE':
        api_key = request.form.get("api-key")
        if api_key == 'TopSecretAPIKey':
            cafe = db.session.get(Cafe, cafe_id)
            if cafe:
                db.session.delete(cafe)
                db.session.commit()
                return redirect(url_for('get_all_cafes'))
            else:
                abort(404, description='Cafe not found.')
        else:
            abort(403, description='Access denied.')
    else:
        abort(405, description='Method not allowed.')
    
# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
