#!/usr/bin/env python3  # Allows execution without 'python'
from analysis import NetworkAnalyzer
from flow_processor import FlowProcessor
import pandas as pd
import argparse
import os
import subprocess
from mitmproxy.io import FlowReader
from mitmproxy.http import HTTPFlow
import time
import json
import tempfile

class GenAIAudit:
    def __init__(self, extension) -> None:
        self.extension = extension
        self.processor = FlowProcessor(self.extension)
        self.flow_path = os.path.join(tempfile.gettempdir(), "working.flow")


    def start_proxy(self):
        flow_path = self.flow_path
        time.sleep(3)

        try:
            proxy_process = subprocess.Popen(["mitmweb", "-w", flow_path]) # change to mitmproxy
            while proxy_process.poll() is None:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nCtrl + C detected. Stopping mitmproxy...")
            proxy_process.terminate()
            proxy_process.wait()
        except subprocess.CalledProcessError as e:
            print(f"Error running mitmproxy: {e}")
            
    def run(self):
        self.start_proxy()
        try:
            df = self.processor.process_flows("working.flow")
            analyzer = NetworkAnalyzer(df, "working.flow", self.extension)
            fp, tp = analyzer.run()

            json_args = json.dumps({"fp": fp, "tp": tp})
            subprocess.Popen(["streamlit", "run", "src/app.py", "--", json_args], start_new_session=True)

        finally:
            if os.path.exists(self.flow_path):
                print(f"Deleting flow file: {self.flow_path}")
                os.remove(self.flow_path)

def main():
    parser = argparse.ArgumentParser(description="Run GenAIAudit with network traffic analysis.")

    parser.add_argument(
        "extension_name",
        type=str,
        help="Name of the browser extension being analyzed (e.g., maxai)."
    )
    
    args = parser.parse_args()
    audit = GenAIAudit(extension=args.extension_name)
    audit.run()

if __name__ == "__main__":
    main()


"""
TODO:
2. get argparse to work extension_audit --extnension_name --gui
3. remove changing wi-fi
4. better gui using js
5. temp file
5. better payload viewing
"""