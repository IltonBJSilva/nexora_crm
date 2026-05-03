from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Sum
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DeleteView, RedirectView, TemplateView, UpdateView

from .forms import CRMAuthenticationForm
from .models import AcademicTask, FinanceEntry, RoadmapStep, StatusChoices, WorkTask
from .registry import AREA_LABELS, ENTITY_REGISTRY, get_entity_config, permission_codename


def get_entity_or_404(entity_slug):
    config = get_entity_config(entity_slug)
    if not config:
        raise Http404("Módulo não encontrado.")
    return config


def format_field_value(obj, field_name):
    display_method = getattr(obj, f"get_{field_name}_display", None)
    if callable(display_method):
        return display_method()
    value = getattr(obj, field_name)
    if value in (None, ""):
        return "—"
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    return value


def build_record_cards(queryset, config):
    model = config["model"]
    columns = config.get("columns", [])
    cards = []
    for obj in queryset:
        details = []
        for field_name in columns:
            field = model._meta.get_field(field_name)
            details.append((field.verbose_name, format_field_value(obj, field_name)))

        excerpts = []
        for candidate in ("description", "notes", "concept", "example", "learning", "impact", "goal", "insight", "resource"):
            value = getattr(obj, candidate, "")
            if value:
                excerpts.append(str(value))
            if len(excerpts) == 2:
                break

        cards.append(
            {
                "object": obj,
                "title": str(obj),
                "details": details,
                "excerpts": excerpts,
            }
        )
    return cards


class WorkspaceContextMixin:
    def get_workspace_groups(self):
        grouped = defaultdict(list)
        for slug, config in ENTITY_REGISTRY.items():
            if not self.request.user.has_perm(permission_codename(config["model"], "view")):
                continue
            grouped[config["area"]].append(
                {
                    "slug": slug,
                    "title": config["title"],
                    "description": config["description"],
                    "icon": config["icon"],
                    "count": config["model"].objects.count(),
                    "url": reverse("entity-list", kwargs={"entity_slug": slug}),
                }
            )
        return [{"key": area, "label": AREA_LABELS[area], "items": items} for area, items in grouped.items()]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workspace_groups"] = self.get_workspace_groups()
        context["current_entity_slug"] = getattr(self, "entity_slug", None)
        context["current_area_key"] = getattr(self, "entity_config", {}).get("area")
        context["current_user_role"] = getattr(getattr(self.request.user, "profile", None), "get_role_display", lambda: "Usuario")()
        return context


class AuthRedirectView(RedirectView):
    pattern_name = "dashboard"

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse("login")
        return super().get_redirect_url(*args, **kwargs)


class CRMLoginView(LoginView):
    template_name = "auth/login.html"
    authentication_form = CRMAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("dashboard")


class CRMLogoutView(LogoutView):
    next_page = "login"


class DashboardView(LoginRequiredMixin, WorkspaceContextMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        month_entries = FinanceEntry.objects.filter(date__year=today.year, date__month=today.month)
        income = month_entries.filter(entry_type=FinanceEntry.EntryType.INCOME).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        expenses = (
            month_entries.filter(entry_type=FinanceEntry.EntryType.EXPENSE).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        )
        investments = (
            month_entries.filter(entry_type=FinanceEntry.EntryType.INVESTMENT).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        )

        overdue_tasks = list(
            AcademicTask.objects.exclude(status=StatusChoices.DONE).filter(due_date__isnull=False, due_date__lt=today)[:4]
        )
        overdue_tasks.extend(
            list(WorkTask.objects.exclude(status=StatusChoices.DONE).filter(due_date__isnull=False, due_date__lt=today)[:4])
        )

        roadmap_stages = defaultdict(list)
        for step in RoadmapStep.objects.all():
            roadmap_stages[step.stage].append(step)

        context["hero_stats"] = [
            {"label": "Módulos ativos", "value": len(ENTITY_REGISTRY), "caption": "faculdade, trabalho, pessoal e roadmap"},
            {
                "label": "Tasks abertas",
                "value": AcademicTask.objects.exclude(status=StatusChoices.DONE).count()
                + WorkTask.objects.exclude(status=StatusChoices.DONE).count(),
                "caption": "acadêmicas e profissionais",
            },
            {
                "label": "Saldo do mês",
                "value": f"R$ {(income - expenses):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "caption": "receitas menos despesas",
            },
            {
                "label": "Investimentos",
                "value": f"R$ {investments:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "caption": "aporte registrado no mês",
            },
        ]
        context["focus_columns"] = [
            {
                "title": "Faculdade",
                "description": "Disciplinas, tarefas, base de conhecimento e semestre.",
                "items": build_record_cards(AcademicTask.objects.all()[:3], ENTITY_REGISTRY["tarefas-academicas"]),
                "url": reverse("entity-list", kwargs={"entity_slug": "tarefas-academicas"}),
            },
            {
                "title": "Trabalho",
                "description": "Tasks, aprendizado técnico, lições e metas.",
                "items": build_record_cards(WorkTask.objects.all()[:3], ENTITY_REGISTRY["tarefas-trabalho"]),
                "url": reverse("entity-list", kwargs={"entity_slug": "tarefas-trabalho"}),
            },
            {
                "title": "Pessoal",
                "description": "Fitness, finanças, hábitos, leitura e relacionamentos.",
                "items": build_record_cards(FinanceEntry.objects.all()[:3], ENTITY_REGISTRY["financas"]),
                "url": reverse("entity-list", kwargs={"entity_slug": "financas"}),
            },
        ]
        context["roadmap_stages"] = [{"stage": stage, "items": items} for stage, items in roadmap_stages.items()]
        context["overdue_tasks"] = overdue_tasks
        context["today"] = today
        return context


class WorkspaceIndexView(LoginRequiredMixin, WorkspaceContextMixin, TemplateView):
    template_name = "workspace_index.html"
    login_url = "login"


class EntityListView(LoginRequiredMixin, WorkspaceContextMixin, TemplateView):
    template_name = "entity_list.html"
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        self.entity_slug = kwargs["entity_slug"]
        self.entity_config = get_entity_or_404(self.entity_slug)
        if not request.user.has_perm(permission_codename(self.entity_config["model"], "view")):
            raise Http404("Modulo nao encontrado.")
        return super().dispatch(request, *args, **kwargs)

    def build_search_queryset(self):
        queryset = self.entity_config["model"].objects.all()
        query = self.request.GET.get("q", "").strip()
        if not query:
            return queryset

        search = Q()
        for field in self.entity_config["model"]._meta.fields:
            if field.get_internal_type() in {"CharField", "TextField"}:
                search |= Q(**{f"{field.name}__icontains": query})
        return queryset.filter(search)

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm(permission_codename(self.entity_config["model"], "add")):
            messages.error(request, "Voce nao tem permissao para criar registros neste modulo.")
            return HttpResponseRedirect(reverse("entity-list", kwargs={"entity_slug": self.entity_slug}))
        form = self.entity_config["form"](request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{self.entity_config['title']} salvo com sucesso.")
            return HttpResponseRedirect(reverse("entity-list", kwargs={"entity_slug": self.entity_slug}))
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.build_search_queryset()
        context["entity_config"] = self.entity_config
        context["entity_slug"] = self.entity_slug
        context["form"] = kwargs.get("form") or self.entity_config["form"]()
        context["query"] = self.request.GET.get("q", "").strip()
        context["records"] = build_record_cards(queryset[:30], self.entity_config)
        context["total_records"] = queryset.count()
        context["area_label"] = AREA_LABELS[self.entity_config["area"]]
        context["can_add"] = self.request.user.has_perm(permission_codename(self.entity_config["model"], "add"))
        context["can_change"] = self.request.user.has_perm(permission_codename(self.entity_config["model"], "change"))
        context["can_delete"] = self.request.user.has_perm(permission_codename(self.entity_config["model"], "delete"))
        return context


class EntityUpdateView(LoginRequiredMixin, WorkspaceContextMixin, UpdateView):
    template_name = "entity_form.html"
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        self.entity_slug = kwargs["entity_slug"]
        self.entity_config = get_entity_or_404(self.entity_slug)
        if not request.user.has_perm(permission_codename(self.entity_config["model"], "change")):
            raise Http404("Modulo nao encontrado.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.entity_config["model"].objects.all()

    def get_form_class(self):
        return self.entity_config["form"]

    def get_success_url(self):
        messages.success(self.request, f"{self.entity_config['title']} salvo com sucesso.")
        return reverse("entity-list", kwargs={"entity_slug": self.entity_slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entity_config"] = self.entity_config
        context["entity_slug"] = self.entity_slug
        return context


class EntityDeleteView(LoginRequiredMixin, WorkspaceContextMixin, DeleteView):
    template_name = "entity_confirm_delete.html"
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        self.entity_slug = kwargs["entity_slug"]
        self.entity_config = get_entity_or_404(self.entity_slug)
        if not request.user.has_perm(permission_codename(self.entity_config["model"], "delete")):
            raise Http404("Modulo nao encontrado.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.entity_config["model"].objects.all()

    def get_success_url(self):
        messages.success(self.request, "Registro removido.")
        return reverse("entity-list", kwargs={"entity_slug": self.entity_slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entity_config"] = self.entity_config
        context["entity_slug"] = self.entity_slug
        return context
