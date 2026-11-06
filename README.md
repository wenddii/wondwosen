# Wendwosen Tessema — Developer Portfolio

A clean, minimal, and modern personal developer portfolio built with Django, following a Modular Monolith architecture. Inspired by the understated typography, generous whitespace, and focused design language of modern developer portfolios (such as [dagmawibabi.com](https://www.dagmawibabi.com/)).

---

## 1. Project Architecture

The application is structured as a **Modular Monolith** where domain concerns are cleanly separated into dedicated apps under `apps/`:

```text
my_portfolio/
│
├── apps/
│   ├── core/                  # Profile, biography, tech stack, experience timeline
│   │   ├── management/
│   │   │   └── commands/      # seed_portfolio command for initial data
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── core/          # Single-page index template
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── projects/              # Featured projects, highlights, tech tags, links
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── projects/      # Project list and detail views
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── contact/               # Contact form submissions and DB storage
│       ├── migrations/
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       └── views.py
│
├── config/                    # Django project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   ├── css/
│   │   └── style.css          # Handcrafted minimal, responsive stylesheet
│   ├── js/
│   │   └── main.js            # Vanilla JS for mobile nav & async form UX
│   └── images/
│
├── templates/                 # Global template inheritance
│   ├── base.html              # Base layout, SEO meta tags, OpenGraph, font loading
│   └── includes/
│       ├── navbar.html        # Clean minimal header with CV button & mobile nav
│       └── footer.html        # Clean footer with location & social links
│
├── media/                     # Uploaded avatars, project screenshots, CV PDFs
├── .env                       # Environment variables (secret key, debug, hosts)
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## 2. Django Apps Breakdown

| App | Domain Responsibility |
| :--- | :--- |
| **`apps.core`** | Manages personal identity (`Profile`), categorized skill inventory (`Technology`), and career milestones (`Experience`). Serves the main single-page portfolio view aggregating all sections. |
| **`apps.projects`** | Handles project showcase entities (`Project`) with titles, slugs, highlights, live demo links, repository links, tech tags, and custom order. Fully editable via Django Admin. |
| **`apps.contact`** | Handles direct contact form processing (`ContactMessage` model & `ContactForm`). Includes validation, anti-spam honeypot, dual HTML/JSON response support, and Django Admin review. |

---

## 3. Quick Start & Setup

### Prerequisites
- Python 3.10+
- pip

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` (already created with safe development defaults):
```bash
cp .env.example .env
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Initial Portfolio Content
Populate the database with Wendwosen's profile, the 5 featured projects, experience timeline, and technical skills:
```bash
python manage.py seed_portfolio
```

### 5. Create Superuser (to access Django Admin)
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver
```

Open your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view your portfolio, or [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to manage projects and read contact submissions.

---

## 4. Key Highlights & Features

- **Minimalist Aesthetic**: Typographic hierarchy with `Inter`, dark text on off-white (`#fafafa`), subtle grey borders (`#e5e7eb`), generous spacing, and no bloated frameworks.
- **Dynamic Content via Django Admin**: Projects, experiences, technologies, and bio can be modified anytime without touching code.
- **Contact Inquiries Stored in Database**: All visitor submissions are validated, protected against bots via a honeypot, and recorded in the database.
- **Mobile Responsive**: Flexbox and CSS Grid layout with a hamburger navigation drawer for tablets and phones.
- **Production Ready**: Includes WhiteNoise for static files and environment variable isolation for secrets.

