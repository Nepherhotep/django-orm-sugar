# django_orm_sugar
Sugar library to simplify Django querying

S - Django ORM Sugar

>>> from django_orm_sugar import S
>>> S.username.get_query_param()
'username'

>>> S.user.username.get_query_param()
'user__username'

Typical usage:
>>> S.user.username == 'Bender Rodriguez'
<Q: (AND: ('user__username__exact', 'Bender Rodriguez'))>

>>> S.user.username == 'Bender Rodriguez'
<Q: (AND: ('user__username__exact', 'Bender Rodriguez'))>

>>> S.user.age > 7
<Q: (AND: ('user__age__gt', 7))>

>>> S.user.age >= 7
<Q: (AND: ('user__age__gte', 7))>


>>> S.user.age < 7
<Q: (AND: ('user__age__lt', 7))>

>>> S.user.age <= 7
<Q: (AND: ('user__age__lte', 7))>

Filter by null (or not-null) fields

>>> S.user.favorite_movie.isnull(True)
<Q: (AND: ('user__favorite_movie__isnull', True))>

Filter by fields matching a given list

>>> S.user.id.in_list([1, 2, 3])
<Q: (AND: ('user__id__in', [1, 2, 3]))>

>>> S.user.id.in_range(7, 10)
<Q: (AND: ('user__id__lt', 7), ('user__id__gt', 10))>

>>> S.user.username.iexact('Bender Rodriguez')
<Q: (AND: ('user__username__iexact', 'Bender Rodriguez'))>

>>> S.user.username.exact('Bender Rodriguez')
<Q: (AND: ('user__username__exact', 'Bender Rodriguez'))>

>>> S.user.username.contains('Rodriguez')
<Q: (AND: ('user__username__contains', 'Rodriguez'))>

>>> S.user.username.icontains('Rodriguez')
<Q: (AND: ('user__username__icontains', 'Rodriguez'))>
