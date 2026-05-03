from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import (
    AcademicProject,
    AcademicTask,
    CareerGoal,
    Discipline,
    FinanceEntry,
    FitnessLog,
    Habit,
    KnowledgeBaseEntry,
    LessonLearned,
    LifeGoal,
    ReadingNote,
    RelationshipItem,
    RoadmapStep,
    SemesterPlan,
    TechnicalLearning,
    UserProfile,
    WorkProject,
    WorkTask,
)


ROLE_DEFINITIONS = {
    UserProfile.RoleChoices.SUPER_ADMIN: {
        "group_name": "Nexora Super Admin",
        "description": "Controle total da plataforma, usuarios, grupos e operacao.",
        "staff": True,
        "superuser": True,
        "core_actions": {"view", "add", "change", "delete"},
        "auth_models": {"user": {"view", "add", "change", "delete"}, "group": {"view", "add", "change", "delete"}},
    },
    UserProfile.RoleChoices.MANAGER: {
        "group_name": "Nexora Manager",
        "description": "Gerencia o CRM e a operacao do time, com acesso administrativo sem superusuario.",
        "staff": True,
        "superuser": False,
        "core_actions": {"view", "add", "change", "delete"},
        "auth_models": {"userprofile": {"view", "change"}, "group": {"view"}},
    },
    UserProfile.RoleChoices.OPERATOR: {
        "group_name": "Nexora Operator",
        "description": "Opera os registros do CRM no dia a dia, sem administrar usuarios ou grupos.",
        "staff": False,
        "superuser": False,
        "core_actions": {"view", "add", "change"},
        "auth_models": {"userprofile": {"view"}},
    },
    UserProfile.RoleChoices.VIEWER: {
        "group_name": "Nexora Viewer",
        "description": "Acesso somente leitura aos modulos do CRM.",
        "staff": False,
        "superuser": False,
        "core_actions": {"view"},
        "auth_models": {"userprofile": {"view"}},
    },
}

CORE_MODELS = [
    Discipline,
    AcademicTask,
    KnowledgeBaseEntry,
    AcademicProject,
    SemesterPlan,
    WorkTask,
    TechnicalLearning,
    LessonLearned,
    CareerGoal,
    WorkProject,
    FitnessLog,
    FinanceEntry,
    ReadingNote,
    Habit,
    RelationshipItem,
    LifeGoal,
    RoadmapStep,
    UserProfile,
]


def _permission_codename(action, model):
    return f"{action}_{model._meta.model_name}"


def sync_role_groups():
    for role, definition in ROLE_DEFINITIONS.items():
        group, _ = Group.objects.get_or_create(name=definition["group_name"])
        permissions = []

        for model in CORE_MODELS:
            content_type = ContentType.objects.get_for_model(model)
            model_permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=[_permission_codename(action, model) for action in definition["core_actions"]],
            )
            permissions.extend(model_permissions)

        for model_name, actions in definition.get("auth_models", {}).items():
            codename_prefixes = [f"{action}_{model_name}" for action in actions]
            permissions.extend(Permission.objects.filter(codename__in=codename_prefixes))

        group.permissions.set(permissions)


def apply_role_to_user(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    role_definition = ROLE_DEFINITIONS.get(profile.role)
    if not role_definition:
        return

    sync_role_groups()

    group_name = role_definition["group_name"]
    user.groups.clear()
    user.groups.add(Group.objects.get(name=group_name))

    if user.is_staff != role_definition["staff"]:
        user.is_staff = role_definition["staff"]
    if user.is_superuser != role_definition["superuser"]:
        user.is_superuser = role_definition["superuser"]
    user.save(update_fields=["is_staff", "is_superuser"])
