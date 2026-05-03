from django.contrib import admin

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
    WorkProject,
    WorkTask,
)

admin.site.site_header = "Nexora Control Center"
admin.site.site_title = "Nexora Admin"
admin.site.index_title = "Operacao interna do CRM"


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("name", "instructor", "status", "current_grade")
    search_fields = ("name", "subject", "instructor")
    list_filter = ("status",)


@admin.register(AcademicTask)
class AcademicTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "discipline", "status", "priority", "due_date")
    search_fields = ("title", "description")
    list_filter = ("status", "priority")


@admin.register(KnowledgeBaseEntry)
class KnowledgeBaseEntryAdmin(admin.ModelAdmin):
    list_display = ("topic", "category", "code_reference")
    search_fields = ("topic", "category", "concept")


@admin.register(AcademicProject)
class AcademicProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "discipline", "status", "due_date")
    search_fields = ("title", "description")
    list_filter = ("status",)


@admin.register(SemesterPlan)
class SemesterPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "semester", "status")
    search_fields = ("title", "semester", "goal")
    list_filter = ("status",)


@admin.register(WorkTask)
class WorkTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_type", "status", "priority", "due_date")
    search_fields = ("title", "task_type", "description")
    list_filter = ("status", "priority")


@admin.register(TechnicalLearning)
class TechnicalLearningAdmin(admin.ModelAdmin):
    list_display = ("title", "stack", "status")
    search_fields = ("title", "stack", "concept")
    list_filter = ("status",)


@admin.register(LessonLearned)
class LessonLearnedAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "problem", "learning")


@admin.register(CareerGoal)
class CareerGoalAdmin(admin.ModelAdmin):
    list_display = ("title", "horizon", "status", "target_date")
    search_fields = ("title", "notes")
    list_filter = ("horizon", "status")


@admin.register(WorkProject)
class WorkProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "role", "status")
    search_fields = ("title", "technologies", "impact")
    list_filter = ("status",)


@admin.register(FitnessLog)
class FitnessLogAdmin(admin.ModelAdmin):
    list_display = ("title", "workout_type", "performed_at", "duration_minutes")
    search_fields = ("title", "workout_type", "notes")


@admin.register(FinanceEntry)
class FinanceEntryAdmin(admin.ModelAdmin):
    list_display = ("description", "entry_type", "category", "amount", "date")
    search_fields = ("description", "category", "notes")
    list_filter = ("entry_type",)


@admin.register(ReadingNote)
class ReadingNoteAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status")
    search_fields = ("title", "author", "insight")
    list_filter = ("status",)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "frequency", "streak", "status")
    search_fields = ("name", "category", "notes")
    list_filter = ("frequency", "status")


@admin.register(RelationshipItem)
class RelationshipItemAdmin(admin.ModelAdmin):
    list_display = ("name", "item_type", "reference_date", "next_action")
    search_fields = ("name", "next_action", "notes")
    list_filter = ("item_type",)


@admin.register(LifeGoal)
class LifeGoalAdmin(admin.ModelAdmin):
    list_display = ("title", "area", "status", "target_date")
    search_fields = ("title", "notes")
    list_filter = ("area", "status")


@admin.register(RoadmapStep)
class RoadmapStepAdmin(admin.ModelAdmin):
    list_display = ("title", "stage", "resource_type", "status", "sort_order")
    search_fields = ("title", "resource", "notes")
    list_filter = ("stage", "resource_type", "status")
