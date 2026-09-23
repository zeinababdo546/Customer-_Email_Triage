import pytest
from unittest.mock import MagicMock, patch
from main import analyze_customer_email
from schema import ActionCategory, EmailAnalysis, UrgencyLevel


# Test Case 1: Billing Issue & High Urgency Detection
@patch("main.client.beta.chat.completions.parse")
def test_billing_refund_email(mock_parse):
    mock_parsed_obj = EmailAnalysis(
        intent="Request double-charge refund",
        urgency=UrgencyLevel.HIGH,
        category=ActionCategory.BILLING,
        summary="Customer was double-charged $99 and requests an immediate refund.",
        requires_human_followup=True,
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(parsed=mock_parsed_obj))]
    mock_parse.return_value = mock_response

    email_text = "I was double charged $99! Refund my money ASAP."
    result = analyze_customer_email(email_text)

    assert result.category == ActionCategory.BILLING
    assert result.urgency == UrgencyLevel.HIGH
    assert result.requires_human_followup is True


# Test Case 2: Technical Bug Detection
@patch("main.client.beta.chat.completions.parse")
def test_technical_support_email(mock_parse):
    mock_parsed_obj = EmailAnalysis(
        intent="Report application crash during login",
        urgency=UrgencyLevel.MEDIUM,
        category=ActionCategory.TECHNICAL,
        summary="User experiences crash error code 500 when logging into iOS app.",
        requires_human_followup=True,
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(parsed=mock_parsed_obj))]
    mock_parse.return_value = mock_response

    email_text = "App crashes every time I tap login on iOS (error 500)."
    result = analyze_customer_email(email_text)

    assert result.category == ActionCategory.TECHNICAL
    assert result.urgency == UrgencyLevel.MEDIUM


# Test Case 3: Low Urgency / General Feedback
@patch("main.client.beta.chat.completions.parse")
def test_general_feedback_email(mock_parse):
    mock_parsed_obj = EmailAnalysis(
        intent="Provide positive product feedback",
        urgency=UrgencyLevel.LOW,
        category=ActionCategory.GENERAL,
        summary="Customer loved the new dashboard update.",
        requires_human_followup=False,
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(parsed=mock_parsed_obj))]
    mock_parse.return_value = mock_response

    email_text = "Just wanted to say the new dashboard looks amazing, great job!"
    result = analyze_customer_email(email_text)

    assert result.urgency == UrgencyLevel.LOW
    assert result.requires_human_followup is False


# Test Case 4: Critical Security Escalation
@patch("main.client.beta.chat.completions.parse")
def test_critical_security_threat(mock_parse):
    mock_parsed_obj = EmailAnalysis(
        intent="Report suspected account breach and threat of legal escalation",
        urgency=UrgencyLevel.CRITICAL,
        category=ActionCategory.COMPLAINT,
        summary="Unauthorized access detected on user account; user mentions contacting lawyers.",
        requires_human_followup=True,
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(parsed=mock_parsed_obj))]
    mock_parse.return_value = mock_response

    email_text = "My account was hacked and data leaked! I am calling my lawyer."
    result = analyze_customer_email(email_text)

    assert result.urgency == UrgencyLevel.CRITICAL
    assert result.category == ActionCategory.COMPLAINT


# Test Case 5: Empty Input Validation Error
def test_empty_input_validation():
    with pytest.raises(ValueError, match="Input email text cannot be empty."):
        analyze_customer_email("   ")