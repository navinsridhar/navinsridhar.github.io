---
layout: page
permalink: /cv/
title: CV
nav: true
nav_order: 8
---

{% comment %}
Cache-busting: every Jekyll build regenerates {{ site.time }}, which gives
the embedded PDF a fresh query string. This forces browsers and the
GitHub Pages CDN to refetch the PDF on each new deploy instead of
serving the previously-cached copy — otherwise the CV visible on the site
can lag one or two Overleaf syncs behind the actual file on disk.
{% endcomment %}
{% assign cv_pdf_url = '/assets/pdf/CV.pdf' | relative_url %}
{% assign cv_version = site.time | date: '%s' %}
{% assign cv_pdf_versioned = cv_pdf_url | append: '?v=' | append: cv_version %}

<p class="text-muted mb-3">
  <small>The PDF below is the latest version of my CV — it is rebuilt automatically from my Overleaf source, so this page always reflects the most current version. If you see a stale copy, hit Cmd/Ctrl + Shift + R to hard-refresh.</small>
</p>

<div class="cv-embed" style="width: 100%; height: 90vh; border: 1px solid var(--global-divider-color); border-radius: 6px; overflow: hidden;">
  <object data="{{ cv_pdf_versioned }}#view=FitH" type="application/pdf" width="100%" height="100%">
    <iframe src="{{ cv_pdf_versioned }}#view=FitH" width="100%" height="100%" style="border: none;">
      <p>
        Your browser does not support inline PDFs.
        Please <a href="{{ cv_pdf_versioned }}" target="_blank">download the PDF</a> to view it.
      </p>
    </iframe>
  </object>
</div>

<p class="text-muted mt-2">
  <small>
    Direct link (always latest):
    <a href="{{ cv_pdf_versioned }}" target="_blank">CV.pdf</a>
  </small>
</p>
