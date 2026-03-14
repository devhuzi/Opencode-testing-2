# Send Onboarding Welcome Email

## Goal
Send a personalized welcome email to new contacts when provided with their name and email address.

## Inputs
- `name` (string): Full name of the new contact
- `email` (string): Email address of the new contact

## Outputs
- Email sent successfully to the provided address
- Console confirmation with recipient details

## Tools
- Python script: `execution/send_onboarding_email.py`
- Email library: `smtplib` (built-in)

## Workflow
1. Validate email format using regex
2. Load SMTP credentials from `.env`
3. Connect to SMTP server (smtp.purelymail.com:465)
4. Send welcome email with personalized template
5. Log success/failure to console

## Edge Cases
- **Invalid email format**: Show error "Invalid email format", do not attempt send
- **SMTP connection failure**: Retry up to 3 times with 2-second delay, then raise error
- **SMTP authentication failure**: Raise error with message "SMTP authentication failed"
- **Empty name**: Use "Friend" as default greeting

## Email Template
- **Subject**: Welcome to One Step Sol – Let's Get Started!
- **From**: admin@onestepsol.com

## Example Usage
```bash
python execution/send_onboarding_email.py "John Doe" john@example.com
```
