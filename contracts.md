# API Contracts - Social Media Website

## Frontend Components
- ProfileSection: Display user profile photo and name
- SocialLinksGrid: Display social media links with icons 
- ContactForm: Form untuk masukan dan kritik
- Footer: Information about website creation

## Mock Data (to be replaced)
- socialLinks: Array of social media platforms with URLs
- ContactForm: Currently shows success toast without actual email sending

## Backend Implementation Needed

### Email Service
- **Service**: Nodemailer with Gmail SMTP
- **Purpose**: Send contact form messages to Mochsyafrilramadhani5@gmail.com
- **Required**: Gmail App Password from user

### API Endpoints

#### POST /api/contact
**Purpose**: Send contact form message via email
**Request Body**:
```json
{
  "name": "string (required)",
  "email": "string (required, valid email)",
  "message": "string (required)"
}
```

**Response Success (200)**:
```json
{
  "success": true,
  "message": "Email sent successfully"
}
```

**Response Error (400/500)**:
```json
{
  "success": false,
  "error": "Error message"
}
```

### Environment Variables Needed
- GMAIL_EMAIL: Gmail address (Mochsyafrilramadhani5@gmail.com)
- GMAIL_APP_PASSWORD: Gmail App Password (to be provided by user)

### Frontend Integration
- Remove mock email submission in ContactForm.jsx
- Replace with actual API call to POST /api/contact
- Handle success/error responses properly
- Show appropriate toast messages

### Dependencies to Install
- nodemailer: For sending emails
- @types/nodemailer (if needed)