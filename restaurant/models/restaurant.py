from django.db import models

class RestaurantType(models.Model):
    """This class is using for creating table with types of Restaurants.

        is_deleted check if current type is shown or not.
    """
    rest_type = models.CharField(max_length=256, blank=False)
    is_deleted = models.BooleanField(default=False)

    class Meta(object):
        verbose_name=u"Restaurant type"

    rest_type = models.CharField(max_length=256, blank=False)

    def __unicode__(self):
        return u"%s" % (self.rest_type)

class Restaurant(models.Model):

    ACTIVE = 0
    DELETED = 1
    HIDDEN = 2

    RESTAURANT_STATUSES =(
        (ACTIVE,'active'),
        (DELETED,'deleted'),
        (HIDDEN,'hidden'),
    )

    name = models.CharField(max_length=256, blank=False)
    #logo = models.ImageField(upload_to='restaurant_images/', default='restaurant-images/none/none.jpg')
    logo = models.CharField(max_length=256, default="Logo_added")
    location = models.CharField(max_length=256, blank=False)
    type_id = models.ForeignKey(RestaurantType, blank=True, null=True)
    status = models.IntegerField(choices=RESTAURANT_STATUSES, default=0)
    tables_count = models.IntegerField(null=False)
    description = models.TextField(max_length=256)
    #owner_id = model.ForeignKey(Users)

    class Meta(object):
        verbose_name=u"Restaurant"
        verbose_name_plural=u"Restaurants"

    name = models.CharField(max_length=256, blank=False)

    def __unicode__(self):
        return u"%s %s" % (self.type_id, self.name)

    def delete(self, *args, **kwargs):
        self.status = 1
        self.save()
