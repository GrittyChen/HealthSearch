from __future__ import unicode_literals

from django.db import models
import ast

# Create your models here.

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a list"
 
    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
 
    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)
 
    def get_prep_value(self, value):
        if value is None:
            return value
        return unicode(value)
 
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value) 

class QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    tags = ListField()

    def __unicode__(self):
        return self.question

class TagDict(models.Model):
    tag_ch = models.TextField()
    tag_en = models.TextField()
    tag_class = ListField()

    def __unicode__(self):
        return self.tag_en