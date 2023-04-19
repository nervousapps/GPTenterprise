"""
Test enterprise class
"""
import os
import pytest
from gpt_enterprise.enterprise import Enterprise


@pytest.mark.skip("Need to mock openai")
def test_run_enterprise():
    """
    Test to run a fake enterprise
    """
    enterprise = Enterprise(
        keyfile=os.path.join(os.path.dirname(__file__), "..", "..", "openai_key.txt"),
        guidelines="test",
        output_directory="test",
        manager_retry=1,
        company_name="test",
    )

    assert enterprise.company_name == "test"
    assert enterprise.manager.ceo_guidelines == "test"
    assert enterprise.manager.output_directory == "test"
    assert enterprise.manager.manager_retry == 1
