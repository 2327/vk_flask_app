from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True)
    type = db.Column(db.String(64),
                      index=False,
                      unique=False,
                      nullable=False)
    user_id = db.Column(db.String(64),
                      index=True,
                      unique=True,
                      nullable=False)
    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False)
    first_name = db.Column(db.String(64),
                      index=True,
                      unique=False,
                      nullable=False)
    last_name = db.Column(db.String(64),
                      index=True,
                      unique=False,
                      nullable=False)

    __table_args__ = (
        db.UniqueConstraint("type", "user_id", name="user_id"),
    )
'''
    def __repr__(self):
        return '<User666 {}>'.format(self.username)
'''
