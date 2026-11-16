---
name: create-new-section
description: Automates creation of Shopify section modules with Liquid, TypeScript, and SCSS files
license: MIT
compatibility: opencode
metadata:
  framework: shopify
  audience: developers
  workflow: theme-development
---

# Create New Shopify Section

This skill automates the creation of a new Shopify section module with all necessary files and configurations. This is a **global skill** that works across all Shopify projects.

## What I do

- Parse and convert section names to kebab-case format
- Create Liquid section files with proper schema
- Generate TypeScript and SCSS module files
- Update build configurations (esbuild, webpack, or vite)
- Update SASS compilation scripts in package.json
- Provide a complete summary of created files

## When to use me

Use this skill when you need to create a new Shopify section module in your theme. I'll handle all the boilerplate setup so you can focus on building the actual functionality.

## Prerequisites Check

Before starting, I verify the project structure:
1. Check if `theme/sections/` directory exists (Shopify theme structure)
2. Check if `package.json` exists
3. If structure doesn't match, inform the user and ask if they want to proceed anyway

## Step 1: Parse and Validate Section Name

1. Accept the section name from the user (e.g., "Image Text", "image text", or "image-text")
2. Convert the section name to kebab-case format:
   - Convert to lowercase
   - Replace spaces with hyphens
   - Remove any special characters except hyphens
   - Example: "Image Text" → "image-text"
3. Store both formats:
   - `kebab-case-name`: for file names (e.g., "image-text")
   - `Title Case Name`: for display names (e.g., "Image Text")

## Step 2: Ask User About File Requirements

Ask the user which files they want to create:
- TypeScript file (index.ts)?
- SCSS file (_index.scss)?
- Both? (default)

Store the user's choice for later steps.

## Step 3: Detect Project Structure

Look for the following directories to determine the structure:
- Section directory: `theme/sections/` or `sections/`
- Includes directory: `src/_includes/` or `app/sections/` or `sections/`
- Scripts directory: `src/scripts/` or `app/javascript/` or `assets/`

If custom structure is detected, ask the user to confirm the paths.

## Step 4: Create Liquid File

Create the file in the appropriate section directory (usually `theme/sections/{kebab-case-name}.liquid`)

Use this template structure:

```liquid
<link rel="stylesheet" href="{{ '{kebab-case-name}.min.css' | asset_url }}">

<div {% render 'section-properties' %}>

</div>

<script src="{{ '{kebab-case-name}.min.js' | asset_url }}" defer></script>


{% schema %}
{
  "name": "{Title Case Name}",
  "tag": "section",
  "class": "{kebab-case-name} as-{kebab-case-name}",
  "settings": [
      {
        "type": "header",
        "content": "Section space"
      },
      {
        "type": "select",
        "id": "section_top",
        "label": "Section top space",
        "options": [
          {
            "value": "0",
            "label": "None"
          },
          {
            "value": "extra-small",
            "label": "Extral small"
          },
          {
            "value": "small",
            "label": "Small"
          },
          {
            "value": "medium",
            "label": "Medium"
          },
          {
            "value": "large",
            "label": "Large"
          },
          {
            "value": "extra-large",
            "label": "Extra large"
          }
        ],
        "default": "0"
      },
      {
        "type": "select",
        "id": "section_bottom",
        "label": "Section bottom space",
        "options": [
          {
            "value": "0",
            "label": "None"
          },
          {
            "value": "extra-small",
            "label": "Extral small"
          },
          {
            "value": "small",
            "label": "Small"
          },
          {
            "value": "medium",
            "label": "Medium"
          },
          {
            "value": "large",
            "label": "Large"
          },
          {
            "value": "extra-large",
            "label": "Extra large"
          }
        ],
        "default": "0"
      }
    ]
}
{% endschema %}
```

## Step 5: Create Module Directory and Files

1. Create directory in the detected includes path: `{includes-path}/{kebab-case-name}/`

2. If user wants TypeScript file, create `{includes-path}/{kebab-case-name}/index.ts`:
```typescript
// as-{kebab-case-name}
```

3. If user wants SCSS file, create `{includes-path}/{kebab-case-name}/_index.scss`:
```scss
.{kebab-case-name} {
  
}
```

## Step 6: Update Build Configuration Files

### 6.1 Detect and Update Build Tool Configuration

**For esbuild projects:**
- Look for `esbuild.config.js` and `esbuild.dev.config.js`
- Find the `entryPoints` object
- Add new entry: `'{kebab-case-name}.min': '{includes-path}/{kebab-case-name}/index.ts'`
- **CRITICAL**: Use the correct format with `.min` suffix and proper path
- Example: `'image-text-with-card.min': 'src/_includes/image-text-with-card/index.ts'`
- Ensure proper comma placement (add comma after previous last entry)

**For webpack projects:**
- Look for `webpack.config.js` or `config/webpack/*.js`
- Add entry point according to the webpack configuration structure

**For vite projects:**
- Look for `vite.config.js` or `vite.config.ts`
- Update build configuration if necessary

If no build tool is detected, inform the user and provide manual instructions.

### 6.2 Update Style Compilation Configuration

**For SASS/SCSS:**
- Look for package.json scripts with sass/scss compilation
- Identify both `develop:style` and `build:style` scripts (or similar)
- Add to the END of the script string: ` {includes-path}/{kebab-case-name}/_index.scss:theme/assets/{kebab-case-name}.min.css`
- **CRITICAL**: These scripts are often very long single-line strings
- Use sed or similar to append to the end of the line before the closing quote
- Update both development and build scripts if they exist

**Example sed command:**
```bash
sed -i '' 's/last-module-name.min.css"/last-module-name.min.css src\/_includes\/{kebab-case-name}\/_index.scss:theme\/assets\/{kebab-case-name}.min.css"/' package.json
```

**For other CSS preprocessors:**
- Detect and update accordingly

If no style compilation is detected, inform the user and provide manual instructions.

## Step 7: Summary Report

After all files are created and configurations updated, provide a summary:

```
✅ New section '{Title Case Name}' created successfully!

Files created:
- theme/sections/{kebab-case-name}.liquid
- src/_includes/{kebab-case-name}/index.ts
- src/_includes/{kebab-case-name}/_index.scss

Configuration updated:
- esbuild.config.js (line X)
- esbuild.dev.config.js (line Y)
- package.json develop:style script (line Z)
- package.json build:style script (line W)

Compiled assets (generated on build):
- theme/assets/{kebab-case-name}.min.js
- theme/assets/{kebab-case-name}.min.css

Next steps:
1. Run `yarn develop` or `npm run dev`
2. Add your content to theme/sections/{kebab-case-name}.liquid
3. Add JavaScript functionality to src/_includes/{kebab-case-name}/index.ts
4. Add styles to src/_includes/{kebab-case-name}/_index.scss
5. The section will be available in Shopify theme customizer as "{Title Case Name}"
```

## Important Notes

- **Always read configuration files before editing** to understand their current structure
- Adapt to different Shopify project structures automatically
- Always validate that files don't already exist before creating them
- Ensure proper JSON/JS syntax when updating configuration files
- Maintain consistent indentation and formatting matching the project
- Handle edge cases (e.g., missing commas, special characters in names)
- If any step fails, report the error clearly and suggest solutions
- If project structure is non-standard, ask for user confirmation before proceeding
- **For very long script lines**: Use bash tools (sed, awk) instead of trying to edit in the Edit tool

## Error Handling

- If section name is invalid, ask user to provide a valid name
- If files already exist, ask user if they want to overwrite
- If configuration update fails, report the specific issue and provide manual steps
- If project structure is not recognized, ask user to specify paths manually
- If esbuild entry format is wrong, verify the correct pattern from existing entries

## Common Mistakes to Avoid

1. ❌ Wrong esbuild entry format: `'image-text-with-card': '...'`
   ✅ Correct: `'image-text-with-card.min': '...'`

2. ❌ Not reading files before editing
   ✅ Always use Read tool first

3. ❌ Trying to edit very long single-line strings with Edit tool
   ✅ Use sed or awk for long script strings in package.json

4. ❌ Forgetting to add commas after previous entries
   ✅ Always check proper JSON/JS syntax

## Compatibility

This skill is designed to work with:
- Standard Shopify themes
- Theme Kit projects
- Shopify CLI projects
- Custom Shopify theme structures
- Projects using esbuild, webpack, or vite
- Projects using SASS, SCSS, or other CSS preprocessors

The skill automatically adapts to the detected project structure.
