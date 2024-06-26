from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from home.views import delete_user
from django.conf import settings
from django.conf.urls.static import static
# from .views import WorkerListView
from .views import generate_work_permit_pdf



urlpatterns = [
    path('', views.index,name="index"),
    path('about/', views.about,name="about"),
    path('services/', views.services,name="services"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register,name="register"),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('userpage/', views.userpage,name="userpage"),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('agent_profile/', views.agent_profile, name='agent_profile'),
    path('worker_list/', views.worker_list, name='worker_list'),
    # path('workers/', WorkerListView.as_view(), name='worker-list'),
    path('agentpage/', views.agentpage,name="agentpage"),
    path('addworker/', views.addworker,name="addworker"),
    path('viewworker/', views.viewworker,name="viewworker"),
    path('update_worker/<int:worker_id>/', views.update_worker, name='update_worker'),
    path('delete_worker/<int:worker_id>/', views.delete_worker, name='delete_worker'),
    path('policepage/', views.policepage,name="policepage"),
    path('incidentreported/', views.incidentreported, name='incidentreported'),
    path('activeofficers/', views.activeofficers,name="activeofficers"),
    path('workerprofile/', views.workerprofile,name="workerprofile"),
    path('viewprofile/<int:worker_id>/', views.viewprofile, name='viewprofile'),
    path('workeragent/<int:agent_id>/', views.workeragent, name='workeragent'),
    path('adminpanel/', views.adminpanel,name="adminpanel"),
    path('users/', views.users,name="users"),
    path('workcategory/', views.workcategory,name="workcategory"),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('verify_user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/profile/', views.userpage,name="userpage"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('verify_worker/<int:worker_id>/', views.verify_worker, name='verify_worker'),
    path('reject_worker/<int:worker_id>/', views.reject_worker, name='reject_worker'),
    path('verifyuser/<int:user_id>/', views.verifyuser, name='verifyuser'),
    path('rejectuser/<int:user_id>/', views.rejectuser, name='rejectuser'),
    path('generate_work_permit_pdf/<int:worker_id>/', generate_work_permit_pdf, name='generate_work_permit_pdf'),
    path('agent_contact/<int:agent_id>/<int:worker_id>/', views.agent_contact, name='agent_contact'),
    path('works_available/', views.works_available, name='works_available'),
    path('jobs/', views.jobs, name='jobs'),
    path('salary/', views.salary, name='salary'),
    path('payment_details/', views.payment_details, name='payment_details'),
    path('setting/', views.setting, name='setting'),
    path('book_worker/<int:agent_id>/<int:worker_id>/', views.book_worker, name='book_worker'),
    path('booking-workers/', views.booking_workers_view, name='booking_workers'),
    path('document/', views.document_verification, name='document'),
    path('joblist/<int:employer_id>/', views.joblist, name='joblist'),
    path('bookings/<int:user_id>/', views.bookings, name='bookings'),
    path('pay_salary/<int:booking_id>/', views.pay_salary, name='pay_salary'),
    path('notifications/<int:user_id>/', views.booking_workers_view, name='notification_view'),
    path('worker_tracked/', views.worker_tracked, name='worker_tracked'),
    path('generate_report_worker/', views.generate_report_worker, name='generate_report_worker'),
    path('generate_report_booking/', views.generate_report_booking, name='generate_report_booking'),
    path('report/', views.report, name='report'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)