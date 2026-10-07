from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import (
    ServiceCategory, Service, Industry, FAQ, PortfolioConcept, Lead, AnalyticsEvent, Insight, DigitalAuditSubmission
)
import json
import csv

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    categories = ServiceCategory.objects.prefetch_related('services').all()
    industries = Industry.objects.all()
    faqs = FAQ.objects.all()
    concepts = PortfolioConcept.objects.filter(is_concept=True)[:3]
    featured_insights = Insight.objects.filter(is_featured=True)[:3]

    whatsapp_number = "+447352789073"
    whatsapp_clean = "447352789073"
    default_wa_message = "Hi Quorv, I'm interested in improving the digital presence of my beauty business."
    wa_url = f"https://wa.me/{whatsapp_clean}?text={default_wa_message.replace(' ', '%20')}"

    context = {
        'categories': categories,
        'industries': industries,
        'faqs': faqs,
        'concepts': concepts,
        'featured_insights': featured_insights,
        'whatsapp_number': whatsapp_number,
        'whatsapp_url': wa_url,
        'business_email': "quorv911@gmail.com",
    }
    return render(request, 'index.html', context)


def services_index(request):
    categories = ServiceCategory.objects.prefetch_related('services').all()
    return render(request, 'services.html', {
        'categories': categories,
        'whatsapp_url': "https://wa.me/447352789073?text=Hi%20Quorv%2C%20I%27d%20like%20to%20learn%20more%20about%20your%20services.",
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related_services = Service.objects.filter(category=service.category).exclude(id=service.id)[:3]
    wa_url = f"https://wa.me/447352789073?text={service.whatsapp_prompt.replace(' ', '%20')}"
    return render(request, 'service_detail.html', {
        'service': service,
        'related_services': related_services,
        'whatsapp_url': wa_url,
    })


def industries_index(request):
    industries = Industry.objects.all()
    return render(request, 'industries.html', {'industries': industries})


def industry_detail(request, slug):
    industry = get_object_or_404(Industry, slug=slug)
    return render(request, 'industry_detail.html', {'industry': industry})


def work_index(request):
    concepts = PortfolioConcept.objects.all()
    return render(request, 'work.html', {'concepts': concepts})


def process_view(request):
    return render(request, 'process.html')


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html', {
        'whatsapp_url': "https://wa.me/447352789073?text=Hi%20Quorv%2C%20I%27m%20interested%20in%20improving%20the%20digital%20presence%20of%20my%20beauty%20business."
    })


def insights_index(request):
    insights_list = Insight.objects.all()
    return render(request, 'insights.html', {
        'insights': insights_list,
        'whatsapp_url': settings.QUORV_WHATSAPP_URL
    })


def insight_detail(request, slug):
    insight = get_object_or_404(Insight, slug=slug)
    related = Insight.objects.exclude(id=insight.id)[:2]
    return render(request, 'insight_detail.html', {
        'insight': insight,
        'related_insights': related,
        'whatsapp_url': settings.QUORV_WHATSAPP_URL
    })


@require_POST
def lead_submit(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        business_name = data.get('business_name', '').strip()
        business_type = data.get('business_type', 'salon').strip()
        country = data.get('country', '').strip()
        service_interest = data.get('service_interest', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return JsonResponse({'status': 'error', 'message': 'Please provide your name, email, and a brief message.'}, status=400)

        lead = Lead.objects.create(
            name=name,
            email=email,
            phone=phone,
            business_name=business_name,
            business_type=business_type,
            country=country,
            service_interest=service_interest,
            message=message,
            source="Website Inquiry Form"
        )

        try:
            AnalyticsEvent.objects.create(
                event_type='lead_submit',
                event_label=f"Inquiry: {name} ({business_name or 'Independent'})",
                page_url=request.build_absolute_uri(),
                referrer=request.META.get('HTTP_REFERER', '')[:500],
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:400]
            )
        except Exception:
            pass

        notification_email = getattr(settings, 'STUDIO_NOTIFICATION_EMAIL', 'quorv911@gmail.com')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'QUORV Studio <noreply@quorv.com>')
        subject = f"[QUORV Studio Lead] New inquiry from {name} ({business_name or 'Beauty Professional'})"
        sector_display = dict(Lead.BUSINESS_TYPE_CHOICES).get(business_type, business_type)
        body = f"""New inquiry received on QUORV Brand Studio:

Client Name: {name}
Email: {email}
Phone / WhatsApp: {phone or 'Not provided'}
Business Name: {business_name or 'Not provided'}
Sector: {sector_display}
Country / City: {country or 'Not provided'}
Service Interest: {service_interest or 'General Inquiry'}

Message:
{message}

---
Manage this lead in Django Admin:
{request.build_absolute_uri('/admin/core/lead/')}
"""
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=from_email,
                recipient_list=[notification_email],
                fail_silently=True,
            )
            # Polite client acknowledgment
            client_subject = "We have received your inquiry · QUORV Brand Studio"
            client_body = f"""Dear {name},

Thank you for reaching out to QUORV Brand Studio.

We have received your details and are reviewing your business requirements. One of our directors will follow up with you within 24 hours.

If your inquiry is time-sensitive or you prefer direct communication, you can message us anytime directly on Instagram:
https://www.instagram.com/quorv_01?utm_source=qr&stkn=MWFrdDBjYmZvazBqdA==

Warm regards,
QUORV Brand Studio
Dedicated to the Beauty Sector Exclusively
quorv911@gmail.com
"""
            send_mail(
                subject=client_subject,
                message=client_body,
                from_email=from_email,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass

        response = JsonResponse({'status': 'success', 'message': 'Thank you. Your inquiry has been received. Quorv will reply shortly.'})
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response
    except Exception:
        response = JsonResponse({'status': 'error', 'message': 'Something went wrong. Please connect with us directly on Instagram @quorv_01.'}, status=500)
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response


@require_POST
def audit_submit(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        business_name = data.get('business_name', '').strip()
        website_or_instagram = data.get('website_or_instagram', '').strip()
        contact_name = data.get('contact_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        business_type = data.get('business_type', 'Salon').strip()
        booking_software = data.get('booking_software', 'Fresha').strip()
        primary_challenge = data.get('primary_challenge', 'Low booking conversion').strip()
        current_monthly_revenue = data.get('current_monthly_revenue', '').strip()

        if not business_name or not contact_name or not email:
            return JsonResponse({'status': 'error', 'message': 'Please provide your business name, contact name, and email.'}, status=400)

        # Calculate a realistic diagnostic health score (out of 100)
        base_score = 65
        vulnerabilities = []

        if booking_software.lower() in ('none', 'dm only', 'whatsapp only'):
            base_score -= 18
            vulnerabilities.append("Friction Point: No automated booking engine causing high drop-off during off-hours.")
        elif booking_software.lower() in ('fresha', 'vagaro', 'phorest'):
            base_score += 8
            vulnerabilities.append("Integration Gap: Generic marketplace redirect dilutes brand equity & luxury positioning.")

        if 'outdated' in primary_challenge.lower():
            base_score -= 10
            vulnerabilities.append("Brand Disconnect: Visual aesthetic fails to justify premium or high-ticket service rates.")
        if 'ranking' in primary_challenge.lower() or 'google' in primary_challenge.lower():
            base_score -= 8
            vulnerabilities.append("Visibility Leak: Incomplete local GEO schema prevents discovery in high-intent local searches.")
        if 'conversion' in primary_challenge.lower():
            base_score -= 12
            vulnerabilities.append("Mobile Conversion Friction: Multi-click client pathway resulting in booking abandonment.")

        final_score = max(38, min(89, base_score))
        vuln_text = "\n".join(vulnerabilities)

        try:
            audit = DigitalAuditSubmission.objects.create(
                business_name=business_name,
                website_or_instagram=website_or_instagram,
                contact_name=contact_name,
                email=email,
                phone=phone,
                business_type=business_type,
                booking_software=booking_software,
                primary_challenge=primary_challenge,
                current_monthly_revenue=current_monthly_revenue,
                calculated_score=final_score,
                key_vulnerabilities=vuln_text,
                status='pending'
            )
        except Exception as db_err:
            import logging
            logging.getLogger(__name__).error(f"Audit DB save error: {db_err}")

        # Log analytics
        try:
            AnalyticsEvent.objects.create(
                event_type='lead_submit',
                event_label=f"Audit Request: {business_name} ({final_score}/100)",
                page_url=request.build_absolute_uri(),
                referrer=request.META.get('HTTP_REFERER', '')[:500],
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:400]
            )
        except Exception:
            pass

        # Send instant notification to Studio Director
        try:
            notification_email = getattr(settings, 'STUDIO_NOTIFICATION_EMAIL', 'quorv911@gmail.com')
            host_user = getattr(settings, 'EMAIL_HOST_USER', '')
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or (f"QUORV Studio <{host_user}>" if host_user else 'quorv911@gmail.com')
            subject = f"[QUORV Audit Lead] {business_name} requested a Digital Audit (Score: {final_score}/100)"
            body = f"""New Digital System Audit generated:

Business: {business_name}
Contact: {contact_name}
Email: {email}
Phone/WhatsApp: {phone or 'Not provided'}
Website/IG: {website_or_instagram or 'Not provided'}
Sector: {business_type}
Booking Software: {booking_software}
Primary Challenge: {primary_challenge}

Diagnostic Score: {final_score}/100
Vulnerabilities:
{vuln_text}

---
View in Admin:
{request.build_absolute_uri('/admin/core/digitalauditsubmission/')}
"""
            send_mail(
                subject=subject,
                message=body,
                from_email=from_email,
                recipient_list=[notification_email],
                fail_silently=False
            )
        except Exception as mail_err:
            import logging
            logging.getLogger(__name__).error(f"Audit notification email error: {mail_err}")

        return JsonResponse({
            'status': 'success',
            'score': final_score,
            'vulnerabilities': vulnerabilities,
            'message': f"Diagnostic analysis complete for {business_name}."
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Unable to process audit. Please reach out directly on Instagram @quorv_01.'}, status=500)



@csrf_exempt
@require_POST
def analytics_event(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        event_type = data.get('event_type', 'outbound_link')
        event_label = data.get('event_label', '')[:255]
        page_url = data.get('page_url', '')[:500]

        if not event_label:
            response = JsonResponse({'status': 'ignored'}, status=200)
            response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
            return response

        AnalyticsEvent.objects.create(
            event_type=event_type,
            event_label=event_label,
            page_url=page_url or request.build_absolute_uri(),
            referrer=request.META.get('HTTP_REFERER', '')[:500],
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:400]
        )
        response = JsonResponse({'status': 'recorded'})
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response
    except Exception:
        response = JsonResponse({'status': 'error'}, status=400)
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response


# ===================================================================
# STUDIO OWNER DASHBOARD (Live Analytics, User Interactions & Leads)
# ===================================================================
@staff_member_required(login_url='/admin/login/?next=/dashboard/')
def studio_dashboard(request):
    total_leads = Lead.objects.count()
    new_leads = Lead.objects.filter(status='new').count()
    contacted_leads = Lead.objects.filter(status='contacted').count()
    in_discussion_leads = Lead.objects.filter(status='in_discussion').count()
    closed_leads = Lead.objects.filter(status='closed').count()

    total_instagram = AnalyticsEvent.objects.filter(event_type='instagram_click').count()
    total_whatsapp = AnalyticsEvent.objects.filter(event_type='whatsapp_click').count()
    total_emails = AnalyticsEvent.objects.filter(event_type='email_click').count()
    total_events = AnalyticsEvent.objects.count()

    today = timezone.now().date()
    events_today = AnalyticsEvent.objects.filter(created_at__date=today).count()
    leads_today = Lead.objects.filter(created_at__date=today).count()

    recent_events = AnalyticsEvent.objects.all()[:30]
    recent_leads = Lead.objects.all()[:15]

    top_ctas = (
        AnalyticsEvent.objects.filter(event_type__in=['instagram_click', 'whatsapp_click'])
        .values('event_label')
        .annotate(total=Count('id'))
        .order_by('-total')[:6]
    )

    sector_counts_raw = (
        Lead.objects.values('business_type')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    sector_map = dict(Lead.BUSINESS_TYPE_CHOICES)
    sector_counts = [
        {'name': sector_map.get(item['business_type'], item['business_type']), 'total': item['total']}
        for item in sector_counts_raw
    ]

    context = {
        'total_leads': total_leads,
        'new_leads': new_leads,
        'contacted_leads': contacted_leads,
        'in_discussion_leads': in_discussion_leads,
        'closed_leads': closed_leads,
        'total_instagram': total_instagram,
        'total_whatsapp': total_whatsapp,
        'total_emails': total_emails,
        'total_events': total_events,
        'events_today': events_today,
        'leads_today': leads_today,
        'recent_events': recent_events,
        'recent_leads': recent_leads,
        'top_ctas': top_ctas,
        'sector_counts': sector_counts,
        'user': request.user,
    }
    response = render(request, 'dashboard.html', context)
    response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
    return response


@staff_member_required(login_url='/admin/login/?next=/dashboard/')
@require_POST
def update_lead_status(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        if new_status in dict(Lead.STATUS_CHOICES):
            lead.status = new_status
            lead.save()
            response = JsonResponse({'status': 'ok', 'new_status': lead.status, 'display': lead.get_status_display()})
            response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
            return response
        response = JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response
    except Exception as e:
        response = JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response


@staff_member_required(login_url='/admin/login/?next=/dashboard/')
def export_leads_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="quorv_studio_leads.csv"'
    response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
    writer = csv.writer(response)
    writer.writerow(['Date Received', 'Name', 'Email', 'Phone', 'Business Name', 'Sector', 'Country', 'Service Interest', 'Status', 'Message'])

    for lead in Lead.objects.all().order_by('-created_at'):
        writer.writerow([
            lead.created_at.strftime('%Y-%m-%d %H:%M'),
            lead.name,
            lead.email,
            lead.phone,
            lead.business_name,
            lead.get_business_type_display(),
            lead.country,
            lead.service_interest,
            lead.get_status_display(),
            lead.message
        ])
    return response


def privacy_policy(request):
    return render(request, 'privacy.html', {'whatsapp_url': settings.QUORV_WHATSAPP_URL})


def terms_of_service(request):
    return render(request, 'terms.html', {'whatsapp_url': settings.QUORV_WHATSAPP_URL})


def robots_txt(request):
    """
    Robots.txt optimized for search crawlers and Generative Engine Optimization (GEO).
    Explicitly permits legitimate search and AI discovery crawlers:
    - Googlebot (Google search and AI search)
    - OAI-SearchBot (OpenAI SearchGPT & ChatGPT real-time web search)
    - GPTBot (OpenAI crawler)
    - PerplexityBot (Perplexity AI answer engine)
    - ClaudeBot (Anthropic Claude AI answer engine)
    - bingbot (Microsoft Bing & Copilot)
    - Applebot (Apple Siri & Apple Intelligence)
    - User-agent: * (All legitimate web crawlers)

    Ensures full crawlability for public marketing, service, industry, FAQ, and insight pages.
    Unblocks static assets (/static/) so bots can render styles, fonts, and imagery.
    Prevents crawling of administrative, studio dashboard, and mutating API endpoints.
    Directs all engines to the XML sitemap.
    """
    crawlers = [
        ("OAI-SearchBot", "OpenAI Real-Time Search & Answer Engine"),
        ("GPTBot", "OpenAI AI Training & Retrieval"),
        ("Googlebot", "Google Search & Generative AI Overviews"),
        ("PerplexityBot", "Perplexity AI Answer Engine"),
        ("ClaudeBot", "Anthropic Claude AI"),
        ("bingbot", "Microsoft Bing & Copilot Search"),
        ("Applebot", "Applebot & Apple Intelligence"),
        ("*", "General Legitimate Crawlers"),
    ]

    lines = [
        "# Quorv Robots Configuration for Search & AI Answer Engines",
        "# Website: https://quorv.org",
        "",
    ]

    for bot, description in crawlers:
        lines.append(f"# {description}")
        lines.append(f"User-agent: {bot}")
        lines.append("Allow: /")
        lines.append("Allow: /static/")
        lines.append("Disallow: /admin/")
        lines.append("Disallow: /dashboard/")
        lines.append("Disallow: /api/")
        lines.append("")

    lines.append("# Sitemaps")
    lines.append("Sitemap: https://quorv.org/sitemap.xml")

    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    """
    Dynamically generates the XML Sitemap conforming to sitemaps.org protocol 0.9.
    Includes all public marketing, service, industry, FAQ, work, process, and insight pages.
    """
    pages = [
        # (path, priority, changefreq)
        ("/", "1.0", "weekly"),
        ("/services/", "0.9", "weekly"),
        ("/industries/", "0.9", "weekly"),
        ("/insights/", "0.9", "daily"),
        ("/work/", "0.8", "weekly"),
        ("/process/", "0.8", "monthly"),
        ("/about/", "0.7", "monthly"),
        ("/contact/", "0.8", "monthly"),
        ("/privacy/", "0.3", "yearly"),
        ("/terms/", "0.3", "yearly"),
    ]

    services = Service.objects.all()
    industries = Industry.objects.all()
    insights = Insight.objects.all()

    for s in services:
        pages.append((f"/services/{s.slug}/", "0.9", "weekly"))
    for ind in industries:
        pages.append((f"/industries/{ind.slug}/", "0.9", "weekly"))
    for ins in insights:
        pages.append((f"/insights/{ins.slug}/", "0.8", "weekly"))

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, priority, freq in pages:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>https://quorv.org{path}</loc>")
        xml_lines.append(f"    <changefreq>{freq}</changefreq>")
        xml_lines.append(f"    <priority>{priority}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")

    return HttpResponse("\n".join(xml_lines), content_type="application/xml; charset=utf-8")

