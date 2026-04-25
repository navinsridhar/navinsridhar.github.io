---
layout: page
permalink: /publications/
title: Publications
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<div class="publications">

  <p><b>Total publications: 40+</b> · <em>lead author: 10</em> · <em>≤ 3rd author: 10</em> · <em>co-author: 16</em> · <em>books / white papers: 2</em> · <em>astronomical telegrams: 2</em>.</p>

  <p>
    <a class="btn btn-sm z-depth-0" role="button" href="https://ui.adsabs.harvard.edu/public-libraries/AspXr7NhTAaWjzQzWm-Kuw" target="_blank">NASA ADS</a>
    <a class="btn btn-sm z-depth-0" role="button" href="https://scholar.google.com/citations?user=_F9gI4QAAAAJ" target="_blank">Google Scholar</a>
    <a class="btn btn-sm z-depth-0" role="button" href="https://orcid.org/0000-0002-5519-9550" target="_blank">ORCID</a>
  </p>

  <h2>First-author publications</h2>

{% bibliography -f papers --group_by none --query @*[category=first]* %}

  <h2>Second / third-author publications</h2>

{% bibliography -f papers --group_by none --query @*[category=secondthird]* %}

  <h2>n<sup>th</sup>-author publications</h2>

{% bibliography -f papers --group_by none --query @*[category=nth]* %}

  <h2>Books and white papers</h2>

{% bibliography -f papers --group_by none --query @*[category=books]* %}

  <h2>Astronomical telegrams</h2>

{% bibliography -f papers --group_by none --query @*[category=atel]* %}

</div>
