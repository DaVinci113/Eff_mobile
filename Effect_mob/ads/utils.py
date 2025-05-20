from django.db.models import Q

from .models import Category, Ad, ExchangeProposal


class SearchMixin:
    """Миксин-фильтр поиска"""
    def get_search_queryset(self, queryset=None):
        q = self.request.GET.get('q')
        if queryset is None:
            queryset = self.model.objects.all()
        return queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))


class AuthorCheckMixin:
    """Миксин для проверки автора"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autor'] = context['object'].user == self.request.user
        return context


class UserFilterMixin:
    """Миксин для фильтрации по пользователям"""
    def get_user_filtered_queryset(self, exclude=False):
        queryset = self.model.objects.all()
        if exclude:
            return queryset.exclude(user=self.request.user)
        return queryset.filter(user=self.request.user)


class FilterMixin:

    def get_filtered_queryset(self, queryset, filter_params):
        for field, values in filter_params.items():
            if values:
                queryset = queryset.filter(**{f"{field}__in": values})
        return queryset

    def get_category(self):
        return Category.objects.all().distinct()

    def get_condition(self):
        return Ad.CONDITION


class ProposalFilterMixin:
    """Миксин для фильтрации предложений"""

    def get_status(self):
        return ExchangeProposal.STATUS

    def get_send_or_receive(self):
        return [
            ('sender', 'Отправитель'),
            ('receiver', 'Получатель'),
        ]

    def get_proposal_queryset(self, user, role=None, status=None):
        """Базовый метод для фильтрации предложений"""
        if role and len(role) < 2:
            if 'sender' in role:
                queryset = ExchangeProposal.objects.filter(sender=user)
            elif 'receiver' in role:
                queryset = ExchangeProposal.objects.filter(receiver=user)
        else:
            queryset = ExchangeProposal.objects.filter(Q(sender=user) | Q(receiver=user))

        if status:
            queryset = queryset.filter(status__in=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = self.get_status()
        context['roles'] = self.get_send_or_receive()
        return context