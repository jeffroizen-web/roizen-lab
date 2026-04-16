# Contact Form Status & Jeff Unblock Steps

**Built**: 2026-04-16 (overnight by Ace Scout, with Kleiber dispatch)
**State**: Layer 1 built and locally tested. Two small Jeff steps remaining before the form is live. Layer 2 (Telegram → Kleiber) is deferred.

---

## What the form does now (Layer 1)

Visitor opens the site → scrolls to **Contact** → fills name / email / subject / message → presses **Send**. Two things happen in parallel:

1. **Formspree** routes the submission to your inbox at `jeffroizen@gmail.com`. Persistent record, searchable, spam-filtered.
2. **ntfy.sh push** fires to the `roizen-lab-contact` topic with `From: {name} — {subject}` as the push body. Sub-second delivery to your phone (assuming the ntfy app is subscribed to the topic).

Honeypot field blocks the dumb spam bots. Client-side HTML5 validation catches missing fields before submission. Non-Formspree configuration shows a fallback message telling the visitor to email you directly. All WCAG AA: proper labels, focus-visible, aria-live status region for screen readers.

---

## What YOU need to do to unblock it (about 2 minutes, one time)

### Step 1 — Create the Formspree account (~1 min)

1. Go to https://formspree.io → sign up with `jeffroizen@gmail.com`. Free tier gives you 50 submissions/month, which is plenty for a lab contact form.
2. Create a new form. Any name — call it "Roizen Lab Contact" or similar.
3. Formspree will show you a form endpoint that looks like `https://formspree.io/f/abcd1234`. Copy the `abcd1234` portion — that's your form ID.
4. In `compare-purple-gold.html`, find `FORMSPREE_ID_HERE` (the action attribute of the `#contact-form` element) and replace with your ID. One edit.
5. Formspree will email you asking to confirm the email address on first submission — confirm it, then all future submissions arrive immediately.

### Step 2 — Subscribe to the ntfy topic on your phone (~1 min)

1. Open the **ntfy** app on your phone (the same one you use for the orchestra's `mlb-edge-alerts-jeff` topic).
2. Tap **+** (add subscription) → topic name: `roizen-lab-contact` → Subscribe.
3. The server is the default `ntfy.sh` (public). The topic is a freeform string — anyone who knows the topic name can post to it. This is fine for a contact-form push: the worst case is someone posts a joke message. If the topic ever gets spam-blasted, rotate to a less guessable name in the HTML `data-ntfy-topic` attribute.

That's it. The form is now live end-to-end.

---

## How to test

Locally first:

```bash
cd "/Users/roizenj/Desktop/Claude Apps/Roizen Lab"
python3 -m http.server 8765
```

Open http://localhost:8765/compare-purple-gold.html#contact — fill the form with a test message. You should see:
- Green success status under the Send button
- Formspree email in your inbox (or a confirm-email prompt on first use)
- Ntfy push on your phone immediately

If the Formspree endpoint is still `FORMSPREE_ID_HERE`, the form shows an explicit "not configured" error instead of silently failing. That message also points to `jeffroizen@gmail.com` as a fallback.

---

## What's NOT done — Layer 2 (Telegram to Kleiber)

Kleiber asked for a third channel: when someone submits the contact form, also send a Telegram message to Kleiber so Kleiber sees "New lab contact: {name} — {subject}" in the shared chat.

**Why this is Layer 2**: the Telegram piece needs a hosted HTTP endpoint that holds `TELEGRAM_BOT_TOKEN` and calls the Bot API. The existing `scripts/telegram-respond.sh` is local-only — it can't be called from a static site's JavaScript.

**Recommended home**: Pilot (Ulysses) already has Railway deployment, TypeScript, and can hold the bot token in its environment. Add a tiny `/api/roizen-contact` endpoint (~30 lines) that accepts `{name, subject}` POST and forwards to Telegram Bot API. Then add a fourth `fetch()` to the contact form JS.

**Requires**: Jeff approval to deploy + coordination with Pilot's CM.

Not needed for initial site launch. Add to backlog.

---

## If something goes wrong

- **No email arriving**: Check Formspree dashboard → submissions log. Usually it's a missing email confirmation on first submission.
- **No ntfy push**: Open the ntfy app → pull-to-refresh on the topic. Verify topic name matches `roizen-lab-contact` exactly. Test with `curl -d "test" https://ntfy.sh/roizen-lab-contact` from any terminal.
- **"Form is not configured yet" error on the page**: The `FORMSPREE_ID_HERE` placeholder is still in the HTML. Swap it per Step 1 above.
- **Submission fails silently**: Check browser devtools → Network. Formspree returns 4xx with a JSON `errors[0].message` explaining the cause (most common: unverified email, rate limit).

---

## File changes

- `compare-purple-gold.html` — added Contact form UI, form CSS block, JS submit handler with Formspree + ntfy parallel dispatch. Preserved the original Contact info columns (Location + Email + Join the Lab) on the left of a 2-column grid.
- `docs/contact-form-status.md` — this file.

Nothing deployed. Working file only. Ready when you are.
