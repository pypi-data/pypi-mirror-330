# ZeptoMail Client API Reference (LLM-friendly)

This document contains the complete API reference for the ZeptoMail client,
formatted specifically for use with Large Language Models (LLMs).

This documentation includes all method signatures and their docstrings,
but excludes implementation details.

# ZeptoMail

A Python client for interacting with the ZeptoMail API.

Note: This is an unofficial SDK. Namilink Kft is not affiliated with ZeptoMail.

## Methods

### ZeptoMail(self, api_key: str, base_url: str = 'https://api.zeptomail.eu/v1.1')

Initialize the ZeptoMail client.

Args:
    api_key: Your ZeptoMail API key
    base_url: The base URL for the ZeptoMail API (defaults to https://api.zeptomail.eu/v1.1)

---

### add_attachment_from_content(self, content: str, mime_type: str, name: str) -> Dict

Add an attachment using base64 encoded content.

Args:
    content: Base64 encoded content
    mime_type: MIME type of the content
    name: Name for the file

Returns:
    Attachment dictionary

---

### add_attachment_from_file_cache(self, file_cache_key: str, name: Optional[str] = None) -> Dict

Add an attachment using a file cache key.

Args:
    file_cache_key: File cache key from ZeptoMail
    name: Optional name for the file

Returns:
    Attachment dictionary

---

### add_batch_recipient(self, email: str, name: Optional[str] = None, merge_info: Optional[Dict] = None) -> Dict

Create a batch recipient object with merge info.

Args:
    email: Email address
    name: Recipient name
    merge_info: Merge fields for this recipient

Returns:
    Recipient dictionary with format {"email_address": {"address": email, "name": name}, "merge_info": {...}}

---

### add_inline_image(self, cid: str, content: Optional[str] = None, mime_type: Optional[str] = None, file_cache_key: Optional[str] = None) -> Dict

Add an inline image to the email.

Args:
    cid: Content ID to reference in HTML
    content: Base64 encoded content
    mime_type: MIME type of the content
    file_cache_key: File cache key from ZeptoMail

Returns:
    Inline image dictionary

---

### add_recipient(self, email: str, name: Optional[str] = None) -> Dict

Create a recipient object for use in to, cc, bcc lists.

Args:
    email: Email address
    name: Recipient name

Returns:
    Recipient dictionary with format {"email_address": {"address": email, "name": name}}

---

### build_sender(self, email: str, name: Optional[str] = None) -> Dict

Build a sender object.

Args:
    email: Email address of the sender
    name: Name of the sender

Returns:
    Dict containing sender details with format {"address": email, "name": name}
    
Raises:
    ZeptoMailError: If the email address is invalid

---

### send_batch_email(self, from_email: str, from_name: Optional[str] = None, to: List[Dict] = None, cc: List[Dict] = None, bcc: List[Dict] = None, subject: str = '', html_body: Optional[str] = None, text_body: Optional[str] = None, attachments: List[Dict] = None, inline_images: List[Dict] = None, track_clicks: bool = True, track_opens: bool = True, client_reference: Optional[str] = None, mime_headers: Optional[Dict] = None, merge_info: Optional[Dict] = None) -> Dict

Send a batch email using the ZeptoMail API.

Args:
    from_email: Sender's Email address
    from_name: Sender's name
    to: List of recipient dictionaries with optional merge_info
    cc: List of cc recipient dictionaries
    bcc: List of bcc recipient dictionaries
    subject: Email subject
    html_body: HTML content of the email
    text_body: Plain text content of the email
    attachments: List of attachment dictionaries
    inline_images: List of inline image dictionaries
    track_clicks: Whether to track clicks
    track_opens: Whether to track opens
    client_reference: Client reference identifier
    mime_headers: Additional MIME headers
    merge_info: Global merge info for recipients without specific merge info

Returns:
    API response as a dictionary
    
Raises:
    ZeptoMailError: If required fields are missing or API returns an error

---

### send_email(self, from_email: str, from_name: Optional[str] = None, to: List[Dict] = None, cc: List[Dict] = None, bcc: List[Dict] = None, reply_to: List[Dict] = None, subject: str = '', html_body: Optional[str] = None, text_body: Optional[str] = None, attachments: List[Dict] = None, inline_images: List[Dict] = None, track_clicks: bool = True, track_opens: bool = True, client_reference: Optional[str] = None, mime_headers: Optional[Dict] = None) -> Dict

Send a single email using the ZeptoMail API.

Args:
    from_email: Sender's Email address
    from_name: Sender's name
    to: List of recipient dictionaries
    cc: List of cc recipient dictionaries
    bcc: List of bcc recipient dictionaries
    reply_to: List of reply-to dictionaries
    subject: Email subject
    html_body: HTML content of the email
    text_body: Plain text content of the email
    attachments: List of attachment dictionaries
    inline_images: List of inline image dictionaries
    track_clicks: Whether to track clicks
    track_opens: Whether to track opens
    client_reference: Client reference identifier
    mime_headers: Additional MIME headers

Returns:
    API response as a dictionary
    
Raises:
    ZeptoMailError: If required fields are missing or API returns an error

---
