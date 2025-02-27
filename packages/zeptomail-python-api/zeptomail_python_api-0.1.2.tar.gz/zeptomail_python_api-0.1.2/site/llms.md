# ZeptoMail Client

This page documents the main `ZeptoMail` client class and its methods.

## Class Reference

### `ZeptoMail`

A Python client for interacting with the ZeptoMail API.

Note: This is an unofficial SDK. Namilink Kft is not affiliated with ZeptoMail.

Source code in `zeptomail/client.py`

```
class ZeptoMail:
    """A Python client for interacting with the ZeptoMail API.

    Note: This is an unofficial SDK. Namilink Kft is not affiliated with ZeptoMail.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.zeptomail.eu/v1.1"):
        """
        Initialize the ZeptoMail client.

        Args:
            api_key: Your ZeptoMail API key
            base_url: The base URL for the ZeptoMail API (defaults to https://api.zeptomail.eu/v1.1)
        """
        self.api_key = api_key
        self.base_url = base_url
        if not api_key.startswith("Zoho-enczapikey "):
            api_key = f"Zoho-enczapikey {api_key}"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": api_key
        }

    def _build_recipient(self, address: str, name: Optional[str] = None) -> Dict:
        """
        Build a recipient object.

        Args:
            address: Email address of the recipient
            name: Name of the recipient

        Returns:
            Dict containing recipient details
        """
        recipient = {"email": address}
        if name:
            recipient["name"] = name
        return recipient

    def _build_recipient_with_merge_info(self, address: str, name: Optional[str] = None,
                                         merge_info: Optional[Dict] = None) -> Dict:
        """
        Build a recipient object with merge info.

        Args:
            address: Email address of the recipient
            name: Name of the recipient
            merge_info: Dictionary containing merge fields for this recipient

        Returns:
            Dict containing recipient details with merge info
        """
        recipient = self._build_recipient(address, name)
        if merge_info:
            recipient["merge_info"] = merge_info
        return recipient

    def _handle_response(self, response: requests.Response) -> Dict:
        """
        Handle the API response and check for errors.

        Args:
            response: Response object from requests

        Returns:
            Parsed response as a dictionary

        Raises:
            ZeptoMailError: If the API returns an error
        """
        try:
            response_data = response.json()
        except ValueError:
            raise ZeptoMailError(
                f"Invalid JSON response from API (Status code: {response.status_code})",
                code="TM_3301",
                sub_code="SM_101"
            )

        # Check if the response contains an error
        if "error" in response_data:
            error = response_data["error"]
            error_message = error.get("message", "Unknown error")
            error_code = error.get("code", "unknown")
            error_sub_code = error.get("sub_code", None)
            error_details = error.get("details", [])
            request_id = response_data.get("request_id")

            # Get solution based on error codes
            solution = self._get_error_solution(error_code, error_sub_code, error_details)
            if solution:
                error_message = f"{error_message}. {solution}"

            raise ZeptoMailError(
                message=error_message,
                code=error_code,
                sub_code=error_sub_code,
                details=error_details,
                request_id=request_id
            )

        return response_data

    def _ensure_json_serializable(self, obj: Any) -> Any:
        """
        Recursively process an object to ensure it's JSON serializable.
        Converts bytes to base64-encoded strings.

        Args:
            obj: The object to process

        Returns:
            A JSON serializable version of the object
        """
        if isinstance(obj, dict):
            return {k: self._ensure_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._ensure_json_serializable(item) for item in obj]
        elif isinstance(obj, bytes):
            # Convert bytes to base64 encoded string
            return base64.b64encode(obj).decode('utf-8')
        else:
            return obj

    def _get_error_solution(self, code: str, sub_code: str, details: List[Dict]) -> Optional[str]:
        """
        Get a solution message based on error codes.

        Args:
            code: The error code
            sub_code: The error sub-code
            details: Error details

        Returns:
            A solution message or None
        """
        # Map of error codes to solutions
        error_solutions = {
            "TM_3201": {
                "GE_102": {
                    "subject": "Set a non-empty subject for your email.",
                    "from": "Add the mandatory 'from' field with a valid email address.",
                    "to": "Add at least one recipient using 'to', 'cc', or 'bcc' fields.",
                    "Mail Template Key": "Add the mandatory 'Mail Template Key' field."
                }
            },
            "TM_3301": {
                "SM_101": "Check your API request syntax for valid JSON format.",
                "SM_120": "Ensure the attachment MIME type matches the actual file content."
            },
            "TM_3501": {
                "UE_106": "Use a valid File Cache Key from your Mail Agent's File Cache tab.",
                "MTR_101": "Use a valid Template Key from your Mail Agent.",
                "LE_101": "Your credits have expired. Purchase new credits from the ZeptoMail Subscription page."
            },
            "TM_3601": {
                "SERR_156": "Add your sending IP to the allowed IPs list in settings.",
                "SM_133": "Your trial sending limit is exceeded. Get your account reviewed to continue.",
                "SMI_115": "Daily sending limit reached. Try again tomorrow.",
                "AE_101": "Your account is blocked. Contact ZeptoMail support."
            },
            "TM_4001": {
                "SM_111": "Use a sender address with a domain that is verified in your Mail Agent.",
                "SM_113": "Provide valid values for all required fields.",
                "SM_128": "Your account needs to be reviewed. Get your account approved before sending emails.",
                "SERR_157": "Use a valid Sendmail token from your Mail Agent configuration settings."
            },
            "TM_5001": {
                "LE_102": "Your credits are exhausted. Purchase new credits from the ZeptoMail Subscription page."
            },
            "TM_8001": {
                "SM_127": "Reduce the number of attachments to 60 or fewer.",
                "SM_129": "Ensure all name fields are under 250 characters, subject is under 500 characters, attachment size is under 15MB, and attachment filenames are under 150 characters."
            }
        }

        # Check if we have a solution for this error code
        if code in error_solutions:
            code_solutions = error_solutions[code]

            # If we have a sub-code specific solution
            if sub_code in code_solutions:
                sub_code_solution = code_solutions[sub_code]

                # If the sub-code solution is a string, return it directly
                if isinstance(sub_code_solution, str):
                    return sub_code_solution

                # If it's a dict, try to find a more specific solution based on details
                elif isinstance(sub_code_solution, dict) and details:
                    for detail in details:
                        target = detail.get("target", "")
                        if target in sub_code_solution:
                            return sub_code_solution[target]

                    # If no specific target match, return the first solution
                    return next(iter(sub_code_solution.values()), None)

        return None

    def send_email(self,
                   from_address: str,
                   from_name: Optional[str] = None,
                   to: List[Dict] = None,
                   cc: List[Dict] = None,
                   bcc: List[Dict] = None,
                   reply_to: List[Dict] = None,
                   subject: str = "",
                   html_body: Optional[str] = None,
                   text_body: Optional[str] = None,
                   attachments: List[Dict] = None,
                   inline_images: List[Dict] = None,
                   track_clicks: bool = True,
                   track_opens: bool = True,
                   client_reference: Optional[str] = None,
                   mime_headers: Optional[Dict] = None) -> Dict:
        """
        Send a single email using the ZeptoMail API.

        Args:
            from_address: Sender's email address
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
        """
        url = f"{self.base_url}/email"

        payload = {
            "from": self._build_recipient(from_address, from_name),
            "subject": subject
        }

        # Add recipients
        if to:
            payload["to"] = to

        if cc:
            payload["cc"] = cc

        if bcc:
            payload["bcc"] = bcc

        if reply_to:
            payload["reply_to"] = reply_to

        # Add content
        if html_body:
            payload["htmlbody"] = html_body

        if text_body:
            payload["textbody"] = text_body

        # Add tracking options
        payload["track_clicks"] = track_clicks
        payload["track_opens"] = track_opens

        # Add optional parameters
        if client_reference:
            payload["client_reference"] = client_reference

        if mime_headers:
            payload["mime_headers"] = mime_headers

        if attachments:
            payload["attachments"] = attachments

        if inline_images:
            payload["inline_images"] = inline_images

        # Ensure payload is JSON serializable by encoding any bytes objects to base64 strings
        serializable_payload = self._ensure_json_serializable(payload)
        response = requests.post(url, headers=self.headers, data=json.dumps(serializable_payload))
        return self._handle_response(response)

    def send_batch_email(self,
                         from_address: str,
                         from_name: Optional[str] = None,
                         to: List[Dict] = None,
                         cc: List[Dict] = None,
                         bcc: List[Dict] = None,
                         subject: str = "",
                         html_body: Optional[str] = None,
                         text_body: Optional[str] = None,
                         attachments: List[Dict] = None,
                         inline_images: List[Dict] = None,
                         track_clicks: bool = True,
                         track_opens: bool = True,
                         client_reference: Optional[str] = None,
                         mime_headers: Optional[Dict] = None,
                         merge_info: Optional[Dict] = None) -> Dict:
        """
        Send a batch email using the ZeptoMail API.

        Args:
            from_address: Sender's email address
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
        """
        url = f"{self.base_url}/email/batch"

        payload = {
            "from": self._build_recipient(from_address, from_name),
            "subject": subject
        }

        # Add recipients
        if to:
            payload["to"] = to

        if cc:
            payload["cc"] = cc

        if bcc:
            payload["bcc"] = bcc

        # Add content
        if html_body:
            payload["htmlbody"] = html_body

        if text_body:
            payload["textbody"] = text_body

        # Add tracking options
        payload["track_clicks"] = track_clicks
        payload["track_opens"] = track_opens

        # Add optional parameters
        if client_reference:
            payload["client_reference"] = client_reference

        if mime_headers:
            payload["mime_headers"] = mime_headers

        if attachments:
            payload["attachments"] = attachments

        if inline_images:
            payload["inline_images"] = inline_images

        if merge_info:
            payload["merge_info"] = merge_info

        # Ensure payload is JSON serializable by encoding any bytes objects to base64 strings
        serializable_payload = self._ensure_json_serializable(payload)
        response = requests.post(url, headers=self.headers, data=json.dumps(serializable_payload))
        return self._handle_response(response)

    # Helper methods for common operations

    def add_recipient(self, address: str, name: Optional[str] = None) -> Dict:
        """
        Create a recipient object for use in to, cc, bcc lists.

        Args:
            address: Email address
            name: Recipient name

        Returns:
            Recipient dictionary
        """
        return self._build_recipient(address, name)

    def add_batch_recipient(self, address: str, name: Optional[str] = None,
                            merge_info: Optional[Dict] = None) -> Dict:
        """
        Create a batch recipient object with merge info.

        Args:
            address: Email address
            name: Recipient name
            merge_info: Merge fields for this recipient

        Returns:
            Recipient dictionary with merge info
        """
        return self._build_recipient_with_merge_info(address, name, merge_info)

    def add_attachment_from_file_cache(self, file_cache_key: str, name: Optional[str] = None) -> Dict:
        """
        Add an attachment using a file cache key.

        Args:
            file_cache_key: File cache key from ZeptoMail
            name: Optional name for the file

        Returns:
            Attachment dictionary
        """
        attachment = {"file_cache_key": file_cache_key}
        if name:
            attachment["name"] = name
        return attachment

    def add_attachment_from_content(self, content: str, mime_type: str, name: str) -> Dict:
        """
        Add an attachment using base64 encoded content.

        Args:
            content: Base64 encoded content
            mime_type: MIME type of the content
            name: Name for the file

        Returns:
            Attachment dictionary
        """
        return {
            "content": content,
            "mime_type": mime_type,
            "name": name
        }

    def add_inline_image(self, cid: str, content: Optional[str] = None,
                         mime_type: Optional[str] = None,
                         file_cache_key: Optional[str] = None) -> Dict:
        """
        Add an inline image to the email.

        Args:
            cid: Content ID to reference in HTML
            content: Base64 encoded content
            mime_type: MIME type of the content
            file_cache_key: File cache key from ZeptoMail

        Returns:
            Inline image dictionary
        """
        inline_image = {"cid": cid}

        if content and mime_type:
            inline_image["content"] = content
            inline_image["mime_type"] = mime_type

        if file_cache_key:
            inline_image["file_cache_key"] = file_cache_key

        return inline_image

```

#### Attributes

##### `api_key = api_key`

##### `base_url = base_url`

##### `headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': api_key}`

#### Functions

##### `__init__(api_key, base_url='https://api.zeptomail.eu/v1.1')`

Initialize the ZeptoMail client.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `api_key` | `str` | Your ZeptoMail API key | *required* | | `base_url` | `str` | The base URL for the ZeptoMail API (defaults to https://api.zeptomail.eu/v1.1) | `'https://api.zeptomail.eu/v1.1'` |

Source code in `zeptomail/client.py`

```
def __init__(self, api_key: str, base_url: str = "https://api.zeptomail.eu/v1.1"):
    """
    Initialize the ZeptoMail client.

    Args:
        api_key: Your ZeptoMail API key
        base_url: The base URL for the ZeptoMail API (defaults to https://api.zeptomail.eu/v1.1)
    """
    self.api_key = api_key
    self.base_url = base_url
    if not api_key.startswith("Zoho-enczapikey "):
        api_key = f"Zoho-enczapikey {api_key}"
    self.headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": api_key
    }

```

##### `_build_recipient(address, name=None)`

Build a recipient object.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `address` | `str` | Email address of the recipient | *required* | | `name` | `Optional[str]` | Name of the recipient | `None` |

Returns:

| Type | Description | | --- | --- | | `Dict` | Dict containing recipient details |

Source code in `zeptomail/client.py`

```
def _build_recipient(self, address: str, name: Optional[str] = None) -> Dict:
    """
    Build a recipient object.

    Args:
        address: Email address of the recipient
        name: Name of the recipient

    Returns:
        Dict containing recipient details
    """
    recipient = {"email": address}
    if name:
        recipient["name"] = name
    return recipient

```

##### `_build_recipient_with_merge_info(address, name=None, merge_info=None)`

Build a recipient object with merge info.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `address` | `str` | Email address of the recipient | *required* | | `name` | `Optional[str]` | Name of the recipient | `None` | | `merge_info` | `Optional[Dict]` | Dictionary containing merge fields for this recipient | `None` |

Returns:

| Type | Description | | --- | --- | | `Dict` | Dict containing recipient details with merge info |

Source code in `zeptomail/client.py`

```
def _build_recipient_with_merge_info(self, address: str, name: Optional[str] = None,
                                     merge_info: Optional[Dict] = None) -> Dict:
    """
    Build a recipient object with merge info.

    Args:
        address: Email address of the recipient
        name: Name of the recipient
        merge_info: Dictionary containing merge fields for this recipient

    Returns:
        Dict containing recipient details with merge info
    """
    recipient = self._build_recipient(address, name)
    if merge_info:
        recipient["merge_info"] = merge_info
    return recipient

```

##### `_ensure_json_serializable(obj)`

Recursively process an object to ensure it's JSON serializable. Converts bytes to base64-encoded strings.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `obj` | `Any` | The object to process | *required* |

Returns:

| Type | Description | | --- | --- | | `Any` | A JSON serializable version of the object |

Source code in `zeptomail/client.py`

```
def _ensure_json_serializable(self, obj: Any) -> Any:
    """
    Recursively process an object to ensure it's JSON serializable.
    Converts bytes to base64-encoded strings.

    Args:
        obj: The object to process

    Returns:
        A JSON serializable version of the object
    """
    if isinstance(obj, dict):
        return {k: self._ensure_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [self._ensure_json_serializable(item) for item in obj]
    elif isinstance(obj, bytes):
        # Convert bytes to base64 encoded string
        return base64.b64encode(obj).decode('utf-8')
    else:
        return obj

```

##### `_get_error_solution(code, sub_code, details)`

Get a solution message based on error codes.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `code` | `str` | The error code | *required* | | `sub_code` | `str` | The error sub-code | *required* | | `details` | `List[Dict]` | Error details | *required* |

Returns:

| Type | Description | | --- | --- | | `Optional[str]` | A solution message or None |

Source code in `zeptomail/client.py`

```
def _get_error_solution(self, code: str, sub_code: str, details: List[Dict]) -> Optional[str]:
    """
    Get a solution message based on error codes.

    Args:
        code: The error code
        sub_code: The error sub-code
        details: Error details

    Returns:
        A solution message or None
    """
    # Map of error codes to solutions
    error_solutions = {
        "TM_3201": {
            "GE_102": {
                "subject": "Set a non-empty subject for your email.",
                "from": "Add the mandatory 'from' field with a valid email address.",
                "to": "Add at least one recipient using 'to', 'cc', or 'bcc' fields.",
                "Mail Template Key": "Add the mandatory 'Mail Template Key' field."
            }
        },
        "TM_3301": {
            "SM_101": "Check your API request syntax for valid JSON format.",
            "SM_120": "Ensure the attachment MIME type matches the actual file content."
        },
        "TM_3501": {
            "UE_106": "Use a valid File Cache Key from your Mail Agent's File Cache tab.",
            "MTR_101": "Use a valid Template Key from your Mail Agent.",
            "LE_101": "Your credits have expired. Purchase new credits from the ZeptoMail Subscription page."
        },
        "TM_3601": {
            "SERR_156": "Add your sending IP to the allowed IPs list in settings.",
            "SM_133": "Your trial sending limit is exceeded. Get your account reviewed to continue.",
            "SMI_115": "Daily sending limit reached. Try again tomorrow.",
            "AE_101": "Your account is blocked. Contact ZeptoMail support."
        },
        "TM_4001": {
            "SM_111": "Use a sender address with a domain that is verified in your Mail Agent.",
            "SM_113": "Provide valid values for all required fields.",
            "SM_128": "Your account needs to be reviewed. Get your account approved before sending emails.",
            "SERR_157": "Use a valid Sendmail token from your Mail Agent configuration settings."
        },
        "TM_5001": {
            "LE_102": "Your credits are exhausted. Purchase new credits from the ZeptoMail Subscription page."
        },
        "TM_8001": {
            "SM_127": "Reduce the number of attachments to 60 or fewer.",
            "SM_129": "Ensure all name fields are under 250 characters, subject is under 500 characters, attachment size is under 15MB, and attachment filenames are under 150 characters."
        }
    }

    # Check if we have a solution for this error code
    if code in error_solutions:
        code_solutions = error_solutions[code]

        # If we have a sub-code specific solution
        if sub_code in code_solutions:
            sub_code_solution = code_solutions[sub_code]

            # If the sub-code solution is a string, return it directly
            if isinstance(sub_code_solution, str):
                return sub_code_solution

            # If it's a dict, try to find a more specific solution based on details
            elif isinstance(sub_code_solution, dict) and details:
                for detail in details:
                    target = detail.get("target", "")
                    if target in sub_code_solution:
                        return sub_code_solution[target]

                # If no specific target match, return the first solution
                return next(iter(sub_code_solution.values()), None)

    return None

```

##### `_handle_response(response)`

Handle the API response and check for errors.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `response` | `Response` | Response object from requests | *required* |

Returns:

| Type | Description | | --- | --- | | `Dict` | Parsed response as a dictionary |

Raises:

| Type | Description | | --- | --- | | `ZeptoMailError` | If the API returns an error |

Source code in `zeptomail/client.py`

```
def _handle_response(self, response: requests.Response) -> Dict:
    """
    Handle the API response and check for errors.

    Args:
        response: Response object from requests

    Returns:
        Parsed response as a dictionary

    Raises:
        ZeptoMailError: If the API returns an error
    """
    try:
        response_data = response.json()
    except ValueError:
        raise ZeptoMailError(
            f"Invalid JSON response from API (Status code: {response.status_code})",
            code="TM_3301",
            sub_code="SM_101"
        )

    # Check if the response contains an error
    if "error" in response_data:
        error = response_data["error"]
        error_message = error.get("message", "Unknown error")
        error_code = error.get("code", "unknown")
        error_sub_code = error.get("sub_code", None)
        error_details = error.get("details", [])
        request_id = response_data.get("request_id")

        # Get solution based on error codes
        solution = self._get_error_solution(error_code, error_sub_code, error_details)
        if solution:
            error_message = f"{error_message}. {solution}"

        raise ZeptoMailError(
            message=error_message,
            code=error_code,
            sub_code=error_sub_code,
            details=error_details,
            request_id=request_id
        )

    return response_data

```

##### `add_attachment_from_content(content, mime_type, name)`

Add an attachment using base64 encoded content.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `content` | `str` | Base64 encoded content | *required* | | `mime_type` | `str` | MIME type of the content | *required* | | `name` | `str` | Name for the file | *required* |

Returns:

| Type | Description | | --- | --- | | `Dict` | Attachment dictionary |

Source code in `zeptomail/client.py`

```
def add_attachment_from_content(self, content: str, mime_type: str, name: str) -> Dict:
    """
    Add an attachment using base64 encoded content.

    Args:
        content: Base64 encoded content
        mime_type: MIME type of the content
        name: Name for the file

    Returns:
        Attachment dictionary
    """
    return {
        "content": content,
        "mime_type": mime_type,
        "name": name
    }

```

##### `add_attachment_from_file_cache(file_cache_key, name=None)`

Add an attachment using a file cache key.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `file_cache_key` | `str` | File cache key from ZeptoMail | *required* | | `name` | `Optional[str]` | Optional name for the file | `None` |

Returns:

| Type | Description | | --- | --- | | `Dict` | Attachment dictionary |

Source code in `zeptomail/client.py`

```
def add_attachment_from_file_cache(self, file_cache_key: str, name: Optional[str] = None) -> Dict:
    """
    Add an attachment using a file cache key.

    Args:
        file_cache_key: File cache key from ZeptoMail
        name: Optional name for the file

    Returns:
        Attachment dictionary
    """
    attachment = {"file_cache_key": file_cache_key}
    if name:
        attachment["name"] = name
    return attachment

```

##### `add_batch_recipient(address, name=None, merge_info=None)`

Create a batch recipient object with merge info.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `address` | `str` | Email address | *required* | | `name` | `Optional[str]` | Recipient name | `None` | | `merge_info` | `Optional[Dict]` | Merge fields for this recipient | `None` |

Returns:

| Type | Description | | --- | --- | | `Dict` | Recipient dictionary with merge info |

Source code in `zeptomail/client.py`

```
def add_batch_recipient(self, address: str, name: Optional[str] = None,
                        merge_info: Optional[Dict] = None) -> Dict:
    """
    Create a batch recipient object with merge info.

    Args:
        address: Email address
        name: Recipient name
        merge_info: Merge fields for this recipient

    Returns:
        Recipient dictionary with merge info
    """
    return self._build_recipient_with_merge_info(address, name, merge_info)

```

##### `add_inline_image(cid, content=None, mime_type=None, file_cache_key=None)`

Add an inline image to the email.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `cid` | `str` | Content ID to reference in HTML | *required* | | `content` | `Optional[str]` | Base64 encoded content | `None` | | `mime_type` | `Optional[str]` | MIME type of the content | `None` | | `file_cache_key` | `Optional[str]` | File cache key from ZeptoMail | `None` |

Returns:

| Type | Description | | --- | --- | | `Dict` | Inline image dictionary |

Source code in `zeptomail/client.py`

```
def add_inline_image(self, cid: str, content: Optional[str] = None,
                     mime_type: Optional[str] = None,
                     file_cache_key: Optional[str] = None) -> Dict:
    """
    Add an inline image to the email.

    Args:
        cid: Content ID to reference in HTML
        content: Base64 encoded content
        mime_type: MIME type of the content
        file_cache_key: File cache key from ZeptoMail

    Returns:
        Inline image dictionary
    """
    inline_image = {"cid": cid}

    if content and mime_type:
        inline_image["content"] = content
        inline_image["mime_type"] = mime_type

    if file_cache_key:
        inline_image["file_cache_key"] = file_cache_key

    return inline_image

```

##### `add_recipient(address, name=None)`

Create a recipient object for use in to, cc, bcc lists.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `address` | `str` | Email address | *required* | | `name` | `Optional[str]` | Recipient name | `None` |

Returns:

| Type | Description | | --- | --- | | `Dict` | Recipient dictionary |

Source code in `zeptomail/client.py`

```
def add_recipient(self, address: str, name: Optional[str] = None) -> Dict:
    """
    Create a recipient object for use in to, cc, bcc lists.

    Args:
        address: Email address
        name: Recipient name

    Returns:
        Recipient dictionary
    """
    return self._build_recipient(address, name)

```

##### `send_batch_email(from_address, from_name=None, to=None, cc=None, bcc=None, subject='', html_body=None, text_body=None, attachments=None, inline_images=None, track_clicks=True, track_opens=True, client_reference=None, mime_headers=None, merge_info=None)`

Send a batch email using the ZeptoMail API.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `from_address` | `str` | Sender's email address | *required* | | `from_name` | `Optional[str]` | Sender's name | `None` | | `to` | `List[Dict]` | List of recipient dictionaries with optional merge_info | `None` | | `cc` | `List[Dict]` | List of cc recipient dictionaries | `None` | | `bcc` | `List[Dict]` | List of bcc recipient dictionaries | `None` | | `subject` | `str` | Email subject | `''` | | `html_body` | `Optional[str]` | HTML content of the email | `None` | | `text_body` | `Optional[str]` | Plain text content of the email | `None` | | `attachments` | `List[Dict]` | List of attachment dictionaries | `None` | | `inline_images` | `List[Dict]` | List of inline image dictionaries | `None` | | `track_clicks` | `bool` | Whether to track clicks | `True` | | `track_opens` | `bool` | Whether to track opens | `True` | | `client_reference` | `Optional[str]` | Client reference identifier | `None` | | `mime_headers` | `Optional[Dict]` | Additional MIME headers | `None` | | `merge_info` | `Optional[Dict]` | Global merge info for recipients without specific merge info | `None` |

Returns:

| Type | Description | | --- | --- | | `Dict` | API response as a dictionary |

Source code in `zeptomail/client.py`

```
def send_batch_email(self,
                     from_address: str,
                     from_name: Optional[str] = None,
                     to: List[Dict] = None,
                     cc: List[Dict] = None,
                     bcc: List[Dict] = None,
                     subject: str = "",
                     html_body: Optional[str] = None,
                     text_body: Optional[str] = None,
                     attachments: List[Dict] = None,
                     inline_images: List[Dict] = None,
                     track_clicks: bool = True,
                     track_opens: bool = True,
                     client_reference: Optional[str] = None,
                     mime_headers: Optional[Dict] = None,
                     merge_info: Optional[Dict] = None) -> Dict:
    """
    Send a batch email using the ZeptoMail API.

    Args:
        from_address: Sender's email address
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
    """
    url = f"{self.base_url}/email/batch"

    payload = {
        "from": self._build_recipient(from_address, from_name),
        "subject": subject
    }

    # Add recipients
    if to:
        payload["to"] = to

    if cc:
        payload["cc"] = cc

    if bcc:
        payload["bcc"] = bcc

    # Add content
    if html_body:
        payload["htmlbody"] = html_body

    if text_body:
        payload["textbody"] = text_body

    # Add tracking options
    payload["track_clicks"] = track_clicks
    payload["track_opens"] = track_opens

    # Add optional parameters
    if client_reference:
        payload["client_reference"] = client_reference

    if mime_headers:
        payload["mime_headers"] = mime_headers

    if attachments:
        payload["attachments"] = attachments

    if inline_images:
        payload["inline_images"] = inline_images

    if merge_info:
        payload["merge_info"] = merge_info

    # Ensure payload is JSON serializable by encoding any bytes objects to base64 strings
    serializable_payload = self._ensure_json_serializable(payload)
    response = requests.post(url, headers=self.headers, data=json.dumps(serializable_payload))
    return self._handle_response(response)

```

##### `send_email(from_address, from_name=None, to=None, cc=None, bcc=None, reply_to=None, subject='', html_body=None, text_body=None, attachments=None, inline_images=None, track_clicks=True, track_opens=True, client_reference=None, mime_headers=None)`

Send a single email using the ZeptoMail API.

Parameters:

| Name | Type | Description | Default | | --- | --- | --- | --- | | `from_address` | `str` | Sender's email address | *required* | | `from_name` | `Optional[str]` | Sender's name | `None` | | `to` | `List[Dict]` | List of recipient dictionaries | `None` | | `cc` | `List[Dict]` | List of cc recipient dictionaries | `None` | | `bcc` | `List[Dict]` | List of bcc recipient dictionaries | `None` | | `reply_to` | `List[Dict]` | List of reply-to dictionaries | `None` | | `subject` | `str` | Email subject | `''` | | `html_body` | `Optional[str]` | HTML content of the email | `None` | | `text_body` | `Optional[str]` | Plain text content of the email | `None` | | `attachments` | `List[Dict]` | List of attachment dictionaries | `None` | | `inline_images` | `List[Dict]` | List of inline image dictionaries | `None` | | `track_clicks` | `bool` | Whether to track clicks | `True` | | `track_opens` | `bool` | Whether to track opens | `True` | | `client_reference` | `Optional[str]` | Client reference identifier | `None` | | `mime_headers` | `Optional[Dict]` | Additional MIME headers | `None` |

Returns:

| Type | Description | | --- | --- | | `Dict` | API response as a dictionary |

Source code in `zeptomail/client.py`

```
def send_email(self,
               from_address: str,
               from_name: Optional[str] = None,
               to: List[Dict] = None,
               cc: List[Dict] = None,
               bcc: List[Dict] = None,
               reply_to: List[Dict] = None,
               subject: str = "",
               html_body: Optional[str] = None,
               text_body: Optional[str] = None,
               attachments: List[Dict] = None,
               inline_images: List[Dict] = None,
               track_clicks: bool = True,
               track_opens: bool = True,
               client_reference: Optional[str] = None,
               mime_headers: Optional[Dict] = None) -> Dict:
    """
    Send a single email using the ZeptoMail API.

    Args:
        from_address: Sender's email address
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
    """
    url = f"{self.base_url}/email"

    payload = {
        "from": self._build_recipient(from_address, from_name),
        "subject": subject
    }

    # Add recipients
    if to:
        payload["to"] = to

    if cc:
        payload["cc"] = cc

    if bcc:
        payload["bcc"] = bcc

    if reply_to:
        payload["reply_to"] = reply_to

    # Add content
    if html_body:
        payload["htmlbody"] = html_body

    if text_body:
        payload["textbody"] = text_body

    # Add tracking options
    payload["track_clicks"] = track_clicks
    payload["track_opens"] = track_opens

    # Add optional parameters
    if client_reference:
        payload["client_reference"] = client_reference

    if mime_headers:
        payload["mime_headers"] = mime_headers

    if attachments:
        payload["attachments"] = attachments

    if inline_images:
        payload["inline_images"] = inline_images

    # Ensure payload is JSON serializable by encoding any bytes objects to base64 strings
    serializable_payload = self._ensure_json_serializable(payload)
    response = requests.post(url, headers=self.headers, data=json.dumps(serializable_payload))
    return self._handle_response(response)

```

Source Code in LLMs

When generating the LLMs text file, only function signatures and docstrings are included, not the implementation details.

## Usage Examples

### Basic Initialization

```
from zeptomail import ZeptoMail

# Initialize with API key
client = ZeptoMail("your-api-key-here")

# Or with custom base URL (for different regions)
client = ZeptoMail(
    api_key="your-api-key-here",
    base_url="https://api.zeptomail.com/v1.1"  # Custom API endpoint
)

```

### Sending a Simple Email

```
# Create a recipient
recipient = client.add_recipient("recipient@example.com", "Recipient Name")

# Send a simple email
response = client.send_email(
    from_address="sender@example.com",
    from_name="Sender Name",
    to=[recipient],
    subject="Test Email",
    html_body="<h1>Hello World!</h1><p>This is a test email.</p>",
    text_body="Hello World! This is a test email."
)

print(f"Email sent with message ID: {response['data']['message_id']}")

```

See the [Examples](../../examples/basic-usage/) section for more detailed usage examples.
