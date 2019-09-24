from mongoengine import *

class Score(EmbeddedDocument):
    score = FloatField(required = True)
    type = StringField(required = True)

class Student(Document):
    name = StringField(required = True)
    age = IntField(required = True)
    nationality = StringField(required = True)
    scores = ListField(EmbeddedDocumentField(Score))
    meta = { "collection": "students"}

    def print_info(self):
        print("Name: " + self.name)
        print("Age: " + str(self.age))
        print("Nationality: " + self.nationality)
        print("Scores: ")
        for elem in self.scores:
            print(" " * 4 + elem.type + " " + str(elem.score))


if __name__ == "__main__":

    MONGO_STUDENTS_DB_URI="mongodb://localhost/students"

    connect(host=MONGO_STUDENTS_DB_URI)

    pierre_score_exam = Score(type = "exam", score = 7.35)
    pierre_score_homework = Score(type = "homework", score = 40.81)
    pierre = Student(name = "Pierre",
        age = 32,
        nationality = "french",
        scores = [ pierre_score_exam,pierre_score_homework ] )
    pierre.print_info()

    # Guardo el objeto en la Mongo
    pierre.save()

    # Consulto el primer resultado filtrando por nombre.
    # El resultado ya es una instancia de la clase Student (un objeto)
    pierre_from_database = Student.objects(name = "Pierre")[0]
    print("Informacion recuperada de la base de datos: ")
    pierre_from_database.print_info()
