import re, os, base64

# ── 1. Read source & extract images ─────────────────────────────────────────
SRC  = "/Users/anunaya.choudhary/Windsurf Projects/YMPL guide/ympl-user-journey.html"
DEST = "/Users/anunaya.choudhary/Windsurf Projects/YMPL guide/ympl-guide-deck.html"

with open(SRC, "r") as f:
    lines = f.readlines()

target_lines = [198, 208, 218, 228, 251, 261, 271, 293, 303, 315,
                337, 347, 369, 391, 413, 440, 470, 480, 510]

imgs = {}
for idx, ln in enumerate(target_lines, start=1):
    m = re.search(r'src="(data:image/[^"]+)"', lines[ln - 1])
    if not m:
        raise ValueError(f"No base64 image found at line {ln}")
    imgs[idx] = m.group(1)   # imgs[1] … imgs[19]

# ── 1b. Load onboarding screenshots (ss1–ss10) ────────────────────────────────
ONBOARDING_DIR = "/Users/anunaya.choudhary/Windsurf Projects/YMPL guide/Onboarding Screenshots"

onb = {}
for i in range(1, 11):
    path = os.path.join(ONBOARDING_DIR, f"ss{i}.png")
    with open(path, "rb") as _f:
        onb[i] = "data:image/png;base64," + base64.b64encode(_f.read()).decode()

# ── 1c. Load FD screenshots (ss1–ss12) ────────────────────────────────────────
FD_DIR = "/Users/anunaya.choudhary/Windsurf Projects/YMPL guide/FD Screenshots"

fd = {}
for i in range(1, 13):
    path = os.path.join(FD_DIR, f"ss{i}.png")
    with open(path, "rb") as _f:
        fd[i] = "data:image/png;base64," + base64.b64encode(_f.read()).decode()

# ── 1d. Load Client Onboarding screenshots (ss1–ss8) ──────────────────────────
CO_DIR = "/Users/anunaya.choudhary/Windsurf Projects/YMPL guide/Client Onboarding Screenshots"

co = {}
for i in range(1, 9):
    path = os.path.join(CO_DIR, f"ss{i}.png")
    with open(path, "rb") as _f:
        co[i] = "data:image/png;base64," + base64.b64encode(_f.read()).decode()

# ── 1f. Load Organisation Hierarchy screenshots (ss1–ss5 + Team member ss) ────
OH_DIR = "/Users/anunaya.choudhary/Windsurf Projects/YMPL guide/Organisation Hierarchy Screenshots"

oh = {}
for i in range(1, 6):
    path = os.path.join(OH_DIR, f"ss{i}.png")
    with open(path, "rb") as _f:
        oh[i] = "data:image/png;base64," + base64.b64encode(_f.read()).decode()

with open(os.path.join(OH_DIR, "Team member ss.png"), "rb") as _f:
    oh_tm = "data:image/png;base64," + base64.b64encode(_f.read()).decode()

# ── 1e. Load MF screenshots (Screenshot 1–16) ─────────────────────────────────
MF_DIR = "/Users/anunaya.choudhary/Windsurf Projects/YMPL guide/MF Screenshots"

mf = {}
for i in range(1, 17):
    path = os.path.join(MF_DIR, f"Screenshot {i}.png")
    with open(path, "rb") as _f:
        mf[i] = "data:image/png;base64," + base64.b64encode(_f.read()).decode()

# ── 2. Helper functions ───────────────────────────────────────────────────────

def img_tag(src, extra_style=""):
    """Return an <img> tag with inline style."""
    return f'<img src="{src}" style="width:100%;height:auto;object-fit:contain;{extra_style}" loading="lazy">'

def labeled_img(src, label, img_style=""):
    return f'''<div style="display:flex;flex-direction:column;">
  {img_tag(src, img_style)}
  <div style="font-size:.52rem;color:#94a3b8;text-align:center;margin-top:3px;">{label}</div>
</div>'''

def grid_2x2(i1, l1, i2, l2, i3, l3, i4, l4):
    """2×2 grid for 4 images."""
    style = "display:grid;grid-template-columns:1fr 1fr;gap:6px;flex:1;min-height:0;"
    img_s = "max-height:160px;border-radius:6px;border:1px solid #e2e8f0;"
    return (f'<div style="{style}">'
            + labeled_img(i1, l1, img_s) + labeled_img(i2, l2, img_s)
            + labeled_img(i3, l3, img_s) + labeled_img(i4, l4, img_s)
            + '</div>')

def grid_3col(i1, l1, i2, l2, i3, l3):
    style = "display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;flex:1;min-height:0;"
    img_s = "max-height:200px;border-radius:6px;border:1px solid #e2e8f0;"
    return (f'<div style="{style}">'
            + labeled_img(i1, l1, img_s) + labeled_img(i2, l2, img_s)
            + labeled_img(i3, l3, img_s)
            + '</div>')

def grid_2col(i1, l1, i2, l2):
    style = "display:grid;grid-template-columns:1fr 1fr;gap:12px;flex:1;min-height:0;"
    img_s = "max-height:260px;border-radius:6px;border:1px solid #e2e8f0;"
    return (f'<div style="{style}">'
            + labeled_img(i1, l1, img_s) + labeled_img(i2, l2, img_s)
            + '</div>')

def single_img(src, label):
    img_s = "max-height:340px;max-width:100%;display:block;margin:0 auto;border-radius:8px;border:1px solid #e2e8f0;"
    return (f'<div style="display:flex;flex-direction:column;align-items:center;flex:1;justify-content:center;">'
            + labeled_img(src, label, img_s)
            + '</div>')

def right_panel(title, content_html):
    return f'''<div class="right-panel">
  <div class="rp-title">{title}</div>
  {content_html}
</div>'''

def bullet_li(text):
    return f'<li>{text}</li>'

def left_bullets(points):
    items = "".join(bullet_li(p) for p in points)
    return f'<ul class="kp-list">{items}</ul>'

def kyc_dots(active_step):
    """active_step: 1-5. active=filled blue, done=smaller blue, pending=grey."""
    html = '<div class="kyc-dots">'
    for i in range(1, 6):
        if i < active_step:
            html += f'<div class="kd kd-done" title="Step {i}"></div>'
        elif i == active_step:
            html += f'<div class="kd kd-active" title="Step {i}"><span>{i}</span></div>'
        else:
            html += f'<div class="kd kd-pending" title="Step {i}"></div>'
    html += '</div>'
    return html

def badge(text, color="#2563eb"):
    return f'<span class="badge" style="background:{color}20;color:{color};border:1px solid {color}40;">{text}</span>'

def stat_chip(text):
    return f'<div class="stat-chip">{text}</div>'

def cover_slide(slide_id, bg, eyebrow, h1, sub, chips=None, tags=None, label_19=None):
    chips_html = ""
    if chips:
        chips_html = '<div class="chips">' + "".join(stat_chip(c) for c in chips) + '</div>'
    tags_html = ""
    if tags:
        tags_html = '<div class="tags">' + "".join(badge(t,"#93c5fd") for t in tags) + '</div>'
    label_html = f'<div class="cover-label">{label_19}</div>' if label_19 else ""
    return f'''<div id="{slide_id}" class="slide cover" style="background:{bg};">
  <div class="cover-inner">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="cover-sub">{sub}</p>
    {tags_html}{chips_html}{label_html}
  </div>
</div>'''

def two_col_slide(slide_id, left_bg, left_content, right_content):
    return f'''<div id="{slide_id}" class="slide two-col">
  <div class="left-panel" style="background:{left_bg};">
    {left_content}
  </div>
  {right_content}
</div>'''

def left_panel_content(num, ttl, sub, points, extra="", dots_html=""):
    return f'''<div class="lp-num">{num}</div>
<div class="lp-ttl">{ttl}</div>
<div class="lp-sub">{sub}</div>
{dots_html}
<div class="takeaway-box">
  <div class="tb-title">Key Points</div>
  {left_bullets(points)}
</div>
{extra}'''

def screen_slide(slide_id, bg, eyebrow, title, subtitle, points, body_html, extra_badge=""):
    bullets = "".join(f'<div class="sp-bullet">{p}</div>' for p in points)
    badge_html = f'<div style="margin-top:5px;">{extra_badge}</div>' if extra_badge else ""
    return f'''<div id="{slide_id}" class="slide screen-slide">
  <div class="s-header" style="background:{bg};">
    <div class="s-hdr-left">
      <div class="s-eyebrow">{eyebrow}</div>
      <div class="s-title">{title}</div>
      <div class="s-sub">{subtitle}</div>
    </div>
    <div class="s-hdr-right">
      <div class="s-points">{bullets}</div>
      {badge_html}
    </div>
  </div>
  <div class="s-body">
    {body_html}
  </div>
</div>'''

def full_img(src):
    return f'<img src="{src}" class="s-img">'

# ── 3. Build all 37 slides ────────────────────────────────────────────────────

# SLIDE 2 — Module 01 cover
slide2 = cover_slide(
    "s2",
    "linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #1d4ed8 100%)",
    "Part 01 of 06",
    "Distributor Onboarding &amp; KYC",
    "A fully digital, 5-step KYC process. New distributors go from sign-up to live in under 30 minutes — no paperwork required.",
    chips=["5 KYC Steps","&lt; 30 minutes","No paperwork"]
)

# ── Module 01: Distributor KYC — Authentication (s3–s6, one image each) ──────

slide3 = screen_slide(
    "s3",
    "linear-gradient(160deg, #1e3a5f, #2563eb)",
    "Step 00 · Distributor KYC · Authentication",
    "Login Entry",
    "Enter your mobile number or email to get started",
    [
        "Single entry point — works for both new and returning users",
        "Enter mobile number or email address in the input field",
        "Tap 'Continue' — system detects whether the user is new or existing",
        "New users are guided to account creation; existing users go to OTP",
    ],
    full_img(onb[1]),
    extra_badge='<span style="font-size:.58rem;color:rgba(255,255,255,.7);">Support: support@yubimarkets.com</span>'
)

slide4 = screen_slide(
    "s4",
    "linear-gradient(160deg, #1e3a5f, #2563eb)",
    "Step 00 · Distributor KYC · Authentication",
    "Account Creation",
    "New user details — name and email registration",
    [
        "First-time users fill in their full name and email address",
        "Email must be a valid business address — used for all platform communications",
        "Tap 'Proceed to mobile verification' to move to OTP steps",
        "Returning users skip this screen and go directly to OTP verification",
    ],
    full_img(onb[2])
)

slide5 = screen_slide(
    "s5",
    "linear-gradient(160deg, #1e3a5f, #2563eb)",
    "Step 00 · Distributor KYC · Authentication",
    "Mobile OTP Verification",
    "Verify your mobile number via a 6-digit OTP",
    [
        "A 6-digit OTP is sent to the mobile number entered at login",
        "Enter all 6 digits in the input boxes — auto-advances on completion",
        "Tap 'Verify' to confirm — OTP is valid for a limited window",
        "Both mobile AND email OTPs are required for full authentication",
    ],
    full_img(onb[3])
)

slide6 = screen_slide(
    "s6",
    "linear-gradient(160deg, #1e3a5f, #2563eb)",
    "Step 00 · Distributor KYC · Authentication",
    "Email OTP Verification",
    "Verify your email address via a 6-digit OTP",
    [
        "A 6-digit OTP is sent to the registered email address",
        "Enter all 6 digits to confirm email ownership",
        "Both mobile and email OTPs must be verified to proceed",
        "First login also includes T&amp;C, E-Sign Consent &amp; Privacy Policy acceptance",
    ],
    full_img(onb[4])
)

# ── KYC Step 1: Identity Verification (s7–s9) ────────────────────────────────

slide7 = screen_slide(
    "s7",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 1 / 5 · Distributor KYC · Identity Verification",
    "PAN Entry",
    "Enter PAN to begin identity verification",
    [
        "Enter the 10-character Permanent Account Number",
        "System verifies PAN instantly via HyperVerge",
        "Name is auto-populated from the PAN database on success",
    ],
    full_img(imgs[5]),
    extra_badge=badge("Powered by HyperVerge","#93c5fd")
)

slide8 = screen_slide(
    "s8",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 1 / 5 · Distributor KYC · Identity Verification",
    "PAN Verified",
    "PAN validated — distributor name auto-populated",
    [
        "Green tick confirms successful PAN verification",
        "Distributor's legal name retrieved from the PAN database",
        "Distributor can confirm or edit their business display name",
    ],
    full_img(imgs[6])
)

slide9 = screen_slide(
    "s9",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 1 / 5 · Distributor KYC · Identity Verification",
    "Business Type",
    "Select entity type for the distributorship",
    [
        "Supported types: Individual, Company, Partnership, HUF, LLP, Trust and more",
        "Entity type determines which documents are required in the next step",
        "Selection cannot be changed after KYC submission",
    ],
    full_img(imgs[7])
)

# ── KYC Step 2: Address Verification (s10–s12) ───────────────────────────────

slide10 = screen_slide(
    "s10",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 2 / 5 · Distributor KYC · Address Verification",
    "Choose Verification Method",
    "CIN/LLPIN path or Document upload path",
    [
        "CIN/LLPIN: instant auto-fetch of address from MCA — no manual entry",
        "Document path: upload a supporting address document",
        "CIN path is recommended for Companies and LLPs",
    ],
    full_img(imgs[8])
)

slide11 = screen_slide(
    "s11",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 2 / 5 · Distributor KYC · Address Verification",
    "Select Document Type",
    "Choose the address proof document to upload",
    [
        "Accepted documents: COI, GST certificate, MOA/AOA, Partnership deed, HUF declaration",
        "Select the document type that matches what you will upload",
        "Ensure the document shows the registered business address",
    ],
    full_img(imgs[9])
)

slide12 = screen_slide(
    "s12",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 2 / 5 · Distributor KYC · Address Verification",
    "Address Upload Form",
    "Fill in address details and upload document",
    [
        "Fields: address line, city, state, pincode, country",
        "Pre-filled automatically on the CIN path",
        "Manual entry required on the document upload path",
    ],
    full_img(imgs[10])
)

# ── KYC Step 3: Bank Details (s13–s14) ───────────────────────────────────────

slide13 = screen_slide(
    "s13",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 3 / 5 · Distributor KYC · Bank Details",
    "Choose Verification Method",
    "Penny Drop (recommended) or Manual upload",
    [
        "Penny Drop: ₹1 is deposited via NPCI — returned account holder name matched against PAN",
        "Manual path: upload a blank cheque with account number and IFSC visible",
        "Penny Drop is instant and requires no document upload",
        "Both options appear on this screen — distributor selects based on preference",
    ],
    full_img(onb[5]),
    extra_badge=badge("Recommended: Penny Drop","#93c5fd")
)

slide14 = screen_slide(
    "s14",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 3 / 5 · Distributor KYC · Bank Details",
    "Manual Bank Upload",
    "Upload blank cheque as bank proof",
    [
        "Select account type: Savings or Current",
        "Enter account number and IFSC code manually",
        "Upload a clear image of a blank cheque (JPG/PNG/PDF accepted)",
        "Account number and IFSC must be legible — re-upload if unclear",
    ],
    full_img(onb[6])
)

# ── KYC Step 4: GST Verification (s15) ───────────────────────────────────────

slide15 = screen_slide(
    "s15",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 4 / 5 · Distributor KYC",
    "GST Verification",
    "GST Registration (Optional)",
    [
        "Enter 15-character GSTIN — verified via Digitap against GST portal in real-time",
        "Optional for FD-only distributors — can be skipped initially",
        "Mandatory once annual commissions exceed ₹10L — platform gates transactions",
    ],
    full_img(imgs[13]),
    extra_badge=badge("Required above ₹10L commissions","#fbbf24")
)

# ── eSign Flow — 4 new slides (s16–s19) ──────────────────────────────────────

slide16 = screen_slide(
    "s16",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 5 / 5 · Distributor KYC · eSign",
    "Master Connector Program Agreement",
    "Review and digitally sign the distributor agreement",
    [
        "Full legal text of the Master Connector Program Agreement is displayed",
        "Distributor must scroll through and read the entire document before signing",
        "Tap 'Proceed to Sign' (orange button) to open the eSign panel",
        "Signature is legally binding — powered by Digio eSign infrastructure",
    ],
    full_img(onb[7]),
    extra_badge=badge("Powered by Digio eSign","#93c5fd")
)

slide17 = screen_slide(
    "s17",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 5 / 5 · Distributor KYC · eSign",
    "Create Your Signature",
    "Draw or type your signature to sign the agreement",
    [
        "Two modes: 'Draw' (freehand) or 'Type' your full name",
        "Type mode: enter full legal name and choose a font style for the signature",
        "Preview the signature before submitting — switch modes if needed",
        "Tap 'Submit Signature' to apply the eSign to the agreement document",
    ],
    full_img(onb[8])
)

slide18 = screen_slide(
    "s18",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 5 / 5 · Distributor KYC · eSign",
    "eSign Verification",
    "Verifying your eSign — Terms &amp; Conditions confirmation",
    [
        "'Verifying your eSign…' status shown while Digio processes the signature",
        "Two T&amp;C checkboxes appear: accept terms &amp; conditions, and consent to data sharing",
        "Both checkboxes must be ticked before proceeding",
        "'Proceed E-sign' button activates only after verification completes and both boxes are checked",
    ],
    full_img(onb[9])
)

slide19 = screen_slide(
    "s19",
    "linear-gradient(160deg, #1e3a5f, #1d4ed8)",
    "KYC Step 5 / 5 · Distributor KYC · eSign",
    "Document Signed Successfully",
    "Email confirmation from Digio — agreement PDF attached",
    [
        "Email sent from Digio: 'Document signed successfully with Yubi'",
        "Signed agreement PDF (ESign-agreement.pdf) attached to the confirmation email",
        "Distributor receives this in their registered email inbox",
        "Agreement is now on record — KYC application proceeds to Ops review",
    ],
    full_img(onb[10]),
    extra_badge=badge("Signed PDF emailed via Digio","#6ee7b7")
)

slide21 = screen_slide(
    "s20",
    "linear-gradient(160deg, #0f172a, #1e3a5f)",
    "Post KYC · Distributor KYC",
    "Application Under Review",
    "Ops team reviews submitted application",
    [
        "After submission: 'Our team is processing your application'",
        "Main platform nav is visible but locked until approval",
        "Ops team reaches out if additional documents are needed",
    ],
    full_img(imgs[15]),
    extra_badge=badge("Typical turnaround: same business day","#93c5fd")
)

# ── Module 02: Client Management (s22–s31) ───────────────────────────────────

slide22 = cover_slide(
    "s21",
    "linear-gradient(135deg, #064e3b, #065f46, #059669)",
    "Part 02 of 06",
    "Client Management",
    "After KYC approval, the distributor lands on the Clients dashboard — their central hub for managing investors, tracking KYC status, and adding new clients.",
    chips=["After KYC Approval","Track Investor KYC","Add New Clients"]
)

slide23 = screen_slide(
    "s22",
    "linear-gradient(160deg, #064e3b, #059669)",
    "Module 02 · Step 0 · Client Management",
    "Clients Dashboard",
    "Empty state — no clients added yet",
    [
        "Distributor lands here immediately after KYC approval",
        "3 stat cards: Total Clients, Pending KYC, Failed KYC — all zero on first login",
        "Table columns: Name, Email, Client Type, KYC Status, Navigate, Actions",
        "Click 'Add new client' (top-right) to begin onboarding the first investor",
    ],
    full_img(co[1]),
    extra_badge=badge("Add new client — top-right CTA","#6ee7b7")
)

slide24 = screen_slide(
    "s23",
    "linear-gradient(160deg, #064e3b, #059669)",
    "Module 02 · Onboarding Step 1 · Client Management",
    "Enter Client PAN",
    "Initiate onboarding with the investor's PAN",
    [
        "Click 'Add new client' on the Clients Dashboard to reach this screen",
        "Enter the investor's 10-character PAN number in the input field",
        "System verifies PAN instantly — name and details auto-fetched on validation",
        "Click Proceed to continue once PAN is entered",
    ],
    full_img(co[2])
)

slide25 = screen_slide(
    "s24",
    "linear-gradient(160deg, #064e3b, #059669)",
    "Module 02 · Onboarding Step 1 · Client Management",
    "PAN Validated",
    "PAN verified — green tick confirms success",
    [
        "Green tick icon appears next to the PAN field on successful verification",
        "Client's registered name is retrieved from the PAN database",
        "If PAN is invalid or unrecognised, an error is shown — re-enter the correct PAN",
        "Click Proceed to move to the customer details form",
    ],
    full_img(co[3]),
    extra_badge=badge("Powered by HyperVerge","#6ee7b7")
)

slide26 = screen_slide(
    "s25",
    "linear-gradient(160deg, #064e3b, #059669)",
    "Module 02 · Onboarding Step 2 · Client Management",
    "Customer Details",
    "Fill in client information &amp; optional bank details",
    [
        "Required fields: Customer Name, Email, Mobile Number, Date of Birth",
        "Optional bank details: Account Type (Savings / Current), Account Number, IFSC Code",
        "Bank details can be skipped — client can add them during their own onboarding",
        "Click Continue to proceed to investment preference selection",
    ],
    full_img(co[4])
)

slide27 = screen_slide(
    "s26",
    "linear-gradient(160deg, #064e3b, #059669)",
    "Module 02 · Onboarding Step 3 · Client Management",
    "Investment Preference",
    "Select the client's product type",
    [
        "Three product options: Bonds, Fixed Deposit, Mutual Funds",
        "Select one or more products that match the client's risk appetite",
        "The onboarding link generated will be scoped to the selected product(s)",
        "Click 'Generate customer link' to send the invitation",
    ],
    full_img(co[5])
)

slide28 = screen_slide(
    "s27",
    "linear-gradient(160deg, #064e3b, #059669)",
    "Module 02 · Onboarding Step 4 · Client Management",
    "Invitation Sent",
    "Onboarding email dispatched to client",
    [
        "Confirmation modal: 'Invitation sent successfully'",
        "Email is sent to the client's registered email address",
        "Client must open the email and click 'Get Started' to complete their KYC",
        "Dashboard will show the client with a 'Pending' KYC status immediately",
    ],
    full_img(co[6])
)

slide29 = screen_slide(
    "s28",
    "linear-gradient(160deg, #064e3b, #059669)",
    "Module 02 · Post-Invitation · Client Management",
    "Client Added — Pending KYC",
    "Client now visible in dashboard with Pending status",
    [
        "Total Clients count increments; client row appears in the table",
        "KYC Status shows 'Pending' badge — client has not completed their KYC yet",
        "Actions dropdown: 'Send Onboarding Link' to resend, 'View KYC' to check progress",
        "Distributor can track all pending clients and nudge them from here",
    ],
    full_img(co[7]),
    extra_badge=badge("Resend link available from Actions menu","#6ee7b7")
)

slide30 = screen_slide(
    "s29",
    "linear-gradient(160deg, #064e3b, #059669)",
    "Module 02 · Client's View · Client Management",
    "Onboarding Email",
    "What the client receives in their inbox",
    [
        "Email from Yubi Markets: 'Begin Your Investment Journey'",
        "Contains a 'Get Started' button that launches the client's self-serve KYC flow",
        "The process is quick, simple, and fully secure",
        "Once client completes KYC and it is approved, their status updates to Approved",
    ],
    full_img(co[8])
)

slide31 = screen_slide(
    "s30",
    "linear-gradient(160deg, #064e3b, #059669)",
    "Module 02 · Client Management",
    "Clients Dashboard — After KYC Approval",
    "Investor management hub · Post-KYC approval",
    [
        "3 stat cards at top: Total Clients, Pending KYC, Failed KYC",
        "Client table: Name, Email, Client Type, KYC Status, Navigate to product",
        "Filter by Client Type and KYC Status — colour-coded badges",
        "Navigate column gives direct shortcut to client's product (FD / MF)",
    ],
    full_img(imgs[16]),
    extra_badge=badge("Add New Client — top-right CTA","#6ee7b7")
)

# ── Module 03: Team Members (s32–s34) ────────────────────────────────────────

slide32 = cover_slide(
    "s31",
    "linear-gradient(135deg, #3b0764, #5b21b6, #7c3aed)",
    "Part 03 of 06",
    "Team Members",
    "Distributors can build their team directly from the platform. Each team member gets their own login and role-based access.",
    chips=["Role-based Access","Admin &amp; Client Roles","Email Activation"]
)

slide33 = screen_slide(
    "s32",
    "linear-gradient(160deg, #3b0764, #7c3aed)",
    "Module 03 · Team Members",
    "Profile Menu",
    "Access Team Members via the avatar menu",
    [
        "Click the avatar icon (top-right) to open the profile menu",
        "Select 'Team Members' to navigate to the team directory",
        "Admin and sub-admin roles can access this section",
    ],
    full_img(imgs[17])
)

slide34 = screen_slide(
    "s33",
    "linear-gradient(160deg, #3b0764, #7c3aed)",
    "Module 03 · Team Members",
    "Team Directory",
    "Full team roster with roles and org node mapping",
    [
        "Full directory: Name, Email, Phone, Role, Org Node — searchable",
        "Admin: full platform access, manages team and clients",
        "CLIENT role: investor-level access limited to own portfolio",
        "New members activate via email invitation link",
    ],
    full_img(imgs[18]),
    extra_badge=badge("New members activate via email link","#c4b5fd")
)

slide_tm = screen_slide(
    "s34",
    "linear-gradient(160deg, #3b0764, #7c3aed)",
    "Module 03 · Team Members",
    "Add Team Member",
    "Side panel — fill in details and send an activation link",
    [
        "Name, Email address, and Phone number are required fields",
        "Role: choose from Admin, Relationship Manager, Yubi Markets RM, or Operations Manager",
        "EUIN field: required if this member will distribute mutual funds",
        "Organisation Node (optional): assign the member to a node in the hierarchy at creation time",
        "Click 'Send activation link' — the member receives an email to set their password and activate",
    ],
    full_img(oh_tm),
    extra_badge=badge("Activation email sent instantly on form submit","#c4b5fd")
)

# ── Module 04: Organisation Hierarchy (s35–s36) ──────────────────────────────

slide35 = cover_slide(
    "s35",
    "linear-gradient(135deg, #0f172a, #1e293b, #334155)",
    "Part 04 of 06",
    "Organisation Hierarchy",
    "Define your firm's structure — map RMs to branches, zones, and regions. Business reports drill down through the hierarchy and data access is scoped accordingly.",
    chips=["Multi-level Hierarchy","RM Mapping","Scoped Access"]
)

slide36 = screen_slide(
    "s36",
    "linear-gradient(160deg, #0f172a, #334155)",
    "Module 04 · Organisation Hierarchy",
    "Hierarchy Tree",
    "Full firm structure — HQ, Divisions, and Branches at a glance",
    [
        "Root node (HQ) at top — expandable tree shows all Divisions and Branches below",
        "Each node shows its type label: HQ, Division, or Branch",
        "Three actions per node: Assign Team Members · Add Child · Delete",
        "Number in 'Add Child' button shows count of existing children — e.g. Add Child (4)",
    ],
    full_img(oh[1])
)

oh2 = screen_slide(
    "s37",
    "linear-gradient(160deg, #0f172a, #334155)",
    "Module 04 · Organisation Hierarchy",
    "Add a Child Node",
    "Expand the hierarchy — add branches or sub-divisions inline",
    [
        "Click 'Add Child' on any parent node to open the inline form",
        "Level: auto-filled based on the parent type — e.g. parent is Division → Level is Branch",
        "Node Name: type the name of the new branch or division",
        "Click Save to instantly add the node — appears in the tree without a page reload",
    ],
    full_img(oh[2])
)

oh3 = screen_slide(
    "s40",
    "linear-gradient(160deg, #0f172a, #334155)",
    "Module 04 · Organisation Hierarchy",
    "View Organisation Chart",
    "Visual tree — see the full firm structure in one diagram",
    [
        "Click 'View Organisation Chart' on the Hierarchy Tree page to open this overlay",
        "Root node (HQ) highlighted in orange — Divisions on level 2, Branches on level 3",
        "Each box shows the node name and its type (HQ / Division / Branch)",
        "Use zoom controls (+ / − / Reset Zoom) to navigate large hierarchies",
    ],
    full_img(oh[3]),
    extra_badge=badge("Use Reset Zoom to fit the full chart on screen","#94a3b8")
)

oh4 = screen_slide(
    "s38",
    "linear-gradient(160deg, #0f172a, #334155)",
    "Module 04 · Organisation Hierarchy · Team Assignment",
    "Assign Team Members — Empty State",
    "Map RMs and managers to a specific branch node",
    [
        "Navigate via breadcrumb: Hierarchy → Branch Name → Assign Team Members",
        "Top table: currently assigned members — 'No data found' before any assignment",
        "Bottom table: all Unassigned Users — Name, Email, Phone, Role columns",
        "Click 'Assign User' next to any team member to link them to this branch node",
    ],
    full_img(oh[4])
)

oh5 = screen_slide(
    "s39",
    "linear-gradient(160deg, #0f172a, #334155)",
    "Module 04 · Organisation Hierarchy · Team Assignment",
    "Assign Team Members — After Assignment",
    "RM confirmed — assigned member visible with role and Unassign option",
    [
        "Assigned member moves to the top table with role set to 'RM'",
        "Unassign button available to remove them from the node at any time",
        "Remaining users stay in the Unassigned list — assign multiple RMs per node",
        "Assignments drive data scoping: RMs only see clients and reports under their node",
    ],
    full_img(oh[5]),
    extra_badge=badge("Assigned RMs see only their node's clients and reports","#94a3b8")
)

# ── Module 05: Fixed Deposits (s40–s52) ──────────────────────────────────────

fd_cover = cover_slide(
    "s41",
    "linear-gradient(135deg, #78350f, #b45309, #d97706)",
    "Part 05 of 06",
    "Fixed Deposits",
    "A curated marketplace of high-yield FDs from top-rated small finance banks and NBFCs. Help clients earn up to 9%+ p.a. with capital safety and flexible payout options.",
    chips=["Up to 9%+ p.a.","Tax Saver FD","5 Payout Options","Section 80C"]
)

fd1 = screen_slide(
    "s42",
    "linear-gradient(160deg, #92400e, #d97706)",
    "Module 05 · Fixed Deposits",
    "FD Marketplace",
    "Browse all offerings · personalised rates for Women and Senior Citizens",
    [
        "All FD issuers displayed as cards — interest rate, tenure, and minimum amount visible upfront",
        "Highest-rated issuers: small finance banks, AAA-rated NBFCs, and bank-rated deposits",
        "Women (W): +15–25 bps · Senior Citizen (SC): +25–50 bps · Senior Citizen Women (SCW): highest tier",
        "Use top-right filters to switch persona — cards refresh in real-time · 'Clear All' resets to regular rates",
        "Click any card to open the full FD detail and returns calculator",
    ],
    full_img(fd[2]),
    extra_badge=badge("Top-rated issuers only · Personalised rates available","#fde68a")
)

fd3 = screen_slide(
    "s43",
    "linear-gradient(160deg, #92400e, #d97706)",
    "Module 05 · Fixed Deposits · Issuer Detail",
    "Issuer Profile & Payout Options",
    "Ratings, fees, and returns calculator — choose payout frequency",
    [
        "About Issuer: background, listing status, AUM, customer base · CRISIL rating and minimum deposit",
        "Distribution Fee structure: Base, Incentive 1, Incentive 2 brackets (RM-only data)",
        "Returns Calculator: configure amount, tenure, and payout frequency — returns update in real-time",
        "5 payout modes: Maturity (compounding), Monthly (income), Quarterly / Half-Yearly / Yearly",
        "Pro tip: Monthly for regular income · Maturity for maximum compounded growth",
    ],
    full_img(fd[4]),
    extra_badge=badge("CRISIL A1+ rated · Pro tip: Monthly for income · Maturity for compounding","#fde68a")
)

fd5 = screen_slide(
    "s44",
    "linear-gradient(160deg, #92400e, #d97706)",
    "Module 05 · Fixed Deposits · Tenure Selection",
    "Select Tenure & FD Summary",
    "Choose tenure and rate · review live yield before booking",
    [
        "All available tenures shown with rates — 5-year option tagged 'Tax Saver' (Section 80C, up to ₹1.5 lakh)",
        "Longer tenures generally offer higher rates — compare before selecting via radio button",
        "Selected FD displayed: issuer, tenure, and locked-in rate (e.g. 5-year Tax Saver at 8.05%)",
        "Right panel shows: Annual Yield % and Estimated Returns — updates live as selection changes",
        "Click 'Continue to Book FD' to confirm the selection and proceed to booking",
    ],
    full_img(fd[6]),
    extra_badge=badge("Tax Saver — Section 80C eligible · Live yield estimate","#fde68a")
)

fd7 = screen_slide(
    "s45",
    "linear-gradient(160deg, #92400e, #d97706)",
    "Module 05 · Fixed Deposits · Investment Summary",
    "Investment Details Confirmed",
    "Full summary — amount, tenure, payout, and estimated returns",
    [
        "Complete summary: issuer, invested amount, tenure, payout frequency",
        "Effective annual yield and total estimated interest earnings shown clearly",
        "All parameters editable — modify any input to recalculate before committing",
        "Click 'Invest Now' to begin the booking flow",
    ],
    full_img(fd[7])
)

fd8 = screen_slide(
    "s46",
    "linear-gradient(160deg, #92400e, #d97706)",
    "Module 05 · Fixed Deposits · Rate Card",
    "Full Rate Card",
    "Complete tenure-wise rate table for the issuer",
    [
        "All tenure-rate combinations in a single reference view",
        "Regular Citizen vs Senior Citizen rates displayed side-by-side",
        "Senior citizens get a consistent 15+ bps premium across all tenures",
        "Official rate card — updated whenever the issuer revises rates",
    ],
    full_img(fd[8])
)

fd9 = screen_slide(
    "s47",
    "linear-gradient(160deg, #92400e, #d97706)",
    "Module 05 · Fixed Deposits · Booking",
    "Book FD — Confirm Details",
    "Pre-filled booking form — select client and renewal preference",
    [
        "Most details auto-filled from the calculator: issuer, amount, tenure, payout",
        "Select the client account this FD is being booked under",
        "Set maturity renewal preference: Auto-Renew or No (pay out to bank account)",
        "Review all fields before sending the payment link",
    ],
    full_img(fd[9])
)

fd10 = screen_slide(
    "s48",
    "linear-gradient(160deg, #92400e, #d97706)",
    "Module 05 · Fixed Deposits · Booking",
    "Confirm & Send Payment Link",
    "Investor details confirmed — trigger secure payment email",
    [
        "Client name and renewal preference confirmed on this screen",
        "Setting renewal to 'No' ensures FD matures to the investor's bank account",
        "Click 'Mail Investor for payment' to send a secure one-click payment link",
        "Edit Client or Renewal Preference before sending if needed",
    ],
    full_img(fd[10]),
    extra_badge=badge("Secure payment link via registered email","#fde68a")
)

fd11 = screen_slide(
    "s49",
    "linear-gradient(160deg, #92400e, #d97706)",
    "Module 05 · Fixed Deposits · Booking",
    "Payment Link Sent",
    "Email dispatched — client completes payment to activate FD",
    [
        "Confirmation modal: payment link sent to client's registered email",
        "Client opens the email and completes payment via the secure one-click flow",
        "FD booked and visible in portfolio within 1 working day of payment",
        "Click 'Go to Orders' to track the booking in real-time",
    ],
    full_img(fd[11])
)

fd12 = screen_slide(
    "s50",
    "linear-gradient(160deg, #92400e, #d97706)",
    "Module 05 · Fixed Deposits · Orders",
    "Orders — Track Applications",
    "Monitor all FD bookings and application status",
    [
        "Two tabs: Current Applications (in-progress) and Previous Applications (completed)",
        "Each row shows: Application ID, next interest payout date, maturity date",
        "Use 'All Filters' to filter by issuer, date range, or status",
        "Actions menu per row: view details, check status updates",
    ],
    full_img(fd[12]),
    extra_badge=badge("Status updates sent till FD is fully booked","#fde68a")
)

# ── Module 06: Mutual Funds (s53–s69) ────────────────────────────────────────

mf_cover = cover_slide(
    "s51",
    "linear-gradient(135deg, #083344, #0c4a6e, #0284c7)",
    "Part 06 of 06",
    "Mutual Funds",
    "12,675+ schemes across 7,384 AMCs. Help clients invest via SIP or lumpsum, track portfolio performance with XIRR, and manage mandates — all from one platform.",
    chips=["12,675+ Schemes", "SIP &amp; Lumpsum", "XIRR Tracking", "BSE Integration"]
)

# ss16: Clients Dashboard with Mutual Fund navigate
mf1 = screen_slide(
    "s52",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds",
    "Clients Dashboard",
    "Your entry point — KYC-verified clients with Mutual Fund access",
    [
        "All KYC-verified clients listed with a 'Mutual Fund' navigate button in the table",
        "3 stat cards: Total Clients, Pending KYC, Failed KYC Clients",
        "Filter clients by Client Type or KYC Status — search by name or email",
        "Click 'Mutual Fund' against any client to enter their personal MF dashboard",
    ],
    full_img(mf[16]),
    extra_badge=badge("Click 'Mutual Fund' to enter the client's MF dashboard","#bae6fd")
)

# ss15: Investor Switcher dropdown
mf2 = screen_slide(
    "s53",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds",
    "Investor Switcher",
    "Switch active client context without leaving the screen",
    [
        "Click the investor name at the top to open the switcher dropdown",
        "Search by client name or code for quick lookup",
        "Tap any name to instantly switch the active investor context",
        "The entire MF workspace — portfolio, orders, SIPs — refreshes for the selected client",
    ],
    full_img(mf[15])
)

# ss1: Explore Mutual Funds — Fund Catalogue
mf3 = screen_slide(
    "s54",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Explore",
    "Fund Catalogue",
    "12,675+ schemes across all major AMCs — search, filter, invest",
    [
        "Browse all MF schemes displayed as cards — scheme name, AMC, category, plan, option",
        "Search by scheme name, AMC, or ISIN using the top search bar",
        "Filter by category: Equity, Debt, Hybrid, SIF — or browse All",
        "Click any scheme card to view its full fact sheet and open the invest panel",
    ],
    full_img(mf[1]),
    extra_badge=badge("12,675 schemes · 7,384 AMCs · 8 categories","#bae6fd")
)

# ss10: Fund Fact Sheet (360 ONE BALANCED HYBRID FUND)
mf4 = screen_slide(
    "s55",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Fund Detail",
    "Fund Fact Sheet",
    "Identity, operational details, NAV chart, and SIP/Lumpsum invest panel",
    [
        "Fund Identity: ISIN, AMFI code, scheme code, offer status, offer type, NFO dates",
        "Operational Details: AMC, category, RTA (CAMS/Karvy), face value, settlement (T+T2), exit load",
        "Right panel: 'Start a SIP' or 'Invest Lumpsum' — SIP at a glance shows min/max amount &amp; frequency",
        "Toggle NAV chart: 7D / 1M / 3M / 1Y / YTD for historical performance",
    ],
    full_img(mf[10]),
    extra_badge=badge("Start a SIP or Invest Lumpsum from this screen","#bae6fd")
)

# ss11: Set Up SIP — Step 1 Select Scheme
mf5 = screen_slide(
    "s56",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · SIP Setup · Step 1 of 4",
    "Set Up SIP — Select Scheme",
    "Confirm investor and scheme before configuring the SIP",
    [
        "4-step SIP flow: Select Scheme → Configure SIP → Select Mandate → Review &amp; Confirm",
        "Step 1: confirm the investor name (auto-populated from active client context)",
        "Scheme is pre-filled if accessed via the fund fact sheet",
        "Click 'Continue' to proceed to SIP amount and frequency configuration",
    ],
    full_img(mf[11])
)

# ss12: Set Up SIP — Step 2 Configure SIP
mf6 = screen_slide(
    "s57",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · SIP Setup · Step 2 of 4",
    "Configure Your SIP",
    "Amount, frequency, start date, and optional end date",
    [
        "SIP Frequency: Monthly or Quarterly — Monthly selected by default",
        "Enter amount per installment — minimum varies by scheme (e.g. ₹1,000)",
        "Quick-select tiles: ₹5,000 / ₹10,000 / ₹25,000 / ₹50,000 / ₹1 L",
        "SIP Start Date auto-sets the monthly debit day — leave End Date blank for a perpetual SIP",
    ],
    full_img(mf[12]),
    extra_badge=badge("Leave End Date blank for perpetual SIP","#bae6fd")
)

# ss13: Place New Order — Step 3 Select Bank
mf7 = screen_slide(
    "s58",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Lumpsum Order · Step 3 of 4",
    "Select Bank Account",
    "Choose the registered account to debit for this investment",
    [
        "All registered bank accounts displayed — select any one for this order",
        "Account shows: bank name, masked account number, account type, IFSC",
        "Different bank accounts can be selected for different orders",
        "Click 'Continue' to proceed to the final review before order placement",
    ],
    full_img(mf[13])
)

# ss14: Place New Order — Step 4 Review & Confirm
mf8 = screen_slide(
    "s59",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Lumpsum Order · Step 4 of 4",
    "Review &amp; Confirm Order",
    "Final check — investor, scheme, amount, and payment method",
    [
        "Summary: Investor name, Order Type (Lumpsum/SIP), Scheme, Amount, Payment method",
        "Authorisation notice: 'By clicking confirm, you authorize BSE to debit ₹X via your registered mandate'",
        "Click 'Confirm Order' to place the trade directly with BSE",
        "Order reflects in portfolio within 1–2 working days of confirmation",
    ],
    full_img(mf[14]),
    extra_badge=badge("Orders placed directly with BSE","#bae6fd")
)

# ss3: Portfolio Dashboard
mf9 = screen_slide(
    "s60",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Portfolio",
    "Portfolio Dashboard",
    "Total invested, current value, gain, and XIRR at a glance",
    [
        "4 key metrics: Total Invested, Current Value, Total Gain (absolute ₹), XIRR (annualised %)",
        "Portfolio History chart: toggle 1M / 3M / 6M / 1Y / YTD to view value over time",
        "Portfolio Allocation donut: breakdown by Equity, Debt, Hybrid asset classes",
        "Tabs below: Holdings, Mandates, SIP, STP, SWP — number badge shows count in each",
    ],
    full_img(mf[3]),
    extra_badge=badge("XIRR = your effective annualised return","#bae6fd")
)

# ss4: Portfolio Holdings
mf10 = screen_slide(
    "s61",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Portfolio · Holdings",
    "Holdings — Per-Scheme Breakdown",
    "Current value, invested, units, and NAV for every fund held",
    [
        "Each fund card shows: Current Value, Invested Amount, Units held, Current NAV",
        "Gain/loss shown as both ₹ absolute and % returns per scheme",
        "Click 'Redeem' on any card to initiate a redemption order for that scheme",
        "Click 'View Transactions' to see all activity (buy/sell/switch) for that specific fund",
    ],
    full_img(mf[4]),
    extra_badge=badge("Redeem button available on every fund card","#bae6fd")
)

# ss5: Mandates tab
mf11 = screen_slide(
    "s62",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Portfolio · Mandates",
    "Mandates",
    "One-time bank authorization for all future SIP auto-debits",
    [
        "A mandate authorises the platform to auto-debit the bank account for SIP installments",
        "Set with a high limit (e.g. ₹50,000) to cover all SIPs without repeat authorisation",
        "Type: eNACH — registered once, valid for 10 years (e.g. 2026–2036)",
        "Status flow: Awaiting Authorization → Active — click 'Create Mandate' to register a new one",
    ],
    full_img(mf[5]),
    extra_badge=badge("One mandate covers all SIPs — valid 10 years","#bae6fd")
)

# ss6: STP tab — list of 4 STPs
mf12 = screen_slide(
    "s63",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Portfolio · STP",
    "Systematic Transfer Plans (STP)",
    "Auto-move money between funds at regular intervals",
    [
        "STP transfers a fixed amount from a source fund to a destination fund periodically",
        "Common use: shift corpus from a debt/liquid fund into an equity fund monthly",
        "Each STP card shows: amount, frequency (Weekly/Monthly), start date, registered date",
        "Status types: Awaiting Authorization, Auto Cancelled, Active — click 'View Details' for full info",
    ],
    full_img(mf[6]),
    extra_badge=badge("e.g. ₹5,000/month from liquid fund → equity fund","#bae6fd")
)

# ss7: STP/SIP detail view
mf13 = screen_slide(
    "s64",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · STP / SIP Detail",
    "Plan Detail View",
    "Full schedule, folio, status timeline, and installment history",
    [
        "Plan Details: Scheme Code, Frequency, Start Date, Destination Scheme, Folio, Total Installments",
        "Status Timeline: every status change with timestamp — e.g. '2FA Pending', 'Cancelled'",
        "Installment History: all executed installments to date — empty if none have run yet",
        "Use this screen to troubleshoot any STP or SIP that appears stuck or cancelled",
    ],
    full_img(mf[7])
)

# ss2: Orders — transaction history
mf14 = screen_slide(
    "s65",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Orders",
    "Orders — Transaction History",
    "Every buy, sell, and switch with full BSE traceability",
    [
        "All order types listed: Purchase, Redemption, Switch — with Order ID and BSE reference",
        "Columns: Scheme, Order ID, Type, Amount, Status, Date — all sortable",
        "Status badge: 'Order Placed' shown in real-time after confirmation",
        "Click 'View →' on any row to see complete order details including BSE status",
    ],
    full_img(mf[2]),
    extra_badge=badge("BSE Order ID available for every transaction","#bae6fd")
)

# ss8: Calculators menu
mf15 = screen_slide(
    "s66",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Calculators",
    "MF Calculators",
    "Plan before you invest — 9 calculators for every scenario",
    [
        "Core: SIP, Lumpsum, SIP Step-Up, SIP Delay, Lumpsum + SIP",
        "Systematic: SWP Calculator (withdrawals), STP Calculator (fund transfers)",
        "Planning: Goal Planning (SIP needed for a target), Retirement Calculator",
        "Use SIP Delay to show clients the cost of waiting — powerful for conversion",
    ],
    full_img(mf[8]),
    extra_badge=badge("SIP Delay Calculator is a powerful sales tool","#bae6fd")
)

# ss9: SIP Calculator result
mf16 = screen_slide(
    "s67",
    "linear-gradient(160deg, #083344, #0284c7)",
    "Module 06 · Mutual Funds · Calculators · SIP",
    "SIP Calculator",
    "₹5,000/month at 12% for 10 years → ₹11.62 lakh corpus",
    [
        "Inputs: Monthly Investment (₹100–₹10L), Expected Return % (1–30), Period (1–40 years)",
        "Outputs: Total Invested, Estimated Returns, Future Value, Wealth Gain multiple",
        "Corpus Growth Chart shows year-by-year value split between invested and returns",
        "Run this live with the client — adjust inputs in real-time to match their goals",
    ],
    full_img(mf[9]),
    extra_badge=badge("₹6L invested → ₹11.62L corpus at 12% over 10 years","#bae6fd")
)

# SLIDE 66 — Summary cover
def summary_step(n, text):
    return f'<div class="sum-step"><span class="sum-n">{n}</span><span>{text}</span></div>'

def summary_bullet(text):
    return f'<div class="sum-bullet">&#8227; {text}</div>'

summary_left = f'''<div class="sum-col">
  <div class="sum-col-title">Distributor KYC · 5 Steps</div>
  {summary_step(1,"Sign Up → OTP Verification (Mobile + Email)")}
  {summary_step(2,"PAN + Business Type (HyperVerge)")}
  {summary_step(3,"Address (CIN or Documents)")}
  {summary_step(4,"Bank Account (Penny Drop or Manual)")}
  {summary_step(5,"GST (Optional → Mandatory at ₹10L)")}
  {summary_step(6,"eSign Agreement → T&amp;C → Ops Review → Live")}
</div>'''

summary_right = f'''<div class="sum-col">
  <div class="sum-col-title">Post-Approval Features</div>
  {summary_bullet("Clients Dashboard → Add investors → Track KYC")}
  {summary_bullet("Navigate to products: FD / MF")}
  {summary_bullet("Team Members → Add RMs → Assign roles")}
  {summary_bullet("Organisation Hierarchy → Build firm structure → Map partners")}
</div>'''

slide37 = f'''<div id="s68" class="slide cover" style="background:linear-gradient(135deg, #0f172a, #1e3a5f, #2563eb);">
  <div class="cover-inner">
    <div class="eyebrow">Complete Journey</div>
    <h1>From Sign-Up to Live</h1>
    <div class="sum-grid">
      {summary_left}
      {summary_right}
    </div>
  </div>
</div>'''

# ── 4. Assemble HTML ──────────────────────────────────────────────────────────

all_slides = [slide2,slide3,slide4,slide5,slide6,slide7,slide8,
              slide9,slide10,slide11,slide12,slide13,slide14,slide15,slide16,
              slide17,slide18,slide19,slide21,slide22,slide23,slide24,
              slide25,slide26,slide27,slide28,slide29,slide30,slide31,slide32,
              slide33,slide34,slide_tm,slide35,slide36,oh2,oh4,oh5,oh3,
              fd_cover,fd1,fd3,fd5,fd7,fd8,fd9,fd10,fd11,fd12,
              mf_cover,mf1,mf2,mf3,mf4,mf5,mf6,mf7,mf8,mf9,mf10,mf11,mf12,mf13,mf14,mf15,mf16,
              slide37]

slides_html = "\n".join(all_slides)

dots_nav = "".join(
    f'<button class="dot" data-idx="{i}" aria-label="Go to slide {i+1}"></button>'
    for i in range(67)
)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>YMPL Vista · User Journey Deck</title>
<style>
/* ── Reset & base ─────────────────────────────────────────────────────── */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
body{{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:#0d1117;
  min-height:100vh;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:flex-start;
  padding:24px 16px 32px;
  color:#f8fafc;
}}

/* ── Deck wrapper ─────────────────────────────────────────────────────── */
#deck-wrap{{
  width:min(100%,1200px);
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:16px;
}}

/* ── Slide container ─────────────────────────────────────────────────── */
#deck{{
  width:100%;
  aspect-ratio:16/9;
  border-radius:14px;
  overflow:hidden;
  position:relative;
  box-shadow:0 24px 80px rgba(0,0,0,.6);
}}

/* ── Slide base ──────────────────────────────────────────────────────── */
.slide{{
  position:absolute;
  inset:0;
  display:none;
  width:100%;
  height:100%;
}}
.slide.active{{display:flex;}}

/* ── Cover slide ─────────────────────────────────────────────────────── */
.cover{{
  flex-direction:column;
  align-items:center;
  justify-content:center;
  text-align:center;
  padding:40px 60px;
}}
.cover-inner{{
  max-width:760px;
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:14px;
}}
.eyebrow{{
  font-size:.65rem;
  font-weight:700;
  letter-spacing:.14em;
  text-transform:uppercase;
  color:#93c5fd;
  opacity:.9;
}}
.cover h1{{
  font-size:2.6rem;
  font-weight:800;
  line-height:1.15;
  color:#fff;
  text-shadow:0 2px 20px rgba(0,0,0,.4);
}}
.cover-sub{{
  font-size:.82rem;
  color:#cbd5e1;
  line-height:1.6;
  max-width:560px;
}}
.tags{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:4px;}}
.badge{{
  display:inline-block;
  padding:3px 10px;
  border-radius:999px;
  font-size:.6rem;
  font-weight:600;
  letter-spacing:.04em;
}}
.chips{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:6px;}}
.stat-chip{{
  background:rgba(255,255,255,.12);
  border:1px solid rgba(255,255,255,.2);
  border-radius:8px;
  padding:6px 14px;
  font-size:.68rem;
  font-weight:600;
  color:#e2e8f0;
  backdrop-filter:blur(4px);
}}
.cover-label{{
  font-size:.58rem;
  color:#64748b;
  margin-top:4px;
  letter-spacing:.06em;
}}

/* ── Two-col layout ──────────────────────────────────────────────────── */
.two-col{{flex-direction:row;}}
.left-panel{{
  width:30%;
  flex-shrink:0;
  padding:20px 18px;
  display:flex;
  flex-direction:column;
  gap:6px;
  overflow-y:auto;
}}
.lp-num{{
  font-size:.55rem;
  font-weight:700;
  letter-spacing:.12em;
  text-transform:uppercase;
  color:#93c5fd;
  opacity:.8;
}}
.lp-ttl{{
  font-size:1.05rem;
  font-weight:800;
  color:#fff;
  line-height:1.2;
}}
.lp-sub{{
  font-size:.6rem;
  color:#bfdbfe;
  line-height:1.5;
  margin-bottom:4px;
}}

/* ── KYC dots ────────────────────────────────────────────────────────── */
.kyc-dots{{
  display:flex;
  align-items:center;
  gap:5px;
  margin:4px 0;
}}
.kd{{
  border-radius:50%;
  display:flex;
  align-items:center;
  justify-content:center;
}}
.kd-done{{width:8px;height:8px;background:#60a5fa;opacity:.7;}}
.kd-active{{
  width:20px;height:20px;
  background:#2563eb;
  font-size:.5rem;font-weight:700;color:#fff;
  box-shadow:0 0 0 3px rgba(37,99,235,.3);
}}
.kd-pending{{width:8px;height:8px;background:#475569;}}

/* ── Takeaway box (key points) ───────────────────────────────────────── */
.takeaway-box{{
  background:rgba(255,255,255,.07);
  border-left:3px solid rgba(255,255,255,.3);
  border-radius:0 6px 6px 0;
  padding:8px 10px;
  flex:1;
  min-height:0;
  overflow-y:auto;
}}
.tb-title{{
  font-size:.52rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.1em;
  color:#93c5fd;
  margin-bottom:5px;
}}
.kp-list{{
  list-style:none;
  display:flex;
  flex-direction:column;
  gap:5px;
}}
.kp-list li{{
  font-size:.58rem;
  color:#e2e8f0;
  line-height:1.45;
  padding-left:10px;
  position:relative;
}}
.kp-list li::before{{
  content:"›";
  position:absolute;
  left:0;
  color:#60a5fa;
  font-weight:700;
}}

/* ── Callout ─────────────────────────────────────────────────────────── */
.lp-callout{{
  font-size:.52rem;
  color:#bfdbfe;
  background:rgba(255,255,255,.06);
  border-radius:6px;
  padding:5px 8px;
  margin-top:2px;
}}

/* ── Right panel ─────────────────────────────────────────────────────── */
.right-panel{{
  flex:1;
  background:#fff;
  padding:16px 20px;
  overflow-y:auto;
  display:flex;
  flex-direction:column;
}}
.rp-title{{
  font-size:.65rem;
  font-weight:700;
  color:#1e3a5f;
  text-transform:uppercase;
  letter-spacing:.08em;
  margin-bottom:10px;
  flex-shrink:0;
}}

/* ── Summary slide ───────────────────────────────────────────────────── */
.sum-grid{{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:24px;
  width:100%;
  max-width:760px;
  margin-top:8px;
  text-align:left;
}}
.sum-col{{
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.12);
  border-radius:12px;
  padding:16px 18px;
  display:flex;
  flex-direction:column;
  gap:8px;
}}
.sum-col-title{{
  font-size:.65rem;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.1em;
  color:#93c5fd;
  margin-bottom:4px;
}}
.sum-step{{
  display:flex;
  align-items:flex-start;
  gap:8px;
  font-size:.64rem;
  color:#e2e8f0;
  line-height:1.4;
}}
.sum-n{{
  background:#2563eb;
  color:#fff;
  border-radius:50%;
  width:16px;height:16px;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  font-size:.5rem;
  font-weight:700;
  flex-shrink:0;
  margin-top:1px;
}}
.sum-bullet{{
  font-size:.64rem;
  color:#cbd5e1;
  line-height:1.5;
  padding-left:4px;
}}

/* ── Navigation ──────────────────────────────────────────────────────── */
#nav{{
  display:flex;
  align-items:center;
  gap:14px;
  user-select:none;
}}
.nav-btn{{
  background:rgba(255,255,255,.08);
  border:1px solid rgba(255,255,255,.15);
  border-radius:8px;
  color:#e2e8f0;
  font-size:.8rem;
  padding:7px 16px;
  cursor:pointer;
  transition:background .15s,transform .1s;
  font-family:inherit;
}}
.nav-btn:hover{{background:rgba(255,255,255,.16);transform:scale(1.04);}}
.nav-btn:active{{transform:scale(.97);}}
.nav-btn:disabled{{opacity:.3;cursor:default;transform:none;}}
#dots{{display:flex;gap:6px;align-items:center;}}
.dot{{
  width:8px;height:8px;
  border-radius:50%;
  background:rgba(255,255,255,.22);
  border:none;
  cursor:pointer;
  transition:background .2s,transform .2s;
  padding:0;
}}
.dot.active{{background:#3b82f6;transform:scale(1.4);}}
.dot:hover:not(.active){{background:rgba(255,255,255,.45);}}
#slide-counter{{
  font-size:.6rem;
  color:#475569;
  min-width:46px;
  text-align:center;
}}

/* ── Screen-slide layout ─────────────────────────────────────────────── */
.screen-slide{{flex-direction:column;}}
.s-header{{
  display:flex;
  flex-direction:row;
  align-items:flex-start;
  gap:16px;
  padding:10px 24px;
  flex-shrink:0;
}}
.s-hdr-left{{flex:1;display:flex;flex-direction:column;gap:3px;min-width:0;}}
.s-hdr-right{{flex-shrink:0;max-width:340px;}}
.s-eyebrow{{font-size:.55rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.5);}}
.s-title{{font-size:1.05rem;font-weight:800;color:#fff;line-height:1.2;}}
.s-sub{{font-size:.6rem;color:rgba(255,255,255,.8);line-height:1.4;margin-top:1px;}}
.s-points{{display:flex;flex-direction:column;gap:3px;}}
.sp-bullet{{font-size:.58rem;color:rgba(255,255,255,.9);line-height:1.4;padding-left:10px;position:relative;}}
.sp-bullet::before{{content:"›";position:absolute;left:0;color:rgba(255,255,255,.5);font-weight:700;}}
.s-body{{
  flex:1;
  min-height:0;
  background:#f1f5f9;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:10px 24px 12px;
}}
.s-img{{max-width:100%;max-height:100%;width:auto;height:100%;object-fit:contain;border-radius:6px;box-shadow:0 2px 16px rgba(0,0,0,.12);}}
</style>
</head>
<body>

<div id="deck-wrap">

  <div id="deck">
{slides_html}
  </div>

  <div id="nav">
    <button class="nav-btn" id="prev-btn" disabled>&#8592; Prev</button>
    <div id="dots">{dots_nav}</div>
    <button class="nav-btn" id="next-btn">Next &#8594;</button>
    <span id="slide-counter">1 / 67</span>
  </div>

</div>

<script>
(function(){{
  const total = 67;
  let cur = 0;

  const slides  = Array.from({{length:total}},(_,i)=>document.getElementById('s'+(i+2)));
  const dots    = Array.from(document.querySelectorAll('.dot'));
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const counter = document.getElementById('slide-counter');

  function show(n){{
    slides[cur].classList.remove('active');
    dots[cur].classList.remove('active');
    cur = (n + total) % total;
    slides[cur].classList.add('active');
    dots[cur].classList.add('active');
    prevBtn.disabled = (cur === 0);
    nextBtn.disabled = (cur === total - 1);
    counter.textContent = (cur+1)+' / '+total;
  }}

  // init
  slides[0].classList.add('active');
  dots[0].classList.add('active');
  prevBtn.disabled = true;
  counter.textContent = '1 / '+total;

  prevBtn.addEventListener('click', ()=>show(cur-1));
  nextBtn.addEventListener('click', ()=>show(cur+1));
  dots.forEach((d,i)=>d.addEventListener('click',()=>show(i)));

  document.addEventListener('keydown', e=>{{
    if(e.key==='ArrowRight'||e.key==='ArrowDown') show(cur+1);
    if(e.key==='ArrowLeft'||e.key==='ArrowUp')   show(cur-1);
  }});
}})();
</script>

</body>
</html>'''

# ── 5. Write output ───────────────────────────────────────────────────────────
with open(DEST, "w", encoding="utf-8") as f:
    f.write(html)

size = os.path.getsize(DEST)
print(f"Done. Written to: {DEST}")
print(f"File size: {size:,} bytes  ({size/1024/1024:.2f} MB)")
print(f"Images extracted: {len(imgs)}")
