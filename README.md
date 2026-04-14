# Website Content Scan Updater

This tool updates the Website Content Scan from website sitemaps.

It can run in two ways:

- **Smartsheet mode:** GitHub Actions updates the live Smartsheet sheet directly.
- **Excel fallback mode:** A team member exports the sheet from Smartsheet, runs the script, and receives an updated workbook.

## What It Does

For every site listed in `sites.yml`, the updater:

1. Reads the site's sitemap.
2. Recursively follows sitemap indexes.
3. Applies site-specific path exclusions.
4. Keeps normal web pages and skips files like PDFs, images, videos, XML, ZIPs, and spreadsheets.
5. Normalizes URLs so `http`, `https`, `www`, and trailing slash differences do not create duplicates.
6. Adds missing rows with `Site`, `Page`, `Sub-Page`, `Last Updated`, and `Page Status`.
7. Updates `Last Updated` on existing rows when the sitemap provides a `lastmod` value.
8. Sets `Page Status` to `Page Expired` for rows that no longer appear in the sitemap.

## Required Sheet Columns

The live Smartsheet should contain these columns:

- `URL`
- `Site`
- `Page`
- `Sub-Page`
- `Page Status`
- `Last Updated`

The `URL` column can remain formula-generated. The updater reads it for comparison, but only writes `Site`, `Page`, `Sub-Page`, `Last Updated`, and `Page Status`.

If `Page Status` uses a restricted dropdown, add these allowed values:

- `Not Started`
- `Page Expired`

## Site List

Edit `sites.yml` to add or remove websites:

```yaml
sites:
  - name: ustravel.org
    sitemap: https://www.ustravel.org/sitemap.xml
    exclude_paths:
      - /
      - /news
      - /press
      - /research

  - name: ipw.com
    sitemap: https://www.ipw.com/sitemap.xml
    fallback_sitemap_file: manual-sitemaps/ipw.com/sitemap.xml
    allow_sitemap_errors: true
```

The `name` is for humans. The updater derives the actual site value from each sitemap URL and strips `www.` while preserving real subdomains such as `esto.ustravel.org`.

Use `exclude_paths` when a site has section subpages that should not be added to the scan. Excluding `/news` still includes `/news`, but excludes pages below it, such as `/news/example-story`. Excluding `/` only skips the homepage, not the whole site.

Use `allow_sitemap_errors: true` for a site whose sitemap may be temporarily blocked or unavailable. The workflow will log a warning and continue scanning the other sites.

Use `fallback_sitemap_file` when a sitemap is visible in a browser but blocked from GitHub Actions. The updater tries the live sitemap first; if that fails and the fallback file exists, it reads the uploaded file instead.

## Manual Sitemap Upload

IPW currently uses Cloudflare protection that can block GitHub Actions from reading `https://www.ipw.com/sitemap.xml`. To include IPW in a scan:

1. Open `https://www.ipw.com/sitemap.xml` in a browser.
2. Save the page as `sitemap.xml`.
3. In GitHub, open `manual-sitemaps/ipw.com/`.
4. Click **Add file > Upload files**.
5. Upload the saved `sitemap.xml`.
6. Commit directly to `main`.
7. Run the Excel fallback or Smartsheet workflow again.

The IPW entry in `sites.yml` already points to `manual-sitemaps/ipw.com/sitemap.xml` as its fallback.

## Smartsheet Setup

Smartsheet API access is available on Business and Enterprise plans. A Smartsheet user generates an access token from their Smartsheet account, and GitHub stores that token as an encrypted repository secret.

Recommended ownership:

- Use a permanent staff account or service account, not an intern's personal account.
- Give that account access to the Website Content Scan sheet.
- Store the token in GitHub as `SMARTSHEET_ACCESS_TOKEN`.
- Store the sheet ID in GitHub as `SMARTSHEET_SHEET_ID`.

The sheet ID is the number in the Smartsheet sheet URL.

## GitHub One-Click and Weekly Runs

The workflow at `.github/workflows/update-website-content-scan.yml` supports:

- Manual one-click runs through **Actions > Update Website Content Scan > Run workflow**.
- Weekly automatic runs every Monday at 14:00 UTC.

## Excel Fallback

Install dependencies:

```bash
python3 -m pip install -r website_content_scan/requirements.txt
```

Run the updater against an exported workbook:

```bash
python3 website_content_scan/scripts/update_scan.py \
  --excel-input "/path/to/Website Content Scan.xlsx" \
  --excel-output "/path/to/Website Content Scan.updated.xlsx"
```

The output workbook will include newly found pages, updated `Last Updated` values, and expired page flags.

## Smartsheet Mode Locally

```bash
export SMARTSHEET_ACCESS_TOKEN="your-token"
export SMARTSHEET_SHEET_ID="your-sheet-id"
python3 website_content_scan/scripts/update_scan.py
```

## Notes

- Root pages are stored as `Page = /` and blank `Sub-Page`.
- `/about-us/executives` becomes `Page = /about-us` and `Sub-Page = /executives`.
- If a sitemap entry has no `lastmod`, `Last Updated` is left blank.
