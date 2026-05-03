from decimal import Decimal

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusChoices(models.TextChoices):
    BACKLOG = "backlog", "Backlog"
    NEXT = "next", "Próximo"
    IN_PROGRESS = "in_progress", "Em andamento"
    WAITING = "waiting", "Aguardando"
    DONE = "done", "Concluído"


class PriorityChoices(models.TextChoices):
    LOW = "low", "Baixa"
    MEDIUM = "medium", "Média"
    HIGH = "high", "Alta"
    CRITICAL = "critical", "Crítica"


class AcademicStatusChoices(models.TextChoices):
    PLANNED = "planned", "Planejada"
    IN_PROGRESS = "in_progress", "Cursando"
    DONE = "done", "Concluída"


class HorizonChoices(models.TextChoices):
    SHORT = "short", "Curto prazo"
    MEDIUM = "medium", "Médio prazo"
    LONG = "long", "Longo prazo"


class Discipline(TimeStampedModel):
    name = models.CharField("nome", max_length=140)
    subject = models.CharField("matéria", max_length=140, blank=True)
    instructor = models.CharField("professor", max_length=140, blank=True)
    status = models.CharField(
        "status", max_length=20, choices=AcademicStatusChoices.choices, default=AcademicStatusChoices.PLANNED
    )
    current_grade = models.DecimalField("nota atual", max_digits=5, decimal_places=2, default=Decimal("0.00"))
    notes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self) -> str:
        return self.name


class AcademicTask(TimeStampedModel):
    title = models.CharField("título", max_length=160)
    discipline = models.ForeignKey(
        Discipline, verbose_name="disciplina", related_name="tasks", on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.BACKLOG)
    priority = models.CharField(
        "prioridade", max_length=20, choices=PriorityChoices.choices, default=PriorityChoices.MEDIUM
    )
    due_date = models.DateField("prazo", null=True, blank=True)
    description = models.TextField("descrição", blank=True)

    class Meta:
        ordering = ["due_date", "-created_at"]
        verbose_name = "Tarefa acadêmica"
        verbose_name_plural = "Tarefas acadêmicas"

    def __str__(self) -> str:
        return self.title


class KnowledgeBaseEntry(TimeStampedModel):
    topic = models.CharField("tema", max_length=160)
    category = models.CharField("categoria", max_length=120)
    concept = models.TextField("conceito")
    example = models.TextField("exemplo", blank=True)
    code_reference = models.CharField("referência de código", max_length=255, blank=True)
    notes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["category", "topic"]
        verbose_name = "Base de conhecimento"
        verbose_name_plural = "Base de conhecimento"

    def __str__(self) -> str:
        return self.topic


class AcademicProject(TimeStampedModel):
    title = models.CharField("título", max_length=160)
    discipline = models.ForeignKey(
        Discipline,
        verbose_name="disciplina",
        related_name="projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEXT)
    due_date = models.DateField("prazo", null=True, blank=True)
    description = models.TextField("descrição", blank=True)

    class Meta:
        ordering = ["due_date", "title"]
        verbose_name = "Projeto acadêmico"
        verbose_name_plural = "Projetos acadêmicos"

    def __str__(self) -> str:
        return self.title


class SemesterPlan(TimeStampedModel):
    title = models.CharField("título", max_length=160)
    semester = models.CharField("semestre", max_length=60)
    goal = models.TextField("objetivo")
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEXT)
    notes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["semester", "title"]
        verbose_name = "Planejamento de semestre"
        verbose_name_plural = "Planejamentos de semestre"

    def __str__(self) -> str:
        return f"{self.semester} - {self.title}"


class WorkTask(TimeStampedModel):
    title = models.CharField("título", max_length=160)
    task_type = models.CharField("tipo", max_length=80, blank=True)
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.BACKLOG)
    priority = models.CharField(
        "prioridade", max_length=20, choices=PriorityChoices.choices, default=PriorityChoices.MEDIUM
    )
    due_date = models.DateField("prazo", null=True, blank=True)
    description = models.TextField("descrição", blank=True)

    class Meta:
        ordering = ["due_date", "-created_at"]
        verbose_name = "Atividade de trabalho"
        verbose_name_plural = "Atividades de trabalho"

    def __str__(self) -> str:
        return self.title


class TechnicalLearning(TimeStampedModel):
    title = models.CharField("tema", max_length=160)
    stack = models.CharField("stack", max_length=120, blank=True)
    concept = models.TextField("conceito")
    example = models.TextField("exemplo", blank=True)
    mistake = models.TextField("erro importante", blank=True)
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEXT)

    class Meta:
        ordering = ["title"]
        verbose_name = "Aprendizado técnico"
        verbose_name_plural = "Aprendizados técnicos"

    def __str__(self) -> str:
        return self.title


class LessonLearned(TimeStampedModel):
    title = models.CharField("título", max_length=160)
    problem = models.TextField("problema")
    solution = models.TextField("como resolveu")
    learning = models.TextField("o que aprendeu")
    impact = models.TextField("impacto", blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Erro e lição"
        verbose_name_plural = "Erros e lições"

    def __str__(self) -> str:
        return self.title


class CareerGoal(TimeStampedModel):
    title = models.CharField("título", max_length=160)
    horizon = models.CharField("horizonte", max_length=20, choices=HorizonChoices.choices)
    target_date = models.DateField("data alvo", null=True, blank=True)
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEXT)
    notes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["target_date", "title"]
        verbose_name = "Meta profissional"
        verbose_name_plural = "Metas profissionais"

    def __str__(self) -> str:
        return self.title


class WorkProject(TimeStampedModel):
    title = models.CharField("título", max_length=160)
    technologies = models.CharField("tecnologias", max_length=255, blank=True)
    role = models.CharField("papel", max_length=120, blank=True)
    impact = models.TextField("impacto", blank=True)
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_PROGRESS)
    description = models.TextField("descrição", blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Projeto de trabalho"
        verbose_name_plural = "Projetos de trabalho"

    def __str__(self) -> str:
        return self.title


class FitnessLog(TimeStampedModel):
    title = models.CharField("atividade", max_length=160)
    workout_type = models.CharField("tipo de treino", max_length=120)
    performed_at = models.DateField("data", default=timezone.localdate)
    duration_minutes = models.PositiveIntegerField("duração (min)", default=0)
    notes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["-performed_at", "-created_at"]
        verbose_name = "Registro fitness"
        verbose_name_plural = "Registros fitness"

    def __str__(self) -> str:
        return f"{self.title} ({self.performed_at:%d/%m/%Y})"


class FinanceEntry(TimeStampedModel):
    class EntryType(models.TextChoices):
        INCOME = "income", "Receita"
        EXPENSE = "expense", "Despesa"
        INVESTMENT = "investment", "Investimento"

    description = models.CharField("descrição", max_length=160)
    entry_type = models.CharField("tipo", max_length=20, choices=EntryType.choices)
    category = models.CharField("categoria", max_length=120)
    amount = models.DecimalField("valor", max_digits=12, decimal_places=2)
    date = models.DateField("data", default=timezone.localdate)
    notes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Movimento financeiro"
        verbose_name_plural = "Movimentos financeiros"

    def __str__(self) -> str:
        return self.description


class ReadingNote(TimeStampedModel):
    title = models.CharField("título", max_length=160)
    author = models.CharField("autor", max_length=140, blank=True)
    category = models.CharField("categoria", max_length=120, blank=True)
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEXT)
    insight = models.TextField("insight principal", blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Leitura e reflexão"
        verbose_name_plural = "Leituras e reflexões"

    def __str__(self) -> str:
        return self.title


class Habit(TimeStampedModel):
    class FrequencyChoices(models.TextChoices):
        DAILY = "daily", "Diário"
        WEEKLY = "weekly", "Semanal"
        MONTHLY = "monthly", "Mensal"

    name = models.CharField("hábito", max_length=140)
    category = models.CharField("categoria", max_length=120)
    frequency = models.CharField("frequência", max_length=20, choices=FrequencyChoices.choices)
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_PROGRESS)
    streak = models.PositiveIntegerField("sequência atual", default=0)
    notes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Hábito"
        verbose_name_plural = "Hábitos"

    def __str__(self) -> str:
        return self.name


class RelationshipItem(TimeStampedModel):
    class ItemType(models.TextChoices):
        CONTACT = "contact", "Contato"
        EVENT = "event", "Evento"
        NETWORKING = "networking", "Networking"

    name = models.CharField("nome", max_length=160)
    item_type = models.CharField("tipo", max_length=20, choices=ItemType.choices)
    next_action = models.CharField("próxima ação", max_length=255, blank=True)
    reference_date = models.DateField("data de referência", null=True, blank=True)
    notes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["reference_date", "name"]
        verbose_name = "Relacionamento"
        verbose_name_plural = "Relacionamentos"

    def __str__(self) -> str:
        return self.name


class LifeGoal(TimeStampedModel):
    class AreaChoices(models.TextChoices):
        BODY = "body", "Corpo"
        MONEY = "money", "Dinheiro"
        CAREER = "career", "Carreira"
        SPIRITUAL = "spiritual", "Espiritual"

    title = models.CharField("título", max_length=160)
    area = models.CharField("área", max_length=20, choices=AreaChoices.choices)
    target_date = models.DateField("data alvo", null=True, blank=True)
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEXT)
    notes = models.TextField("observações", blank=True)

    class Meta:
        ordering = ["target_date", "title"]
        verbose_name = "Meta de vida"
        verbose_name_plural = "Metas de vida"

    def __str__(self) -> str:
        return self.title


class RoadmapStep(TimeStampedModel):
    class ResourceTypeChoices(models.TextChoices):
        COURSE = "course", "Curso"
        VIDEO = "video", "Vídeo"
        ARTICLE = "article", "Artigo"
        PROJECT = "project", "Projeto"
        BOOK = "book", "Livro"

    title = models.CharField("título", max_length=180)
    stage = models.PositiveIntegerField("etapa", default=1)
    resource_type = models.CharField("tipo", max_length=20, choices=ResourceTypeChoices.choices)
    resource = models.CharField("recurso", max_length=255)
    source_url = models.URLField("link", blank=True)
    status = models.CharField("status", max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEXT)
    notes = models.TextField("observações", blank=True)
    sort_order = models.PositiveIntegerField("ordem", default=1)

    class Meta:
        ordering = ["stage", "sort_order", "title"]
        verbose_name = "Passo do roadmap"
        verbose_name_plural = "Passos do roadmap"

    def __str__(self) -> str:
        return f"Etapa {self.stage}: {self.title}"
