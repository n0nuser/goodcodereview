# fn-password-min-length: added sources

Checked 2026-11-19 against the published PDFs (pdftotext).

- https://www.cisa.gov/sites/default/files/2023-01/cisa_cpg_checklist_12052022.pdf. CPG 1.4: "Organizations have a system-enforced policy that requires a minimum password length of 15* or more characters for all password protected IT assets". Names 15 characters.
- https://www.ncsc.gov.uk/files/Cyber-Essentials-Requirements-for-Infrastructure-v3-1-April-2023.pdf. Password-based authentication: "A minimum password length of at least 12 characters, with no maximum length restrictions", or 8 with a deny list of common passwords.

The Microsoft Identity settings page was dropped from `borrowed_from`: it documents a configurable default of 6, not a recommendation.
