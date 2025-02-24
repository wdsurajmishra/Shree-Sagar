from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('shop', views.shop, name='shop'),
    path('support', views.support, name='support'),
    path('categories', views.categories, name='categories'),
    path('search', views.search, name='search'),
    path('faqs', views.faq, name='faq'),
    path('our-story', views.our_story, name='our-story'),
    path('contact-us', views.contact, name='contact'),
    path('history', views.history, name='history'),
    path('product/<slug>', views.product, name='product-detail'),
    path('book-a-video-call/<id>', views.videoCallBooking, name='video-call-booking'),
    path('get-slots', views.available_slots, name='available-slots'),
    path('cart/get', views.get_cart, name='get-cart'),
    path('cart/add', views.add_to_cart, name='add-to-cart'),
    path('cart/update', views.update_cart, name='update-cart'),
    path('cart/delete', views.delete_from_cart, name='delete-cart'),
    path('user/profile', views.userProfile, name='user-profile'),
    path('user/addresses', views.userAddresses, name='user-addresses'),
    path('user/addresses/update/<address_id>', views.updateAddress, name='user-addresses-update'),
    path('user/addresses/delete/<address_id>', views.deleteAddress, name='user-addresses-delete'),
]