# firereport

A small web app for generating SCDF Fire Investigation Reports.

Users fill in a form in the browser; the Flask backend fills in the
Jinja placeholders in `docx_template/SCDF_Fire_Investigation_Report_TEMPLATE.docx`
using `docxtpl`, and the finished `.docx` is returned as a download.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000 in a browser, fill in the form, and click
"Generate & Download Report".

## Project layout

- `app.py` – Flask app: serves the form and the `/generate` endpoint that
  renders the docx template with the submitted data.
- `templates/index.html` – the data-entry form.
- `docx_template/SCDF_Fire_Investigation_Report_TEMPLATE.docx` – the source
  Word template with Jinja tags (e.g. `{{ incident_no }}`), used by docxtpl.

## Notes

- Eyewitness details are optional; any left blank render as "NIL" in the
  report, matching the template's defaults.
- The template also contains an insurance-coverage checkbox
  (`insured_mark_no`) and a free-form "Other Information" section
  (`other_information`) that aren't collected by the form and are left
  blank in the generated report.
