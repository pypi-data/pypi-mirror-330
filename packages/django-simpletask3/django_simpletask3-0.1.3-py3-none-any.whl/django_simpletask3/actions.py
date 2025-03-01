from django.contrib import admin
from django.contrib import messages

__all__ = [
    "django_simpletask3_execute_for_selected",
    "django_simpletask3_reset_for_selected",
]


def django_simpletask3_execute_for_selected(modeladmin, request, queryset):
    selected = 0
    success = 0
    failed = 0
    for item in queryset.all():
        result = item.execute(
            modeladmin=modeladmin,
            request=request,
            queryset=queryset,
        )
        selected += 1
        if result:
            success += 1
        else:
            failed += 1
    level = messages.INFO
    if failed:
        level = messages.WARNING
    modeladmin.message_user(
        request,
        f"执行所选的 {selected}个 {modeladmin.model._meta.verbose_name} 任务，成功 {success} 个，失败 {failed} 个。",
        level=level,
    )


django_simpletask3_execute_for_selected.allowed_permissions = [
    "django_simpletask3_execute"
]
django_simpletask3_execute_for_selected.short_description = (
    "立即执行 %(verbose_name)s 任务"
)


def django_simpletask3_reset_for_selected(modeladmin, request, queryset):
    selected = 0
    for item in queryset.all():
        result = item.reset()
        selected += 1
    modeladmin.message_user(
        request,
        f"重置所选的 {selected}个 {modeladmin.model._meta.verbose_name} 任务成功。",
    )


django_simpletask3_reset_for_selected.allowed_permissions = ["django_simpletask3_reset"]
django_simpletask3_reset_for_selected.short_description = (
    "重置所选的 %(verbose_name)s 任务"
)
