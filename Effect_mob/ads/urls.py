from django.urls import path
from .views import AdsList, CreateAd, UserAdsList, UpdateAd, DeleteAd, DetailAd, SearchAd, SearchUserAd, AdsFilter, \
    CreateProposal, ProposalList, ProposalDetail, ProposalUpdate, ProposalFiltered

app_name = 'ads'
urlpatterns = [
    # path('', Ads.as_view(), name='ads'),
    path('ads/', AdsList.as_view(), name='ads-list'),
    path('filter/', AdsFilter.as_view(), name='ads-filter'),
    path('create_ad/', CreateAd.as_view(), name='ad-create'),
    path('ads/user_ads/', UserAdsList.as_view(), name='user-ads'),
    path('ads/user_ads/update/<int:ad_pk>/', UpdateAd.as_view(), name='ad-update'),
    path('ads/user_ads/delete/<int:ad_pk>/', DeleteAd.as_view(), name='ad-delete'),
    path('ads/detail/<int:ad_pk>/', DetailAd.as_view(), name='ad-detail'),
    path('ads/search_ad/', SearchAd.as_view(), name='ad-search'),
    path('ads/search_user_ad/', SearchUserAd.as_view(), name='user-ad-search'),
    path('ads/proposal/<int:id>/', CreateProposal.as_view(), name='proposal'),
    path('proposal/', ProposalList.as_view(), name='proposal-list'),
    path('proposal/detail/<int:proposal_pk>/', ProposalDetail.as_view(), name='proposal-detail'),
    path('proposal/update/<int:proposal_pk>/', ProposalUpdate.as_view(), name='proposal-detail'),
    path('filtered/', ProposalFiltered.as_view(), name='proposal-filter')
]