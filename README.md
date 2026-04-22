# Website Content Scan

This repo powers the automation that scans website sitemaps and updates the Website Content Scan in Smartsheet.

## Where To Edit Things

- `sites.yml`: add sites, update sitemap URLs, and manage excluded sections
- `manual-sitemaps/`: fallback location for manual sitemap files like IPW
- `docs/index.html`: simple admin dashboard for status and quick links
- `CHECKLIST.md`: quick validation list after changes
- `MAINTAINERS.md`: backup notes for the dormant Excel fallback path

## Daily Use

Most users only need these three things:

1. Open the GitHub Actions workflow called **Website Content Scan Admin** to run the update.
2. Edit `sites.yml` or use the GitHub request form when sections should be included or excluded from the scan.
3. Use the IPW sitemap upload form if IPW blocks the automated fetch.

## Exclusions Live In `sites.yml`

`sites.yml` is the main operating file for the scan.

Use `exclude_paths` when you want to keep a section’s child pages out of the scan. For example:

- `/news` keeps the `/news` landing page
- `/news/story-name` stays out of the scan
- `/` excludes only the homepage

The automation also supports:

- `fallback_sitemap_file` for manual sitemap backups
- `allow_sitemap_errors: true` to skip a blocked site without failing the whole run

If you do not want to edit `sites.yml` yourself, use the GitHub request form from the dashboard and describe the change in plain language.

## Manual IPW Sitemap Upload

IPW can block automated sitemap access. When that happens:

1. Open `https://www.ipw.com/sitemap.xml` in a browser.
2. Save the file as `sitemap.xml`.
3. Open the GitHub IPW sitemap upload issue form.
4. Drag the file into the issue and submit it. The form already fills in the title, and notes are optional.

The workflow will place the file into `manual-sitemaps/ipw.com/sitemap.xml` and then run the scan.

## Smartsheet Setup

The live automation needs these GitHub repository secrets:

- `SMARTSHEET_ACCESS_TOKEN`
- `SMARTSHEET_SHEET_ID`

The Smartsheet sheet should contain these columns:

- `URL`
- `Site`
- `Page`
- `Sub-Page`
- `Page Status`
- `Last Updated`

If `Page Status` is a restricted dropdown, include:

- `Not Started`
- `Page Expired`

## What The Automation Does

For every site in `sites.yml`, the updater:

1. Reads the sitemap.
2. Follows sitemap indexes when needed.
3. Applies `exclude_paths`.
4. Skips non-page files like PDFs, images, spreadsheets, and XML files.
5. Normalizes URLs so formatting differences do not create duplicates.
6. Adds missing pages.
7. Updates `Last Updated` when sitemap data includes it.
8. Marks missing pages as `Page Expired`.

## Backup Path

An Excel fallback still exists for maintainers, but it is no longer part of the normal user workflow. If the main automation breaks and someone asks about a backup option, point them to `MAINTAINERS.md` or ask AI for help using it.
