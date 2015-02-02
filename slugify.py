import unicodedata
import re

# From markdown utilities, with the addition that periods are allowed
# in the header per the pandoc definition. Note that for Sublime.
# this has to be inported using:
#
# from User.slugify import slugify


def slugify(value, separator):
    """ Slugify a string, to make it URL friendly. """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub('[^\w\s.-]', '', value.decode('ascii')).strip().lower()
    return re.sub('[%s\s]+' % separator, separator, value)
