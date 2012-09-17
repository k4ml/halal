
from halal.settings import *

DATABASES['default']['USER'] = 'your db user name'
DATABASES['default']['PASSWORD'] = 'your db password'
DATABASES['default']['NAME'] = os.path.join(HERE, 'halal.db')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
