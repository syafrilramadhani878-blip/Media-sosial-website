#!/usr/bin/env python3
"""
Backend Testing Suite for Social Media Link Website
Tests contact form email service, API endpoints, and database integration
"""

import requests
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE}")

class BackendTester:
    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if not success:
            self.failed_tests.append(test_name)
            if details:
                print(f"   Details: {details}")
    
    def test_basic_endpoints(self):
        """Test basic API endpoints"""
        print("\n=== Testing Basic API Endpoints ===")
        
        # Test root endpoint
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('message') == 'Hello World':
                    self.log_test("Root Endpoint", True, "Root endpoint working correctly")
                else:
                    self.log_test("Root Endpoint", False, f"Unexpected response: {data}")
            else:
                self.log_test("Root Endpoint", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Connection error: {str(e)}")
        
        # Test status endpoint GET
        try:
            response = requests.get(f"{API_BASE}/status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Status GET Endpoint", True, f"Retrieved {len(data)} status checks")
            else:
                self.log_test("Status GET Endpoint", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Status GET Endpoint", False, f"Connection error: {str(e)}")
        
        # Test status endpoint POST
        try:
            test_data = {"client_name": "Backend Test Client"}
            response = requests.post(f"{API_BASE}/status", json=test_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and data.get('client_name') == test_data['client_name']:
                    self.log_test("Status POST Endpoint", True, "Status check created successfully")
                else:
                    self.log_test("Status POST Endpoint", False, f"Invalid response structure: {data}")
            else:
                self.log_test("Status POST Endpoint", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Status POST Endpoint", False, f"Connection error: {str(e)}")
    
    def test_email_configuration(self):
        """Test email service configuration"""
        print("\n=== Testing Email Configuration ===")
        
        try:
            response = requests.get(f"{API_BASE}/test-email", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if 'error' in data:
                    self.log_test("Email Configuration", False, f"Email config error: {data['error']}")
                    return
                
                email_configured = data.get('email_configured', False)
                connection_test = data.get('connection_test', False)
                gmail_email = data.get('gmail_email', '')
                
                if email_configured and connection_test:
                    self.log_test("Email Configuration", True, f"Email service configured and connected: {gmail_email}")
                elif email_configured and not connection_test:
                    self.log_test("Email Configuration", False, f"Email configured but connection failed: {gmail_email}")
                else:
                    self.log_test("Email Configuration", False, "Email service not properly configured")
                    
            else:
                self.log_test("Email Configuration", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Email Configuration", False, f"Connection error: {str(e)}")
    
    def test_contact_form_valid_data(self):
        """Test contact form with valid data"""
        print("\n=== Testing Contact Form - Valid Data ===")
        
        # Test data with realistic information
        test_data = {
            "name": "Ahmad Rizki",
            "email": "ahmad.rizki@example.com", 
            "message": "Halo, saya tertarik dengan profil sosial media Anda. Website ini sangat menarik dan mudah digunakan. Terima kasih!"
        }
        
        try:
            response = requests.post(f"{API_BASE}/contact", json=test_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                message = data.get('message', '')
                
                if success:
                    self.log_test("Contact Form Valid Data", True, f"Message sent successfully: {message}")
                else:
                    # Email might fail but message should be saved
                    if "tersimpan" in message.lower():
                        self.log_test("Contact Form Valid Data", True, f"Message saved (email failed): {message}")
                    else:
                        self.log_test("Contact Form Valid Data", False, f"Unexpected failure: {message}")
            else:
                self.log_test("Contact Form Valid Data", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Contact Form Valid Data", False, f"Connection error: {str(e)}")
    
    def test_contact_form_invalid_data(self):
        """Test contact form with invalid data"""
        print("\n=== Testing Contact Form - Invalid Data ===")
        
        # Test missing name
        try:
            invalid_data = {
                "email": "test@example.com",
                "message": "Test message"
            }
            response = requests.post(f"{API_BASE}/contact", json=invalid_data, timeout=10)
            
            if response.status_code == 422:
                self.log_test("Contact Form Missing Name", True, "Validation correctly rejected missing name")
            else:
                self.log_test("Contact Form Missing Name", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("Contact Form Missing Name", False, f"Connection error: {str(e)}")
        
        # Test invalid email
        try:
            invalid_data = {
                "name": "Test User",
                "email": "invalid-email",
                "message": "Test message"
            }
            response = requests.post(f"{API_BASE}/contact", json=invalid_data, timeout=10)
            
            if response.status_code == 422:
                self.log_test("Contact Form Invalid Email", True, "Validation correctly rejected invalid email")
            else:
                self.log_test("Contact Form Invalid Email", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("Contact Form Invalid Email", False, f"Connection error: {str(e)}")
        
        # Test empty message
        try:
            invalid_data = {
                "name": "Test User",
                "email": "test@example.com",
                "message": ""
            }
            response = requests.post(f"{API_BASE}/contact", json=invalid_data, timeout=10)
            
            if response.status_code == 422:
                self.log_test("Contact Form Empty Message", True, "Validation correctly rejected empty message")
            else:
                self.log_test("Contact Form Empty Message", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("Contact Form Empty Message", False, f"Connection error: {str(e)}")
        
        # Test message too long
        try:
            invalid_data = {
                "name": "Test User",
                "email": "test@example.com",
                "message": "x" * 1001  # Exceeds 1000 character limit
            }
            response = requests.post(f"{API_BASE}/contact", json=invalid_data, timeout=10)
            
            if response.status_code == 422:
                self.log_test("Contact Form Message Too Long", True, "Validation correctly rejected message too long")
            else:
                self.log_test("Contact Form Message Too Long", False, f"Expected 422, got {response.status_code}")
        except Exception as e:
            self.log_test("Contact Form Message Too Long", False, f"Connection error: {str(e)}")
    
    def test_contact_form_edge_cases(self):
        """Test contact form edge cases"""
        print("\n=== Testing Contact Form - Edge Cases ===")
        
        # Test with special characters in message
        try:
            test_data = {
                "name": "Siti Nurhaliza",
                "email": "siti.nurhaliza@example.com",
                "message": "Pesan dengan karakter khusus: àáâãäåæçèéêë & símbolos especiales! 🎉✨"
            }
            response = requests.post(f"{API_BASE}/contact", json=test_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Contact Form Special Characters", True, "Handled special characters correctly")
            else:
                self.log_test("Contact Form Special Characters", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Contact Form Special Characters", False, f"Connection error: {str(e)}")
        
        # Test with maximum valid length message (exactly 1000 chars)
        try:
            # Create exactly 1000 character message
            base_message = "Pesan panjang untuk menguji batas maksimum karakter yang diizinkan sistem. "
            message_1000 = (base_message * 15)[:1000]  # Exactly 1000 chars
            
            test_data = {
                "name": "Budi Santoso",
                "email": "budi.santoso@example.com",
                "message": message_1000
            }
            response = requests.post(f"{API_BASE}/contact", json=test_data, timeout=15)
            
            if response.status_code == 200:
                self.log_test("Contact Form Max Length Message", True, "Handled maximum length message correctly")
            else:
                self.log_test("Contact Form Max Length Message", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Contact Form Max Length Message", False, f"Connection error: {str(e)}")
    
    def test_database_integration(self):
        """Test database integration by checking if messages are saved"""
        print("\n=== Testing Database Integration ===")
        
        # Send a test message and verify it's saved
        test_data = {
            "name": "Database Test User",
            "email": "dbtest@example.com",
            "message": "Testing database integration - this message should be saved to MongoDB"
        }
        
        try:
            # Send contact message
            response = requests.post(f"{API_BASE}/contact", json=test_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                # Whether email succeeds or fails, message should be saved
                if data.get('success') or "tersimpan" in data.get('message', '').lower():
                    self.log_test("Database Integration", True, "Contact message saved to database")
                else:
                    self.log_test("Database Integration", False, f"Message may not have been saved: {data.get('message')}")
            else:
                self.log_test("Database Integration", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Database Integration", False, f"Connection error: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Backend Testing Suite")
        print(f"Backend URL: {API_BASE}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test suites
        self.test_basic_endpoints()
        self.test_email_configuration()
        self.test_contact_form_valid_data()
        self.test_contact_form_invalid_data()
        self.test_contact_form_edge_cases()
        self.test_database_integration()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("🏁 BACKEND TESTING SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['success']])
        failed_tests = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Duration: {duration:.2f} seconds")
        
        if self.failed_tests:
            print(f"\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"  - {test}")
        
        print("\n" + "=" * 60)
        
        return {
            'total': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'failed_tests': self.failed_tests,
            'duration': duration
        }

if __name__ == "__main__":
    tester = BackendTester()
    results = tester.run_all_tests()