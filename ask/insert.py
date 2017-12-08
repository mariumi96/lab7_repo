from ask.connection import Connection
class Question:
    def __init__(self, title, text, snippet, rating, created_at):
        self.connection = Connection("localhost", "ask_db", "dbuser", "123", 'utf8')
        self.title = title
        self.text = text
        self.snippet = snippet
        self.rating = rating
        self.created_at = created_at

    def save(self):
        with self.connection as c:
            cursor = c.cursor()
            cursor.execute("""insert into ask_question (title, text, snippet, rating, created_at)
                                values (%s, %s, %s, %s, %s)""", (self.title,
                                                                 self.text,
                                                                 self.snippet,
                                                                 self.rating,
                                                                 self.created_at) )
            c.commit()


question = Question("Вопрос №2", "Вступление. Полный текст вопроса", "Вступление", "3", "07.12.2017")
question.save()
