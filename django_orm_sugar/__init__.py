__author__ = 'Alexey Zankevich'

from .q_factory import Q, QFactory, register_helper

# make old-style references for backward compatibility, will be removed in next stable release
S = Q
SugarQueryHelper = QFactory
