from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from data_versioning.models import UserDataVersion


class DynamicDbAdmin(admin.ModelAdmin):
    """
    This admin implementation overrides all the methods where a model is modified in order to use the database
    assigned to the user that is using the admin.
    """
    def _get_db_by_user(self, user):
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

    def get_queryset(self, request):
        """
        Overrides standard queryset to use user assigned database.
        """
        db = self._get_db_by_user(request.user)
        qs = self.model._default_manager.using(db)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def save_model(self, request, obj, form, change):
        """
        Overrides standars save_model to save into the user assigned database.
        """
        db = self._get_db_by_user(request.user)
        obj.save(using=db)

    def delete_model(self, request, obj):
        """
        Overrides standard delete_model method to delete from the user assigned database.
        """
        db = self._get_db_by_user(request.user)
        obj.delete(using=db)

    def save_formset(self, request, form, formset, change):
        """
        Overrides standard method to use the user assigned database.
        """
        db = self._get_db_by_user(request.user)
        formset.save(using=db)
