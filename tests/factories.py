from courses.models import Course, Lesson
from quizzes.models import Question, Quiz


def make_course(code="CS101", credits=3, lessons=((1, "Intro", 20), (2, "Loops", 35), (3, "Functions", 45))):
    course = Course.objects.create(code=code, title=f"Course {code}", credits=credits)
    for order, title, minutes in lessons:
        Lesson.objects.create(course=course, order=order, title=title, minutes=minutes)
    return course


def make_quiz(course, due_hour=100, answers=("a", "b", "c", "d")):
    quiz = Quiz.objects.create(course=course, title=f"{course.code} quiz", due_hour=due_hour)
    questions = [Question.objects.create(quiz=quiz, prompt=f"Q{i}", answer_key=a, points=1) for i, a in enumerate(answers, 1)]
    return quiz, questions
