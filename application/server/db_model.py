from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, JSON
from sqlalchemy.types import DateTime
from datetime import datetime

Base = declarative_base()


class Query:
    def __init__(
        self,
        DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/tegami",
    ) -> None:
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def add_message(self, message: dict):
        model_message = MQ(message=message)
        self.session.add(model_message)
        self.session.commit()

    def get_message(self):
        try:
            # ロックがかかってない中で、IDが最も大きいレコードを取得し、ロックをかける
            message = (
                self.session.query(MQ)
                .order_by(MQ.id.asc())
                .with_for_update(skip_locked=True)
                .limit(1)
                .one()
            )
            self.session.delete(message)
            self.session.commit()
            return message.message
        except Exception as e:
            self.session.rollback()
            return None


class MQ(Base):
    __tablename__ = "mq"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
