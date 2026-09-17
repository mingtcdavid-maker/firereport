# firereport

A small static web app for generating SCDF Fire Investigation Reports —
no backend required.

Users fill in a form in the browser; client-side JavaScript
(`docxtemplater` + `pizzip`) fills in the placeholders in
`docx_template/SCDF_Fire_Investigation_Report_TEMPLATE.docx` directly in
the browser, and the finished `.docx` is downloaded — everything runs
entirely on the client, with no server-side processing of form data.

## Run locally

Any static file server works, e.g.:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000 in a browser, fill in the form, and click
"Generate & Download Report".

(Opening `index.html` directly via `file://` will not work — browsers
block `fetch()` of local files under that scheme, so the template can't
be loaded. Serve it over `http://` instead.)

## Project layout

- `index.html` – the data-entry form and all client-side logic: builds
  the template context from the form, renders the docx template in the
  browser, and triggers the download.
- `docx_template/SCDF_Fire_Investigation_Report_TEMPLATE.docx` – the
  source Word template with simple `{{tag}}` placeholders, used by
  docxtemplater.
- `static/vendor/` – vendored copies of `pizzip` and `docxtemplater`
  (both MIT-licensed), so the page has no runtime dependency on any CDN.

## Notes

- Eyewitness details are optional; any left blank render as "NIL" in the
  report.
- The template also contains an insurance-coverage checkbox
  (`insured_mark_no`) and a free-form "Other Information" section
  (`other_information`) that aren't collected by the form and are left
  blank in the generated report.
- The template's placeholders were simplified from Jinja-style tags
  (e.g. `{{ eyewitness.name|default('NIL') }}`) to flat `{{tag}}` names
  (e.g. `{{eyewitness_name}}`) to work with docxtemplater, which doesn't
  parse dotted paths or filters out of the box. The "NIL" fallback logic
  now lives in `index.html`'s `buildContext()` function instead.
