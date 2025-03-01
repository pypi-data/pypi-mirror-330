from django.contrib import admin
from django.contrib.auth import get_permission_codename
from .actions import django_simpletask3_execute_for_selected
from .actions import django_simpletask3_reset_for_selected


class SimpleTaskAdmin(admin.ModelAdmin):

    def has_django_simpletask3_execute_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("django_simpletask3_execute", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def has_django_simpletask3_reset_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("django_simpletask3_reset", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def get_actions(self, reqeust):
        actions = super().get_actions(reqeust)
        actions.update(
            {
                "django_simpletask3_execute_for_selected": self.get_action(
                    django_simpletask3_execute_for_selected
                ),
                "django_simpletask3_reset_for_selected": self.get_action(
                    django_simpletask3_reset_for_selected
                ),
            }
        )
        return actions
