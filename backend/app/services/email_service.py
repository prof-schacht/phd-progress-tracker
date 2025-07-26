"""Email notification service."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending email notifications."""
    
    def __init__(self):
        """Initialize email service with Jinja2 template environment."""
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates', 'emails')
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        context: Dict[str, Any],
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email using a template.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            template_name: Name of the template file (without extension)
            context: Context data for the template
            cc: List of CC recipients
            bcc: List of BCC recipients
            
        Returns:
            bool: True if email was sent successfully
        """
        try:
            # For development with mailhog or when SMTP is not configured
            if not settings.SMTP_HOST or settings.SMTP_HOST == "localhost":
                logger.info(f"Email service not configured. Would send email to {to_email}: {subject}")
                logger.info(f"Email content preview: {context}")
                return True
            
            # Render templates
            html_template = self.env.get_template(f"{template_name}.html")
            text_template = self.env.get_template(f"{template_name}.txt")
            
            html_content = html_template.render(**context)
            text_content = text_template.render(**context)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{settings.PROJECT_NAME} <{settings.EMAILS_FROM_EMAIL}>"
            msg['To'] = to_email
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Add parts
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            if settings.SMTP_TLS:
                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    server.starttls()
                    if settings.SMTP_USER and settings.SMTP_PASSWORD:
                        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    
                    recipients = [to_email]
                    if cc:
                        recipients.extend(cc)
                    if bcc:
                        recipients.extend(bcc)
                    
                    server.send_message(msg, to_addrs=recipients)
            else:
                with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    if settings.SMTP_USER and settings.SMTP_PASSWORD:
                        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    
                    recipients = [to_email]
                    if cc:
                        recipients.extend(cc)
                    if bcc:
                        recipients.extend(bcc)
                    
                    server.send_message(msg, to_addrs=recipients)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    async def send_reminder_email(
        self,
        to_email: str,
        user_name: str,
        reminder_type: str,
        entity_type: str,
        entity_details: Dict[str, Any]
    ) -> bool:
        """
        Send a reminder email.
        
        Args:
            to_email: Recipient email
            user_name: Name of the user
            reminder_type: Type of reminder (e.g., 'T-3days', 'T-0')
            entity_type: What the reminder is for (e.g., 'report_period')
            entity_details: Details about the entity
            
        Returns:
            bool: True if sent successfully
        """
        subject_map = {
            'T-3days': f"Reminder: {entity_details.get('title', 'Deadline')} due in 3 days",
            'T-0': f"Due Today: {entity_details.get('title', 'Deadline')}",
            'T+2days': f"Overdue: {entity_details.get('title', 'Deadline')} was due 2 days ago",
            'T+7days': f"Urgent: {entity_details.get('title', 'Deadline')} overdue by 7 days"
        }
        
        context = {
            'user_name': user_name,
            'reminder_type': reminder_type,
            'entity_type': entity_type,
            'entity_details': entity_details,
            'current_year': datetime.utcnow().year,
            'app_url': settings.FRONTEND_URL
        }
        
        return await self.send_email(
            to_email=to_email,
            subject=subject_map.get(reminder_type, "Reminder from PhD Progress Tracker"),
            template_name='reminder',
            context=context
        )
    
    async def send_test_email(self, to_email: str) -> bool:
        """Send a test email to verify configuration."""
        context = {
            'user_name': 'Test User',
            'current_year': datetime.utcnow().year,
            'app_url': settings.FRONTEND_URL
        }
        
        return await self.send_email(
            to_email=to_email,
            subject="PhD Progress Tracker - Test Email",
            template_name='test',
            context=context
        )


# Global instance
email_service = EmailService()