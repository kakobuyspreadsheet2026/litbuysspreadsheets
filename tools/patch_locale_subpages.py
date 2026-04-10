#!/usr/bin/env python3
"""Patch de/es/pt/*.html copied from English root: ../styles, locale header, lang menu, breadcrumb."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LOCALES: dict[str, dict[str, str]] = {
    "de": {
        "lang": "de",
        "home": "/de/",
        "home_label": "Startseite",
        "cats": "Alle Kategorien",
        "guides": "Anleitungen",
        "contact": "Kontakt",
        "news": "News",
        "nav_aria": "Hauptnavigation",
        "lang_aria": "Sprache",
        "lang_btn": "Sprache wählen",
        "skip": "Zum Inhalt springen",
        "brand_aria": "litbuy spreadsheet Startseite",
    },
    "es": {
        "lang": "es",
        "home": "/es/",
        "home_label": "Inicio",
        "cats": "Todas las categorías",
        "guides": "Guías",
        "contact": "Contacto",
        "news": "Noticias",
        "nav_aria": "Principal",
        "lang_aria": "Idioma",
        "lang_btn": "Elegir idioma",
        "skip": "Ir al contenido",
        "brand_aria": "litbuy spreadsheet inicio",
    },
    "pt": {
        "lang": "pt",
        "home": "/pt/",
        "home_label": "Início",
        "cats": "Todas as categorias",
        "guides": "Guias",
        "contact": "Contacto",
        "news": "Notícias",
        "nav_aria": "Principal",
        "lang_aria": "Idioma",
        "lang_btn": "Escolher idioma",
        "skip": "Ir para o conteúdo",
        "brand_aria": "litbuy spreadsheet início",
    },
}

PAGES: dict[str, dict] = {
    "guides.html": {
        "breadcrumb": {"de": "Anleitungen", "es": "Guías", "pt": "Guias"},
        "current": "guides",
    },
    "spreadsheet.html": {
        "breadcrumb": {"de": "Spreadsheet", "es": "Spreadsheet", "pt": "Spreadsheet"},
        "current": "spreadsheet",
    },
    "contact.html": {
        "breadcrumb": {"de": "Kontakt", "es": "Contacto", "pt": "Contacto"},
        "current": "contact",
    },
    "news.html": {
        "breadcrumb": {"de": "News", "es": "Noticias", "pt": "Notícias"},
        "current": "news",
    },
}

SUBMENU = """                <a href="https://maisonlooks.com/en/c/shoes" role="menuitem">Shoes</a>
                <a href="https://maisonlooks.com/en/c/jackets" role="menuitem">Jackets</a>
                <a href="https://maisonlooks.com/en/c/clothing" role="menuitem">Hoodies / Sweaters</a>
                <a href="https://maisonlooks.com/en/c/t-shirts" role="menuitem">T-Shirts</a>
                <a href="https://maisonlooks.com/en/c/clothing" role="menuitem">Pants / Shorts</a>
                <a href="https://maisonlooks.com/en/products" role="menuitem">Bags</a>
                <a href="https://maisonlooks.com/en/c/headwear" role="menuitem">Headwear</a>
                <a href="https://maisonlooks.com/en/c/accessories" role="menuitem">Accessories</a>
                <a href="https://maisonlooks.com/en/c/electronics" role="menuitem">Electronics</a>
                <a href="https://maisonlooks.com/en/c/perfume" role="menuitem">Perfume</a>
                <a href="https://maisonlooks.com/en/products" role="menuitem">Jersey</a>
                <a href="https://maisonlooks.com/en/products" role="menuitem">Other</a>"""


def lang_menu_lines(page: str, loc: str) -> str:
    slug = page
    rows = [
        ("EN", f"/{slug}", None),
        ("PL", f"/pl/{slug}", "pl"),
        ("PT", f"/pt/{slug}", "pt-PT"),
        ("ES", f"/es/{slug}", "es"),
        ("DE", f"/de/{slug}", "de"),
    ]
    lines = []
    for label, href, lang_attr in rows:
        code = {"EN": "en", "PL": "pl", "PT": "pt", "ES": "es", "DE": "de"}[label]
        cur = ' aria-current="page"' if (code == loc) else ""
        if lang_attr:
            lines.append(f'              <a href="{href}"{cur} lang="{lang_attr}">{label}</a>')
        else:
            lines.append(f'              <a href="{href}"{cur}>{label}</a>')
    return "\n".join(lines)


def build_nav(cfg: dict, page: str, loc: str) -> str:
    cur = PAGES[page]["current"]
    g_attr = ' aria-current="page"' if cur == "guides" else ""
    s_attr = ' aria-current="page"' if cur == "spreadsheet" else ""
    c_attr = ' aria-current="page"' if cur == "contact" else ""
    n_attr = ' aria-current="page"' if cur == "news" else ""
    return f"""        <nav aria-label="{cfg["nav_aria"]}">
          <ul>
            <li><a href="{cfg["home"]}">{cfg["home_label"]}</a></li>
            <li class="has-sub">
              <button type="button" aria-expanded="false" aria-haspopup="true">{cfg["cats"]}</button>
              <div class="submenu" role="menu">
{SUBMENU}
              </div>
            </li>
            <li><a href="guides.html"{g_attr}>{cfg["guides"]}</a></li>
            <li><a href="spreadsheet.html"{s_attr}>Spreadsheet</a></li>
            <li><a href="contact.html"{c_attr}>{cfg["contact"]}</a></li>
            <li><a href="news.html"{n_attr}>{cfg["news"]}</a></li>
          </ul>
        </nav>"""


def build_header_inner(cfg: dict, page: str, loc: str) -> str:
    lang_block = f"""          <nav class="language-switcher has-lang" aria-label="{cfg["lang_aria"]}">
            <button type="button" class="lang-globe-btn" aria-haspopup="true" aria-expanded="false" aria-label="{cfg["lang_btn"]}">
              <svg class="lang-globe-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="10" />
                <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
              </svg>
            </button>
            <div class="lang-menu" role="menu">
{lang_menu_lines(page, loc)}
            </div>
          </nav>"""
    return f"""      <div class="header-inner">
        <a class="brand" href="{cfg["home"]}" aria-label="{cfg["brand_aria"]}">
          <span class="brand-mark" aria-hidden="true">LS</span>
          <span class="brand-text">litbuy spreadsheet</span>
        </a>
{build_nav(cfg, page, loc)}
        <div class="header-end">
          <div class="header-cta">
            <a
              class="btn btn-primary"
              href="https://maisonlooks.com/?utm_source=litbuy_sheet_seo&amp;utm_medium=referral&amp;utm_campaign=spreadsheet_hub"
              >litbuy spreadsheet</a
            >
          </div>
{lang_block}
        </div>
      </div>"""


def patch_file(path: Path, loc: str, page: str) -> None:
    cfg = LOCALES[loc]
    t = path.read_text()
    t = t.replace('href="styles.css"', 'href="../styles.css"')
    t = t.replace(f"https://litbuysspreadsheets.com/{page}", f"https://litbuysspreadsheets.com/{loc}/{page}")
    t = re.sub(
        r"https://litbuysspreadsheets\.com/news\.html#",
        f"https://litbuysspreadsheets.com/{loc}/news.html#",
        t,
    )
    t = t.replace('html lang="en"', f'html lang="{cfg["lang"]}"')
    t = t.replace('src="images/news/', 'src="../images/news/')
    t = t.replace('href="/#hub-ai-tools"', f'href="{cfg["home"]}#hub-ai-tools"')
    t = t.replace('"inLanguage": "en"', f'"inLanguage": "{cfg["lang"]}"')

    t = t.replace('<a class="skip-link" href="#main">Skip to content</a>', f'<a class="skip-link" href="#main">{cfg["skip"]}</a>')

    inner = build_header_inner(cfg, page, loc)
    t = re.sub(
        r"      <div class=\"header-inner\">.*?</div>\s*</header>",
        inner + "\n    </header>",
        t,
        count=1,
        flags=re.S,
    )

    bc = PAGES[page]["breadcrumb"][loc]
    hl = cfg["home_label"]
    home = cfg["home"]
    t = re.sub(
        r'<p class="breadcrumb"><a href="/">Home</a> · [^<]+</p>',
        f'<p class="breadcrumb"><a href="{home}">{hl}</a> · {bc}</p>',
        t,
        count=1,
    )

    path.write_text(t)


def main() -> None:
    for loc in LOCALES:
        for page in PAGES:
            patch_file(ROOT / loc / page, loc, page)
            print("OK", loc, page)


if __name__ == "__main__":
    main()
