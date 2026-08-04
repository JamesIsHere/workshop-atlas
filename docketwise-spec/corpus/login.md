# module: login

Docketwise's own vocabulary (help-center category "Login", 2
articles, fx-0003). Phase 3 sparse-tail module: full extraction from
the collection page (fx-0227) and articles fx-0228..fx-0229. No
embeds. Nav-grouping category, so no module anchor
(personal-settings precedent). The MFA ground is owned cross-module:
firm-settings.two-factor-authentication joined in-place (+fx-0228:
first-login MFA, same three delivery methods, remember-device
option). The homepage nav "Login" link (fx-0001) was considered and
NOT cited: it attests a login surface exists but not the
email/password mechanic this module's criteria name, and citing it
would force a confirmed tier the evidence does not support (check-4
bidirectionality). Carve: email/password login + firm custom
subdomains + password reset.

## entry: login.email-password-login
- name: How to Login to 8am DocketWise
- named-by-us: no
- description: Users log in at www.docketwise.com/login (the app
  lives at app.docketwise.com) by entering the email address and
  password associated with their Docketwise account (fx-0227,
  fx-0228, fx-0229).
- criterion: User enters their account email and password on the
  login page and clicks Log In -> they are authenticated into their
  firm's account
- sources: fx-0227, fx-0228, fx-0229
- tier: provisional
- detail: A user with access to multiple firm accounts logs into
  the correct firm subdomain to reach the intended account
  (fx-0228). Loading app.docketwise.com/logout clears the session
  (fx-0229). First login requires MFA enrollment -- owned by
  firm-settings.two-factor-authentication.

## entry: login.firm-custom-subdomain
- name: Custom Subdomain
- named-by-us: no
- description: A firm can use a custom subdomain of docketwise.com
  (e.g. immigration-law-partners.docketwise.com) and users can log
  in directly from it (fx-0228).
- criterion: User visits their firm's custom subdomain -> the
  firm's login page is served and login proceeds there
- sources: fx-0228
- tier: provisional

## entry: login.password-reset
- name: Forgot Your Password?
- named-by-us: no
- description: A forgotten password is reset from the login page via
  Forgot your password?: the user enters their account email and
  receives an email with a password reset link to create a new
  password (fx-0228, fx-0229).
- criterion: User clicks Forgot your password? and submits their
  account email -> a reset-link email is sent and completing it sets
  a new password
- sources: fx-0228, fx-0229
- tier: provisional
