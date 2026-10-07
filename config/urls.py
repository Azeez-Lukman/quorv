from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('services/', views.services_index, name='services_index'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('industries/', views.industries_index, name='industries_index'),
    path('industries/<slug:slug>/', views.industry_detail, name='industry_detail'),
    path('work/', views.work_index, name='work_index'),
    path('process/', views.process_view, name='process'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('api/leads/submit/', views.lead_submit, name='lead_submit'),
    path('api/audit/submit/', views.audit_submit, name='audit_submit'),
    path('api/analytics/event/', views.analytics_event, name='analytics_event'),

    # Studio Owner Analytics Dashboard
    path('dashboard/', views.studio_dashboard, name='studio_dashboard'),
    path('dashboard/export-leads/', views.export_leads_csv, name='export_leads_csv'),
    path('dashboard/lead/<int:lead_id>/status/', views.update_lead_status, name='update_lead_status'),

    path('insights/', views.insights_index, name='insights_index'),
    path('insights/<slug:slug>/', views.insight_detail, name='insight_detail'),

    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_of_service, name='terms_of_service'),

    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]



if settings.DEBUG and settings.STATICFILES_DIRS:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
