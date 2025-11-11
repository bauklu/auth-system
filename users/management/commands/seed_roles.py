"""Создаёт базовые роли и права в системе: admin и user."""

from django.core.management.base import BaseCommand
from users.models import Role, Permission, RolePermission


class Command(BaseCommand):
    help = "Seed roles and permissions"

    def handle(self, *args, **kwargs):
        roles = ["admin", "user"]
        permissions = [
            ("view_resource", "view_resource"),
            ("edit_resource", "edit_resource"),
            ("manage_roles", "manage_roles"),
        ]

        for name in roles:
            Role.objects.get_or_create(name=name)

        for name, code in permissions:
            Permission.objects.get_or_create(name=name, codename=code)

        admin_role = Role.objects.get(name="admin")
        for perm in Permission.objects.all():
            RolePermission.objects.get_or_create(
                role=admin_role,
                permission=perm
            )

        self.stdout.write(self.style.SUCCESS("Roles & permissions seeded"))
