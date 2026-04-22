# Website Content Scan Automation — User Guide

---

## Contents

1. [Overview](#1-overview)
2. [Getting Started / Running the Automation](#2-getting-started--running-the-automation)
3. [How the Automation Works](#3-how-the-automation-works)
4. [Key Components](#4-key-components)
5. [How to Verify It Worked](#5-how-to-verify-it-worked)
6. [How New Pages Are Added](#6-how-new-pages-are-added)
7. [Troubleshooting](#7-troubleshooting)
8. [Maintenance / Updating the System](#8-maintenance--updating-the-system)
9. [Best Practices](#9-best-practices)
10. [Appendix](#10-appendix)

---

## 1. Overview

The Website Content Scan automation monitors website sitemaps for several U.S. Travel Association properties, identifies new and updated pages, and automatically adds them to the Website Content Scan SmartSheet. This keeps the sheet current without requiring anyone to manually check each site for new content.

The automation runs on a weekly schedule and can also be triggered manually at any time. Results are visible through a live dashboard and reflected in SmartSheet within minutes of a successful run.

**What this system does:**

- Scans the sitemaps for each configured website
- Identifies pages not yet in SmartSheet
- Adds new pages with their URL, Site, Page, Sub-Page, and Last Updated fields populated
- Marks pages that have been removed from the site as Page Expired
- Reports results to a live dashboard

**What this system does not do:**

- Evaluate or prioritize content — that remains a human judgment call
- Scan sections that are excluded by configuration (such as /news or /press on ustravel.org)
- Automatically add new sites — that requires a configuration update in `sites.yml`

---

## 2. Getting Started / Running the Automation

This section covers everything you need to operate the system. All steps use the GitHub web interface or the dashboard — no software installation or command-line access is required.

---

### Setting Up for a New Owner

If you are taking over ownership of this automation from someone else, work through these steps before anything else. If the system is already running and you just need to use it, skip to [Opening the Dashboard](#opening-the-dashboard).

**Step 1 — Get repository access**

You need a GitHub account and collaborator access to the repository. If you do not have one yet, create a free account at **github.com**.

Ask the current owner or your GitHub organization administrator to invite you as a collaborator. They do this by going to the repository, clicking **Settings**, selecting **Collaborators and teams** in the left sidebar, and searching for your GitHub username. You will receive an email invitation — accept it to gain access.

Once accepted, the repository is available at:

**github.com/gzciteli/website-content-scan**

For all day-to-day tasks in this guide, the GitHub web interface is sufficient. If you ever need a local copy of the files on your computer — for example, to make more complex edits — download **GitHub Desktop** from desktop.github.com. It allows you to work with the repository without using the terminal.

**Step 2 — Verify the system is running**

Open the dashboard at **https://gzciteli.github.io/website-content-scan/** and confirm:

- **Latest result** shows **success**
- **Smartsheet connection** shows **Connected**
- **Last time it ran** shows a recent date

If all three look healthy, the system is working and you can proceed to operate it normally. If any card shows an error or an outdated date, see [Troubleshooting](#7-troubleshooting).

**Step 3 — Set up SmartSheet credentials (only needed if starting fresh)**

The automation connects to SmartSheet using an API token. This token is stored securely in GitHub. If you are taking over a working system, the token is already in place and you do not need to do anything. If you are setting up from scratch or the credentials have been lost, follow these steps.

*Get an API token from SmartSheet:*

1. Log in to SmartSheet and click your profile icon in the top-right corner.
2. Select **Apps & Integrations**.
3. Under **API Access**, click **Generate new access token**.
4. Give the token a name (e.g., "Website Content Scan") and confirm.
5. Copy the token that appears. **This is the only time you will be able to see it.** Paste it somewhere safe temporarily.

*Get the Sheet ID:*

1. Open the Website Content Scan sheet in SmartSheet.
2. Go to **File > Properties**.
3. The **Sheet ID** is listed there as a long number. Copy it.

*Save both values as GitHub Secrets:*

1. Go to the repository at **github.com/gzciteli/website-content-scan**.
2. Click **Settings** in the top navigation bar.
3. In the left sidebar, click **Secrets and variables**, then **Actions**.
4. Click **New repository secret**.
5. For the first secret: Name it `SMARTSHEET_ACCESS_TOKEN` and paste the API token as the value. Click **Add secret**.
6. Repeat for the second secret: Name it `SMARTSHEET_SHEET_ID` and paste the Sheet ID as the value. Click **Add secret**.

Once both secrets are saved, run the workflow manually (see [Running the Workflow Manually](#running-the-workflow-manually)) and confirm the **Smartsheet connection** card on the dashboard shows **Connected**.

---

### Opening the Dashboard

The dashboard is the primary interface for checking status and taking action. Open it at:

**https://gzciteli.github.io/website-content-scan/**

The dashboard is titled **Sitemap Automation**. At the top it shows five status cards: when the automation last ran, when the next scheduled run is (in your local time), whether the last run succeeded, whether SmartSheet is connected, and how many pages were added. Below that are sections for the IPW manual upload and for viewing and editing the list of scanned sites.

---

### Understanding the Automatic Schedule

The workflow runs automatically once a week — on Friday evening for U.S.-based users (1:00 AM UTC Saturday). The **Next automatic fetch** card on the dashboard shows the exact time of the next scheduled run in your local time zone.

If the scheduled run is coming up soon and fits your timeline, you do not need to do anything. The scan will run on its own.

---

### Running the Workflow Manually

If you need the scan to run before the next scheduled time:

1. Open the dashboard and click **Open the workflow**. This opens the GitHub Actions page for the workflow in a new tab.
2. On the Actions page, locate the **Run workflow** button on the right side of the screen and click it. A small dropdown will appear.
3. Click the green **Run workflow** button inside the dropdown to confirm.
4. The workflow will start within a few seconds. You can refresh the Actions page to see it running.

The workflow typically completes in under two minutes. Once it finishes, the dashboard will update to reflect the latest status.

> **Note on dashboard timing:** The dashboard is published by GitHub Pages, which updates shortly after the workflow commits its status file. If the dashboard does not immediately show the latest result after the run finishes, wait about a minute and refresh the page.

---

### Checking Whether the SmartSheet Connection Is Working

After any run, check the **Smartsheet connection** card on the dashboard:

- **Connected** — the API credentials are valid and the sheet is reachable; rows were written successfully
- **Needs attention** — the connection check failed; new pages found during the scan may not have been written to SmartSheet
- **Not checked yet** — no run has occurred since the system was last reset

If the connection shows **Needs attention**, see the [Troubleshooting](#7-troubleshooting) section.

---

### Using the IPW Manual Upload Fallback

ipw.com occasionally blocks automated sitemap requests, even though the sitemap opens normally in a browser. When this happens, use the manual upload flow built into the dashboard.

**Step-by-step:**

1. Open **https://www.ipw.com/sitemap.xml** in Chrome.
2. In Chrome, go to **File > Save Page As**.
3. Save the file to your computer. Name it **sitemap.xml** exactly.
4. Return to the dashboard and click **Open IPW upload form**. This opens a GitHub issue form in a new tab.
5. Drag the **sitemap.xml** file you saved into the issue form. You will see it appear as an attachment.
6. The title is already filled in — you do not need to change it. Notes are optional.
7. Click **Submit new issue**.

After submission, the automation detects the uploaded file, saves it into the repository, and immediately runs the full content scan — the same scan that runs on the weekly schedule. You do not need to trigger anything separately. When the process completes, the GitHub issue will be closed automatically with a confirmation comment, and the dashboard will reflect the updated results.

The **Manual IPW upload** section of the dashboard shows the date of the last processed upload and whether it succeeded, so you can confirm the file was received and the scan ran.

---

## 3. How the Automation Works

When the workflow runs — whether on schedule, manually, or triggered by an IPW upload — it follows these steps for each site configured in `sites.yml`:

1. **Fetches the sitemap.** The automation requests the XML sitemap from the live website. For ipw.com, if the live request fails, it uses the most recently uploaded manual sitemap file instead.
2. **Follows sitemap indexes.** Many sitemaps point to sub-sitemaps rather than listing pages directly. The automation follows those links and collects all underlying URLs.
3. **Applies exclusions.** Any paths listed under `exclude_paths` in `sites.yml` are skipped. For example, if `/news` is excluded on ustravel.org, pages under `/news/` will not be added to SmartSheet.
4. **Filters non-page files.** PDFs, images, spreadsheets, XML files, and other non-HTML assets are automatically excluded.
5. **Normalizes URLs.** Minor formatting differences — such as trailing slashes — are resolved so the same page is never added more than once.
6. **Compares against SmartSheet.** Each URL found in the sitemap is checked against existing rows in SmartSheet.
7. **Adds new pages.** Pages not already present in SmartSheet are added as new rows, with all relevant fields populated.
8. **Updates Last Updated.** For pages already in SmartSheet, the Last Updated field is refreshed if the sitemap provides a newer modification date.
9. **Marks removed pages.** Pages previously in SmartSheet that are no longer found in the sitemap are updated to **Page Expired**.

---

## 4. Key Components

### The Dashboard

**URL:** https://gzciteli.github.io/website-content-scan/

The dashboard is the primary place to check run status, review results, and access quick-action buttons. It is a GitHub Pages site updated automatically after each workflow run.

---

### The Workflow

**Name:** Website Content Scan Admin

The workflow is the engine that runs the scan. It lives under the **Actions** tab of the repository. This is the only workflow most users will ever need to interact with. It can be triggered manually or will run automatically on schedule.

---

### `sites.yml`

This file controls which sites are scanned and which sections are excluded. It is the only file most users ever need to edit. It lives in the root of the repository.

Each entry in the file can include:

| Setting | Purpose |
|---|---|
| `name` | A label used in SmartSheet and the dashboard |
| `sitemap` | The URL of the site's XML sitemap |
| `exclude_paths` | Page path prefixes to skip (optional) |
| `fallback_sitemap_file` | A local file to use if the live sitemap is unavailable |
| `allow_sitemap_errors` | If true, a failure on this site will not stop the rest of the scan |

**Exclusion path behavior:** A path like `/news` excludes pages whose URL path begins with `/news/` (such as `/news/story-title`), but does not exclude the `/news` landing page itself. To exclude the homepage only, list `/`.

---

### The IPW Upload Form

The IPW upload form is a GitHub issue template. Submitting it places the sitemap file into the repository and immediately triggers the content scan. It is accessible from the dashboard and from the repository's Issues tab (via **New issue**).

---

### The SmartSheet

The SmartSheet is the destination for all scan results. The automation populates these columns:

| Column | Description |
|---|---|
| URL | Full page URL, normalized |
| Site | Site name as configured in `sites.yml` (e.g., ustravel.org) |
| Page | Top-level page path (e.g., /about) |
| Sub-Page | Second-level path segment, when applicable (e.g., /leadership) |
| Page Status | Set to **Not Started** for new pages; **Page Expired** for removed pages |
| Last Updated | Date the page was last modified, sourced from the sitemap when available |

---

## 5. How to Verify It Worked

After a workflow run completes, use the following checks to confirm it succeeded.

### On the Dashboard

1. Open **https://gzciteli.github.io/website-content-scan/**
2. Confirm **Latest result** shows **success**
3. Confirm **Smartsheet connection** shows **Connected**
4. Check **Pages added last run** to see how many new pages were found
5. Click **See which pages** to view the specific pages that were added, including their site, page path, and URL

### In GitHub Actions

1. Go to the repository at **github.com/gzciteli/website-content-scan**
2. Click the **Actions** tab
3. Find the most recent run of **Website Content Scan Admin**
4. A green checkmark indicates the run completed successfully; a red X indicates it failed

### In SmartSheet

Open the Website Content Scan sheet and look for rows with a **Page Status** of **Not Started** added recently, or rows where **Last Updated** was refreshed. Newly added rows will appear at the bottom of the sheet unless sorting has been applied.

> **Timing note:** The dashboard reflects the run as soon as GitHub Pages finishes publishing the updated status file — typically one to two minutes after the workflow completes. If you check immediately after the run finishes in Actions, the dashboard may still show the previous run's data. Wait a moment and refresh.

---

## 6. How New Pages Are Added

When the automation finds a URL that is not already in SmartSheet, it adds a new row with the following fields populated:

| Field | Value |
|---|---|
| URL | The full page address |
| Site | The name of the website (e.g., ustravel.org) |
| Page | The top-level section of the URL path (e.g., /about) |
| Sub-Page | The next level of the path, if present (e.g., /leadership) |
| Page Status | Set to **Not Started** |
| Last Updated | Pulled from the sitemap's last-modified date, when available |

Pages are added only once. If a page is already in SmartSheet under any status, the automation will not create a duplicate row.

If a page that was previously in SmartSheet is no longer found in the sitemap, its **Page Status** is updated to **Page Expired**. This indicates the page may have been removed from the site or its URL may have changed.

---

## 7. Troubleshooting

### The workflow failed in GitHub Actions

**What you will see:** A red X next to the run in the Actions tab. The dashboard **Latest result** card will show **failure**.

**What to do:**

1. Click on the failed run in the Actions tab to open the run details.
2. Expand the failed step to read the error message.
3. Common causes include a temporary network issue when fetching a sitemap, or a problem with the SmartSheet credentials.
4. For a one-time failure, try running the workflow again manually. Most transient failures resolve on their own.
5. If the failure repeats, note the error message and contact a technical maintainer.

---

### The SmartSheet connection shows "Needs attention"

**What you will see:** The **Smartsheet connection** card on the dashboard shows **Needs attention** after a run.

**What this means:** The automation was unable to verify a connection to SmartSheet. New pages found during the scan may not have been written to the sheet.

**What to do:**

1. Confirm the Website Content Scan sheet still exists and has not been renamed, moved, or deleted.
2. The SmartSheet API token may have expired. This is stored in the repository's GitHub Secrets and requires a technical maintainer to update.
3. If you are not sure, contact a technical maintainer and share the dashboard screenshot.

---

### IPW could not be fetched automatically

**What you will see:** The workflow completes successfully overall, but no new IPW pages are added. The dashboard workflow message may indicate IPW was skipped or failed.

**What to do:**

This is a known limitation — ipw.com occasionally blocks automated requests. Use the manual IPW upload flow described in [Getting Started](#2-getting-started--running-the-automation). The upload takes only a few minutes and triggers the scan automatically.

---

### The dashboard does not reflect the latest run

**What you will see:** After a successful run in Actions, the dashboard still shows an older timestamp or result.

**What to do:**

Wait one to two minutes and refresh the page. The dashboard is published by GitHub Pages, which processes the updated status file shortly after the workflow completes. There is a brief delay between when the workflow finishes and when the dashboard reflects it. If the dashboard still appears stale after a few minutes, check that the run in Actions ended with a green checkmark rather than a failure.

---

### Pages are not appearing in SmartSheet

**What you will see:** The dashboard shows a successful run, but expected pages are missing from SmartSheet.

**What to check:**

- Confirm **Smartsheet connection** shows **Connected** — if it shows **Needs attention**, the scan ran but could not write to SmartSheet
- Check whether the pages in question fall under an excluded path in `sites.yml` (e.g., `/news` on ustravel.org)
- Confirm the pages are actually present in the site's sitemap by opening the sitemap URL directly in a browser
- If the pages were already in SmartSheet under any status, the automation will not add a duplicate row

---

## 8. Maintenance / Updating the System

### Adding a New Site to the Scan

Open `sites.yml` in GitHub — the dashboard's Sites and exclusions section includes a direct **Open sites.yml** link. Add a new entry following the pattern of the existing sites. At minimum, a new site needs a `name` and a `sitemap` URL. An AI assistant can prepare the update for you if you describe what you want.

Changes take effect on the next workflow run.

---

### Updating Exclusions

Exclusions are managed within `sites.yml` under the `exclude_paths` key for each site. To exclude a new section, add its path to the list. To stop excluding a section, remove it.

Exclusion paths use a prefix rule: `/news` excludes all pages whose path starts with `/news/`, but the `/news` landing page itself is still included. To exclude only the homepage, use `/`.

---

### Removing a Site from the Scan

Open `sites.yml` and delete the entry for the site you want to remove. The automation will stop scanning it on the next run. Existing rows in SmartSheet will not be affected — they will not be automatically removed.

---

### Rotating SmartSheet Credentials

If the SmartSheet API token is rotated or expires, the new token must be updated in the repository's GitHub Secrets. This is done under **Settings > Secrets and variables > Actions** in the repository. The relevant secrets are:

- `SMARTSHEET_ACCESS_TOKEN` — the SmartSheet API token
- `SMARTSHEET_SHEET_ID` — the numeric ID of the Website Content Scan sheet

Updating secrets requires repository admin access. If you are not comfortable with this step, ask a technical maintainer.

---

### Emergency Backup Option

If the normal GitHub and SmartSheet automation breaks entirely and cannot be quickly restored, a backup path exists. A maintainer can run the scan locally and export results to an Excel workbook. This process is documented in `MAINTAINERS.md` in the repository root.

This backup is not part of the normal workflow and is intended only for emergency recovery. If you think you need it, ask a technical maintainer or AI assistant to guide you through it.

---

## 9. Best Practices

**Let the schedule do the work.** The automation runs weekly automatically. Before triggering a manual run, check the **Next automatic fetch** time on the dashboard. If the scheduled run is within a day or two, it is usually better to wait.

**Check the dashboard before escalating.** Most questions about whether the scan ran and what it found can be answered from the dashboard in seconds, without needing to open GitHub Actions or contact anyone.

**Upload the IPW sitemap in advance of review cycles.** If IPW content is needed for an upcoming content review and the automated fetch has been failing, submit the manual upload a day or two before you need it rather than waiting until the last moment.

**Review new pages before acting on them.** The automation adds pages with a status of **Not Started**. This is a neutral starting point — it does not indicate urgency. Use the existing content review process to prioritize newly discovered pages.

**Keep `sites.yml` tidy.** When a site is removed from scope, remove it from `sites.yml` so the automation does not continue attempting to scan it. Sites with persistent failures that go unnoticed create noise in the workflow history.

**Do not manually edit files in the `docs/` folder.** The files `docs/status.json` and `docs/sites-summary.json` are written automatically by the workflow. Any manual edits will be overwritten on the next run.

---

## 10. Appendix

### Sites Currently in the Scan

| Site | Sitemap URL | Excluded Sections |
|---|---|---|
| ustravel.org | https://www.ustravel.org/sitemap.xml | / (homepage), /news, /press, /research |
| ipw.com | https://www.ipw.com/sitemap.xml | None (manual fallback used if blocked) |
| esto.ustravel.org | https://www.esto.ustravel.org/sitemap.xml | /attendees, /events, /speakers |

---

### SmartSheet Column Reference

| Column | Set by | Notes |
|---|---|---|
| URL | Automation | Full page URL, normalized to avoid duplicates |
| Site | Automation | Site name from `sites.yml` |
| Page | Automation | Top-level path segment |
| Sub-Page | Automation | Second-level path segment, if applicable |
| Page Status | Automation | **Not Started** for new pages; **Page Expired** for removed pages |
| Last Updated | Automation | From sitemap; not always present for every page |

---

### Quick Reference — Where to Find Things

| Task | Where to go |
|---|---|
| Check run status | Dashboard → Latest result card |
| See when the next run is scheduled | Dashboard → Next automatic fetch card |
| Run the workflow manually | Dashboard → Open the workflow → Run workflow |
| Check SmartSheet connection | Dashboard → Smartsheet connection card |
| See which pages were added | Dashboard → Pages added last run → See which pages |
| Upload an IPW sitemap | Dashboard → Open IPW upload form |
| View or update scanned sites and exclusions | Dashboard → Sites and exclusions → Open sites.yml |
| Review workflow run logs | GitHub → Actions tab → Website Content Scan Admin |
| Emergency backup path | `MAINTAINERS.md` in the repository root |

---

### Key Links

| Resource | URL |
|---|---|
| Dashboard | https://gzciteli.github.io/website-content-scan/ |
| Repository | https://github.com/gzciteli/website-content-scan |
| Workflow (Actions) | https://github.com/gzciteli/website-content-scan/actions/workflows/update-website-content-scan.yml |
| sites.yml | https://github.com/gzciteli/website-content-scan/blob/main/sites.yml |
| IPW upload form | https://github.com/gzciteli/website-content-scan/issues/new?template=ipw-sitemap-upload.yml |
| MAINTAINERS.md | https://github.com/gzciteli/website-content-scan/blob/main/MAINTAINERS.md |
