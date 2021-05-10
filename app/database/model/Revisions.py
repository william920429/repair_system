import datetime
from .common import db, timeformat


class Revisions(db.Model):
    """
    After the admin views the reports, they will make a revision record.
    The table is connected to `Records`, `Users` and `Statuses`.

    id: PK.
    record_id: `id` in `Records` table.
    user_id: `id` in `Users` table.
    status_id: `id` in `Statuses` table.
    time: Revision time. The value will be automatically added.
    description: If the admins fail to find a status for the situation, the field can be used.
    """

    __tablename__ = "revisions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.ForeignKey("records.id"), nullable=False)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    status_id = db.Column(db.ForeignKey("statuses.id"), nullable=False)
    time = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), nullable=False, index=True
    )
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, record_id, user_id, status_id, description, **kwargs):
        self.record_id = record_id
        self.user_id = user_id
        self.status_id = status_id
        self.description = description
        if "id" in kwargs:
            self.id = kwargs["id"]
        if "time" in kwargs:
            self.time = datetime.datetime.strptime(kwargs["time"], timeformat)

    def __repr__(self):
        return (
            "Revisions(id={id},record_id={record_id},user_id={user_id},status_id={status_id},time='{mytime}',description='{description}')"
            .format(mytime=self.time.strftime(timeformat), **self.__dict__)
        )
