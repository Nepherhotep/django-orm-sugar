from django.db.models import Q as DjangoQ

__author__ = 'Alexey Zankevich'


class Q(object):
    """
    >>> q = Q()
    >>> q.username.get_query_param()
    'username'

    >>> Q().user.username.get_query_param()
    'user__username'

    """
    def __init__(self, name='', parent=None):
        self.__parent = parent
        self.__name = name

    def __getattr__(self, item):
        return Q(item, self)

    def __unicode__(self):
        return "Q('{}')".format(self.__name)

    def get_query_param(self):
        if self.__parent:
            parent_param = self.__parent.get_query_param()
            if parent_param:
                return '__'.join([parent_param, self.__name])
        return self.__name


if __name__ == "__main__":
    import doctest
    doctest.testmod()