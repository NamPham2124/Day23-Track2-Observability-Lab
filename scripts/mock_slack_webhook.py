#!/usr/bin/env python3
"""A simple HTTP server to mock Slack incoming webhooks.

Intercepts Alertmanager alerts and logs them to a file to verify the alert
lifecycle (firing -> resolved) without requiring a real Slack workspace.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import datetime

PORT = 5001
LOG_PATH = Path("/home/namtp2124/Project_Track2/Day23-Track2-Observability-Lab/submission/screenshots/mock-slack-alerts.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

class MockSlackHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode("utf-8"))
            timestamp = datetime.datetime.now().isoformat()
            
            # Print to stdout for debugging
            print(f"\n[{timestamp}] Mock Slack Webhook Received Payload:")
            print(json.dumps(payload, indent=2))
            
            # Log to file
            with open(LOG_PATH, "a") as f:
                f.write(f"\n--- Alert Received at {timestamp} ---\n")
                f.write(json.dumps(payload, indent=2))
                f.write("\n")
                
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
        except Exception as e:
            print(f"Error handling webhook: {e}")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode())

def run():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, MockSlackHandler)
    print(f"Starting mock Slack webhook server on port {PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Server stopped.")

if __name__ == "__main__":
    run()
