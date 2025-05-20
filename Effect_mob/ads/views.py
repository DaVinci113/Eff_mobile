from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView
from .models import Ad, ExchangeProposal
from .forms import CreateAdForm, CreateProposalForm
from .utils import AuthorCheckMixin, SearchMixin, UserFilterMixin, FilterMixin, ProposalFilterMixin


# Create your views here.


class Index(TemplateView):
    """Главная страница"""
    template_name = 'ads/index.html'


class AdsFilter(FilterMixin, ListView):
    """Фильтрует на основании выбора категории"""

    template_name = 'ads/ads_list.html'

    def get_queryset(self):
        queryset = Ad.objects.exclude(user=self.request.user)
        filter_params = {
            'category' : self.request.GET.getlist('category'),
            'condition' : self.request.GET.getlist('condition'),
        }
        return self.get_filtered_queryset(queryset, filter_params)


class AdsList(UserFilterMixin, AdsFilter, ListView):
    """Вывод чужих объявлений"""

    model = Ad
    template_name = 'ads/ads_list.html'

    def get_queryset(self):
        return self.get_user_filtered_queryset(exclude=True)


class UserAdsList(UserFilterMixin, ListView):
    """Вывод своих объявлений"""

    model = Ad
    template_name = 'ads/user_ads_list.html'

    def get_queryset(self):
        return self.get_user_filtered_queryset(exclude=False)


class CreateAd(CreateView):
    """Создает объявление"""

    form_class = CreateAdForm
    template_name = 'ads/ad_create.html'
    success_url = reverse_lazy('ads:confirmation')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


class ConfirmCreateAd(TemplateView):
    """Подтверждение создания объявления"""
    template_name = 'ads/confirmation.html'


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


class DetailAd(AuthorCheckMixin, DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    pk_url_kwarg = 'ad_pk'


class SearchAd(SearchMixin, UserFilterMixin, FilterMixin, ListView):
    model = Ad
    template_name = 'ads/ads_list.html'

    def get_queryset(self):
        queryset = self.get_user_filtered_queryset(exclude=True)
        return self.get_search_queryset(queryset)


class SearchUserAd(SearchMixin, UserFilterMixin, ListView):
    """Поиск своих объявлений по введденным данным"""

    model = Ad
    template_name = 'ads/user_ads_list.html'

    def get_queryset(self):
        queryset = self.get_user_filtered_queryset(exclude=False)
        return self.get_search_queryset(queryset)


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


class ProposalFiltered(ProposalFilterMixin, ListView):
    """Список предложений с примененными фильтрами"""

    template_name = 'ads/proposal_list.html'

    def get_queryset(self):
        status = self.request.GET.getlist('status')
        role = self.request.GET.getlist('role')

        return self.get_proposal_queryset(self.request.user, role, status)




class ProposalList(ProposalFilterMixin, ListView):
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


