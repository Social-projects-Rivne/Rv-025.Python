from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class Role(Group):

    """Implement a fully featured Role model and handle roles data
    in DB.
    """

    class Meta:
        proxy = True
        verbose_name = _('role')
