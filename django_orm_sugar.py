import sys
from django.db.models import Q as QNode

__author__ = 'Alexey Zankevich'


class QFactory(object):
    """
    Usage:

    >>> Q.username.get_path()
    'username'

    >>> Q.user.username.get_path()
    'user__username'

    Typical usage:
    >>> Q.user.username == 'Bender Rodriguez'
    <Q: (AND: ('user__username', 'Bender Rodriguez'))>

    The old-style usage is still available:
    >>> Q(user__username='Bender')
    <Q: (AND: ('user__username', 'Bender'))>

    Different usage cases:
    >>> Q.user.username.iexact('Bender Rodriguez')
    <Q: (AND: ('user__username__iexact', 'Bender Rodriguez'))>

    >>> Q.user.username.exact('Bender Rodriguez')
    <Q: (AND: ('user__username__exact', 'Bender Rodriguez'))>

    >>> Q.user.username.contains('Rodriguez')
    <Q: (AND: ('user__username__contains', 'Rodriguez'))>

    >>> Q.user.username.icontains('Rodriguez')
    <Q: (AND: ('user__username__icontains', 'Rodriguez'))>

    Passing items as a single list argument
    >>> Q.user.tags[0:1].overlap(['item1', 'item2'])
    <Q: (AND: ('user__tags__0_1__overlap', ['item1', 'item2']))>

    Passing items as multiple arguments
    >>> Q.user.created.range('start date', 'end date')
    <Q: (AND: ('user__created__range', ('start date', 'end date')))>

    >>> Q.data.contained_by({'breed': 'collie'})
    <Q: (AND: ('data__contained_by', {'breed': 'collie'}))>

    """

    _helpers = {}

    def __init__(self, name='', parent=None):
        self._name = name
        self._parent = parent

    def __getattr__(self, item):
        """
        :return: QFactory()
        """
        # Made module doctestable, otherwise doctest runner failed into infinite loop
        if item == '__wrapped__':
            raise AttributeError('No attribute __wrapped__')
        else:
            return QFactory(name=item, parent=self)

    def __getitem__(self, item):
        """
        >>> Q.user.tags[0].name == 'My Tag'
        <Q: (AND: ('user__tags__0__name', 'My Tag'))>

        >>> Q.user.tags[0:1].name == "My Tag"
        <Q: (AND: ('user__tags__0_1__name', 'My Tag'))>

        """
        if isinstance(item, slice):
            return QFactory('{}_{}'.format(item.start, item.stop), self)
        else:
            return QFactory(str(item), self)

    def __eq__(self, value):
        """
        >>> Q.username == 'Bender Rodriguez'
        <Q: (AND: ('username', 'Bender Rodriguez'))>

        >>> Q.user.username == 'Bender Rodriguez'
        <Q: (AND: ('user__username', 'Bender Rodriguez'))>
        """
        return QNode(**{self.get_path(): value})

    def __ne__(self, value):
        """
        >>> QFactory().user.username != 'Bender Rodriguez'
        <Q: (NOT (AND: ('user__username', 'Bender Rodriguez')))>
        """
        return ~QNode(**{self.get_path(): value})

    def __gt__(self, value):
        """
        >>> QFactory().user.age > 7
        <Q: (AND: ('user__age__gt', 7))>
        """
        return QNode(**{'{}__gt'.format(self.get_path()): value})

    def __ge__(self, value):
        """
        >>> QFactory().user.age >= 7
        <Q: (AND: ('user__age__gte', 7))>
        """
        return QNode(**{'{}__gte'.format(self.get_path()): value})

    def __lt__(self, value):
        """
        >>> QFactory().user.age < 7
        <Q: (AND: ('user__age__lt', 7))>
        """
        return QNode(**{'{}__lt'.format(self.get_path()): value})

    def __le__(self, value):
        """
        >>> QFactory().user.age <= 7
        <Q: (AND: ('user__age__lte', 7))>
        """
        return QNode(**{'{}__lte'.format(self.get_path()): value})

    def __call__(self, *args, **kwargs):
        """
        Lookup custom helpers, otherwise keep old-style Q usage

        >>> Q(user__age__lte=7)
        <Q: (AND: ('user__age__lte', 7))>

        >>> Q.article.tags.overlap('holiday', 'x-mas')
        <Q: (AND: ('article__tags__overlap', ('holiday', 'x-mas')))>

        >>> tags = Q.article.tags
        >>> tags.overlap('holiday', 'x-mas')
        <Q: (AND: ('article__tags__overlap', ('holiday', 'x-mas')))>

        """
        if self._parent:
            helper = self._helpers.get(self._name)
            if helper:
                return helper(self._parent.get_path(), *args, **kwargs)
            else:
                # create Q object based on full path
                if len(args) == 1:
                    value = args[0]
                else:
                    value = args
                return QNode(**{self.get_path(): value})
        else:
            # just create usual Q object
            return QNode(**kwargs)

    def is_null(self, value=True):
        """
        Filter by null (or not-null) fields

        >>> QFactory().user.favorite_movie.is_null()
        <Q: (AND: ('user__favorite_movie__isnull', True))>

        """
        return QNode(**{'{}__isnull'.format(self.get_path()): value})

    def is_not_null(self):
        """
        Filter by not null (or not-null) fields

        >>> QFactory().user.favorite_movie.is_not_null()
        <Q: (AND: ('user__favorite_movie__isnull', False))>
        """
        return self.is_null(False)

    def in_list(self, lst):
        """
        Filter by fields matching a given list

        >>> QFactory().user.id.in_list([1, 2, 3])
        <Q: (AND: ('user__id__in', [1, 2, 3]))>
        """
        return QNode(**{'{}__in'.format(self.get_path()): lst})

    def in_range(self, min_value, max_value):
        """
        >>> QFactory().user.id.in_range(7, 10)
        <Q: (AND: ('user__id__lte', 7), ('user__id__gte', 10))>
        """
        return (self <= min_value) & (self >= max_value)

    def get_path(self):
        """
        Get Django-compatible query path

        >>> QFactory().user.username.get_path()
        'user__username'
        
        """
        if self._parent is not None:
            parent_param = self._parent.get_path()
            if parent_param:
                return '__'.join([parent_param, self._name])
        return self._name

    @classmethod
    def register_helper(cls, name, function):
        cls._helpers[name] = function


def register_helper(helper_name):
    """
    Register a custom helper.
    Decorated function should take at least one param - queried path, which
    will be passed automatically by QFactory.

    Example:

     >>> import datetime
     >>> @register_helper('is_today')
     ... def is_today_helper(path):
     ...    return QNode(**{path: datetime.date.today()})

     >>> q = Q.user.last_login_date.is_today()
     >>> isinstance(q, QNode)
     True

    """
    def decorator(func):
        QFactory.register_helper(helper_name, func)
        return func
    return decorator


# creating shortcut
Q = QFactory()

# make old-style references for backward compatibility, will be removed in next stable release
S = Q
SugarQueryHelper = QFactory


if __name__ == "__main__":
    import doctest
    test_results = doctest.testmod()
    print(test_results)
    sys.exit(test_results[0])
