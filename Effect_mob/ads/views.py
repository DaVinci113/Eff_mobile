from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import Ad, Category, ExchangeProposal
from .forms import CreateAdForm, CreateProposalForm


# Create your views here.
class Filter:
    """Категории фильтрации"""

    def get_category(self):
        return Category.objects.all().distinct()

    def get_condition(self):
        return Ad.CONDITION


class AdsFilter(Filter, ListView):
    """Фильтрует на основании выбора категории"""

    template_name = 'ads/ads_list.html'

    def get_queryset(self):
        category = self.request.GET.getlist('category')
        condition = self.request.GET.getlist('condition')
        if category and condition:
            return Ad.objects.filter(
                category__in=category,
                condition__in=condition
            ).exclude(user=self.request.user)
        elif condition:
            return Ad.objects.filter(
                condition__in=condition
            ).exclude(user=self.request.user)
        else:
            return Ad.objects.filter(
                category__in=category
            ).exclude(user=self.request.user)


class AdsList(AdsFilter, ListView):
    """Вывод чужих объявлений"""

    # paginate_by = 5
    model = Ad
    template_name = 'ads/ads_list.html'

    def get_queryset(self):
        return Ad.objects.exclude(user=self.request.user)


class UserAdsList(Filter, ListView):
    """Вывод своих объявлений"""

    model = Ad
    template_name = 'ads/user_ads_list.html'

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)


class CreateAd(CreateView):
    """Создает объявление"""

    form_class = CreateAdForm
    template_name = 'ads/ad_create.html'
    success_url = '/ads/user_ads'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


class UpdateAd(UpdateView):
    """Обновляет объявление"""

    model = Ad
    fields = [
        'title',
        'description',
        'image_url',
        'category',
        'condition',
    ]
    template_name = 'ads/ad_update.html'
    pk_url_kwarg = 'ad_pk'
    success_url = '/ads/user_ads/'


class DeleteAd(DeleteView):
    """Удаляет объявление"""

    model = Ad
    pk_url_kwarg = 'ad_pk'
    template_name = 'ads/delete.html'
    success_url = '/ads/user_ads/'


class DetailAd(DetailView):
    """Вывод подробной инф-ии по объявлению"""

    model = Ad
    template_name = 'ads/ad_detail.html'
    pk_url_kwarg = 'ad_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if context['object'].user == self.request.user:
            context['autor'] = True
        else:
            context['autor'] = False
        return context


class SearchAd(ListView):
    """Поиск чужих объявлений по введденным данным"""

    model = Ad
    template_name = 'ads/ads_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Ad.objects.filter(Q(title__icontains=q)|Q(description__icontains=q)).exclude(user=self.request.user)
        return query


class SearchUserAd(ListView):
    """Поиск своих объявлений по введденным данным"""

    model = Ad
    template_name = 'ads/user_ads_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = Ad.objects.filter(Q(title__icontains=q)|Q(description__icontains=q)).filter(user=self.request.user)
        return query


class CreateProposal(CreateView):
    """Создание предложения"""

    form_class = CreateProposalForm
    template_name = 'ads/proposal_create.html'
    success_url = '/ads'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.sender = User.objects.get(id=self.request.user.id)
        instance.receiver = Ad.objects.get(id=self.kwargs['id']).user
        instance.ad_receiver_id = Ad.objects.get(id=self.kwargs['id'])
        instance.status = 'awaits'
        instance.save()
        return super().form_valid(form)



class PropFilter:
    """Категории фильтрации предложений"""

    def get_status(self):
        return ExchangeProposal.STATUS

    def get_send_or_receive(self):
        return [
            ('sender', 'Отправитель'),
            ('receiver', 'Получатель'),
        ]


class ProposalFiltered(PropFilter, ListView):
    """Список предложений с примененными фильтрами"""

    template_name = 'ads/proposal_list.html'

    def get_queryset(self):
        status = self.request.GET.getlist('status')
        role = self.request.GET.getlist('role')
        user = self.request.user
        if len(role)<2 and 'sender' in role:
            filter_by = ExchangeProposal.objects.filter(
                sender=user
            )
        elif len(role)<2 and 'receiver' in role:
            filter_by = ExchangeProposal.objects.filter(
                receiver=user
            )
        else:
            filter_by = ExchangeProposal.objects.filter(
                Q(sender=user)|Q(receiver=user)
            )
        if status:
            filter_by = filter_by.filter(
                status__in=status
            )
        return filter_by




class ProposalList(ProposalFiltered, ListView):
    """Список предложений"""

    model = ExchangeProposal
    template_name = 'ads/proposal_list.html'


class ProposalDetail(DetailView):
    """Информация по предложению"""

    model = ExchangeProposal
    template_name = 'ads/proposal_detail.html'
    pk_url_kwarg = 'proposal_pk'


class ProposalUpdate(UpdateView):
    """Обновляет предложение"""

    model = ExchangeProposal
    fields = ['status']
    template_name = 'ads/proposal_update.html'
    pk_url_kwarg = 'proposal_pk'
    success_url = '/proposal'
