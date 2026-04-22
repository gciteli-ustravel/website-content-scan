# Manual Sitemaps

This folder is the easy-to-find fallback location for sitemap files that cannot be fetched automatically.

Why this exists:

- Some websites, especially `ipw.com`, can block automated sitemap downloads even when the sitemap opens in a normal browser.
- When that happens, the automation can use a manually uploaded sitemap file from this folder instead.

How it works:

- The IPW fallback file lives at `manual-sitemaps/ipw.com/sitemap.xml`.
- The automation first tries the live IPW sitemap.
- If that fails, it looks for the manual fallback file here.

How non-technical users should use it:

1. Open the dashboard or the IPW upload issue form.
2. Download the IPW sitemap from the browser.
3. Submit it through the GitHub upload form.

The workflow will place the file in this folder automatically. Most users should not need to edit anything here by hand.
