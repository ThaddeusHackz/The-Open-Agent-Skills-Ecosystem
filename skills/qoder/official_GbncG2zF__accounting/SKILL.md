---
name: accounting
description: Akaunting browser automation - create invoices, log bills, manage customers/vendors, check dashboard
user-invocable: true
---

# Akaunting Browser Automation

Automate accounting tasks in Akaunting using the `mcp__claude-in-chrome__*` browser tools. Handles creating sales invoices, logging purchase bills, managing customers/vendors, and checking the dashboard.

## Setup

1. Call `tabs_context_mcp` to get current browser tabs
2. Create a new tab with `tabs_create_mcp`
3. Navigate to the Akaunting instance URL (e.g. `https://accounting.com/{company}/`)
4. Take a `screenshot` to confirm Akaunting is loaded and logged in

## Outbound: Sales Invoices

### Create a new invoice

1. Navigate to `/{company}/sales/invoices/create` or use sidebar: Sales > Invoices, then click "New Invoice" button
2. Take a `screenshot` to see the invoice form

### Fill invoice fields

1. **Customer**: Use `find` with `"customer"` or `"contact"` to locate the customer dropdown. `left_click` to open it, then `type` the customer name to search. Select from results or create a new customer if not found.
2. **Invoice Date**: Use `find` with `"invoice date"` to locate the date field. `left_click` and `type` the date (format: DD/MM/YYYY or as shown)
3. **Due Date**: Use `find` with `"due date"` to locate and set the due date
4. **Invoice Number**: Usually auto-generated. Override by clicking the invoice number field and typing a new value if needed.

### Add line items

1. Use `find` with `"Add an Item"` or `"add item"` button and `left_click` it
2. For each line item:
   - **Name/Description**: Use `find` with `"item name"` or the first input in the new row. `left_click` and `type` the item description (e.g. "Sponsorship", "Consulting Services")
   - **Quantity**: Use `find` with `"quantity"` field. `left_click` and `type` the quantity
   - **Price**: Use `find` with `"price"` field. `left_click` and `type` the unit price
3. Repeat for additional line items by clicking "Add an Item" again

### Save the invoice

1. Use `find` with `"Save"` button at the bottom of the form
2. `left_click` the Save button
3. Take a `screenshot` to confirm the invoice was saved
4. The invoice will be created as a Draft by default

### Download invoice PDF

1. After saving, you should be on the invoice detail page
2. Use `find` with `"PDF"` or `"download"` button to locate the PDF download button
3. **Confirm with the user before downloading**
4. `left_click` the PDF button to download
5. Note the downloaded file for later use (e.g. attaching to an email via the Gmail skill)

## Inbound: Purchase Bills

### Create a new bill

1. Navigate to `/{company}/purchases/bills/create` or use sidebar: Purchases > Bills, then click "New Bill" button
2. Take a `screenshot` to see the bill form

### Fill bill fields

1. **Vendor**: Use `find` with `"vendor"` or `"contact"` to locate the vendor dropdown. `left_click` to open it, then `type` the vendor name to search. If the vendor doesn't exist, you'll need to create one first (see Vendor Management below).
2. **Bill Number**: Use `find` with `"bill number"` and enter the invoice/bill number from the source document
3. **Bill Date**: Use `find` with `"bill date"` or `"billed at"` and enter the date from the invoice
4. **Due Date**: Use `find` with `"due date"` and enter the payment due date

### Add line items from extracted invoice data

1. Use `find` with `"Add an Item"` and `left_click`
2. For each line item from the source invoice:
   - Enter the item description, quantity, and price matching the original invoice
3. Verify the total matches the source invoice amount

### Save the bill

1. Use `find` with `"Save"` button and `left_click`
2. Take a `screenshot` to confirm the bill was saved
3. Optionally mark as "Received" if the goods/services have been delivered

## Customer Management

### Create a new customer

1. Navigate to `/{company}/sales/customers/create` or sidebar: Sales > Customers > New Customer
2. Fill in:
   - **Name**: Use `find` with `"name"` field and type the customer name
   - **Email**: Use `find` with `"email"` field and type the email address
   - **Currency**: Set if different from default
3. `left_click` Save

## Vendor Management

### Create a new vendor

1. Navigate to `/{company}/purchases/vendors/create` or sidebar: Purchases > Vendors > New Vendor
2. Fill in:
   - **Name**: Use `find` with `"name"` field and type the vendor name
   - **Email**: Use `find` with `"email"` field and type the email address
   - **Currency**: Set if different from default
3. `left_click` Save
4. Return to the bill creation flow

## Dashboard Verification

### Check financial summary

1. Navigate to `/{company}/` (the main dashboard)
2. Take a `screenshot` to see the dashboard widgets
3. Use `get_page_text` to extract dashboard values
4. Look for key widgets:
   - **Receivables**: Outstanding invoices owed to you
   - **Payables**: Outstanding bills you owe
   - **Cash Flow**: Income vs expenses chart
   - **Latest Income / Latest Expenses**: Recent transaction lists

## Key Akaunting UI Patterns

- **Sidebar navigation**: Left sidebar with sections: Sales, Purchases, Banking, Reports
- **Sales submenu**: Invoices, Revenues, Customers
- **Purchases submenu**: Bills, Payments, Vendors
- **"Add an Item" button**: Adds a new line item row in invoice/bill forms
- **Quick Actions (+)**: Floating action button (usually top-right) for shortcuts to create invoices, bills, etc.
- **Save button**: Bottom of forms, typically a green or blue button
- **PDF button**: On invoice/bill detail pages, generates and downloads a PDF
- **Status badges**: Draft, Sent, Paid, Overdue etc. shown on document list/detail pages

## Tips

- Akaunting pages load dynamically - always `screenshot` after navigation
- Use `read_page` with `filter: "interactive"` if `find` doesn't locate form fields
- Date formats may vary by Akaunting locale settings - check the existing format before entering dates
- Currency is usually set at the customer/vendor level - set it when creating the contact
- After creating invoices or bills, navigate to the Dashboard to verify totals updated correctly
- Use the sidebar for navigation rather than URL guessing when possible
- If a dropdown doesn't respond to typing, try `left_click` to open it first, then use `find` to locate options in the dropdown list
