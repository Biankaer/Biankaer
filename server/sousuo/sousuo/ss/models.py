from django.db import models


class Pu(models.Model):
    name = models.TextField()
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pu口袋校园'


class ahau(models.Model):
    title = models.TextField()
    url = models.TextField()
    text = models.TextField()
    ss_date = models.DateField()
    source = models.CharField(max_length=50)


class rsc(models.Model):
    title = models.TextField()
    url = models.TextField()
    text = models.TextField()
# def __str__(self):
#     return self.pu
