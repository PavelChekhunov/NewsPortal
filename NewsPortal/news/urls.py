from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (PostsList, PostDetail, PostDetailImage, PostSearch, PostCreate, PostUpdate, PostDelete,
                    CreateArticle, SubscribeCategories, subscription, testlog)


urlpatterns = [
   path('', PostsList.as_view(), name="post_list"),
   # path('<int:id>', cache_page(300)(PostDetail.as_view()), name="post_detail"),
   path('<int:id>', PostDetail.as_view(), name="post_detail"),
   path('<int:id>-img', PostDetailImage.as_view(), name="post_detail-img"),
   path('search/', PostSearch.as_view(), name="post_search"),
   path('createnew/', PostCreate.as_view(), name='post_createnew'),
   path('<int:id>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:id>/delete/', PostDelete.as_view(), name='post_delete'),
   path('createarticle/', CreateArticle.as_view(), name='post_createart'),
   path('subscribe/', SubscribeCategories.as_view(), name="subscribe"),
   path('subscription/', subscription, name="subscription"),
   path('testlog', testlog, name='testlog'),
]
