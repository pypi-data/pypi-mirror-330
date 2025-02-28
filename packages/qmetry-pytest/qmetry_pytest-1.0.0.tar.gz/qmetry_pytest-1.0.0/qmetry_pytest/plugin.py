import pytest
import requests
import os
from typing import Dict, Any, Optional, List
from .config import QMetryConfig


class QMetryApi:
    def __init__(self):

        self.properties = {}
        try:
            config_paths = [
                os.path.join(os.getcwd(), 'qmetry.properties')
            ]
            
            config_file = None
            for path in config_paths:
                if os.path.exists(path):
                    config_file = path
                    break
                    
            if not config_file:
                raise FileNotFoundError("qmetry.properties not found in any of the expected locations")
                
            with open(config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        self.properties[key.strip()] = value.strip()
            
        except FileNotFoundError:
            # Fallback to environment variables if properties file not found
            raise FileNotFoundError("qmetry.properties not found in any of the expected locations")
        

    def validate_qmetry_config(self):
        """
        Validates QMetry configuration settings and determines which flow to use.

        Returns:
            Tuple[bool, Optional[str], Optional[str]]: 
                - is_valid: Boolean indicating if the configuration is valid
                - flow_type: String indicating which flow to use ('library', 'openapi', 'automation', None)
                - error_message: String containing error message if validation fails
        """
        qmetry_enabled = self.properties.get('qmetry.enabled', 'false').lower() == 'true'
        openapi_enabled = self.properties.get('openapi.qmetry.enabled', 'false').lower() == 'true'
        automation_enabled = self.properties.get('qmetry.automation.enabled', 'false').lower() == 'true'

        # Check if both openapi and automation are enabled or disabled
        if openapi_enabled == automation_enabled:
            return False, None, "openapi.qmetry.enabled and qmetry.automation.enabled cannot be both true or both false"

        # Determine which flow to use
        if not qmetry_enabled:
            return False, None, "qmetry.enabled must be true to proceed with any QMetry integration"

        if openapi_enabled:
            return True, 'openapi', None
        
        if automation_enabled:
            missing_configs = self.check_missing_configs()
            if missing_configs:
                raise ValueError(f"Invalid QMetry configuration: Missing mandatory configurations: {', '.join(missing_configs)}")
            return True, 'automation', None
        
        return True, 'library', None

    def check_missing_configs(self) -> List[str]:
        """Check for missing mandatory configurations."""
        required_configs = [
            'qmetry.automation.apikey',
            'qmetry.automation.resultfile',
            'qmetry.authorization',
            'qmetry.url'
        ]
        return [config for config in required_configs if not self.properties.get(config)]

class QMetryPytestPlugin:
    q = False

    def __init__(self):
        self.test_results = []
        self.flow_type = None

    @staticmethod 
    def pytest_addoption(parser):
        group = parser.getgroup('qmetry')
        group.addoption(
            '--qmetry',
            action='store_true',
            default=False,
            help='Enable QMetry test results reporting'
        )
    
    @staticmethod
    @pytest.hookimpl(tryfirst=True)
    def pytest_configure(config):
        QMetryPytestPlugin.q = config.getoption('qmetry')
        if QMetryPytestPlugin.q is False: return

        qmetry_api = QMetryApi()

        if qmetry_api.properties.get('qmetry.enabled') == 'false':
            return

        global is_valid, flow_type, error_message
        # Now properties will be available as an instance variable
        is_valid, flow_type, error_message = qmetry_api.validate_qmetry_config()
        if not is_valid:
            raise ValueError(f"Invalid QMetry configuration: {error_message}")
        
        if QMetryPytestPlugin().flow_type == 'openapi':
            config.addinivalue_line(
                "markers",
                "qid(id): mark test with QMetry test case ID"
            )
    
    @pytest.mark.hookwrapper
    def pytest_runtest_makereport(item, call):
        outcome = yield

        try:
            if flow_type == 'openapi':    
                rep = outcome.get_result()
                if rep.when == "call" and rep.failed:
                    if 'qid' in item.keywords:
                        print(f"Failed test case with qid: {item.keywords['qid']}")
                    else:
                        print("Failed test case without qid")
                elif(rep.when == "call" and rep.passed):
                    if 'qid' in item.keywords:
                        print(f"Passed test case with qid: {item.keywords['qid']}")
                    else:
                        print("Passed test case without qid")
                elif(rep.when == "call" and rep.skipped):
                    if 'qid' in item.keywords:
                        print(f"Skipped test case with qid: {item.keywords['qid']}")
                    else:
                        print("Skipped test case without qid")
                elif(rep.when == "call" and rep.error):
                    if 'qid' in item.keywords:
                        print(f"Error test case with qid: {item.keywords['qid']}")
                    else:
                        print("Error test case without qid")
            else:
                pass
        
        except Exception as NameError:
            pass
    
    @staticmethod
    def pytest_sessionfinish(session):
        qmetry_plugin = QMetryPytestPlugin()

        if qmetry_plugin.q is False: return

        qmetry_api = QMetryApi()
        if qmetry_api.properties.get('qmetry.enabled') == 'false': return

        qmetry_plugin.create_test_execution()


    def create_test_execution(self):
        """
        Create test execution in QMetry based on the configured flow type
        
        Args:
            test_results: Dictionary containing test results
        
        Returns:
            Optional[str]: Execution ID if successful, None if failed
        """

        if not is_valid:
            raise ValueError(f"Invalid QMetry configuration: {error_message}")

        if flow_type == 'openapi':
            return self._create_openapi_execution()
        elif flow_type == 'automation':
            url = self._automation_import_result()
            self._automation_upload_file(url)


    def _create_openapi_execution(self, test_results: Dict[str, Any]) -> Optional[str]:
        """Handle OpenAPI-specific test execution creation"""
        headers = {
            'Content-Type': 'application/json',
            'apiKey': self.api_key
        }
        
        payload = {
            'projectId': self.project_id,
            'testResults': test_results,
            # Add any OpenAPI-specific fields here
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/openapi/testexecution",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json().get('id')
        except requests.exceptions.RequestException as e:
            print(f"Error creating OpenAPI test execution: {e}")
            return None


    def _automation_import_result(self):
        """Handle Automation-specific test execution creation"""
        qmetry_config = QMetryConfig()

        try:
            response = requests.post(
                f"{qmetry_config.qmetry_url}/rest/qtm4j/automation/latest/importresult",
                headers=qmetry_config.automation_import_result_header(),
                json=qmetry_config.automation_import_result_payload()
            )
            response.raise_for_status()
            return response.json().get('url')
        except requests.exceptions.RequestException as e:
            print(f"Error creating Automation test execution: {e}")
            return None


    def _automation_upload_file(self, url):
        qmetry_config = QMetryConfig()

        try:
            response = requests.request("POST", url,
                headers=qmetry_config.automation_file_upload_header(),
                files=qmetry_config.automation_file_upload_payload()
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error creating Automation test execution: {e}")
            print(e.response.text)
