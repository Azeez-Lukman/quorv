from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from .models import (
    ServiceCategory, Service, Industry, FAQ, PortfolioConcept, Lead, AnalyticsEvent, Insight, DigitalAuditSubmission
)
from django.db import connection, OperationalError
import json
import csv
import urllib.parse

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_safe_industries():
    try:
        return list(Industry.objects.all())
    except OperationalError as e:
        if 'image_url' in str(e).lower():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("ALTER TABLE core_industry ADD COLUMN image_url varchar(500) DEFAULT '';")
                return list(Industry.objects.all())
            except Exception:
                pass
        raise e


def get_safe_industry(slug):
    try:
        return get_object_or_404(Industry, slug=slug)
    except OperationalError as e:
        if 'image_url' in str(e).lower():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("ALTER TABLE core_industry ADD COLUMN image_url varchar(500) DEFAULT '';")
                return get_object_or_404(Industry, slug=slug)
            except Exception:
                pass
        raise e


def home(request):
    categories = ServiceCategory.objects.prefetch_related('services').all()
    industries = get_safe_industries()

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
    industries = get_safe_industries()
    return render(request, 'industries.html', {'industries': industries})


def industry_detail(request, slug):
    industry = get_safe_industry(slug)
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


LOCATION_HUBS = {
    'london': {
        'slug': 'london',
        'city': 'London',
        'country': 'United Kingdom',
        'country_code': 'GB',
        'region': 'Greater London',
        'geo_region': 'GB-LND',
        'lat': '51.5074',
        'lng': '-0.1278',
        'hero_title': 'Bespoke Digital Systems for Luxury Salons & Clinics in London',
        'hero_tagline': 'From Mayfair and Chelsea to Marylebone, Quorv builds bespoke websites that reflect the world-class prestige of London’s premier aesthetic and hair studios.',
        'seo_title': 'Luxury Salon & Aesthetic Clinic Web Design London · Quorv',
        'meta_description': 'Quorv builds bespoke websites, booking system integrations, and local SEO for luxury hair salons, medspas, and aesthetic clinics across London (Mayfair, Chelsea, Marylebone).',
        'currency': 'GBP (£)',
        'neighborhoods': ['Mayfair', 'Chelsea', 'Knightsbridge', 'Marylebone', 'Soho', 'Covent Garden', 'Kensington', 'Notting Hill'],
        'market_insights': 'London is one of the world’s most competitive luxury beauty markets. Discerning clientele in Mayfair and Chelsea expect flawless digital journeys that match opulent interiors. Generic templates and disjointed booking redirects immediately erode confidence for £200+ haircuts and £500+ cosmetic treatments.',
        'recommended_booking': 'Fresha, Phorest UK, Boulevard, Acuity Scheduling',
        'case_angle': 'High-ticket Mayfair salon with automated deposit capture and Chelsea aesthetic clinic consultation screening.',
    },
    'new-york': {
        'slug': 'new-york',
        'city': 'New York',
        'country': 'United States',
        'country_code': 'US',
        'region': 'New York State',
        'geo_region': 'US-NY',
        'lat': '40.7128',
        'lng': '-74.0060',
        'hero_title': 'Digital Systems for Premier Medspas & Salons in New York City',
        'hero_tagline': 'From Soho and Tribeca to the Upper East Side, Quorv builds high-converting digital architecture for NYC’s top beauty and cosmetic practices.',
        'seo_title': 'Medspa & Salon Website Design New York City · Quorv',
        'meta_description': 'Bespoke web design, Boulevard and Jane App integrations, and local search dominance for high-end aesthetic clinics, medspas, and hair salons across Manhattan and Brooklyn.',
        'currency': 'USD ($)',
        'neighborhoods': ['SoHo', 'Upper East Side', 'Tribeca', 'Flatiron', 'Meatpacking District', 'Williamsburg', 'NoHo', 'West Village'],
        'market_insights': 'New York clients demand instant mobile responsiveness, zero booking friction, and striking editorial aesthetics. Whether booking injectable treatments in Flatiron or bespoke hair extensions in SoHo, your website must establish immediate price authority before clients schedule.',
        'recommended_booking': 'Boulevard, Jane App (HIPAA compliant), Fresha, Vagaro',
        'case_angle': 'Upper East Side aesthetic dermatology clinic with seamless consultation intake and SoHo luxury studio deposit engine.',
    },
    'dubai': {
        'slug': 'dubai',
        'city': 'Dubai',
        'country': 'United Arab Emirates',
        'country_code': 'AE',
        'region': 'Emirate of Dubai',
        'geo_region': 'AE-DU',
        'lat': '25.2048',
        'lng': '55.2708',
        'hero_title': 'Luxury Digital Architecture for Aesthetic Clinics & Salons in Dubai',
        'hero_tagline': 'In the luxury capital of the Middle East—from Downtown and DIFC to Jumeirah and Palm Jumeirah—Quorv elevates the digital prestige of premier beauty practices.',
        'seo_title': 'Luxury Aesthetic Clinic & Salon Web Design Dubai · Quorv',
        'meta_description': 'Quorv builds ultra-luxury websites, booking workflows, and VIP consultation engines for high-end beauty salons, aesthetic clinics, and medspas across Dubai (DIFC, Jumeirah, Downtown).',
        'currency': 'AED (د.إ)',
        'neighborhoods': ['DIFC', 'Downtown Dubai', 'Jumeirah', 'Palm Jumeirah', 'Dubai Marina', 'Business Bay', 'City Walk', 'Al Wasl'],
        'market_insights': 'Dubai beauty consumers demand ultra-high luxury aesthetics, bilingual sophistication, and VIP concierge intake workflows. With world-class aesthetic clinics concentrated across Jumeirah and Downtown, an exceptional digital presence is the foundation of high-ticket client acquisition.',
        'recommended_booking': 'Phorest, Fresha, Custom VIP WhatsApp Intake & Deposit Gateways',
        'case_angle': 'DIFC executive clinic with private consultation booking and Jumeirah bespoke beauty lounge appointment flow.',
    },
    'los-angeles': {
        'slug': 'los-angeles',
        'city': 'Los Angeles',
        'country': 'United States',
        'country_code': 'US',
        'region': 'California',
        'geo_region': 'US-CA',
        'lat': '34.0522',
        'lng': '-118.2437',
        'hero_title': 'Editorial Web Design for Medspas & Stylists in Los Angeles',
        'hero_tagline': 'From Beverly Hills and West Hollywood to Santa Monica, Quorv creates bespoke digital systems for LA’s most discerning cosmetic and beauty specialists.',
        'seo_title': 'Beverly Hills & Los Angeles Salon & Medspa Web Design · Quorv',
        'meta_description': 'Quorv designs bespoke websites, booking integrations, and SEO systems for celebrity stylists, luxury medspas, and aesthetic doctors in Beverly Hills, West Hollywood, and LA.',
        'currency': 'USD ($)',
        'neighborhoods': ['Beverly Hills', 'West Hollywood', 'Santa Monica', 'Brentwood', 'Silver Lake', 'Melrose', 'Studio City', 'Century City'],
        'market_insights': 'In Los Angeles, aesthetic credibility is visual and immediate. Clients booking in Beverly Hills or West Hollywood expect cinematic treatment presentation, celebrity-grade confidentiality, and effortless scheduling on mobile.',
        'recommended_booking': 'Boulevard, Jane App, Fresha, Vagaro',
        'case_angle': 'Beverly Hills dermal practice with pre-consultation medical workflows and West Hollywood studio booking integration.',
    }
}


def locations_index(request):
    """
    Renders overview directory of Quorv's key international luxury beauty hubs.
    """
    return render(request, 'locations.html', {
        'locations': list(LOCATION_HUBS.values()),
        'whatsapp_url': "https://wa.me/447352789073?text=Hi%20Quorv%2C%20I%27d%20like%20to%20discuss%20a%20project%20for%20my%20beauty%20business.",
    })


def location_detail(request, city_slug):
    """
    Renders dedicated localized landing page for a target city.
    Provides local business schema, neighborhood targeting, and booking integration guidance.
    """
    from django.http import Http404
    loc = LOCATION_HUBS.get(city_slug.lower())
    if not loc:
        raise Http404(f"Location '{city_slug}' not found.")
    
    industries = get_safe_industries()
    services = Service.objects.all()[:6]
    other_locations = [l for slug, l in LOCATION_HUBS.items() if slug != city_slug.lower()]

    return render(request, 'location_detail.html', {
        'loc': loc,
        'industries': industries,
        'services': services,
        'other_locations': other_locations,
        'whatsapp_url': f"https://wa.me/447352789073?text=Hi%20Quorv%2C%20I%27m%20interested%20in%20elevating%20my%20beauty%20business%20in%20{loc['city']}.",
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

        booking_lower = booking_software.lower()
        if any(term in booking_lower for term in ('none', 'dm only', 'whatsapp only')):
            base_score -= 18
            vulnerabilities.append("Friction Point: Lack of automated booking infrastructure causes high client abandonment during evening & weekend hours.")
        elif any(term in booking_lower for term in ('fresha', 'vagaro', 'phorest')):
            base_score += 8
            vulnerabilities.append("Integration Gap: Generic marketplace redirect dilutes client perception and exposes your clientele to nearby competitors.")

        challenge_lower = primary_challenge.lower()
        if 'outdated' in challenge_lower or 'design' in challenge_lower:
            base_score -= 10
            vulnerabilities.append("Brand Disconnect: Current visual aesthetic does not justify high-ticket or premium service price points.")
        if 'ranking' in challenge_lower or 'google' in challenge_lower or 'search' in challenge_lower:
            base_score -= 8
            vulnerabilities.append("Visibility Leak: Incomplete local GEO schema prevents client discovery in high-intent local searches.")
        if 'conversion' in challenge_lower or 'drop-off' in challenge_lower or 'drop' in challenge_lower:
            base_score -= 12
            vulnerabilities.append("Mobile Pathway Friction: Multi-step booking pathway causing client fatigue and booking abandonment.")

        if not vulnerabilities:
            vulnerabilities.append("Optimization Opportunity: Service architecture and booking touchpoints require bespoke luxury positioning.")

        final_score = max(38, min(89, base_score))
        vuln_text = "\n".join(f"• {v}" for v in vulnerabilities)
        submission_time_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        client_ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')[:300]
        referrer = request.META.get('HTTP_REFERER', 'Direct')[:400]

        # 1. Save Digital Audit Submission
        audit = None
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

        # 2. Mirror into Lead Pipeline (so it shows in operator dashboard)
        lead_biz_type = 'salon'
        btype_lower = business_type.lower()
        if 'aesthetic' in btype_lower or 'medspa' in btype_lower or 'clinic' in btype_lower:
            lead_biz_type = 'aesthetic'
        elif 'hair' in btype_lower:
            lead_biz_type = 'salon'
        elif 'nail' in btype_lower or 'lash' in btype_lower:
            lead_biz_type = 'nail_lash'
        elif 'barber' in btype_lower:
            lead_biz_type = 'barber'
        elif 'spa' in btype_lower or 'wellness' in btype_lower:
            lead_biz_type = 'spa_wellness'
        elif 'brand' in btype_lower:
            lead_biz_type = 'beauty_brand'
        else:
            lead_biz_type = 'other'

        try:
            Lead.objects.create(
                name=contact_name,
                email=email,
                phone=phone or '',
                business_name=business_name,
                business_type=lead_biz_type,
                country='',
                service_interest=f"Digital Audit Health Score ({final_score}/100)",
                message=(
                    f"FREE DIGITAL AUDIT REPORT\n"
                    f"Score: {final_score}/100\n"
                    f"Sector: {business_type}\n"
                    f"Website/IG: {website_or_instagram or 'Not provided'}\n"
                    f"Booking System: {booking_software}\n"
                    f"Primary Challenge: {primary_challenge}\n"
                    f"Revenue: {current_monthly_revenue or 'Not provided'}\n\n"
                    f"Identified Friction Points:\n{vuln_text}"
                ),
                source="Digital Audit Engine",
                status='new'
            )
        except Exception as lead_err:
            import logging
            logging.getLogger(__name__).error(f"Audit Lead mirror error: {lead_err}")

        # 3. Log Analytics Event
        try:
            AnalyticsEvent.objects.create(
                event_type='lead_submit',
                event_label=f"Audit Request: {business_name} ({final_score}/100)",
                page_url=request.build_absolute_uri(),
                referrer=referrer,
                ip_address=client_ip,
                user_agent=user_agent
            )
        except Exception:
            pass

        # 4. Prepare Formatted Message for Instagram Direct Message
        dm_message = (
            f"Hi Quorv, I just completed a digital audit on quorv.org for {business_name}.\n\n"
            f"Health Score: {final_score}/100\n"
            f"Primary Challenge: {primary_challenge}\n\n"
            f"Friction points noted:\n"
            f"{vuln_text}\n\n"
            f"I would like to discuss fixing these issues and upgrading our digital setup."
        )

        dm_url = "https://ig.me/m/quorv_01"
        wa_url = f"https://wa.me/447352789073?text={urllib.parse.quote(dm_message)}"

        admin_audit_url = request.build_absolute_uri(reverse('admin:core_digitalauditsubmission_changelist'))
        dashboard_url = request.build_absolute_uri('/dashboard/')

        # 5. Send High-Priority Studio Notification Email with ALL submitted details
        try:
            notification_email = getattr(settings, 'STUDIO_NOTIFICATION_EMAIL', 'quorv911@gmail.com')
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'QUORV Brand Studio <quorv911@gmail.com>'
            subject = f"[🚨 NEW AUDIT LEAD] {business_name} - Score {final_score}/100 ({business_type})"

            plain_body = f"""==================================================
NEW DIGITAL AUDIT SUBMISSION — QUORV BRAND STUDIO
==================================================

HEALTH INDEX SCORE: {final_score} / 100
SUBMISSION TIME:    {submission_time_str}

--------------------------------------------------
CLIENT & BUSINESS PROFILE:
--------------------------------------------------
• Business / Clinic Name: {business_name}
• Contact Person:         {contact_name}
• Work Email:             {email}
• Phone / WhatsApp:       {phone or 'Not provided'}
• Website / Instagram:    {website_or_instagram or 'Not provided'}
• Sector Specialization:  {business_type}
• Current Booking Engine: {booking_software}
• Primary Challenge:      {primary_challenge}
• Monthly Revenue:        {current_monthly_revenue or 'Not specified'}

--------------------------------------------------
IDENTIFIED SYSTEM FRICTION POINTS:
--------------------------------------------------
{vuln_text}

--------------------------------------------------
DIAGNOSTIC METADATA:
--------------------------------------------------
• IP Address: {client_ip}
• Referrer:   {referrer}
• User Agent: {user_agent}

--------------------------------------------------
DIRECT OPERATOR ACTIONS:
--------------------------------------------------
• Message on Instagram DM:  {dm_url}
• Reply via Email:          mailto:{email}?subject=Your%20QUORV%20Digital%20Audit%20Results
• Django Admin (Audits):    {admin_audit_url}
• Studio Operator Pipeline: {dashboard_url}

==================================================
QUORV Brand Studio · Automated Intelligence System
"""

            vuln_html_items = "".join(f"<li style='margin-bottom:8px;color:#FAF8F5;'>{v}</li>" for v in vulnerabilities)
            score_color = "#ef4444" if final_score < 55 else ("#eab308" if final_score < 75 else "#22c55e")
            phone_clean = phone.replace(' ', '').replace('+', '').replace('-', '') if phone else ''

            html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>New Digital Audit Lead</title>
</head>
<body style="margin:0;padding:24px;background-color:#08090C;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#FAF8F5;">
  <div style="max-width:620px;margin:0 auto;background-color:#0E1015;border:1px solid #E4C388;border-radius:12px;padding:32px;box-shadow:0 20px 40px rgba(0,0,0,0.6);">
    
    <!-- Header -->
    <div style="border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:18px;margin-bottom:24px;">
      <span style="font-size:10px;text-transform:uppercase;letter-spacing:0.25em;color:#E4C388;font-weight:600;display:block;margin-bottom:6px;">Quorv Brand Studio · Lead Intelligence</span>
      <h1 style="margin:0;font-size:22px;color:#FAF8F5;font-weight:700;">New Digital System Audit</h1>
      <p style="margin:6px 0 0;font-size:12px;color:#8C8F9F;">Submitted on {submission_time_str}</p>
    </div>

    <!-- Health Score Pill -->
    <div style="background-color:#141620;border:1px solid rgba(228,195,136,0.3);border-radius:10px;padding:20px;text-align:center;margin-bottom:28px;">
      <span style="font-size:11px;text-transform:uppercase;letter-spacing:0.18em;color:#8C8F9F;display:block;">Digital Health Index</span>
      <div style="font-size:48px;font-weight:800;color:{score_color};line-height:1.1;margin:6px 0;">
        {final_score} <span style="font-size:18px;color:#8C8F9F;font-weight:400;">/ 100</span>
      </div>
      <span style="display:inline-block;padding:3px 12px;background-color:rgba(255,255,255,0.05);border-radius:20px;font-size:11px;color:#FAF8F5;font-weight:600;">
        {business_name} ({business_type})
      </span>
    </div>

    <!-- Submitted Details Table -->
    <h2 style="font-size:13px;text-transform:uppercase;letter-spacing:0.15em;color:#E4C388;margin:0 0 14px;border-bottom:1px solid rgba(228,195,136,0.2);padding-bottom:6px;">
      All Submitted Lead Details
    </h2>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:28px;">
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;width:40%;font-weight:500;">Business / Clinic:</td>
        <td style="padding:10px 6px;color:#FAF8F5;font-weight:700;">{business_name}</td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;font-weight:500;">Contact Person:</td>
        <td style="padding:10px 6px;color:#FAF8F5;font-weight:600;">{contact_name}</td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;font-weight:500;">Work Email:</td>
        <td style="padding:10px 6px;"><a href="mailto:{email}" style="color:#E4C388;text-decoration:none;font-weight:600;">{email}</a></td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;font-weight:500;">Phone Number:</td>
        <td style="padding:10px 6px;color:#FAF8F5;">{f'<a href="tel:{phone}" style="color:#22c55e;text-decoration:none;">{phone}</a>' if phone else '<span style="color:#8C8F9F;">Not provided</span>'}</td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;font-weight:500;">Website / Instagram:</td>
        <td style="padding:10px 6px;color:#FAF8F5;">{website_or_instagram or '<span style="color:#8C8F9F;">Not provided</span>'}</td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;font-weight:500;">Sector Specialization:</td>
        <td style="padding:10px 6px;color:#FAF8F5;">{business_type}</td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;font-weight:500;">Current Booking Engine:</td>
        <td style="padding:10px 6px;color:#FAF8F5;">{booking_software}</td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;font-weight:500;">Primary Challenge:</td>
        <td style="padding:10px 6px;color:#FAF8F5;">{primary_challenge}</td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;font-weight:500;">Monthly Revenue:</td>
        <td style="padding:10px 6px;color:#FAF8F5;">{current_monthly_revenue or '<span style="color:#8C8F9F;">Not specified</span>'}</td>
      </tr>
      <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
        <td style="padding:10px 6px;color:#8C8F9F;font-weight:500;">Visitor IP / Origin:</td>
        <td style="padding:10px 6px;color:#8C8F9F;font-size:11px;">{client_ip}</td>
      </tr>
    </table>

    <!-- Vulnerabilities Section -->
    <h2 style="font-size:13px;text-transform:uppercase;letter-spacing:0.15em;color:#E4C388;margin:0 0 12px;border-bottom:1px solid rgba(228,195,136,0.2);padding-bottom:6px;">
      Identified Friction Points
    </h2>
    <div style="background-color:#141620;border-left:3px solid #E4C388;padding:14px 18px;border-radius:6px;margin-bottom:28px;">
      <ul style="margin:0;padding-left:18px;font-size:13px;line-height:1.6;">
        {vuln_html_items}
      </ul>
    </div>

    <!-- Quick Operator Action Buttons -->
    <div style="text-align:center;padding-top:10px;border-top:1px solid rgba(255,255,255,0.08);">
      <p style="font-size:11px;color:#8C8F9F;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:14px;">Instant Actions</p>
      <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;">
        <a href="{dm_url}" target="_blank" style="display:inline-block;background-color:#E1306C;color:#fff;text-decoration:none;padding:10px 18px;border-radius:6px;font-size:12px;font-weight:700;margin:4px;">
          📸 Open IG Direct Message
        </a>
        <a href="mailto:{email}?subject=Your%20QUORV%20Digital%20Audit%20Report" style="display:inline-block;background-color:#E4C388;color:#08090C;text-decoration:none;padding:10px 18px;border-radius:6px;font-size:12px;font-weight:700;margin:4px;">
          ✉️ Reply via Email
        </a>
        <a href="{admin_audit_url}" target="_blank" style="display:inline-block;background-color:#1A1D27;border:1px solid rgba(255,255,255,0.15);color:#FAF8F5;text-decoration:none;padding:10px 18px;border-radius:6px;font-size:12px;margin:4px;">
          ⚙️ Open Django Admin
        </a>
      </div>
    </div>

  </div>
</body>
</html>"""

            msg = EmailMultiAlternatives(
                subject=subject,
                body=plain_body,
                from_email=from_email,
                to=[notification_email]
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send(fail_silently=False)
        except Exception as mail_err:
            import logging
            logging.getLogger(__name__).error(f"Audit notification email error: {mail_err}")

        # 6. Send Client Diagnostic Receipt Email with Instagram DM Link
        try:
            client_subject = f"Your Digital System Audit Results · QUORV Brand Studio ({final_score}/100)"
            client_body = f"""Dear {contact_name},

Thank you for requesting a Digital System Audit for {business_name}.

Your diagnostic health index score has been calculated at {final_score}/100.

Key Findings & Friction Points:
{vuln_text}

To discuss repairing these booking and brand leakages with a Quorv director, you can direct message us immediately on Instagram:
{dm_url}

Warm regards,
QUORV Brand Studio
Dedicated Exclusively to High-Ticket Beauty & Aesthetics
https://quorv.org
quorv911@gmail.com
"""
            send_mail(
                subject=client_subject,
                message=client_body,
                from_email=from_email,
                recipient_list=[email],
                fail_silently=True
            )
        except Exception:
            pass

        return JsonResponse({
            'status': 'success',
            'score': final_score,
            'vulnerabilities': vulnerabilities,
            'business_name': business_name,
            'contact_name': contact_name,
            'dm_url': dm_url,
            'wa_url': wa_url,
            'dm_message': dm_message,
            'message': f"Diagnostic analysis complete for {business_name}."
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Unable to process audit. Please reach out directly on Instagram DM @quorv_01.'}, status=500)




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

    total_audits = DigitalAuditSubmission.objects.count()
    recent_audits = DigitalAuditSubmission.objects.all()[:10]

    context = {
        'total_leads': total_leads,
        'new_leads': new_leads,
        'contacted_leads': contacted_leads,
        'in_discussion_leads': in_discussion_leads,
        'closed_leads': closed_leads,
        'total_audits': total_audits,
        'recent_audits': recent_audits,
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

    lines.append("# Sitemaps & LLMs Discovery")
    lines.append("Sitemap: https://quorv.org/sitemap.xml")
    lines.append("# AI Engine Documentation (LLMs Standard): https://quorv.org/llms.txt")

    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def llms_txt(request):
    """
    Standard /llms.txt specification endpoint for AI search & answer engines
    (OpenAI ChatGPT Search, Perplexity AI, Claude, Google Gemini, Copilot).
    Provides structured, markdown-formatted entity facts, service modules, and canonical links.
    """
    services = Service.objects.select_related('category').all()
    industries = get_safe_industries()

    doc = [
        "# Quorv",
        "",
        "> Quorv is a specialized brand and digital systems studio dedicated exclusively to premium beauty businesses, aesthetic clinics, luxury salons, and medspas internationally.",
        "",
        "Quorv bridges the disconnect between physical luxury salon/clinic environments and high-converting digital ecosystems. We build bespoke editorial websites, implement frictionless booking platform integrations (Fresha, Phorest, Boulevard, Vagaro, Jane App, Acuity), execute local SEO dominance across major international luxury beauty hubs, and elevate client retention.",
        "",
        "## Key Studio Facts",
        "- **Specialization**: Exclusively premium beauty, hair studios, aesthetic medicine, medspas, and wellness.",
        "- **Headquarters & Service Hubs**: Operating internationally across London (UK), New York (US), Los Angeles (US), Dubai (UAE), Toronto (Canada), and Sydney (Australia).",
        "- **Primary Contact**: Instagram Direct [@quorv_01](https://www.instagram.com/quorv_01) | Email: quorv911@gmail.com | Phone/WhatsApp: +44 7352 789073",
        "- **Website**: https://quorv.org",
        "",
        "## The 3-Pillar Digital System",
        "1. **Look Premium**: Bespoke editorial visual architecture, dark luxury aesthetic, responsive mobile typography, elevated imagery presentation, and distinct brand positioning that justifies premium price points.",
        "2. **Get Discovered**: High-intent search engine optimization (SEO) and generative engine optimization (GEO) targeting clients actively searching for high-end beauty services in specific cities.",
        "3. **Get Booked**: Frictionless booking engine integrations and consultation inquiry workflows that eliminate WhatsApp/DM back-and-forth and capture upfront deposits.",
        "",
        "## Supported Booking Engine & Practice Management Integrations",
        "- **Fresha**: Custom website embeds, stylized booking buttons, and seamless deep-links preserving brand prestige.",
        "- **Phorest Salon Software**: Enterprise integration for multi-chair salons, automated client retention, and salon branches.",
        "- **Boulevard**: Precision booking flows and modern point-of-sale integration for luxury salons and spas.",
        "- **Vagaro**: Intuitive appointment and package booking flows for boutique salons and independent stylists.",
        "- **Jane App**: HIPAA/GDPR-compliant chart and appointment workflows for aesthetic medical clinics and dermal doctors.",
        "- **Acuity Scheduling**: Flexible automated booking and pre-payment workflows.",
        "",
        "## Sector Specializations",
    ]

    for ind in industries:
        doc.append(f"- **{ind.title}**: {ind.subtitle} [Read Overview](https://quorv.org/industries/{ind.slug}/)")

    doc.extend([
        "",
        "## Core Services",
    ])

    for s in services:
        doc.append(f"- **{s.title}** ({s.category.name}): {s.outcome} [Details](https://quorv.org/services/{s.slug}/)")

    doc.extend([
        "",
        "## Canonical Resources & Documentation",
        "- [Home](https://quorv.org/): Studio overview, portfolio concepts, and digital audit tool.",
        "- [Services Directory](https://quorv.org/services/): Full suite of brand and digital services.",
        "- [Industries Directory](https://quorv.org/industries/): Dedicated industry blueprints.",
        "- [The 5-Stage Process](https://quorv.org/process/): How Quorv executes from audit to launch.",
        "- [Studio Insights](https://quorv.org/insights/): Case studies, conversion teardowns, and salon growth frameworks.",
        "- [About Quorv](https://quorv.org/about/): Studio manifesto and philosophy.",
        "- [Start a Dialogue](https://quorv.org/contact/): Consultation request and contact points.",
        "- [International Location Hubs](https://quorv.org/locations/): London, New York, Dubai, Los Angeles.",
        "",
        "## Key International City Hubs",
    ])

    for c_slug, c_info in LOCATION_HUBS.items():
        doc.append(f"- **{c_info['city']} ({c_info['country']})**: {c_info['hero_tagline']} [City Hub](https://quorv.org/locations/{c_slug}/)")

    doc.extend([
        "",
        "## Full Machine-Readable Knowledge Base",
        "- [Full LLM Context (llms-full.txt)](https://quorv.org/llms-full.txt): Comprehensive deep-dive documentation.",
    ])

    return HttpResponse("\n".join(doc), content_type="text/plain; charset=utf-8")


def llms_full_txt(request):
    """
    Extended /llms-full.txt documentation providing full depth on methodology,
    FAQ, technical specifications, and client criteria for AI answer synthesis.
    """
    services = Service.objects.select_related('category').all()
    industries = get_safe_industries()
    faqs = FAQ.objects.all()
    insights = Insight.objects.all()

    full_doc = [
        "# Quorv · Comprehensive Digital Studio Knowledge Base",
        "",
        "## About Quorv",
        "Quorv (https://quorv.org) is a premier brand studio and digital architecture consultancy operating internationally. Quorv operates exclusively within the beauty, aesthetic medicine, and luxury wellness sectors. The studio addresses the prevalent industry disconnect where businesses with world-class physical salons or clinical premises have dated, generic, or fragmented websites that fail to convert high-ticket clients.",
        "",
        "## The 5-Stage Studio Process",
        "1. **Stage 1: Discovery & Digital Audit**: Comprehensive audit of current conversion leaks, local search footprint, booking drop-off points, and competitor positioning.",
        "2. **Stage 2: Visual & Brand Blueprint**: Bespoke editorial design direction, luxury dark palette, typography pairing (Italiana serif + Plus Jakarta Sans + Space Grotesk mono), and asset curation.",
        "3. **Stage 3: Technical Architecture**: Clean, semantic, high-speed engineering with responsive mobile layouts, SEO meta frameworks, and micro-interactions.",
        "4. **Stage 4: Booking & Workflow Integration**: Direct connection with Fresha, Phorest, Boulevard, Vagaro, or Jane App. Deposit capture, consultation pre-screening forms, and automated confirmation flows.",
        "5. **Stage 5: Launch & Local Search Activation**: Search console submission, XML sitemap indexing, local business schema deployment, and Google My Business synchronization.",
        "",
        "## Detailed Service Breakdown",
    ]

    for s in services:
        full_doc.extend([
            f"### {s.title} (Category: {s.category.name})",
            f"**Outcome**: {s.outcome}",
            f"**Overview**: {s.full_description or s.outcome}",
            f"**URL**: https://quorv.org/services/{s.slug}/",
            "",
        ])

    full_doc.extend([
        "## Industry Blueprints & Solutions",
    ])

    for ind in industries:
        full_doc.extend([
            f"### {ind.title}",
            f"**Focus**: {ind.key_focus}",
            f"**Subtitle**: {ind.subtitle}",
            f"**Challenge**: {ind.the_challenge}",
            f"**Quorv Solution**: {ind.the_solution}",
            f"**URL**: https://quorv.org/industries/{ind.slug}/",
            "",
        ])

    full_doc.extend([
        "## Studio Insights & Publications",
    ])

    for ins in insights:
        full_doc.extend([
            f"- **{ins.title}** ({ins.category} · {ins.read_time}): {ins.summary} [Read Article](https://quorv.org/insights/{ins.slug}/)",
        ])

    full_doc.extend([
        "",
        "## Frequently Asked Questions",
    ])

    for faq in faqs:
        full_doc.extend([
            f"### Q: {faq.question}",
            f"**A**: {faq.answer}",
            "",
        ])

    full_doc.extend([
        "## Contact & Working With Quorv",
        "- **Instagram**: Direct message [@quorv_01](https://www.instagram.com/quorv_01)",
        "- **Email**: quorv911@gmail.com",
        "- **Phone/WhatsApp**: +44 7352 789073",
        "- **Website Inquiry Form**: https://quorv.org/contact/",
        "- **Audit Engine**: https://quorv.org/#audit",
        "- **Geographic Footprint**: United Kingdom, United States, Canada, United Arab Emirates, Australia.",
    ])

    return HttpResponse("\n".join(full_doc), content_type="text/plain; charset=utf-8")



def sitemap_xml(request):
    """
    Dynamically generates the XML Sitemap conforming to sitemaps.org protocol 0.9.
    Includes all public marketing, service, industry, FAQ, work, process, and insight pages
    with RFC 3339 lastmod timestamps for accelerated search indexing.
    """
    today_str = timezone.now().strftime('%Y-%m-%d')
    pages = [
        # (path, priority, changefreq, lastmod)
        ("/", "1.0", "weekly", today_str),
        ("/services/", "0.9", "weekly", today_str),
        ("/industries/", "0.9", "weekly", today_str),
        ("/insights/", "0.9", "daily", today_str),
        ("/work/", "0.8", "weekly", today_str),
        ("/process/", "0.8", "monthly", today_str),
        ("/about/", "0.7", "monthly", today_str),
        ("/contact/", "0.8", "monthly", today_str),
        ("/privacy/", "0.3", "yearly", today_str),
        ("/terms/", "0.3", "yearly", today_str),
    ]

    services = Service.objects.all()
    industries = Industry.objects.all()
    insights = Insight.objects.all()

    for s in services:
        pages.append((f"/services/{s.slug}/", "0.9", "weekly", today_str))
    for ind in industries:
        pages.append((f"/industries/{ind.slug}/", "0.9", "weekly", today_str))
    for ins in insights:
        ins_date = ins.published_date.strftime('%Y-%m-%d') if ins.published_date else today_str
        pages.append((f"/insights/{ins.slug}/", "0.8", "weekly", ins_date))

    pages.append(("/locations/", "0.8", "weekly", today_str))
    for c_slug in LOCATION_HUBS:
        pages.append((f"/locations/{c_slug}/", "0.9", "weekly", today_str))

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, priority, freq, lastmod in pages:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>https://quorv.org{path}</loc>")
        xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_lines.append(f"    <changefreq>{freq}</changefreq>")
        xml_lines.append(f"    <priority>{priority}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")

    return HttpResponse("\n".join(xml_lines), content_type="application/xml; charset=utf-8")


def custom_404_view(request, exception=None):
    """
    Renders custom branded luxury 404 error page.
    """
    return render(request, '404.html', status=404)


def custom_500_view(request):
    """
    Renders custom branded luxury 500 server error page.
    """
    return render(request, '500.html', status=500)


