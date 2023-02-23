from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FileField, IntegerField, HiddenField, SelectMultipleField, DateField, DecimalField, BooleanField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, URL
from wtforms.widgets import ListWidget, CheckboxInput
import pycountry

class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(c.alpha_2, c.name) for c in pycountry.countries]

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class StoreInfoForm(FlaskForm):
    storename = StringField('Store Name', validators=[DataRequired()])
    url = StringField('Store URL', validators=[URL()])
    currency = SelectField('Currency')
    address1 = StringField('Address 1', validators=[DataRequired()])
    address2 = StringField('Address 2')
    city = StringField('City', validators=[DataRequired()])
    stateprovince = StringField('State/Province')
    postalcode = StringField('Postal Code')
    country = CountrySelectField('Country')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    description = TextAreaField('Description', render_kw={"rows": 5, "cols": 11})
    image = FileField('Category Image', validators=[FileAllowed(['jpg', 'png'])])

class ProductForm(FlaskForm):
    sku = StringField('SKU', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    longdescription = TextAreaField('Long Description')
    shortdescription = TextAreaField('Short Description')
    price = DecimalField('Sell Price', render_kw={"step": ".01"})
    retail = DecimalField('Retail Price', render_kw={"step": ".01"})
    weight = DecimalField('Item Weight', render_kw={"step": ".01"})
    thumb = FileField('Thumbnail Image', validators=[FileAllowed(['jpg', 'png'])])
    image = FileField('Full Image', validators=[FileAllowed(['jpg', 'png'])])
    categories = MultiCheckboxField('Categories', coerce=int)
    livedate = DateField('Live Date')
    stock = IntegerField('Stock Quantity')
    isfeatured = BooleanField('Featured?')

class DeleteConfirm(FlaskForm):
    deleteid = HiddenField('Delete ID')
    deletename = HiddenField('Delete Name')