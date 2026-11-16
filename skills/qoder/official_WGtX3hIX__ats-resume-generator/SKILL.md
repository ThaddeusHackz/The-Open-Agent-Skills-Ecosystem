---
name: ats-resume-generator
description: >
  Generates high-impact, ATS-optimized resumes in reverse chronological format from raw, messy, or unstructured user input — including work history, LinkedIn dumps, project notes, internship descriptions, education details, certifications, skills lists, GitHub links, and anything else the user provides. Use this skill immediately whenever the user wants to write, build, create, update, improve, or generate a resume, CV, or job application document — even if they just paste a wall of notes and say "make me a resume out of this." Also trigger when the user asks to rewrite bullet points, optimize a resume for ATS, tailor a resume to a job description, or turn a LinkedIn profile into a resume.
---

# ATS Resume Generator

Your job is to take whatever the user gives you — raw notes, half-finished bullet points, LinkedIn dumps, job descriptions from memory, project descriptions, anything — and turn it into a polished, recruiter-ready, ATS-compliant resume delivered as a **compilable LaTeX document**. The user's raw input is valuable raw material; your job is to refine it into gold.

## Understanding the Goal

ATS (Applicant Tracking Systems) are the software gatekeepers that scan resumes before a human ever sees them. They reward:
- Simple, linear formatting (no tables, columns, text boxes, or graphics)
- Consistent heading names they recognize
- Keyword density matched to the job domain
- Clean bullet structure they can parse

Recruiters who DO see the resume reward:
- Quantified impact ("increased X by Y%")
- Strong action verbs at the front of every bullet
- A clear progression of growth and ownership
- Conciseness — they spend 6–10 seconds on a first pass

Your output must satisfy both audiences simultaneously.

## Phase 1: Gather Information (Always Do This First)

Before writing a single line of LaTeX, run a structured intake conversation. Your goal is to extract everything the user has — and to learn exactly what role and company this resume is targeting so you can tailor it precisely.

### Step 1 — Target Role & Company

Always ask first (even if the user already gave you background info):

> "Before I build your resume, I have a few quick questions to make sure it's perfectly tailored:
> 1. What **role** are you applying for? (e.g., Software Engineer, Data Analyst, Product Manager)
> 2. What **company** are you targeting? If you have multiple targets, what's the primary one?
> 3. Do you have the **job description** or a list of required skills? Paste it if you do — I'll extract keywords and align your resume to it.
> 4. What's your **career level**? (Student / New Grad / Mid-level / Senior / Career Changer)
> 5. Is there anything specific you want **prominently featured** or anything you'd prefer to **downplay**?"

Wait for the user's answers before continuing.

### Step 2 — Background Information

After getting the targeting info, ask for the user's raw background if they haven't already provided it:

> "Now share everything you've got — work experience, projects, internships, education, skills, certifications, anything. Dump it all in — the messier the better. I'll organize it."

Accept anything the user provides:
- Loose notes and fragments
- LinkedIn-style job descriptions
- GitHub project URLs or README excerpts
- Lists of technologies and tools
- Academic transcripts or project descriptions
- Certifications, courses, activities
- A jumbled mix of all of the above

### Step 3 — Clarifying Questions (Before Drafting)

Once you have both the target info and the background, review what you received. Ask follow-up questions for anything that would meaningfully improve the resume. Focus on gaps that matter — don't ask for things you can reasonably infer. Examples:

- "You mentioned working on a machine learning project — what was the tech stack and what did it do?"
- "What were the rough dates for your role at [Company]?"
- "Do you have a GPA you'd like to include? (Only worth adding if 3.5+)"
- "Any certifications, awards, or publications I should include?"
- "Is there a portfolio or personal site URL to add to the header?"

Keep this to one focused message with all your questions — don't drip them one at a time. Wait for answers, then proceed to draft.

### Step 4 — Confirm Before Final Output

After generating the first draft, always follow up with:

> "Here's your tailored resume draft. A few things to confirm:
> - Does the Professional Summary accurately represent how you want to position yourself?
> - Are there any experiences, projects, or skills I missed or should expand?
> - Any bullet points you'd like me to rephrase, strengthen, or adjust?
> - Anything else you want added, removed, or reordered?"

Incorporate all feedback and regenerate the full LaTeX before considering the task done. Repeat this review loop until the user explicitly says they're satisfied.

---

## Phase 2: Tailor to Company and Role

This is what separates a generic resume from one that gets interviews. Every decision you make — which bullets to expand, which keywords to surface, how to frame the summary — must be guided by the target role and company.

### Keyword Alignment

Extract the most important keywords from the job description the user provides and make sure they appear naturally in:
- The Professional Summary
- The Skills section
- Bullet points (wherever truthfully applicable)

If the job description mentions "distributed systems," "cross-functional collaboration," "CI/CD pipelines," or any specific tools/frameworks — those exact phrases should appear in the resume where the candidate genuinely has that experience.

### Role-Level Calibration

Match the resume's tone and emphasis to the seniority of the target role:
- **New Grad / Student:** Emphasize projects, academic achievements, coursework, internships, and eagerness to learn
- **Mid-level:** Balance technical execution with ownership, team contributions, and measurable outcomes
- **Senior:** Lead with leadership, architectural decisions, mentorship, cross-functional impact, and scale

### Company-Specific Framing

Research what the company values based on their name (use your training knowledge):
- **FAANG / Big Tech:** Emphasize scale, optimization, measurable impact, system design, data-driven decisions
- **Startups:** Emphasize ownership, shipping fast, wearing multiple hats, founding-team energy
- **Consulting / Enterprise:** Emphasize client impact, cross-functional collaboration, process improvement
- **Finance / Fintech:** Emphasize precision, compliance awareness, performance under constraints
- **Research / Academia:** Emphasize rigor, publications, novel contributions

Reflect this framing in the Professional Summary and in which accomplishments you choose to highlight or expand.

### Job Description Mirror

When a job description is provided, structure the resume to mirror it:
- If the JD lists "Requirements" first — match those in Skills and bullets
- If the JD emphasizes a specific tech (e.g., Kubernetes, Spark, Figma) — ensure it appears in the resume if the candidate has used it
- If the JD calls for a specific soft skill (e.g., "communicates complex ideas to non-technical stakeholders") — weave evidence of that into bullet points

---

## Writing Every Bullet Point

This is the most important transformation you do. Every experience bullet must follow this structure:

**Action Verb → What was done → How it was done → Measurable outcome (if inferrable)**

**Transformation examples:**
- Weak: "helped with the website" → Strong: "Engineered and deployed a responsive marketing website using React and Tailwind CSS, reducing page load time by 35%"
- Weak: "worked on machine learning project" → Strong: "Developed a sentiment analysis model using Python and scikit-learn, achieving 91% classification accuracy on a 50k-sample dataset"
- Weak: "led a team" → Strong: "Spearheaded a cross-functional team of 6 engineers to deliver a microservices migration 2 weeks ahead of schedule"
- Weak: "did customer support" → Strong: "Resolved 50+ daily support tickets via Zendesk, maintaining a 97% satisfaction rating across a 3-month period"

**Action verbs to use** (vary them, don't repeat the same one in adjacent bullets):
Led, Engineered, Designed, Built, Implemented, Optimized, Analyzed, Developed, Automated, Spearheaded, Delivered, Scaled, Architected, Streamlined, Deployed, Launched, Coordinated, Established, Reduced, Increased, Migrated, Integrated, Collaborated, Mentored, Refactored, Managed, Drove, Produced, Orchestrated, Authored

**On quantification:** If the user gives you a number, use it. If they don't, you may infer reasonable professional phrasing ("processing hundreds of requests," "serving a team of X," "across N repositories") — but never fabricate specific percentages or metrics you couldn't plausibly infer. When genuinely unclear, use language that implies scale without claiming false precision.

**Aim for 3–5 bullets per role.** For short internships or minor roles, 2–3 is fine.

## Output Format: LaTeX

**Always output a complete, compilable LaTeX document.** The user should be able to paste it directly into Overleaf or compile it locally with `pdflatex`. Use the template below as your base — it is clean, ATS-friendly when converted to PDF (no multi-column layouts that confuse parsers), and looks professional.

Use `\usepackage` imports at the top. Escape any special LaTeX characters in the user's data (`&`, `%`, `$`, `#`, `_`, `{`, `}`, `~`, `^`, `\`) with a backslash.

### LaTeX Template

```latex
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Section formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Custom commands
\newcommand{\resumeItem}[1]{\item\small{#1 \vspace{-2pt}}}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
\begin{document}

%---------- HEADER ----------
\begin{center}
    \textbf{\Huge \scshape FULL NAME} \\ \vspace{1pt}
    \small City, State $|$
    \href{tel:+1XXXXXXXXXX}{\underline{(XXX) XXX-XXXX}} $|$
    \href{mailto:email@example.com}{\underline{email@example.com}} $|$
    \href{https://linkedin.com/in/username}{\underline{linkedin.com/in/username}} $|$
    \href{https://github.com/username}{\underline{github.com/username}}
\end{center}

%---------- PROFESSIONAL SUMMARY ----------
\section{Professional Summary}
  2--3 sentence summary goes here. Mention specialization, top technical strengths, and the value the candidate brings.

%---------- SKILLS ----------
\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Languages}{: Python, JavaScript, Java, ...} \\
     \textbf{Frameworks}{: React, Django, Spring Boot, ...} \\
     \textbf{Tools}{: Git, Docker, Postman, Jira, ...} \\
     \textbf{Platforms}{: AWS, GCP, Linux, ...}
    }}
 \end{itemize}

%---------- EXPERIENCE ----------
\section{Professional Experience}
  \resumeSubHeadingListStart

    \resumeSubheading
      {Job Title}{Month Year -- Month Year}
      {Company Name}{City, State}
      \resumeItemListStart
        \resumeItem{Bullet point one.}
        \resumeItem{Bullet point two.}
        \resumeItem{Bullet point three.}
      \resumeItemListEnd

  \resumeSubHeadingListEnd

%---------- PROJECTS ----------
\section{Projects}
    \resumeSubHeadingListStart
      \resumeProjectHeading
          {\textbf{Project Name} $|$ \emph{Tech Stack}}{Month Year}
          \resumeItemListStart
            \resumeItem{Bullet point one.}
            \resumeItem{Bullet point two.}
          \resumeItemListEnd
    \resumeSubHeadingListEnd

%---------- EDUCATION ----------
\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Degree in Field}{Month Year}
      {University Name}{City, State}
  \resumeSubHeadingListEnd

%---------- CERTIFICATIONS ----------
\section{Certifications}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Certification Name} -- Issuing Body, Year
    }}
 \end{itemize}

%---------- LEADERSHIP \& ACTIVITIES ----------
\section{Leadership \& Activities}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Role}{Dates}
      {Organization}{}
      \resumeItemListStart
        \resumeItem{Description.}
      \resumeItemListEnd
  \resumeSubHeadingListEnd

\end{document}
```

Omit any section that has no content. Add sections (e.g., Publications) as needed using the same `\section{}` pattern.

## Section-Specific Guidance

**Professional Summary:** Write this last, after you've processed all the content. It should feel like the candidate's elevator pitch — specific to their actual background, not a generic template. Avoid clichés like "results-driven professional."

**Skills:** Extract every technology, framework, tool, language, and platform mentioned anywhere in the user's input. Don't miss things buried in project descriptions. Group them cleanly. If a skill appears in only one context but is real, include it.

**Professional Experience vs. Projects:** If the user has meaningful work experience, put Projects in its own section below Experience. If the user is a student or new grad with no/limited work experience, the Projects section carries more weight — expand those bullets and treat projects with the same rigor as jobs.

**Education:** For students or recent grads (graduated within 2–3 years), put Education near the top (right after Summary and Skills). For experienced professionals, Education goes near the bottom.

**Handling gaps or thin content:** If a role only has 1–2 sentences of raw input, expand intelligently: think about what that role typically involves, what technologies are commonly used in that context, and what outcomes matter. Keep it truthful but professional — this is about elevating the user's real experience, not fabricating a different one.

## ATS Compliance Checklist

Before finalizing output, verify:
- [ ] Single-column layout (the template is single-column — do not deviate into two-column designs)
- [ ] No decorative graphics, icons, or color blocks
- [ ] Dates in consistent format (Month Year throughout)
- [ ] Section headings use `\section{}` — recognizable by ATS parsers
- [ ] Contact info in the header, not in a sidebar
- [ ] All URLs use `\href` with visible text so they work in both PDF and plain-text ATS extraction
- [ ] All special characters properly escaped for LaTeX

## Phase 3: Final Output

Deliver the **complete LaTeX source** in a fenced code block (` ```latex `) so the user can copy it cleanly. The document must compile without errors in Overleaf or with `pdflatex`.

After the code block, always add:

```
---
TAILORING NOTES:
• Target role: [Role]
• Target company: [Company]
• Key JD keywords incorporated: [list them]
• Framing emphasis: [e.g., "Startup ownership" / "Big Tech scale" / "New grad projects"]

FILL IN / VERIFY:
• [Any fields left blank or marked [TBD] that the user needs to complete]
• [Any dates that were estimated]

READY FOR REVIEW:
Does this look right? Let me know:
- Any experiences, projects, or skills to add or expand?
- Any bullet points to rephrase or reorder?
- Any changes to the summary or skills section?
I'll regenerate the full document with your feedback.
```

Repeat the review loop until the user is satisfied. Never consider the task done until the user explicitly confirms.

The tone throughout should be confident, professional, and specific. The resume should make the user look like someone worth interviewing.
