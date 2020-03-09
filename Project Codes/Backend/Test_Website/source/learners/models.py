from django.db import models


# Create your models here.
class Group(models.Model):
    course_code = models.CharField(max_length=30)
    section = models.IntegerField()
    name = models.CharField(max_length=128)
    status = models.CharField(max_length=12)
    instructor = models.ForeignKey('users.User', related_name='submission_group', on_delete=models.CASCADE)
    members = models.ManyToManyField('users.User')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_code', 'section', 'name'], name='unique_group')
        ]

    def get_string(self):
        return f'Group: {self.name}, Course: {self.course_code}, Section: {self.section}'

    def __str__(self):
        return f'{self.course_code}.{self.section}_{self.name}'
