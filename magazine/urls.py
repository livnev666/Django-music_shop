from django.urls import path
from magazine import views as views_magazine


urlpatterns = [

    path('', views_magazine.main_page, name='main-page'),
    path('list/', views_magazine.ListProduct.as_view(), name='all_prod'),
    path('product/<slug:slug_product>/', views_magazine.DetailProduct.as_view(), name='one_product'),
    path('guitars/', views_magazine.ListProductGuitars.as_view(), name='guitars'),
    path('drums/', views_magazine.ListProductDrums.as_view(), name='drums'),
    path('wind/', views_magazine.ListProductWind.as_view(), name='wind_instr'),
    path('related/', views_magazine.ListProductRelated.as_view(), name='related_prod'),
    path('registration/', views_magazine.RegisterView.as_view(), name='register'),
    path('login/', views_magazine.AuthorizationView.as_view(), name='log_in'),
    path('logout/', views_magazine.log_out_user, name='log_out'),

    path('cart/', views_magazine.all_detail, name='cart_detail'),
    path('add/<int:product_id>/', views_magazine.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views_magazine.cart_remove, name='cart_remove'),

    # path('category/<slug:slug_cat>/', views_magazine.DetailCategory.as_view(), name='category')



]