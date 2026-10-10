from django.conf import settings

def studio_settings(request):
    return {
        'instagram_url': getattr(settings, 'QUORV_INSTAGRAM_URL', 'https://www.instagram.com/quorv_01?utm_source=qr&stkn=MWFrdDBjYmZvazBqdA=='),
        'instagram_dm_url': getattr(settings, 'QUORV_INSTAGRAM_DM_URL', 'https://ig.me/m/quorv_01'),
        'whatsapp_url': getattr(settings, 'QUORV_WHATSAPP_URL', 'https://wa.me/447352789073?text=Hi%20Quorv%2C%20I%27m%20interested%20in%20improving%20the%20digital%20presence%20of%20my%20beauty%20business.'),
        'whatsapp_number': getattr(settings, 'QUORV_WHATSAPP_NUMBER', '+447352789073'),
        'business_email': getattr(settings, 'STUDIO_NOTIFICATION_EMAIL', 'quorv911@gmail.com'),
    }
