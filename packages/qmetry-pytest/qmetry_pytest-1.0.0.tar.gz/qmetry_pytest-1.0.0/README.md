# QMetry PyTest

A PyTest plugin that provides seamless integration with QMetry Test Management Platform.

## Features

- Automatically uploads test results to QMetry
- Generates test cycles and updates test case statuses seamlessly
- Supports JUnit XML reports for Automation API
- Supports Cucumber JSON reports for Automation API

## Installation

```
pip install qmetry-pytest
```

## Configuration

You'll need to create a qmetry.properties file in your project root:
```
qmetry.enabled=true
qmetry.url=<your_qmetry_url>
qmetry.authorization=<your_authorization>

qmetry.automation.enabled=true
qmetry.automation.apikey=<your_api_key>
qmetry.automation.format=<junit/cucumber>
qmetry.automation.resultfile=<your_report_path/filename.xml/json>
```

## Test Example

```
# test_example.py
import pytest

@pytest.mark.qid("TC-123")
def test_example():
    assert True

@pytest.mark.qid("TC-124")
def test_another_example():
    assert 1 + 1 == 2
```

## Test Execution

```
pytest --qmetry
```

### Generate XML report before upload
```
pytest --qmetry --junitxml=report/results.xml
```

## Best Practices

- No markers are required for the automation flow.
- Ensure secure authentication and keep the configuration updated in `qmetry.properties`.
- Remember to include --qmetry as a command-line argument during test execution.
