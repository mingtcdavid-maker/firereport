# firereport

A single self-contained `index.html` file for generating SCDF Fire
Investigation Reports — no backend, no build step, no other files.

Users fill in a form in the browser; client-side JavaScript
(`docxtemplater` + `pizzip`) fills in the placeholders of an embedded
copy of the Word report template, and the finished `.docx` is
downloaded — everything runs entirely on the client, with no
server-side processing of form data. A live preview of the rendered
document (via `docx-preview` + `jszip`) updates as the form is filled
in.

The docx template and all four of those libraries are embedded
directly inside `index.html` (the template as a base64 string, the
libraries inlined as `<script>` blocks), so the file has no external
dependencies and needs no network access to run.

## Run locally

Just open `index.html` directly in a browser — double-click it, or:

```bash
open index.html        # macOS
xdg-open index.html    # Linux
```

No server is needed; it works from the `file://` URL as well as from
any static file host.

## Project layout

- `index.html` – the entire app: the data-entry form, the embedded
  docx template (base64-encoded), the vendored libraries, and all
  client-side logic to build the template context, render the docx,
  keep the live preview panel in sync, and trigger the download.

## Notes

- Eyewitness details are optional; any left blank render as "NIL" in the
  report.
- The template also contains an insurance-coverage checkbox
  (`insured_mark_no`) that isn't collected by the form and is left blank
  in the generated report.
- The template's placeholders were simplified from Jinja-style tags
  (e.g. `{{ eyewitness.name|default('NIL') }}`) to flat `{{tag}}` names
  (e.g. `{{eyewitness_name}}`) to work with docxtemplater, which doesn't
  parse dotted paths or filters out of the box. The "NIL" fallback logic
  lives in `index.html`'s `buildContext()` function instead.
- The live preview re-renders the full document (via `docx.renderAsync`)
  on a short debounce after each keystroke, so it may lag slightly
  behind typing on slower devices.
- The embedded libraries are `pizzip` and `docxtemplater` (MIT/GPLv3
  dual-licensed), `jszip` (MIT/GPLv3 dual-licensed), and `docx-preview`
  (Apache-2.0) — each inline `<script>` block in `index.html` is
  preceded by a comment naming the library, version, license, and
  upstream repository.
- To update the docx template, regenerate the base64 string (e.g.
  `base64 -w0 template.docx`) and replace the `TEMPLATE_BASE64` constant
  near the top of the main `<script>` block.
