import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import ServiceCategory, Service, Industry, FAQ, PortfolioConcept

def seed_data():
    print("Clearing and seeding Quorv database...")
    ServiceCategory.objects.all().delete()
    Service.objects.all().delete()
    Industry.objects.all().delete()
    FAQ.objects.all().delete()
    PortfolioConcept.objects.all().delete()

    # 1. Categories
    cat_brand = ServiceCategory.objects.create(
        name="BRAND",
        code="01",
        outcome_statement="Make your business recognizable before someone ever walks through the door.",
        order=1
    )
    cat_digital = ServiceCategory.objects.create(
        name="DIGITAL",
        code="02",
        outcome_statement="Give your business a digital home that feels as premium as the experience you provide.",
        order=2
    )
    cat_content = ServiceCategory.objects.create(
        name="CONTENT",
        code="03",
        outcome_statement="Turn your craft into visual content people want to stop and look at.",
        order=3
    )
    cat_growth = ServiceCategory.objects.create(
        name="GROWTH",
        code="04",
        outcome_statement="Help more of the right clients discover you, trust your pricing, and take action.",
        order=4
    )

    # 2. Services
    # BRAND
    Service.objects.create(
        category=cat_brand,
        title="Brand Identity & Visual System",
        slug="beauty-branding",
        tagline="A cohesive, elevated visual identity built specifically for luxury beauty businesses.",
        outcome="Transforms how potential clients perceive your standard of care and justifies premium pricing before they ever consult.",
        full_description="We design comprehensive brand identities tailored to the nuances of salons, aesthetic clinics, and beauty professionals. From bespoke typography and color palettes to print finishes and texture guidelines, every element reflects luxury and intentionality.",
        deliverables="Bespoke Wordmark & Emblem\nComprehensive Brand Guidelines\nTypography & Editorial Color Palette\nTreatment Menu & Price List Styling\nPrint & Packaging Direction\nDigital Asset Toolkit",
        whatsapp_prompt="Hi Quorv, I'm interested in branding and visual identity for my beauty business.",
        order=1
    )
    Service.objects.create(
        category=cat_brand,
        title="Social Brand Guidelines & Templates",
        slug="social-brand-systems",
        tagline="Elevate your Instagram and digital channels from ad-hoc posts into a curated brand feed.",
        outcome="Ensures your everyday social presence matches the architectural beauty and high caliber of your physical studio.",
        full_description="We build modular, easy-to-use social kits and style systems. No generic Canva templates. Every layout is crafted around client transformations, editorial typography, and treatment highlights.",
        deliverables="Curated Feed & Story Architecture\nTreatment Announcement Layouts\nClient Transformation Storyboards\nTypography & Color Presets\nDirecting Guidelines for In-Salon Capture",
        whatsapp_prompt="Hi Quorv, I'd like to improve the visual consistency of my beauty brand's social media.",
        order=2
    )

    # DIGITAL
    Service.objects.create(
        category=cat_digital,
        title="Custom Beauty Website Design & Build",
        slug="beauty-website-design",
        tagline="Bespoke, high-performance digital homes engineered for beauty brands, salons, and clinics.",
        outcome="Gives high-value clients an effortless, editorial experience that builds immediate trust and drives qualified bookings.",
        full_description="Your website is your flagship digital location. We combine editorial magazine aesthetic with swift loading, clean hierarchy, and frictionless mobile booking flows. Every page is structured to present your treatments, team, and space with undeniable authority.",
        deliverables="Bespoke UI/UX Design & Architecture\nLightning-Fast Mobile Optimization\nTreatment Showcase & Transparent Pricing Displays\nDirect WhatsApp & Booking Engine Integration\nLocal SEO Architecture & Schema Markup\nZero-Friction Client Experience",
        whatsapp_prompt="Hi Quorv, I'm interested in a custom website for my beauty business.",
        order=1
    )
    Service.objects.create(
        category=cat_digital,
        title="Salon & Clinic Booking Experiences",
        slug="salon-booking-websites",
        tagline="Eliminate manual DM booking friction with a seamless, brand-aligned reservation journey.",
        outcome="Reduces client drop-off and ends the back-and-forth messaging cycle with clear service selection and deposit workflows.",
        full_description="Whether integrating with Fresha, Timely, Phorest, Vagaro, Jane, or bespoke booking systems, we ensure the transition from discovering your brand to securing an appointment feels unified, prestigious, and effortless.",
        deliverables="Booking Platform Optimization (Fresha, Timely, Phorest, etc.)\nTreatment Menu Categorization & Clarity\nDeposit & Policy Visual Communication\nMobile-First Scheduling Funnel\nAutomated Confirmation Experience",
        whatsapp_prompt="Hi Quorv, I'd like to improve the booking experience and reduce manual messaging for my salon/clinic.",
        order=2
    )
    Service.objects.create(
        category=cat_digital,
        title="Website Redesign & Modernization",
        slug="website-redesign",
        tagline="Upgrade an outdated, clunky website into a sleek, editorial digital home.",
        outcome="Brings your digital presence up to the actual caliber of your in-person work, elevating your business above local competitors.",
        full_description="If your physical salon or aesthetic practice has evolved, but your website was made years ago and looks generic, we rebuild it from the ground up with modern typography, refined aesthetics, and modern technical standards.",
        deliverables="Comprehensive UX Audit & Strategy\nComplete Visual & Editorial Redesign\nMobile Responsiveness Overhaul\nSEO Structure Migration & Redirection\nConversion Rate Optimization",
        whatsapp_prompt="Hi Quorv, I'm interested in redesigning our existing beauty website.",
        order=3
    )

    # CONTENT
    Service.objects.create(
        category=cat_content,
        title="Content Direction & Short-Form Video",
        slug="beauty-content-creation",
        tagline="Turn salon chair transformations and clinical procedures into captivating visual narratives.",
        outcome="Attracts the exact clients who appreciate high-end artistry and premium services, without relying on cheap viral gimmicks.",
        full_description="We establish the creative direction, pacing, and editing style for your Reels, TikToks, and portfolio photography. We help you showcase texture, shine, skin clarity, and atmosphere with cinematic elegance.",
        deliverables="Content Capture Guidelines for Staff\nHigh-End Short-Form Video Editing (Reels / TikTok)\nColor Grading & Sound Direction\nEditorial Before/After Layout Systems\nQuarterly Content Strategy Themes",
        whatsapp_prompt="Hi Quorv, I'm interested in content direction and video editing for my beauty business.",
        order=1
    )

    # GROWTH
    Service.objects.create(
        category=cat_growth,
        title="Beauty SEO & Google Business Optimization",
        slug="beauty-seo",
        tagline="Be discovered by high-intent clients searching for your exact specialty in your area.",
        outcome="Captures steady organic search traffic from clients actively looking to book treatments, reducing dependency on social algorithms.",
        full_description="We optimize your local search profile, Google Maps presence, and on-page beauty search terms (e.g. 'balayage specialist London', 'aesthetic clinic facial Scottsdale', 'luxury nail studio Toronto'). No spammy keyword stuffing, just clean, authoritative structure.",
        deliverables="Local Search & Google Business Profile Architecture\nTreatment & Service On-Page SEO\nHigh-Intent Geographic Keyword Mapping\nSchema.org Structured Data Implementation\nSpeed & Technical Core Web Vitals Polish",
        whatsapp_prompt="Hi Quorv, I'm interested in improving our Google search visibility and local rankings.",
        order=1
    )

    # 3. Industries
    Industry.objects.create(
        title="Salons & Hair Studios",
        slug="salons",
        subtitle="For premium salons and color studios seeking to elevate their clientele and brand stature.",
        the_challenge="Many exceptional salons rely entirely on Instagram and word-of-mouth. While the work is stunning, the booking journey requires chaotic DM chats, and the brand looks identical to every standard high-street salon.",
        the_solution="We craft an editorial brand identity and high-converting website that showcases your stylists' artistry, organizes your service tiers, and seamlessly directs appointments into your booking platform.",
        key_focus="Stylist portfolios, transparent service menus, frictionless booking, and local search visibility.",
        order=1
    )
    Industry.objects.create(
        title="Aesthetic Clinics & Medspas",
        slug="aesthetic-clinics",
        subtitle="For medical aesthetic practices, cosmetic injectors, and skin rejuvenation clinics.",
        the_challenge="Aesthetic treatments require immense trust, medical credibility, and clinical elegance. Outdated, clinical-looking or generic spa templates fail to communicate high practitioner skill and patient safety.",
        the_solution="We engineer a calm, prestigious digital presence with clear treatment education, consultation booking funnels, practitioner accreditations, and refined aesthetic hierarchy.",
        key_focus="Clinical credibility, consultation funnels, patient education, and luxury restraint.",
        order=2
    )
    Industry.objects.create(
        title="Independent Hairstylists & Artists",
        slug="hairstylists",
        subtitle="For high-demand independent stylists, extension specialists, and session artists.",
        the_challenge="Independent professionals often lose hours every week managing DMs, sending manual price lists, and fielding clients who aren't the right fit for their price point.",
        the_solution="A sleek, single-destination portfolio and booking portal that filters for ideal clients, displays exact policy details, and elevates your personal brand.",
        key_focus="Curated transformation showcases, clear boundary communication, and automated inquiries.",
        order=3
    )
    Industry.objects.create(
        title="Nail & Lash Studios",
        slug="nail-lash-studios",
        subtitle="For bespoke nail artists, lash boutiques, and brow bars.",
        the_challenge="High volume, rapid appointment cycles, and visual trend-driven clients who need to see precise portfolio quality before booking.",
        the_solution="Tactile, high-aesthetic digital experiences highlighting attention to detail, hygienic standards, and direct booking links.",
        key_focus="Visual texture, rapid mobile booking, and distinct brand personality.",
        order=4
    )
    Industry.objects.create(
        title="Spas & Wellness Sanctuaries",
        slug="spas",
        subtitle="For holistic wellness retreats, luxury day spas, and modern bathhouses.",
        the_challenge="Communicating serenity, sensory atmosphere, and multi-treatment packages without feeling cluttered or overwhelming.",
        the_solution="Spacious editorial layouts, gentle pacing, sensory visual hierarchy, and intuitive package reservations.",
        key_focus="Atmospheric visual storytelling, package exploration, and gift card / reservation flows.",
        order=5
    )
    Industry.objects.create(
        title="Independent Beauty Brands",
        slug="beauty-professionals",
        subtitle="For emerging skincare, haircare, and cosmetic creators with specialized treatment lines.",
        the_challenge="Competing with conglomerate beauty brands requires an unmistakable point of view, tactile packaging aesthetics, and credible digital storytelling.",
        the_solution="Full-spectrum brand positioning, digital flagships, and commercial clarity engineered to convert curious scrollers into loyal advocates.",
        key_focus="Brand storytelling, ingredient transparency, and premium retail conversion.",
        order=6
    )

    # 4. FAQs (GEO and User Search Aligned)
    faqs_seed = [
        ("What does Quorv do?", "Quorv is a digital studio specializing in premium beauty businesses. We build the connected digital system behind salons, aesthetic clinics, med spas, and beauty professionals, including custom websites, booking system integrations, visual identity, and local search visibility.", "general", 1),
        ("What does a premium beauty website project involve?", "A Quorv website project encompasses discovery, brand positioning, editorial typography, mobile-first design, treatment menu architecture, booking software integration, local SEO schema, and speed optimization. We deliver a complete system engineered to convert visitors into confirmed appointments.", "services", 2),
        ("Can Quorv work with Fresha, Phorest, Vagaro, or our existing booking software?", "Yes. We integrate directly with leading salon and clinic management software, including Fresha, Phorest, Vagaro, Boulevard, Jane App, and Acuity. Clients explore your treatments and credentials on your bespoke website before transitioning smoothly into your scheduling system without any disruption.", "services", 3),
        ("What if our beauty business does not have booking software yet?", "We work with your existing setup or help you establish one. If you already use platforms like Fresha, Phorest, Vagaro, or Acuity, we seamlessly integrate your booking experience into your website. If you don’t have a system yet, we can recommend and set up the right solution for your business.", "services", 4),
        ("Can Quorv redesign our existing website?", "Yes. We frequently conduct UX and visual audits of existing beauty websites that are outdated, slow, or failing to convert. We rebuild the experience from the ground up into a modern editorial digital flagship while preserving your existing domain authority and customer data.", "services", 5),
        ("How long does a website project take?", "Most projects follow one of two tracks: a focused 2-week sprint for solo artists and boutique studios, or a 4 to 6-week architecture for multi-chair salons, medical aesthetic clinics, and medspas with extensive treatment menus and booking workflows.", "process", 6),
        ("What does Quorv handle beyond the website?", "Beyond website design and development, Quorv establishes brand visual identity, typography standards, treatment menu nomenclature, local SEO architecture, Google Business Profile optimization, and automated client consultation workflows.", "services", 7),
        ("What types of beauty businesses does Quorv work with?", "We work exclusively with beauty businesses, including hair salons, medical aesthetic clinics, med spas, independent hairstylists, nail and lash studios, wellness sanctuaries, and specialized beauty brands.", "general", 8),
        ("Do you work with beauty businesses outside the UK?", "Yes. Quorv operates internationally, collaborating with premium salons, aesthetic clinics, and beauty professionals across the United Kingdom, United States, Canada, the United Arab Emirates, Australia, and lots more.", "general", 9),
        ("How much does a Quorv website project cost?", "Quorv projects are custom quoted because every beauty business has distinct requirements, existing assets, and scope, ranging from boutique specialist booking portals to multi-chair salon digital systems. We provide a clear, transparent proposal after a short dialogue.", "pricing", 10),
        ("What happens after launch?", "After launch, we verify domain propagation, test live booking transactions, confirm Google indexation, and provide staff guidance. We also offer ongoing monthly technical care, local search enhancements, and performance refinements.", "process", 11),
    ]
    for q, a, cat, ord in faqs_seed:
        FAQ.objects.create(question=q, answer=a, category=cat, order=ord)

    # 5. Portfolio Concepts (Explicitly labelled CONCEPT)
    PortfolioConcept.objects.create(
        title="AURA Medical Aesthetics",
        slug="aura-medical-aesthetics-concept",
        client_type="Aesthetic Clinic Concept",
        category="Brand & Digital Architecture",
        concept_summary="An editorial visual identity and patient booking portal designed for a physician-led skin and injectables clinic. Features serene neutral tones, tactile medical typography, and treatment pathway clarity.",
        deliverables="Brand Identity, Website Design, Consultation Funnel Architecture, Treatment Menu System",
        image_url="https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=1200&q=80",
        is_concept=True,
        order=1
    )
    PortfolioConcept.objects.create(
        title="MAISON NOIR Studio",
        slug="maison-noir-concept",
        client_type="Luxury Hair & Color Salon Concept",
        category="Visual Identity & Booking System",
        concept_summary="A sophisticated identity system and mobile-first digital experience for an upscale hair salon. Structured around stylist portfolios, transparent service tiers, and automated Fresha integration.",
        deliverables="Wordmark Design, Color System, Mobile Web Experience, Social Media Grid System",
        image_url="https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=1200&q=80",
        is_concept=True,
        order=2
    )
    PortfolioConcept.objects.create(
        title="TERRA Botanical Sanctuary",
        slug="terra-botanical-concept",
        client_type="Holistic Spa & Treatment Menu Concept",
        category="Digital Experience & Local Search",
        concept_summary="Digital experience and atmospheric storytelling for an organic day spa and bathhouse, focusing on sensorial pacing, ritual descriptions, and local search visibility.",
        deliverables="Digital Flagship, Ritual Architecture, Local SEO Structure, Gift Certificate Flow",
        image_url="https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80",
        is_concept=True,
        order=3
    )
    PortfolioConcept.objects.create(
        title="VELOUR Nail & Lash Atelier",
        slug="velour-nail-lash-concept",
        client_type="Boutique Nail & Lash Atelier Concept",
        category="Brand Identity & Direct Booking Flow",
        concept_summary="A tactile editorial identity and friction-free direct appointment journey for an upscale lash and nail atelier, eliminating DM back-and-forth and driving deposit pre-authorizations.",
        deliverables="Brand Direction, Direct Booking UX, Treatment Menu System, WhatsApp Deposit Automation",
        image_url="https://images.unsplash.com/photo-1632345031435-8727f6897d53?auto=format&fit=crop&w=1200&q=80",
        is_concept=True,
        order=4
    )
    PortfolioConcept.objects.create(
        title="ÉLAN Aesthetic Dermatology",
        slug="elan-aesthetic-dermatology-concept",
        client_type="Doctor-Led Aesthetic Dermatology Concept",
        category="Medical Aesthetics Web Flagship & Local SEO",
        concept_summary="A reassuring, clinical digital flagship for a physician-led dermatology and skin rejuvenation practice, featuring interactive consultation pre-screening and localized search supremacy.",
        deliverables="Clinical Web Flagship, Consultation Funnel, Doctor Credentials Architecture, Local SEO Architecture",
        image_url="https://images.unsplash.com/photo-1512290900672-1f41ec430c00?auto=format&fit=crop&w=1200&q=80",
        is_concept=True,
        order=5
    )

    print("Seeding completed successfully.")

if __name__ == '__main__':
    seed_data()
