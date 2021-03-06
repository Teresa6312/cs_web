from . import views
from . import package_views as pk_views
from . import information_views as info_views
from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# , permission_required



urlpatterns = [
# open for everyone

    path('accounts/register/', views.RegisterView.as_view(), name = 'register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='main/login.html'), name = 'login'),

    path('myaccount/location/', views.locationView, name='location'),

    path('shipping/', views.ShippingView.as_view(), name='shipping'),

    path('contact-us/', views.SendEmailView.as_view(), name='contact_us'),
    path('tracking/', views.TrackingView.as_view(), name='tracking'),
    path('customer-service/', info_views.CustomerServiceView.as_view(), name='customer_service'),

    path('543243243234234/', views.CollectionPointView.as_view()),



# login_required
    path('myaccount/logout/', login_required(views.logout_view), name = 'logout'),

    path('myaccount/', login_required(views.AccountView.as_view()), name='account'),
    path('myaccount/send-Confirmation-email/', login_required(views.sendConfirmationEmail), name="send_confirmation_email"),
    path('myaccount/profile/update', login_required(views.UpdateProfileView.as_view()), name='updateprofile'),
    path('myaccount/change-password/', login_required(views.ChangePasswordView.as_view()), name='changepassword'),

    path('myaccount/address', login_required(views.AddressView.as_view()), name='useraddress'),
    path('myaccount/address/<int:add_id>/eidt', login_required(views.EditAddressView.as_view()), name='editaddress'),

    path('myaccount/address/<int:add_id>/delete', login_required(views.DeleteAddressView.as_view()), name='deleteaddress'),
    path('myaccount/address/<int:add_id>/set_dedault_address', login_required(views.SetDefaultAddressView.as_view()), name='set_dedault_address'),


    path('package/<int:pack_id>/detail', login_required(pk_views.PackageDetailView.as_view()), name='package_detail'),

    path('myaccount/wallet', login_required(views.WalletView.as_view()), name='userwallet'),

    path('myaccount/packages', login_required(pk_views.PackagesView.as_view()), name='userpackage'),

    path('packages/<int:selected_col>/add', login_required(pk_views.AddCoShipping.as_view()), name='add_co_shipping'),
    path('packages/direct-shipping/add', login_required(pk_views.AddDirectShipping.as_view()), name='add_direct_shipping'),
    path('packages/direct-shipping/confirm', login_required(pk_views.ConfirmDirectShipping.as_view()), name='confirm_direct_shipping'),
    path('packages/', login_required(pk_views.PackagesView.as_view()), name='packages'),
    path('packages/cart/', login_required(pk_views.PackageCartView.as_view()), name='packagecart'),
    path('packages/cart/number', login_required(pk_views.ReturnPackageNumber), name='packageNumber'),
    path('packages/cart/coupon', login_required(pk_views.couponView), name='coupon'),



# need to locked for logged in user
    path('accounts/reset-password/', auth_views.PasswordResetView.as_view(template_name='password/password_reset_form.html', email_template_name='email/password_reset_email.html'), name='password_reset'),

    path('accounts/reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),

    re_path(r'^accounts/reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),name='password_reset_confirm'),

    path('accounts/reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),

]

# change
