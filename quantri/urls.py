from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'post'
urlpatterns = [

    path('', views.home, name='home'),

    # Trang chi tiết bài viết
    path('article_detail/<int:id>/', views.article_detail, name='article_detail'),
    path('add_comment/<int:id>/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    # Xử lý thêm bình luận
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('search_view/', views.search_view, name='search'),
    path('show_related_articles/', views.show_related_articles, name='show_related_articles'),

    path('register/', views.register, name='register'),
    # URL cho xử lý đăng ký
    path('gmail_verification/', views.gmail_verification, name='gmail_verification'),
    path('login/', views.user_login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'),
    path("logout/", views.logout_view, name='logout'),

    path("edit_comment/", views.edit_comment, name='edit_comment'),
    path('weather/', views.weather, name='weather'),
    path('notification/<int:id>/', views.notification, name='notification'),

    path('create_article/', views.create_article, name='create_article'),
    path('get_user_articles/<int:user_id_param>/', views.get_user_articles, name='get_user_articles'),
    path('delete_article/<int:article_id>/', views.delete_article, name='delete_article'),
    path('edit_article/<int:article_id>/', views.edit_article, name='edit_article'),

    path('display_notifications/', views.display_notifications, name='display_notifications'),
    path('article_notifications/<int:article_id>/<int:feedback_id>/', views.article_notifications,
         name='article_notifications'),

    # path('delete_img/<int:img_id>/', views.delete_img, name='delete_img'),
    # path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),

    path('update_account/', views.update_account, name='update_account'),
    path('create_growing_region/', views.create_growing_region, name='create_growing_region'),
    path('detail_seasonPlans/<int:id>', views.detail_seasonPlans, name='detail_seasonPlans'),
    path('items/<int:id>', views.item, name='item'),
    path('items_list/', views.item_list, name='item_list'),

    path('newspaper/<int:id>', views.newspaper, name='newspaper'),
    path('newspaper_list/', views.newspaper_list, name='newspaper_list'),

    # path('editfruitConten/<int:id>', views.editfruitConten, name='editfruitConten'),
    path('videos/<int:id>', views.videos, name='video'),
    path('videos_list/', views.videos_list, name='videos_list'),
    # path('price_list/', views.price_list, name='price_list'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)