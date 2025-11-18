# GitHub Pages Setup Guide

Follow these simple steps to deploy your documentation to GitHub Pages.

## Prerequisites

- Your repository is already pushed to GitHub  
- The template includes the GitHub Actions workflow  
- You have admin access to your repository  

## Step 1: Enable GitHub Pages

1. **Go to your repository on GitHub**
2. **Click the "Settings" tab** (near the top right of the repository page)
3. **Scroll down to "Pages"** in the left sidebar
4. **Under "Source"**, select **"GitHub Actions"**
5. **Click "Save"**

[GitHub Pages Settings](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Step 2: Trigger First Deployment

The documentation will automatically deploy when you push changes to the main branch.

```bash
# If you haven't already pushed the template changes:
git add .
git commit -m "Setup documentation with GitHub Pages"
git push origin main
```

## Step 3: Monitor the Deployment

1. **Go to the "Actions" tab** in your repository
2. **You should see a workflow** called "Deploy Documentation to GitHub Pages"
3. **Wait for it to complete** (usually 2-3 minutes)
4. **Green checkmark = success!**

## Step 4: Access Your Live Documentation

Once deployment completes:

- **Your docs URL:** `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME`
- Example: `https://john-doe.github.io/my-python-project`

## You're Done!

Your documentation is now set up to automatically deploy to GitHub Pages! Every time you push to the main branch, your docs will be built and deployed.

To view your live documentation, visit: `https://yourusername.github.io/your-repo-name`

## Troubleshooting

### Build Failed?

**Check the Actions tab for error details. Common issues:**

- **Python syntax errors** in your source code
- **Broken markdown links** in documentation files
- **Missing dependencies** (usually auto-resolved)

### Pages Not Updating?

1. **Verify GitHub Pages source** is set to "GitHub Actions"
2. **Check if Actions are enabled** in your repository settings
3. **Ensure the workflow file exists** at `.github/workflows/docs.yml`

### 404 Error on Documentation Site?

- Wait 5-10 minutes for GitHub's CDN to update
- Check that the workflow completed successfully
- Verify your repository is public (or you have GitHub Pro for private repos)

## Next Steps

**Customize your documentation:**
- Edit `docs/index.md` for your homepage
- Add new pages in the `docs/` directory
- Update navigation in `mkdocs.yml`

**Enhance with custom domain:**
- Add a `CNAME` file to `docs/` directory
- Configure DNS settings with your domain provider

**Monitor and maintain:**
- Check Actions tab occasionally for failed builds
- Keep documentation updated as code changes

---

**Need help?** Check the [Documentation Setup Tutorial](tutorials/docs-setup.md) for advanced configuration options.