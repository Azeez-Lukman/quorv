# Quorv · The Digital System Behind Premium Beauty Businesses

Quorv designs and engineers premium websites, brand positioning, and connected digital booking systems exclusively for the beauty sector — including aesthetic clinics, medical spas, luxury hair salons, skin clinics, cosmetic practitioners, and bespoke beauty professionals across the UK, US, Canada, UAE, Australia, and internationally.

---

## 🌟 Core Architecture & Capabilities

* **Generative Engine Optimization (GEO)**: Built for native readability and high citation probability by AI answer engines (ChatGPT / SearchGPT, Google AI Overviews, Perplexity, Claude, Microsoft Copilot) via Schema.org `@graph` (`Organization`, `WebSite`, `Service`, `FAQPage`, `Article`).
* **Booking System Continuity**: Seamless integration with enterprise salon management software (Fresha, Phorest, Vagaro, Jane App, Boulevard, Acuity, Timely) without jarring transitions or lost revenue.
* **Vertical Industry Landing Pages**: Dedicated architectural pages tailored to Salons, Aesthetic Clinics, Med Spas, Nail & Lash Studios, and Independent Practitioners.
* **GEO Insights Knowledge Base**: Long-form editorial guides addressing high-intent operational queries (e.g. Med Spa structure, Salon website requirements, Fresha vs Website dynamics).
* **Studio Owner Analytics Dashboard**: Real-time staff dashboard (`/dashboard/`) tracking lead volume, sector breakdowns, WhatsApp touchpoints, inquiry statuses, and CSV export.
* **Crawler & Search Discovery**: Fully compliant `robots.txt` granting explicit rendering and crawling permissions to Googlebot, OAI-SearchBot, PerplexityBot, ClaudeBot, and Bingbot with XML Sitemap protocol.

---

## 🛠️ Technology Stack

* **Backend**: Python 3.14 / Django 6.x
* **Frontend**: Modern Vanilla HTML5 / Tailwind CSS runtime / Google Fonts (Italiana, Plus Jakarta Sans, Space Grotesk)
* **Structured Data**: Schema.org JSON-LD linked entity graph
* **Database**: SQLite (Development) / PostgreSQL compatible (Production)
* **Deployment Ready**: WhiteNoise static file serving, Gunicorn / Procfile configuration

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Azeez-Lukman/quorv.git
cd quorv
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 4. Database Setup & Data Seeding
```bash
python manage.py migrate
python seed_quorv.py
```

### 5. Create Studio Admin User
```bash
python create_studio_admin.py
# Or standard django command:
python manage.py createsuperuser
```

### 6. Run the Local Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🧭 Routes & Endpoints

| URL Path | Description |
| :--- | :--- |
| `/` | Homepage with interactive system breakdown, services, concepts, insights, & FAQ |
| `/services/` | Studio services catalog |
| `/services/<slug>/` | Standalone service detail pages |
| `/industries/` | Industry verticals index |
| `/industries/<slug>/` | Specialized industry landing pages |
| `/insights/` | Editorial guides & industry authority index |
| `/insights/<slug>/` | Detailed GEO insight articles |
| `/work/` | Selected studio concept showcases |
| `/process/` | Studio engagement & delivery phases |
| `/about/` | Studio philosophy & positioning |
| `/contact/` | Direct inquiry form & WhatsApp portal |
| `/dashboard/` | Studio owner analytics & lead management (`noindex`) |
| `/robots.txt` | Crawler access rules for search & AI discovery bots |
| `/sitemap.xml` | Dynamic XML sitemap |

---

## 📄 License

Proprietary © QUORV. All rights reserved.
