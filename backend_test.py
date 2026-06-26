import requests
import sys
from datetime import datetime
import json

class AidAssistAPITester:
    def __init__(self, base_url="https://hearing-aid-help.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.session_id = None
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, auth_required=True):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}" if not endpoint.startswith("http") else endpoint
        headers = {'Content-Type': 'application/json'}
        
        if auth_required and self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2)}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)

            print(f"   Response Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                self.failed_tests.append(f"{name}: Expected {expected_status}, got {response.status_code}")

            return success, response.json() if response.text and success else response.text

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed - Network Error: {str(e)}")
            self.failed_tests.append(f"{name}: Network Error - {str(e)}")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append(f"{name}: Error - {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health check endpoint"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "",
            200,
            auth_required=False
        )
        return success

    def test_signup(self):
        """Test user signup"""
        timestamp = datetime.now().strftime('%H%M%S')
        success, response = self.run_test(
            "User Signup",
            "POST",
            "auth/signup",
            200,
            data={
                "email": f"test_{timestamp}@example.com",
                "password": "TestPass123!",
                "name": "Test User",
                "preferred_language": "en"
            },
            auth_required=False
        )
        
        if success and isinstance(response, dict):
            self.token = response.get('access_token')
            return True
        return False

    def test_login(self):
        """Test user login"""
        timestamp = datetime.now().strftime('%H%M%S')
        
        # First signup a user
        signup_data = {
            "email": f"login_test_{timestamp}@example.com",
            "password": "TestPass123!",
            "name": "Login Test User",
            "preferred_language": "en"
        }
        
        signup_success, _ = self.run_test(
            "Signup for Login Test",
            "POST", 
            "auth/signup",
            200,
            data=signup_data,
            auth_required=False
        )
        
        if not signup_success:
            return False
            
        # Now test login
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data={
                "email": signup_data["email"],
                "password": signup_data["password"]
            },
            auth_required=False
        )
        
        if success and isinstance(response, dict):
            self.token = response.get('access_token')
            return True
        return False

    def test_get_current_user(self):
        """Test get current user info"""
        if not self.token:
            print("❌ Cannot test get user - no token available")
            return False
            
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        return success

    def test_triage_submission(self):
        """Test triage submission"""
        if not self.token:
            print("❌ Cannot test triage - no token available")
            return False
            
        success, response = self.run_test(
            "Submit Triage",
            "POST",
            "triage/submit",
            200,
            data={
                "main_issue": "No sound",
                "side": "LEFT",
                "device_type": "RIC",
                "power_type": "BATTERY",
                "exposed_to_water": False,
                "language": "en",
                "additional_details": "The hearing aid stopped working yesterday"
            }
        )
        return success

    def test_classify_complaint(self):
        """Test complaint classification"""
        if not self.token:
            print("❌ Cannot test classification - no token available")
            return False
            
        success, response = self.run_test(
            "Classify Complaint",
            "POST",
            "classify",
            200,
            data={
                "complaint_text": "My hearing aid has no sound at all",
                "triage_data": {
                    "main_issue": "No sound",
                    "side": "LEFT",
                    "device_type": "RIC",
                    "power_type": "BATTERY",
                    "exposed_to_water": False,
                    "additional_details": "The hearing aid stopped working yesterday"
                },
                "language": "en"
            }
        )
        return success

    def test_session_creation(self):
        """Test session creation"""
        if not self.token:
            print("❌ Cannot test session creation - no token available")
            return False
            
        success, response = self.run_test(
            "Create Session",
            "POST",
            "session/create",
            200,
            data={
                "triage_data": {
                    "main_issue": "No sound",
                    "side": "LEFT", 
                    "device_type": "RIC",
                    "power_type": "BATTERY",
                    "exposed_to_water": False,
                    "additional_details": "Test session"
                },
                "classification_result": {
                    "issue_category": "NO_SOUND",
                    "confidence_score": 0.9,
                    "needs_clarification": False
                },
                "language": "en"
            }
        )
        
        if success and isinstance(response, dict):
            self.session_id = response.get('session_id')
            return True
        return False

    def test_get_current_step(self):
        """Test get current troubleshooting step"""
        if not self.token or not self.session_id:
            print("❌ Cannot test current step - no token or session ID available")
            return False
            
        success, response = self.run_test(
            "Get Current Step",
            "GET",
            f"session/{self.session_id}/current-step",
            200
        )
        return success

    def test_update_step(self):
        """Test updating step progress"""
        if not self.token or not self.session_id:
            print("❌ Cannot test step update - no token or session ID available")
            return False
            
        success, response = self.run_test(
            "Update Step",
            "POST",
            f"session/{self.session_id}/update-step",
            200,
            data={
                "step_id": "CHECK_POWER",
                "action": "CONTINUE",
                "outcome": "continued"
            }
        )
        return success

    def test_session_history(self):
        """Test session history retrieval"""
        if not self.token:
            print("❌ Cannot test session history - no token available")
            return False
            
        success, response = self.run_test(
            "Get Session History",
            "GET",
            "session/history",
            200
        )
        return success

    def test_get_session(self):
        """Test get specific session"""
        if not self.token or not self.session_id:
            print("❌ Cannot test get session - no token or session ID available")
            return False
            
        success, response = self.run_test(
            "Get Session",
            "GET",
            f"session/{self.session_id}",
            200
        )
        return success

    def test_pdf_generation(self):
        """Test PDF generation"""
        if not self.token or not self.session_id:
            print("❌ Cannot test PDF generation - no token or session ID available")
            return False
            
        success, response = self.run_test(
            "Generate PDF",
            "POST",
            "support-summary/generate",
            200,
            data={
                "session_id": self.session_id,
                "language": "en"
            }
        )
        return success

def main():
    print("🚀 Starting AidAssist API Tests")
    print("=" * 50)
    
    # Setup
    tester = AidAssistAPITester()

    # Run tests in order
    test_results = {}
    
    # Basic tests
    test_results['health'] = tester.test_health_check()
    test_results['signup'] = tester.test_signup()
    test_results['login'] = tester.test_login()
    test_results['get_user'] = tester.test_get_current_user()
    
    # Triage and classification
    test_results['triage'] = tester.test_triage_submission()
    test_results['classify'] = tester.test_classify_complaint()
    
    # Session management
    test_results['create_session'] = tester.test_session_creation()
    test_results['current_step'] = tester.test_get_current_step()
    test_results['update_step'] = tester.test_update_step()
    test_results['session_history'] = tester.test_session_history()
    test_results['get_session'] = tester.test_get_session()
    
    # PDF generation
    test_results['pdf'] = tester.test_pdf_generation()

    # Print results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    print(f"Success rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.failed_tests:
        print("\n❌ FAILED TESTS:")
        for failure in tester.failed_tests:
            print(f"  - {failure}")
    
    print("\n📋 DETAILED RESULTS:")
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())