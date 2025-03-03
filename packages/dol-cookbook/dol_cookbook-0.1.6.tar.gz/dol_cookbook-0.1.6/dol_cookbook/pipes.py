"""A bunch of useful function compositions (Pipe instances)"""

from dol import Pipe
from functools import partial
from operator import itemgetter, methodcaller

# Some times you want to get an iterator over the rows of a DataFrame,
# but you don't want the index.
# One solution is to do .itertuples(index=False), but that gets you namedtuples, not
# the Series, like iterrows does. Only thing is iterrows gets you the index as well,
# so...
get_rows_iterator = Pipe(methodcaller("iterrows"), partial(map, itemgetter(1)))
get_rows_iterator.__doc__ = "Get an iterator over the rows of a DataFrame"
