from django.db import migrations


def sync_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    User = apps.get_model("auth", "User")
    ContentType = apps.get_model("contenttypes", "ContentType")
    UserProfile = apps.get_model("core", "UserProfile")

    role_definitions = {
        "super_admin": {
            "group_name": "Nexora Super Admin",
            "core_actions": {"view", "add", "change", "delete"},
            "auth_models": {"user": {"view", "add", "change", "delete"}, "group": {"view", "add", "change", "delete"}},
        },
        "manager": {
            "group_name": "Nexora Manager",
            "core_actions": {"view", "add", "change", "delete"},
            "auth_models": {"userprofile": {"view", "change"}, "group": {"view"}},
        },
        "operator": {
            "group_name": "Nexora Operator",
            "core_actions": {"view", "add", "change"},
            "auth_models": {"userprofile": {"view"}},
        },
        "viewer": {
            "group_name": "Nexora Viewer",
            "core_actions": {"view"},
            "auth_models": {"userprofile": {"view"}},
        },
    }

    core_models = [
        "discipline",
        "academictask",
        "knowledgebaseentry",
        "academicproject",
        "semesterplan",
        "worktask",
        "technicallearning",
        "lessonlearned",
        "careergoal",
        "workproject",
        "fitnesslog",
        "financeentry",
        "readingnote",
        "habit",
        "relationshipitem",
        "lifegoal",
        "roadmapstep",
        "userprofile",
    ]

    core_content_types = ContentType.objects.filter(app_label="core", model__in=core_models)

    for role, definition in role_definitions.items():
        group, _ = Group.objects.get_or_create(name=definition["group_name"])
        permissions = []

        for content_type in core_content_types:
            codenames = [f"{action}_{content_type.model}" for action in definition["core_actions"]]
            permissions.extend(Permission.objects.filter(content_type=content_type, codename__in=codenames))

        auth_codenames = []
        for model_name, actions in definition["auth_models"].items():
            auth_codenames.extend([f"{action}_{model_name}" for action in actions])

        if auth_codenames:
            permissions.extend(Permission.objects.filter(codename__in=auth_codenames))

        group.permissions.set(permissions)

    for user in User.objects.all():
        default_role = "super_admin" if user.is_superuser else "viewer"
        profile, created = UserProfile.objects.get_or_create(user=user, defaults={"role": default_role})
        if not created and user.is_superuser and profile.role != "super_admin":
            profile.role = "super_admin"
            profile.save(update_fields=["role"])

        group_name = role_definitions[profile.role]["group_name"]
        group = Group.objects.get(name=group_name)
        user.groups.set([group])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_userprofile"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(sync_groups, migrations.RunPython.noop),
    ]
