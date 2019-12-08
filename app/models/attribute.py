from app.database.db import db

class AttributeModel(db.Model):
    __tablename__ = "attributes"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    attribute_id = db.Column(db.Integer)
    attribute_key = db.Column(db.String(50))
    attribute_value = db.Column(db.String(80))

    def __init__(self, product_id, attribute_id, attribute_key, attribute_value):
        self.product_id = product_id
        self.attribute_id = attribute_id
        self.attribute_key = attribute_key
        self.attribute_value = attribute_value

    def json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "attribute_id": self.attribute_id,
            "attribute_key": self.attribute_key,
            "attribute_value": self.attribute_value
        }, 200

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_attr_by_id(cls, attribute_id):
        return cls.query.filter_by(attribute_id=attribute_id).first().attribute_value