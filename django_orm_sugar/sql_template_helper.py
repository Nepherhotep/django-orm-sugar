from django.apps import apps
from django.template import Context
from django.template.loader import get_template


__author__ = 'Alexey Zankevich'


class AppWrapper(object):
    def __init__(self, app_name):
        self._app_name = app_name

    def __getattr__(self, model_name):
        return ModelWrapper(apps.get_model(self._app_name, model_name))


class ModelWrapper(object):
    def __init__(self, model):
        self._model = model

    def __getattr__(self, field_name):
        return FieldWrapper(self._model, field_name)

    def __unicode__(self):
        return '"{}"'.format(self._model._meta.db_table)


class FieldWrapper(object):
    def __init__(self, model, field_name):
        self._model = model
        self._field_name = field_name

    def __unicode__(self):
        return '"{}"."{}"'.format(self._model._meta.db_table, self._field_name)


def exec_sql_template(model, template_name, params):
    """
    Exec SQL template end return RawSQLQuerySet object

    :param model: Model which should be used to map results into object
    :param template_name: SQL template name
    :param params: a dictionary, containing additional params
    :rtype: django.db.models.query.RawQuerySet
    """
    d = {}
    t = get_template(template_name)
    d['model'] = ModelWrapper(model)

    for key in params:
        d[key] = '%({})s'.format(key)

    c = Context(d)
    sql = t.render(c)
    return model.objects.raw(sql, params)
