from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
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


class Command(BaseCommand):
    help = "Popula o CRM com dados iniciais alinhados ao dashboard."

    def handle(self, *args, **options):
        today = timezone.localdate()

        backend, _ = Discipline.objects.get_or_create(
            name="Backend com Django",
            defaults={
                "subject": "Arquitetura e APIs",
                "instructor": "Autoestudo guiado",
                "status": "in_progress",
                "current_grade": Decimal("8.70"),
                "notes": "Foco em models, views, autenticação e deploy.",
            },
        )
        architecture, _ = Discipline.objects.get_or_create(
            name="System Design",
            defaults={
                "subject": "Escalabilidade",
                "instructor": "Trilha prática",
                "status": "planned",
                "current_grade": Decimal("0.00"),
                "notes": "Leitura focada em cache, filas e banco distribuído.",
            },
        )

        AcademicTask.objects.get_or_create(
            title="Modelar entidades principais do CRM",
            defaults={
                "discipline": backend,
                "status": "done",
                "priority": "critical",
                "due_date": today + timedelta(days=1),
                "description": "Disciplinas, trabalho, pessoal e roadmap.",
            },
        )
        AcademicTask.objects.get_or_create(
            title="Fechar backlog de arquitetura",
            defaults={
                "discipline": architecture,
                "status": "in_progress",
                "priority": "high",
                "due_date": today + timedelta(days=5),
                "description": "Revisar trade-offs de cache, filas e observabilidade.",
            },
        )

        KnowledgeBaseEntry.objects.get_or_create(
            topic="Views genéricas em Django",
            defaults={
                "category": "Framework",
                "concept": "Usar TemplateView, UpdateView e DeleteView para acelerar o CRUD.",
                "example": "Um módulo genérico consegue atender várias entidades.",
                "code_reference": "core/views.py",
                "notes": "Manter registry central reduz duplicação.",
            },
        )

        AcademicProject.objects.get_or_create(
            title="CRM pessoal integrado",
            defaults={
                "discipline": backend,
                "status": "in_progress",
                "due_date": today + timedelta(days=14),
                "description": "Projeto principal combinando organização acadêmica, trabalho e vida pessoal.",
            },
        )
        SemesterPlan.objects.get_or_create(
            title="Semestre de execução",
            defaults={
                "semester": "2026.1",
                "goal": "Consolidar Django, arquitetura e rotina de execução semanal.",
                "status": "in_progress",
                "notes": "Subir projeto, manter ritmo e registrar aprendizados.",
            },
        )

        WorkTask.objects.get_or_create(
            title="Refinar dashboard principal",
            defaults={
                "task_type": "Feature",
                "status": "in_progress",
                "priority": "high",
                "due_date": today + timedelta(days=2),
                "description": "Visual escuro inspirado na referência com cards operacionais.",
            },
        )
        WorkTask.objects.get_or_create(
            title="Criar seed de dados",
            defaults={
                "task_type": "Task",
                "status": "done",
                "priority": "medium",
                "due_date": today,
                "description": "Dados iniciais para validar o CRM sem cadastro manual.",
            },
        )

        TechnicalLearning.objects.get_or_create(
            title="Arquitetura de CRM em Django",
            defaults={
                "stack": "Python + Django",
                "concept": "Concentrar entidades em um app coeso com registry de módulos.",
                "example": "Cada slug aponta para model, form e apresentação.",
                "mistake": "Espalhar regras sem convenção aumenta custo de manutenção.",
                "status": "in_progress",
            },
        )
        LessonLearned.objects.get_or_create(
            title="Evitar CRUD duplicado",
            defaults={
                "problem": "Cada módulo tinha tendência a virar uma view e template próprios.",
                "solution": "Centralizar configuração em registry e reaproveitar views genéricas.",
                "learning": "Padronização acelera o projeto sem sacrificar flexibilidade.",
                "impact": "Menos código repetido e onboarding mais simples.",
            },
        )
        CareerGoal.objects.get_or_create(
            title="Fechar stack backend forte",
            defaults={
                "horizon": "medium",
                "target_date": today + timedelta(days=180),
                "status": "in_progress",
                "notes": "Django, APIs, arquitetura e performance.",
            },
        )
        WorkProject.objects.get_or_create(
            title="Nexora CRM",
            defaults={
                "technologies": "Python, Django, HTML, CSS",
                "role": "Owner / Backend",
                "impact": "Centraliza execução pessoal e profissional em um só painel.",
                "status": "in_progress",
                "description": "Produto principal da rotina.",
            },
        )

        FitnessLog.objects.get_or_create(
            title="Treino ABC - Peito e tríceps",
            defaults={
                "workout_type": "ABC",
                "performed_at": today,
                "duration_minutes": 52,
                "notes": "Manter consistência e registrar evolução.",
            },
        )
        FinanceEntry.objects.get_or_create(
            description="Salário principal",
            defaults={
                "entry_type": "income",
                "category": "Salário",
                "amount": Decimal("4500.00"),
                "date": today.replace(day=1),
                "notes": "Receita base do mês.",
            },
        )
        FinanceEntry.objects.get_or_create(
            description="Aporte carteira",
            defaults={
                "entry_type": "investment",
                "category": "Investimentos",
                "amount": Decimal("850.00"),
                "date": today,
                "notes": "Transferência para reserva e ativos.",
            },
        )
        FinanceEntry.objects.get_or_create(
            description="Infra do projeto",
            defaults={
                "entry_type": "expense",
                "category": "Ferramentas",
                "amount": Decimal("120.00"),
                "date": today,
                "notes": "Custos de domínio, hospedagem e ferramentas.",
            },
        )
        ReadingNote.objects.get_or_create(
            title="Arquitetura de Software na Prática",
            defaults={
                "author": "Trilha técnica",
                "category": "Arquitetura",
                "status": "in_progress",
                "insight": "Projetos crescem melhor quando a estrutura de decisões aparece no código.",
            },
        )
        Habit.objects.get_or_create(
            name="Estudo profundo diário",
            defaults={
                "category": "Aprendizado",
                "frequency": "daily",
                "status": "in_progress",
                "streak": 6,
                "notes": "90 minutos sem interrupção.",
            },
        )
        RelationshipItem.objects.get_or_create(
            name="Networking backend",
            defaults={
                "item_type": "networking",
                "next_action": "Publicar evolução do CRM e conversar com 2 devs",
                "reference_date": today + timedelta(days=7),
                "notes": "Manter presença e relacionamento técnico.",
            },
        )
        LifeGoal.objects.get_or_create(
            title="Organizar vida em um sistema único",
            defaults={
                "area": "career",
                "target_date": today + timedelta(days=90),
                "status": "in_progress",
                "notes": "Operar com clareza entre faculdade, trabalho e pessoal.",
            },
        )

        roadmap_steps = [
            (1, 1, "Fundamentos JavaScript", "course", "Curso JavaScript | Sintaxe básica"),
            (1, 2, "TypeScript para iniciantes", "course", "Curso de TypeScript para iniciantes"),
            (1, 3, "System Design essencial", "course", "System Design: Escalando uma Arquitetura"),
            (1, 4, "Arquitetando na prática", "video", "Arquitetando o YouTube na prática"),
            (2, 1, "Modelagem de software", "video", "Modelagem de Software é Difícil?"),
            (2, 2, "Cache e escalabilidade", "article", "CACHE-ASIDE: Performance e Arquitetura"),
        ]
        for stage, order, title, resource_type, resource in roadmap_steps:
            RoadmapStep.objects.get_or_create(
                title=title,
                defaults={
                    "stage": stage,
                    "resource_type": resource_type,
                    "resource": resource,
                    "status": "next" if stage > 1 else "in_progress",
                    "sort_order": order,
                    "notes": "Trilha extraída da referência visual do dashboard.",
                },
            )

        self.stdout.write(self.style.SUCCESS("Dados iniciais do CRM prontos."))
