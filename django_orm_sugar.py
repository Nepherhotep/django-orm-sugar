from django.db.models import Q as OldQ

__author__ = 'Alexey Zankevich'


class SugarQueryHelper(OldQ):
    """
    S - Django ORM Sugar

    >>> Q.username.get_path()
    'username'

    >>> Q.user.username.get_path()
    'user__username'

    Typical usage:
    >>> Q.user.username == 'Bender Rodriguez'
    <Q: (AND: ('user__username__exact', 'Bender Rodriguez'))>

    The old-style usage is still available:
    >>> Q(user__username='Bender')
    <Q: (AND: ('user__username', 'Bender'))>

    """
    def __init__(self, *args, **kwargs):
        self._parent = kwargs.pop('_parent', None)
        self._name = kwargs.pop('_name', '')
        super(SugarQueryHelper, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        """
        :return: SugarQueryHelper()
        """
        return SugarQueryHelper(_name=item, _parent=self)

    def __eq__(self, value):
        """
        >>> Q.user.username == 'Bender Rodriguez'
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
        return OldQ(**{'{}__gt'.format(self.get_path()): value})

    def __ge__(self, value):
        """
        >>> SugarQueryHelper().user.age >= 7
        <Q: (AND: ('user__age__gte', 7))>
        """
        return OldQ(**{'{}__gte'.format(self.get_path()): value})

    def __lt__(self, value):
        """
        >>> SugarQueryHelper().user.age < 7
        <Q: (AND: ('user__age__lt', 7))>
        """
        return OldQ(**{'{}__lt'.format(self.get_path()): value})

    def __le__(self, value):
        """
        >>> SugarQueryHelper().user.age <= 7
        <Q: (AND: ('user__age__lte', 7))>
        """
        return OldQ(**{'{}__lte'.format(self.get_path()): value})

    def __call__(self, *args, **kwargs):
        """
        Keep old-style Q usage

        >>> Q(user__age__lte=7)
        <Q: (AND: ('user__age__lte', 7))>

        """
        return OldQ(*args, **kwargs)

    def is_null(self, value=True):
        """
        Filter by null (or not-null) fields

        >>> SugarQueryHelper().user.favorite_movie.is_null()
        <Q: (AND: ('user__favorite_movie__isnull', True))>

        """
        return OldQ(**{'{}__isnull'.format(self.get_path()): value})

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
        return OldQ(**{'{}__in'.format(self.get_path()): lst})

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
        return OldQ(**{'{}__iexact'.format(self.get_path()): value})

    def exact(self, value):
        """
        >>> SugarQueryHelper().user.username.exact('Bender Rodriguez')
        <Q: (AND: ('user__username__exact', 'Bender Rodriguez'))>
        """
        return OldQ(**{'{}__exact'.format(self.get_path()): value})

    def contains(self, s):
        """
        >>> SugarQueryHelper().user.username.contains('Rodriguez')
        <Q: (AND: ('user__username__contains', 'Rodriguez'))>
        """
        return OldQ(**{'{}__contains'.format(self.get_path()): s})

    def icontains(self, s):
        """
        >>> SugarQueryHelper().user.username.icontains('Rodriguez')
        <Q: (AND: ('user__username__icontains', 'Rodriguez'))>
        """
        return OldQ(**{'{}__icontains'.format(self.get_path()): s})

    def get_path(self):
        """
        Get Django-compatible query path

        >>> SugarQueryHelper().user.username.get_path()
        'user__username'

        """
        if self._parent is not None:
            parent_param = self._parent.get_path()
            if parent_param:
                return '__'.join([parent_param, self._name])
        return self._name


# creating shortcut
Q = S = SugarQueryHelper()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
