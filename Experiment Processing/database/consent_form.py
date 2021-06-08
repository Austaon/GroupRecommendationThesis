from mongoengine import Document, ObjectIdField, StringField, DictField, DateTimeField


class ConsentForm(Document):
    """
    Model class for the consent forms in the database.
    """

    meta = {"collection": "consent_forms"}

    _id = ObjectIdField(required=True)

    email_address = StringField(required=True)
    session_id = StringField()

    consent_form = DictField(required=True)

    updated_at = DateTimeField()
    created_at = DateTimeField()
