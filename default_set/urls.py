from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from default_set.forms import CustomPasswordResetForm

urlpatterns = patterns('',
                       url(r'^$', 'default_set.views.index', name='account_index'),
                       url(r'^signin/$', 'default_set.views.signin', name='account_signin'),
                       url(r'^signup/$', 'default_set.views.signup', name='account_signup'),
                       url(r'^signout/$', 'default_set.views.signout', name='account_signout'),
                       url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', dict(
                           template_name='default_set/password_reset_form.html',
                           html_email_template_name='mail/password_reset_email.html',
                           subject_template_name='mail/password_reset_subject.txt',
                           password_reset_form=CustomPasswordResetForm, ), name='password_reset'),
                       url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', dict(
                           template_name='default_set/password_reset_done.html'), name='password_reset_done'),
                       url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           'django.contrib.auth.views.password_reset_confirm', dict(
                               template_name='default_set/password_reset_confirm.html'), name='password_reset_confirm'),
                       url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', dict(
                           template_name='default_set/password_reset_complete.html'
                       ), name='password_reset_complete'),

                       url(r'^deposit/$', 'default_set.views.deposit', name='account_deposit'),
                       url(r'^deposit/continue/(?P<pk>\d+)/$', 'default_set.views.deposit_continue',
                           name='deposit_continue'),
                       url(r'^deposit/cancel/(?P<pk>\d+)/$', 'default_set.views.deposit_cancel',
                           name='account_deposit_cancel'),
                       url(r'^withdraw/$', 'default_set.views.withdraw', name='account_withdraw'),
                       url(r'^transfer/$', 'default_set.views.transfer', name='account_transfer'),

                       url(r'^history/$', 'default_set.views.history', name='account_history'),
                       url(r'^referrals/$', 'default_set.views.referrals', name='account_referrals'),
                       url(r'^tickets/', include('default_set.tickets.urls')),
                       url(r'^dialogs/', include('default_set.dialogs.urls')),
                       url(r'^settings/$', 'default_set.views.profile_settings', name='account_settings'),
                       url(r'^payment_systems/$', 'default_set.views.payment_systems_settings',
                           name='account_payment_systems_settings'),
                       url(r'^deposit/ok/', TemplateView.as_view(template_name='default_set/deposit_ok.html'),
                           name='deposit_ok'),
                       url(r'^deposit/error/', TemplateView.as_view(template_name='default_set/deposit_error.html'),
                           name='deposit_error'),
                       url(r'^deposit/perfect_money/', include('payment_systems.perfect_money.urls')),
                       url(r'^deposit/payeer/', include('payment_systems.payeer.urls')),
)
