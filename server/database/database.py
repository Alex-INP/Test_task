from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class DatabaseOperator:
	settings = {
		"drivername": "postgresql+psycopg2",
		"host": "postgres_database",
		"port": "5432",
		"username": "postgres",
		"password": "admin",
		"database": "questions_db"
	}
	declarative_db = declarative_base()
	db_engine = create_engine(
		f"{settings['drivername']}://{settings['username']}:{settings['password']}@{settings['host']}:{settings['port']}/{settings['database']}",
		pool_recycle=7200
	)

	class Questions(declarative_db):
		__tablename__ = "questions"
		id = Column(Integer, primary_key=True)
		question_id = Column(Integer, unique=True)
		text = Column(Text)
		answer = Column(String)
		creation_date = Column(DateTime)

		def __init__(self, question_id: int, text: str, answer: str, creation_date: str):
			self.question_id, self.text, self.answer, self.creation_date = question_id, text, answer, creation_date

	def __init__(self):
		if not database_exists(self.db_engine.url):
			create_database(self.db_engine.url)
		self.session = sessionmaker(bind=self.db_engine)()
		self.declarative_db.metadata.create_all(self.db_engine)

	def get_all_questions(self) -> list:
		return self.session.query(self.Questions).all()

	def add_question(self, data: dict):
		new_question = self.Questions(**data)
		self.session.add(new_question)
		self.session.commit()

	def get_last_record(self):
		return self.session.query(self.Questions).order_by(self.Questions.id.desc()).first()
