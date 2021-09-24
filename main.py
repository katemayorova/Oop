from functools import total_ordering


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def grade_lectures(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and \
                (course in self.courses_in_progress or course in self.finished_courses) and \
                course in lecturer.courses_attached and \
                1 <= grade <= 10:
            lecturer.lecture_grades[course].append(grade)
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\n" \
               f"Фамилия: {self.surname}\n" \
               f"Средняя оценка за домашние задания: {self.average_hw_grade()}\n" \
               f"Курсы в процессе изучения: {self.list_courses(self.courses_in_progress)}\n" \
               f"Завершеные курсы: {self.list_courses(self.finished_courses)}"

    def average_hw_grade(self):
        grade_sum = 0
        for grade in self.grades.values():
            grade_sum += grade
        if len(self.grades) == 0:
            return "n/a"
        return grade_sum / len(self.grades)

    @staticmethod
    def list_courses(courses):
        if len(courses) == 0:
            return "n/a"
        return ', '.join(courses)

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.average_hw_grade() == other.average_hw_grade()

    def __ne__(self, other):
        if not isinstance(other, Student):
            return True
        return self.average_hw_grade() != other.average_hw_grade()

    def __le__(self, other):
        if not isinstance(other, Student):
            return False
        return self.average_hw_grade() <= other.average_hw_grade()


class Mentor:
    def __init__(self, name, surname, courses_attached):
        self.name = name
        self.surname = surname
        self.courses_attached = courses_attached

    def __str__(self):
        return f"Имя: {self.name}\n" \
               f"Фамилия: {self.surname}"


@total_ordering
class Lecturer (Mentor):
    def __init__(self, name, surname, courses_attached):
        super().__init__(name, surname, courses_attached)
        self.lecture_grades = {}
        for course in self.courses_attached:
            self.lecture_grades[course] = []

    def __str__(self):
        return f"{super().__str__()}\n" \
               f"Средняя оценка за лекции: {self.average_lecture_grade()}"

    def average_lecture_grade(self):
        grade_sum = 0
        grade_count = 0
        for course_grades in self.lecture_grades.values():
            for grade in course_grades:
                grade_sum += grade
            grade_count += len(course_grades)
        if grade_count == 0:
            return "n/a"
        return grade_sum / grade_count

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return False
        return self.average_lecture_grade() == other.average_lecture_grade()

    def __ne__(self, other):
        if not isinstance(other, Lecturer):
            return True
        return self.average_lecture_grade() != other.average_lecture_grade()

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return False
        return self.average_lecture_grade() <= other.average_lecture_grade()


class Reviewer (Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            student.grades[course] = grade
        else:
            return 'Ошибка'


def average_course_hw_grade(students, course):
    grade_sum = 0
    grade_count = 0
    for student in students:
        if course in student.grades:
            grade_count += 1
            grade_sum += student.grades[course]
    if grade_count == 0:
        return "n/a"
    return grade_sum / grade_count


def average_lecture_grade(lecturers, course):
    grade_sum = 0
    grade_count = 0
    for lecturer in lecturers:
        if course in lecturer.lecture_grades:
            for grade in lecturer.lecture_grades[course]:
                grade_count += 1
                grade_sum += grade
    if grade_count == 0:
        return "n/a"
    return grade_sum / grade_count


# best_student = Student('Ruoy', 'Eman', 'your_gender')
# best_student.courses_in_progress += ['Python']
#
# cool_mentor = Mentor('Some', 'Buddy')
# cool_mentor.courses_attached += ['Python']
#
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
#
# print(best_student.grades)

lecturer1 = Lecturer("Ivan", "Ivanov", ["Python", "Git"])
lecturer2 = Lecturer("Egor", "Smirnov", ["Git", "Java"])

student1 = Student("Gleb", "Glebov", "M")
student2 = Student("Elena", "Petrova", "F")
student1.finished_courses.append("Java")
student1.courses_in_progress.append("Python")
student1.courses_in_progress.append("Git")
student2.finished_courses.append("Python")
student2.courses_in_progress.append("Java")
student2.finished_courses.append("Git")

reviewer1 = Reviewer("Petr", "Morozov", ["Python", "Git"])
reviewer2 = Reviewer("Makar", "Makarov", ["Java", "Git"])

student1.grade_lectures(lecturer1, "Python", 4)
student2.grade_lectures(lecturer2, "Git", 5)

reviewer1.rate_hw(student1, "Python", 3)
reviewer2.rate_hw(student2, "Java", 4)

print(reviewer1)
print(reviewer2)
print(lecturer1)
print(lecturer2)
print(student1)
print(student2)
print(f"Средняя оценка студентов за курс \"Python\": {average_course_hw_grade([student1, student2], 'Python')}")
print(f"Средняя оценка лекторов за курс \"Git\": {average_lecture_grade([lecturer1, lecturer2], 'Git')}")

if lecturer1 > lecturer2:
    print("Лектор1 ведет лекции лучше, чем лектор2")
else:
    print("Лектор2 ведет лекции лучше или также, как лектор1")

if student1 > student2:
    print("Студент1 учиться лучше, чем студент2")
else:
    print("Студент2 учиться лучше или также, как студент1")

