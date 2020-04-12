from django.db import models


# Create your models here.
def user_directory_path(instance, file_name):
    return f'uploads/{instance.quiz.classroom.id}/{instance.quiz.id}/{file_name}'


class Classroom(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=128)
    semester = models.CharField(max_length=12)
    course_code = models.CharField(max_length=30)
    section = models.IntegerField()
    students = models.ManyToManyField('users.User', related_name='class_room')
    instructor = models.ForeignKey('users.User', related_name='classroom', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_code', 'section', 'semester'], name='unique_classroom')
        ]

    def get_string(self):
        return f'{self.course_code}.{self.section} ({self.semester}): {self.name}'

    def __str__(self):
        return f'{self.id}_{self.name}'


class Quiz(models.Model):
    title = models.CharField(max_length=128)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='quiz')
    students = models.ManyToManyField('users.User', related_name='quizzes', through='Performance')
    is_open = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    due_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['classroom', 'title'], name='unique_quiz')
        ]

    def evaluate_response(self, user, response):
        performance = self.performance_set.get(student=user)
        response = response.strip(', ')
        performance.response = response
        response = response.split(', ')
        i = 0
        for question in self.question.all():
            question.total_responses += 1
            if question.answer == response[i]:
                question.correct_responses += 1
                performance.points += question.points
                performance.correct_responses += 1
            performance.save()
            question.save()
            i += 1

    def get_string(self):
        return f'{self.classroom.get_string()}, {self.title}'

    def __str__(self):
        return f'{self.title}'


class Performance(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey('users.User', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    response = models.CharField(max_length=25, default='')
    correct_responses = models.IntegerField(default=0)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quiz.classroom}_{self.quiz}_{self.points}'


class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question')
    options = models.TextField()
    answer = models.CharField(max_length=128)
    points = models.IntegerField(default=1)
    time = models.IntegerField(default=60, help_text='Time in Seconds')
    total_responses = models.IntegerField(default=0)
    correct_responses = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['quiz', 'text'], name='unique_question')
        ]

    def __str__(self):
        return f'{self.text}'


class Resource(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='resource')
    item = models.FileField(upload_to=user_directory_path)

    def delete(self, using=None, keep_parents=False):
        self.item.storage.delete(self.item.name)
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.item.name
