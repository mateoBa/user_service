from app import app

from flask_mongoalchemy import MongoAlchemy

db = MongoAlchemy(app)


class Sale(db.Document):
    uuid = db.StringField()
    amount = db.FloatField()
    date = db.StringField()
    approved = db.BoolField()

    def to_dict(self):
        return dict(uuid=self.uuid, amount=self.amount, date=self.date, approved=self.approved)


def calc_sales_amount(sales):
    return sum([sale.amount for sale in sales if sale.approved])


class User(db.Document):
    name = db.StringField()
    last_name = db.StringField()
    email = db.StringField()
    address = db.StringField()
    approved = db.BoolField()
    sales = db.ListField(db.DocumentField(Sale), db_field='sales')

    def to_dict(self):
        return dict(name=self.name, last_name=self.last_name, email=self.email,
                    address=self.address, approved=self.approved, sales_total=len(self.sales),
                    operated_total_import=calc_sales_amount(self.sales))

    def get_sale(self, uuid):
        if not uuid:
            return None

        for sale in self.sales:
            if uuid == sale.uuid:
                return sale
