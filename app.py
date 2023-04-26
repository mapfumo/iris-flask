from flask import Flask, render_template, request
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from decimal import Decimal
from wtforms import SubmitField, DecimalField
from wtforms.validators import InputRequired, NumberRange
import matplotlib
# matplotlib.use('agg')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ants are great'
Bootstrap(app)


@app.route('/manual')
def manual():
    return render_template('manual.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    sepal_length = None
    sepal_width = None
    petal_length = None
    petal_width = None
    flower = None
    flower_file = None
    image = plot_iris()
    form = IrisForm()
    if form.validate_on_submit():
        sepal_length = form.sepal_length.data
        sepal_width = form.sepal_width.data
        petal_length = form.petal_length.data
        petal_width = form.petal_width.data
        flowers = {"virginica": "static/virginica.jpg",
                   "setosa": "static/setosa.jpg",
                   "versicolor": "static/versicolor.jpg"}
        flower = predict(sepal_length, sepal_width, petal_length, petal_width)
        flower_file = flowers[flower]
        form.sepal_length.data = ''
        form.sepal_width.data = ''
        form.petal_length.data = ''
        form.petal_length.data = ''
        image = ''
    return render_template('index.html', form=form,
                           sepal_length=sepal_length,
                           sepal_width=sepal_width,
                           petal_length=petal_length,
                           petal_width=petal_width,
                           image=image,
                           flower=flower,
                           flower_file=flower_file)


@app.route('/plot')
def plot_iris():
    iris = sns.load_dataset("iris")
    sns.set(style="ticks", color_codes=True)
    plt.xkcd()

    figure = sns.pairplot(iris,
                          height=4,
                          x_vars=["sepal_width", "sepal_length"],
                          y_vars=["petal_width", "petal_length"],
                          hue="species")
    sio = BytesIO()
    figure.savefig(sio, format="png")
    image = base64.encodebytes(sio.getvalue()).decode()
    # image = base64.b64encode(sio.getvalue())
    plt.clf()
    return image


class IrisForm(FlaskForm):
    sepal_length = DecimalField(
        'Sepal Length', default=6.5,
        validators=[InputRequired(), NumberRange(min=Decimal('0.5'))])
    sepal_width = DecimalField(
        'Sepal Width', default=3.2,
        validators=[InputRequired(), NumberRange(min=Decimal('0.5'))])
    petal_length = DecimalField(
        'Petal Length', default=5.1,
        validators=[InputRequired(), NumberRange(min=Decimal('0.5'))])
    petal_width = DecimalField(
        'Petal Width', default=2.0,
        validators=[InputRequired(), NumberRange(min=Decimal('0.5'))])
    submit = SubmitField('Submit')


def predict(sepal_length, sepal_width, petal_length, petal_width):
    iris = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.33)
    knn = KNeighborsClassifier().fit(x_train, y_train)
    classes = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    new_sample = [[sepal_length, sepal_width, petal_length, petal_width]]
    specie = knn.predict(new_sample)
    return classes[specie[0]]


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(host='0.0.0.0')
    # app.run()
