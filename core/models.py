from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class ServiceCategory(models.Model):
    name = models.CharField(max_length=60, help_text="e.g. Brand, Digital, Content, Growth")
    code = models.CharField(max_length=10, help_text="e.g. 01, 02, 03, 04")
    outcome_statement = models.CharField(max_length=255, help_text="e.g. Make your business recognizable before someone walks through the door.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'code']
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return f"CATEGORY {self.code}: {self.name}"


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, related_name='services', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    tagline = models.CharField(max_length=220, blank=True)
    outcome = models.TextField(help_text="Concrete business outcome for a beauty business")
    full_description = models.TextField(blank=True)
    deliverables = models.TextField(help_text="Comma-separated or newline-separated deliverables")
    whatsapp_prompt = models.CharField(
        max_length=255,
        default="Hi Quorv, I'm interested in discussing this service for my beauty business.",
        help_text="Prefilled message for WhatsApp CTA"
    )
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category__order', 'order']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_deliverables_list(self):
        if not self.deliverables:
            return []
        return [item.strip() for item in self.deliverables.replace('\r\n', '\n').split('\n') if item.strip()]

    def __str__(self):
        return f"{self.title} ({self.category.name})"


class Industry(models.Model):
    title = models.CharField(max_length=100, help_text="e.g. Salons, Aesthetic Clinics, Hairstylists")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    subtitle = models.CharField(max_length=255)
    the_challenge = models.TextField(help_text="Common digital mismatch for this beauty sector")
    the_solution = models.TextField(help_text="How Quorv connects branding, web, and booking")
    key_focus = models.CharField(max_length=200, help_text="e.g. Visual distinction, local search, frictionless booking")
    image_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Sector showcase image URL or static path"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Industry Specialization"
        verbose_name_plural = "Industry Specializations"

    @property
    def get_image_url(self):
        if self.image_url and self.image_url.strip():
            return self.image_url
        defaults = {
            'salons': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=1200&q=80',
            'aesthetic-clinics': 'https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80',
            'hairstylists': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=1200&q=80',
            'nail-lash-studios': 'https://images.unsplash.com/photo-1632345031435-8727f6897d53?auto=format&fit=crop&w=1200&q=80',
            'spas': 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80',
            'beauty-professionals': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=1200&q=80',
        }
        return defaults.get(self.slug, 'https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=1200&q=80')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PortfolioConcept(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    client_type = models.CharField(max_length=100, help_text="e.g. Aesthetic Clinic Concept / Hair Studio System")
    category = models.CharField(max_length=80, default="Brand & Digital System")
    concept_summary = models.TextField()
    deliverables = models.CharField(max_length=255, help_text="e.g. Visual Identity, Web Architecture, Booking Experience")
    image_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Image URL or static path (e.g. /static/... or https://...)"
    )
    is_concept = models.BooleanField(
        default=True,
        help_text="Clearly distinguishes design concepts from client work until case studies exist."
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Portfolio Concept"
        verbose_name_plural = "Portfolio Concepts"

    @property
    def display_image_url(self):
        if not self.image_url or "photo-1512290900672" in str(self.image_url):
            return "/static/images/elan-dermatology.jpg"
        return self.image_url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.image_url and "photo-1512290900672" in str(self.image_url):
            self.image_url = "/static/images/elan-dermatology.jpg"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} [CONCEPT]" if self.is_concept else self.title


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General & Positioning'),
        ('services', 'Services & Deliverables'),
        ('process', 'Process & Timelines'),
        ('pricing', 'Pricing & Engagements'),
    ]
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='general')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New Inquiry'),
        ('contacted', 'Contacted via WhatsApp/Email'),
        ('in_discussion', 'In Discussion / Scoping'),
        ('closed', 'Closed'),
    ]

    BUSINESS_TYPE_CHOICES = [
        ('salon', 'Hair / Beauty Salon'),
        ('aesthetic_clinic', 'Aesthetic Clinic / Medspa'),
        ('hairstylist', 'Independent Hairstylist / Colorist'),
        ('barber', 'Luxury Barbershop'),
        ('nail_lash', 'Nail / Lash Studio'),
        ('spa_wellness', 'Spa & Wellness Sanctuary'),
        ('beauty_brand', 'Independent Beauty Brand'),
        ('other', 'Other Beauty Professional'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    business_name = models.CharField(max_length=140, blank=True)
    business_type = models.CharField(max_length=40, choices=BUSINESS_TYPE_CHOICES, default='salon')
    country = models.CharField(max_length=80, blank=True, help_text="e.g. UK, USA, UAE, Canada, Australia")
    service_interest = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    source = models.CharField(max_length=80, default="Website Form")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Inquiry Lead"
        verbose_name_plural = "Inquiry Leads"

    def __str__(self):
        return f"{self.name} - {self.business_name or 'Independent'} ({self.get_status_display()})"


class AnalyticsEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('instagram_click', 'Instagram DM CTA Click'),
        ('whatsapp_click', 'WhatsApp CTA Click'),
        ('email_click', 'Email CTA Click'),
        ('lead_submit', 'Lead Form Submission'),
        ('service_view', 'Service Page View'),
        ('concept_view', 'Concept View'),
        ('outbound_link', 'Outbound Link Click'),
    ]

    event_type = models.CharField(max_length=40, choices=EVENT_TYPE_CHOICES)
    event_label = models.CharField(max_length=255, help_text="e.g. Hero WhatsApp CTA, Category 02 Digital")
    page_url = models.CharField(max_length=500, blank=True)
    referrer = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Conversion Analytics Event"
        verbose_name_plural = "Conversion Analytics Events"

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.event_label} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class Insight(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    subtitle = models.CharField(max_length=300)
    category = models.CharField(max_length=100, help_text="e.g. Salon Website Architecture, Med Spa Systems, Booking Integration")
    read_time = models.CharField(max_length=30, default="5 min read")
    summary = models.TextField(help_text="Concise executive summary for AI search and quick human scanning")
    content = models.TextField(help_text="Full markdown or HTML content")
    published_date = models.DateField(default=timezone.now)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-published_date']
        verbose_name = "Studio Insight"
        verbose_name_plural = "Studio Insights"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class DigitalAuditSubmission(models.Model):
    AUDIT_STATUS_CHOICES = [
        ('pending', 'Audit Pending Review'),
        ('analyzed', 'Score Generated / Sent'),
        ('booked_consult', 'Booked Consultation'),
        ('closed', 'Closed'),
    ]

    business_name = models.CharField(max_length=150)
    website_or_instagram = models.CharField(max_length=200, help_text="Current website URL or @handle")
    contact_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    business_type = models.CharField(max_length=80, help_text="e.g. Aesthetic Clinic, Salon, Medspa")
    booking_software = models.CharField(max_length=80, help_text="e.g. Fresha, Phorest, Vagaro, Boulevard, None")
    primary_challenge = models.CharField(max_length=150, help_text="e.g. Look outdated, low booking conversion, poor Google ranking")
    current_monthly_revenue = models.CharField(max_length=80, blank=True)
    calculated_score = models.IntegerField(default=68, help_text="Calculated health score out of 100")
    key_vulnerabilities = models.TextField(blank=True, help_text="Identified leakages e.g. Booking friction, mobile bounce")
    status = models.CharField(max_length=30, choices=AUDIT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Digital Audit Submission"
        verbose_name_plural = "Digital Audit Submissions"

    def __str__(self):
        return f"{self.business_name} (Score: {self.calculated_score}/100) - {self.get_status_display()}"

