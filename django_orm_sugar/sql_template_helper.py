from django.apps import apps
from django.template import Context
from django.template.loader import get_template


__author__ = 'Alexey Zankevich'


class AppWrapper(object):
    def __init__(self, app_name):
        self.app_name = app_name

    def __getattr__(self, model_name):
        return ModelWrapper(apps.get_model(self.app_name, model_name))


class ModelWrapper(object):
    def __init__(self, model):
        self.model = self.model

    def __getattr__(self, field_name):
        return FieldWrapper(self.model, field_name)

    def __unicode__(self):
        return "'{}'".format(self.model._meta.name)


class FieldWrapper(object):
    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name

    def __unicode__(self):
        return "'{}'.'{}'".format(self.model._meta.name, self.field_name)


def exec_sql_template(model, template_name, params):
    """
    Exec SQL template end return RawSQLQuerySet object

    :param model: Model which should be used to map results into object
    :param template_name: SQL template name
    :param params: a dictionary, containing additional params
    :rtype: django.db.models.query.RawQuerySet
    """
    t = get_template(template_name)
    params['model'] = model
    c = Context(params)
    sql = t.render(c)
    return model.raw(sql)
