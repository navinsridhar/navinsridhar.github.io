---
layout: page
permalink: /cv/
title: CV
nav: true
nav_order: 7
---

<div class="cv-download mb-3">
  <a class="btn btn-primary z-depth-0" role="button" href="{{ '/assets/pdf/CV.pdf' | relative_url }}" target="_blank">
    <i class="fa-solid fa-file-pdf"></i>&nbsp; View full CV (PDF)
  </a>
</div>

<p class="text-muted mb-3">
  <small>The PDF below is the latest version of my CV — it is rebuilt automatically from my Overleaf source every day, so this page always reflects the most current version.</small>
</p>

<div class="cv-embed" style="width: 100%; height: 90vh; border: 1px solid var(--global-divider-color); border-radius: 6px; overflow: hidden;">
  <object data="{{ '/assets/pdf/CV.pdf' | relative_url }}#view=FitH" type="application/pdf" width="100%" height="100%">
    <iframe src="{{ '/assets/pdf/CV.pdf' | relative_url }}#view=FitH" width="100%" height="100%" style="border: none;">
      <p>
        Your browser does not support inline PDFs.
        Please <a href="{{ '/assets/pdf/CV.pdf' | relative_url }}" target="_blank">download the PDF</a> to view it.
      </p>
    </iframe>
  </object>
</div>
