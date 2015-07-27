# Django ORM Sugar
Sugar library to simplify Django querying

S - Django ORM Sugar

This library tries to replace calls like:
    
    >>> SomeModel.objects.filter(user__profile__common_bucket__seq_count__gte=7)
    
With more pythonic syntax

    >>> SomeModel.objects.filter(S.user.profile.common_bucket.seq_count >= 7)
    
Not much shorter, but much more readable.


## Queries

    >>> S.user.username == 'Bender Rodriguez'
    Q(user__username='Bender Rodriguez')
    
    >>> S.user.age > 7
    Q(user__age__gt=7)
    
    >>> S.user.age >= 7
    Q(user__age__gte=7)
    
    >>> S.user.age < 7
    Q(user__age__lt=7)
    
    >>> S.user.age <= 7
    Q(user__age__lte=7)

Filter by null (or not-null) fields

    >>> S.user.favorite_movie.isnull(True)
    Q(user__favorite_movie__isnull=True)

Filter by fields matching a given list

    >>> S.user.id.in_list([1, 2, 3])
    Q(user__id__in=[1, 2, 3])
    
Filter by fields in range
    
    >>> S.user.id.in_range(7, 10)
    Q(user__id__lte=7) | Q(user__id__gte=10)
    
Common Django filter shortcuts
    
    >>> S.user.username.iexact('Bender Rodriguez')
    Q(user__username__iexact='Bender Rodriguez')
    
    >>> S.user.username.exact('Bender Rodriguez')
    Q(user__username__exact='Bender Rodriguez')
    
    >>> S.user.username.contains('Rodriguez')
    Q(user__username__contains='Rodriguez')
    
    >>> S.user.username.icontains('Rodriguez')
    Q(user__username__icontains='Rodriguez')
