from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import urllib.parse
from .models import (
    ServiceCategory, Service, Industry, PortfolioConcept, FAQ, Lead, AnalyticsEvent, Insight, DigitalAuditSubmission
)


admin.site.site_header = mark_safe('QUORV Brand Studio &nbsp;•&nbsp; <a href="/dashboard/" style="background: #E4C388; color: #08090C; font-size: 11px; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-weight: bold; vertical-align: middle;">📊 Launch Intelligence Dashboard ↗</a>')
admin.site.site_title = "QUORV Admin"
admin.site.index_title = "Studio Content & Lead Management"



@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'outcome_statement', 'order')
    list_editable = ('order',)
    ordering = ('order', 'code')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'outcome', 'full_description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'order')


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'order')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    search_fields = ('title', 'the_challenge', 'the_solution')


@admin.register(PortfolioConcept)
class PortfolioConceptAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_type', 'category', 'is_concept', 'order', 'created_at')
    list_filter = ('is_concept', 'category')
    search_fields = ('title', 'client_type', 'concept_summary')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_concept', 'order')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    list_editable = ('order',)
    search_fields = ('question', 'answer')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'business_name', 'sector_label', 'country', 'status_badge', 'whatsapp_reply_button', 'email')
    list_filter = ('status', 'business_type', 'country', 'created_at')
    search_fields = ('name', 'business_name', 'email', 'phone', 'message', 'service_interest')
    readonly_fields = ('created_at', 'source')
    list_per_page = 25
    actions = ['mark_as_contacted', 'mark_as_in_discussion', 'mark_as_closed']

    def sector_label(self, obj):
        return obj.get_business_type_display()
    sector_label.short_description = "Sector"

    def status_badge(self, obj):
        colors = {
            'new': '#22c55e',          # Green
            'contacted': '#3b82f6',    # Blue
            'in_discussion': '#eab308', # Amber
            'closed': '#6b7280',       # Gray
        }
        color = colors.get(obj.status, '#94a3b8')
        return format_html(
            '<span style="background-color: {}; color: #000; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Inquiry Status"

    def whatsapp_reply_button(self, obj):
        phone_clean = ''.join(filter(str.isdigit, obj.phone or ''))
        greeting = f"Hi {obj.name}, thank you for reaching out to QUORV Brand Studio regarding {obj.business_name or 'your beauty business'}."
        encoded = urllib.parse.quote(greeting)

        if phone_clean:
            url = f"https://wa.me/{phone_clean}?text={encoded}"
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer" style="background: #25D366; color: #fff; padding: 4px 10px; border-radius: 6px; text-decoration: none; font-size: 11px; font-weight: bold;">💬 WhatsApp Client</a>',
                url
            )
        else:
            return mark_safe('<span style="color: #9ca3af; font-size: 11px;">No Phone Provided</span>')
    whatsapp_reply_button.short_description = "Direct Action"


    @admin.action(description="Mark selected leads as Contacted")
    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')

    @admin.action(description="Mark selected leads as In Discussion")
    def mark_as_in_discussion(self, request, queryset):
        queryset.update(status='in_discussion')

    @admin.action(description="Mark selected leads as Closed")
    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'event_type_badge', 'event_label', 'page_url', 'ip_address')
    list_filter = ('event_type', 'created_at')
    search_fields = ('event_label', 'page_url', 'ip_address', 'user_agent')
    readonly_fields = ('event_type', 'event_label', 'page_url', 'referrer', 'ip_address', 'user_agent', 'created_at')
    list_per_page = 50

    def event_type_badge(self, obj):
        colors = {
            'whatsapp_click': '#22c55e',
            'lead_submit': '#eab308',
            'email_click': '#3b82f6',
            'service_view': '#a855f7',
            'concept_view': '#ec4899',
            'outbound_link': '#64748b',
        }
        color = colors.get(obj.event_type, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 600;">{}</span>',
            color,
            obj.get_event_type_display()
        )
    event_type_badge.short_description = "Event Type"


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'read_time', 'is_featured', 'order', 'published_date')
    list_filter = ('category', 'is_featured', 'published_date')
    search_fields = ('title', 'subtitle', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'order')


@admin.register(DigitalAuditSubmission)
class DigitalAuditSubmissionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'business_name', 'contact_name', 'business_type', 'booking_software', 'score_badge', 'status_badge')
    list_filter = ('status', 'business_type', 'booking_software', 'created_at')
    search_fields = ('business_name', 'contact_name', 'email', 'phone', 'website_or_instagram')
    readonly_fields = ('created_at', 'calculated_score', 'key_vulnerabilities')
    list_per_page = 25

    def score_badge(self, obj):
        score = obj.calculated_score
        bg = '#ef4444' if score < 60 else ('#eab308' if score < 80 else '#22c55e')
        return format_html(
            '<span style="background-color: {}; color: #000; padding: 2px 8px; border-radius: 9999px; font-weight: bold; font-size: 11px;">{}/100</span>',
            bg, score
        )
    score_badge.short_description = "Audit Score"

    def status_badge(self, obj):
        colors = {
            'pending': '#eab308',
            'analyzed': '#3b82f6',
            'booked_consult': '#22c55e',
            'closed': '#6b7280',
        }
        color = colors.get(obj.status, '#94a3b8')
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"

