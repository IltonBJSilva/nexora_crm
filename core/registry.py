from collections import OrderedDict

from django.forms import modelform_factory

from .forms import StyledModelForm
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


def build_form(model):
    return modelform_factory(model, form=StyledModelForm, fields="__all__")


ENTITY_REGISTRY = OrderedDict(
    {
        "disciplinas": {
            "model": Discipline,
            "form": build_form(Discipline),
            "title": "Disciplinas",
            "area": "faculdade",
            "description": "Controle de matérias, professor, notas e andamento.",
            "icon": "🎓",
            "columns": ["status", "instructor", "current_grade"],
        },
        "tarefas-academicas": {
            "model": AcademicTask,
            "form": build_form(AcademicTask),
            "title": "Tarefas Acadêmicas",
            "area": "faculdade",
            "description": "Provas, trabalhos e entregas com prazo e prioridade.",
            "icon": "📝",
            "columns": ["status", "priority", "due_date"],
        },
        "base-conhecimento": {
            "model": KnowledgeBaseEntry,
            "form": build_form(KnowledgeBaseEntry),
            "title": "Base de Conhecimento",
            "area": "faculdade",
            "description": "Conceitos, exemplos e referências de código.",
            "icon": "📚",
            "columns": ["category", "code_reference"],
        },
        "projetos-academicos": {
            "model": AcademicProject,
            "form": build_form(AcademicProject),
            "title": "Projetos Acadêmicos",
            "area": "faculdade",
            "description": "TCC, projetos em grupo e desafios práticos.",
            "icon": "📁",
            "columns": ["status", "discipline", "due_date"],
        },
        "planejamentos-semestre": {
            "model": SemesterPlan,
            "form": build_form(SemesterPlan),
            "title": "Planejamentos de Semestre",
            "area": "faculdade",
            "description": "Objetivos e foco do semestre atual.",
            "icon": "🗓️",
            "columns": ["semester", "status"],
        },
        "tarefas-trabalho": {
            "model": WorkTask,
            "form": build_form(WorkTask),
            "title": "Atividades do Trabalho",
            "area": "trabalho",
            "description": "Tasks, bugs, features e prazos.",
            "icon": "💼",
            "columns": ["task_type", "status", "priority", "due_date"],
        },
        "aprendizados-tecnicos": {
            "model": TechnicalLearning,
            "form": build_form(TechnicalLearning),
            "title": "Aprendizados Técnicos",
            "area": "trabalho",
            "description": "Stack, conceitos, exemplos e erros importantes.",
            "icon": "🧠",
            "columns": ["stack", "status"],
        },
        "erros-licoes": {
            "model": LessonLearned,
            "form": build_form(LessonLearned),
            "title": "Erros e Lições",
            "area": "trabalho",
            "description": "Problemas enfrentados, solução e aprendizado.",
            "icon": "🧩",
            "columns": ["impact"],
        },
        "metas-profissionais": {
            "model": CareerGoal,
            "form": build_form(CareerGoal),
            "title": "Metas Profissionais",
            "area": "trabalho",
            "description": "Curto, médio e longo prazo de carreira.",
            "icon": "🎯",
            "columns": ["horizon", "status", "target_date"],
        },
        "projetos-trabalho": {
            "model": WorkProject,
            "form": build_form(WorkProject),
            "title": "Projetos do Trabalho",
            "area": "trabalho",
            "description": "Impacto, papel e tecnologias usadas.",
            "icon": "🚀",
            "columns": ["role", "technologies", "status"],
        },
        "fitness": {
            "model": FitnessLog,
            "form": build_form(FitnessLog),
            "title": "Fitness",
            "area": "pessoal",
            "description": "Treinos, evolução e rotina corporal.",
            "icon": "🏋️",
            "columns": ["workout_type", "performed_at", "duration_minutes"],
        },
        "financas": {
            "model": FinanceEntry,
            "form": build_form(FinanceEntry),
            "title": "Finanças",
            "area": "pessoal",
            "description": "Salário, despesas, investimentos e metas.",
            "icon": "💰",
            "columns": ["entry_type", "category", "amount", "date"],
        },
        "leituras": {
            "model": ReadingNote,
            "form": build_form(ReadingNote),
            "title": "Leitura e Espiritualidade",
            "area": "pessoal",
            "description": "Livros, reflexões e estado mental.",
            "icon": "📖",
            "columns": ["author", "category", "status"],
        },
        "habitos": {
            "model": Habit,
            "form": build_form(Habit),
            "title": "Desenvolvimento Pessoal",
            "area": "pessoal",
            "description": "Hábitos, disciplina, vícios e progresso semanal.",
            "icon": "🌱",
            "columns": ["category", "frequency", "streak", "status"],
        },
        "relacionamentos": {
            "model": RelationshipItem,
            "form": build_form(RelationshipItem),
            "title": "Vida Social e Relacionamentos",
            "area": "pessoal",
            "description": "Contatos, networking e eventos relevantes.",
            "icon": "🤝",
            "columns": ["item_type", "reference_date", "next_action"],
        },
        "metas-vida": {
            "model": LifeGoal,
            "form": build_form(LifeGoal),
            "title": "Metas de Vida",
            "area": "pessoal",
            "description": "Objetivos de corpo, dinheiro, carreira e espiritualidade.",
            "icon": "✨",
            "columns": ["area", "status", "target_date"],
        },
        "roadmap": {
            "model": RoadmapStep,
            "form": build_form(RoadmapStep),
            "title": "Roadmap Necessário",
            "area": "roadmap",
            "description": "Sequência de cursos, projetos e materiais essenciais.",
            "icon": "🛣️",
            "columns": ["stage", "resource_type", "status", "sort_order"],
        },
    }
)

AREA_LABELS = {
    "faculdade": "Faculdade",
    "trabalho": "Trabalho",
    "pessoal": "Pessoal",
    "roadmap": "Roadmap",
}


def get_entity_config(slug):
    return ENTITY_REGISTRY.get(slug)
