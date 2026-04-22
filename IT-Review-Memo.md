# IT Review Memo: Website Content Scan Automation

## To
IT Department

## From
Web and Digital / Marketing Team

## Subject
Request for IT Review of Website Content Scan Automation

## Date
April 22, 2026

## Purpose

This memo requests IT review of a custom internal automation developed to support website content review and governance. The tool helps our team maintain a current inventory of website pages in SmartSheet by scanning public website sitemap files and automatically updating the tracking sheet.

The goal of this request is to confirm that the automation is appropriate for ongoing internal use, identify any security or governance concerns, and determine the best long-term ownership model for the repository and its credentials.

## Business Need

Our team is responsible for reviewing and maintaining content across multiple public-facing website properties. Because website content changes regularly, it is difficult to reliably identify new pages, updated pages, and pages that are no longer present through manual review alone.

This creates an operational gap in our content review process:

- new pages can be missed
- outdated pages may remain unreviewed
- staff time is spent manually checking sitemap content
- the SmartSheet inventory can become incomplete over time

This automation was created to reduce that manual effort and support a more consistent content review workflow. It scans public site maps, compares the results against the current SmartSheet inventory, and updates the sheet so the team can focus on the review process itself rather than manual page discovery.

## System Overview

The Website Content Scan Automation is a lightweight custom program hosted in GitHub. It uses GitHub Actions to run on a schedule or on demand.

At a high level, the system:

1. Reads public XML sitemap files for configured websites
2. Identifies the pages listed in those sitemaps
3. Compares those pages against rows already in SmartSheet
4. Adds newly discovered pages to SmartSheet
5. Updates page metadata such as Last Updated when available
6. Marks rows as expired when pages are no longer found
7. Publishes a simple dashboard so staff can confirm status and run the process manually when needed

## Current Hosting and Ownership Note

The original version of this automation was built in Gabriel Citeli’s personal GitHub account as the initial setup repository.

If the tool is approved for continuing team use, it should be forked or transferred into a U.S. Travel-managed GitHub repository or organization account so that:

- the system is not dependent on an individual employee account
- repository access can be managed institutionally
- credentials and maintenance responsibility can be owned by the organization

## Data and Security Considerations

The automation was designed to keep scope narrow and limit the amount of sensitive integration involved.

Key points:

- It reads only public website sitemap files.
- It does not require website admin credentials.
- It does not access private website content.
- It writes to SmartSheet through the SmartSheet API.
- The SmartSheet API token is not stored in code.
- SmartSheet credentials are stored in GitHub Actions secrets.
- Access to the repository controls who can manage the workflow and view or update the automation.

This means the tool primarily acts as a bridge between public website sitemap data and an internal SmartSheet used for operational tracking.

## Repository Components

| Component | Purpose |
|---|---|
| `.github/workflows/update-website-content-scan.yml` | Main GitHub Actions workflow that runs the sitemap scan, updates SmartSheet, and refreshes dashboard data |
| `scripts/update_scan.py` | Core script that scans sitemap content, compares URLs, and writes changes to SmartSheet |
| `scripts/check_smartsheet_connection.py` | Verifies whether the configured SmartSheet connection is valid and reachable |
| `scripts/update_status_json.py` | Writes dashboard status data used by the GitHub Pages interface |
| `scripts/generate_sites_summary.py` | Creates a readable summary of configured sites and exclusions for the dashboard |
| `scripts/process_ipw_issue.py` | Handles a manual fallback upload flow for IPW sitemap files when that site cannot be pulled automatically |
| `sites.yml` | Main configuration file listing scanned sites and excluded paths or sections |
| `docs/index.html` | GitHub Pages dashboard used by staff to check status, run the workflow, and access support links |
| `docs/status.json` | Dashboard data file showing latest run status, SmartSheet connection state, and pages added |
| `docs/sites-summary.json` | Dashboard data file summarizing sites being scanned and their exclusions |
| `manual-sitemaps/` | Fallback location for manually uploaded sitemap files when a site blocks automated retrieval |
| `USER-GUIDE.md` | User-facing guide for operating and maintaining the automation |
| `MAINTAINERS.md` | Technical maintenance notes and backup/fallback guidance |
| `README.md` | Repository overview and setup context |
| `.github/ISSUE_TEMPLATE/ipw-sitemap-upload.yml` | GitHub issue form used for manual IPW sitemap upload fallback |

## Operational Support and Maintainability

I would not describe the tool as maintenance-free, but it was intentionally designed to be low-maintenance and narrow in scope.

A more accurate description is:

- it is a relatively simple, purpose-built automation
- it uses standard GitHub Actions workflow patterns
- it uses a single SmartSheet API integration
- it should require limited ongoing maintenance under normal conditions
- user-facing documentation has already been written to support day-to-day operation
- technical maintainer documentation and backup guidance also exist in the repository

The intent is not to leave behind an undocumented custom script, but rather a small operational tool with written instructions for both users and maintainers.

## User Support Readiness

The repository currently includes:

- a user guide for operating the automation
- troubleshooting guidance, including SmartSheet connection support
- instructions for manual fallback when a sitemap cannot be fetched automatically
- maintainer guidance for backup or recovery scenarios

These materials were created so the tool can be supported after transition and so non-technical staff can use the dashboard and GitHub workflow without relying on terminal-based setup or development workflows.

## Request to IT

We are requesting that IT review this automation and advise on the following:

- whether the tool is acceptable for ongoing internal use
- whether GitHub is an appropriate hosting and orchestration layer for this workflow
- whether the current use of GitHub Actions secrets is acceptable for storing the SmartSheet API token and sheet identifier
- whether the repository should be transferred or forked into a U.S. Travel-managed GitHub location
- whether any additional controls, review steps, or documentation are required before long-term team adoption

## Requested Outcome

We are seeking either:

- approval to continue using this automation in an organization-managed GitHub repository, or
- an alternative recommendation for how this workflow should be hosted or managed

## Closing

This automation supports an existing business need: maintaining an accurate SmartSheet inventory of website content for review. It reduces manual work, improves consistency, and helps ensure new or changed pages are not overlooked.

If approved, the next logical step would be to move the repository into a U.S. Travel-managed GitHub location and continue using the existing user guide and maintenance materials to support the team going forward.
