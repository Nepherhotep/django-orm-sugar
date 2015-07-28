from django.db.models import Q

__author__ = 'Alexey Zankevich'


class SugarQueryHelper(object):
    """
    S - Django ORM Sugar

    >>> s = SugarQueryHelper()
    >>> s.username.get_path()
    'username'

    >>> SugarQueryHelper().user.username.get_path()
    'user__username'

    Typical usage:
    >>> SugarQueryHelper().user.username == 'Bender Rodriguez'
    <Q: (AND: ('user__username__exact', 'Bender Rodriguez'))>

    """
    def __init__(self, *args, **kwargs):
        self.__parent = kwargs.pop('__parent', None)
        self.__name = kwargs.pop('__name', '')

    def __getattr__(self, item):
        """
        :return: SugarQueryHelper()
        """
        return SugarQueryHelper(__name=item, __parent=self)

    def __eq__(self, value):
        """
        >>> SugarQueryHelper().user.username == 'Bender Rodriguez'
        <Q: (AND: ('user__username__exact', 'Bender Rodriguez'))>
        """
        return self.exact(value)

    def __ne__(self, value):
        """
        >>> SugarQueryHelper().user.username != 'Bender Rodriguez'
        <Q: (NOT (AND: ('user__username__exact', 'Bender Rodriguez')))>
        """
        return ~self.exact(value)

    def __gt__(self, value):
        """
        >>> SugarQueryHelper().user.age > 7
        <Q: (AND: ('user__age__gt', 7))>
        """
        return Q(**{'{}__gt'.format(self.get_path()): value})

    def __ge__(self, value):
        """
        >>> SugarQueryHelper().user.age >= 7
        <Q: (AND: ('user__age__gte', 7))>
        """
        return Q(**{'{}__gte'.format(self.get_path()): value})

    def __lt__(self, value):
        """
        >>> SugarQueryHelper().user.age < 7
        <Q: (AND: ('user__age__lt', 7))>
        """
        return Q(**{'{}__lt'.format(self.get_path()): value})

    def __le__(self, value):
        """
        >>> SugarQueryHelper().user.age <= 7
        <Q: (AND: ('user__age__lte', 7))>
        """
        return Q(**{'{}__lte'.format(self.get_path()): value})

    def is_null(self, value=True):
        """
        Filter by null (or not-null) fields

        >>> SugarQueryHelper().user.favorite_movie.is_null()
        <Q: (AND: ('user__favorite_movie__isnull', True))>

        """
        return Q(**{'{}__isnull'.format(self.get_path()): value})

    def is_not_null(self):
        """
        Filter by not null (or not-null) fields

        >>> SugarQueryHelper().user.favorite_movie.is_not_null()
        <Q: (AND: ('user__favorite_movie__isnull', False))>
        """
        return self.is_null(False)

    def in_list(self, lst):
        """
        Filter by fields matching a given list

        >>> SugarQueryHelper().user.id.in_list([1, 2, 3])
        <Q: (AND: ('user__id__in', [1, 2, 3]))>
        """
        return Q(**{'{}__in'.format(self.get_path()): lst})

    def in_range(self, min_value, max_value):
        """
        >>> SugarQueryHelper().user.id.in_range(7, 10)
        <Q: (AND: ('user__id__lte', 7), ('user__id__gte', 10))>
        """
        return (self <= min_value) & (self >= max_value)

    def iexact(self, value):
        """
        >>> SugarQueryHelper().user.username.iexact('Bender Rodriguez')
        <Q: (AND: ('user__username__iexact', 'Bender Rodriguez'))>
        """
        return Q(**{'{}__iexact'.format(self.get_path()): value})

    def exact(self, value):
        """
        >>> SugarQueryHelper().user.username.exact('Bender Rodriguez')
        <Q: (AND: ('user__username__exact', 'Bender Rodriguez'))>
        """
        return Q(**{'{}__exact'.format(self.get_path()): value})

    def contains(self, s):
        """
        >>> SugarQueryHelper().user.username.contains('Rodriguez')
        <Q: (AND: ('user__username__contains', 'Rodriguez'))>
        """
        return Q(**{'{}__contains'.format(self.get_path()): s})

    def icontains(self, s):
        """
        >>> SugarQueryHelper().user.username.icontains('Rodriguez')
        <Q: (AND: ('user__username__icontains', 'Rodriguez'))>
        """
        return Q(**{'{}__icontains'.format(self.get_path()): s})

    def get_path(self):
        """
        Get Django-compatible query path

        >>> SugarQueryHelper().user.username.get_path()
        'user__username'

        """
        if self.__parent:
            parent_param = self.__parent.get_path()
            if parent_param:
                return '__'.join([parent_param, self.__name])
        return self.__name


# creating shortcut
S = SugarQueryHelper()

if __name__ == "__main__":
    import doctest
    doctest.testmod()