from django.core.exceptions import ObjectDoesNotExist

from django.contrib.admin import ModelAdmin, StackedInline

from data_versioning.models import UserDataVersion


def _get_db_by_user(user):
    """
    Args:
        user (auth.User): Instance of Django user.

    Returns:
        (str) database name.
    """
    try:
        data = UserDataVersion.objects.get(user=user)
    except ObjectDoesNotExist:
        return "default"
    return data.current_version.name


class DynamicDbAdmin(ModelAdmin):
    """
    This admin implementation overrides all the methods where a model is modified in order to use the database
    assigned to the user that is using the admin.
    """
    using = 'other'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=_get_db_by_user(request.user))

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=_get_db_by_user(request.user))

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(DynamicDbAdmin, self).get_queryset(request).using(_get_db_by_user(request.user))

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(DynamicDbAdmin, self).formfield_for_foreignkey(db_field, request=request,
                                                                    using=_get_db_by_user(request.user), **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(DynamicDbAdmin, self).formfield_for_manytomany(db_field, request=request,
                                                                    using=_get_db_by_user(request.user), **kwargs)


class DynamicDbStackedInline(StackedInline):
    using = 'other'

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super(DynamicDbStackedInline, self).get_queryset(request).using(_get_db_by_user(request.user))

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(DynamicDbStackedInline, self).formfield_for_foreignkey(db_field, request=request,
                                                                            using=_get_db_by_user(request.user),
                                                                            **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(DynamicDbStackedInline, self).formfield_for_manytomany(db_field, request=request,
                                                                            using=_get_db_by_user(request.user),
                                                                            **kwargs)
