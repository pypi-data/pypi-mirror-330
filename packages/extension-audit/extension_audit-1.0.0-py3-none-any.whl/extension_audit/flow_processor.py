import os
import json
import csv
from mitmproxy.io import FlowReader
from mitmproxy.websocket import WebSocketMessage
import pandas as pd

class FlowProcessor:
    def __init__(self, extension_name, output_csv = None):
        self.extension_name = extension_name
        # self.flow_directory = flow_directory
        self.disconnect_json = "src/disconnect.json"
        self.disconnect_mapping_file = "disconnect_mapping.json"
        self.headers_list = ["req_header_cookie", "res_header_cookie", "req_header_set-cookie", "res_header_set-cookie"]
        self.categories_of_interest = ["Advertising", "Analytics", "FingerprintingInvasive", "FingerprintingGeneral", "Social"]
        self.output_rows = []
        self.disconnect_mapping = self.load_disconnect_mapping()
        self.output_csv = output_csv

    def load_disconnect_mapping(self):
        if os.path.exists(self.disconnect_mapping_file):
            with open(self.disconnect_mapping_file, "r", encoding="utf-8") as f:
                return json.load(f)

        with open(self.disconnect_json, "r", encoding="utf-8") as f:
            disconnect_data = json.load(f)

        host_to_category = {}
        for category, entries in disconnect_data.get("categories", {}).items():
            for entry in entries:
                for host_dict in entry.values():
                    for host_list in host_dict.values():
                        for host in host_list:
                            host_to_category[host] = category

        # with open(self.disconnect_mapping_file, "w", encoding="utf-8") as f:
        #     json.dump(host_to_category, f, indent=4)

        return host_to_category

    def parse_flow_file(self, file_path):
        with open(file_path, "rb") as file:
            try:
                reader = FlowReader(file)
            except Exception as e:
                print(f"Skipping invalid .flow file: {file_path} ({e})")
                return

            for flow in reader.stream():
                if not hasattr(flow, "request") or not flow.request:
                    continue
                # print(flow.request.host, flow.request.timestamp_end)

                self.process_flow(flow)

    def process_flow(self, flow):
        request = flow.request
        response = flow.response
        timestamp = request.timestamp_start

        if not timestamp:
            return

        request_domain = request.host
        request_url = request.url
        method = request.method
        status = response.status_code if response else None

        size = len(response.content) if response and response.content else 0
        cookies = request.cookies.fields

        try:
            payload = request.content.decode("utf-8") if request.content else ""
        except UnicodeDecodeError:
            payload = "[Binary or Non-UTF-8 Content]"

        request_headers = request.headers
        response_headers = response.headers if response else {}
        disconnect_category = self.disconnect_mapping.get(request_domain, "Other")
        origin_header = request_headers.get("origin", "")
        context = "Extension" if origin_header.startswith("chrome-extension://") or self.extension_name.lower() in origin_header else "Foreground"

        if context != "Extension" and disconnect_category not in self.categories_of_interest:
            return

        response_body = self.determine_response_body(request_url, response_headers)
        payload = self.handle_websocket_payloads(flow, payload)

        row = {
            "extension": self.extension_name,
            "filename": os.path.basename(flow.metadata.get("file_path", "")),
            "timestamp": timestamp,
            "request_url": request_url,
            "request_domain": request_domain,
            "method": method,
            "status": status,
            "response": response_body,
            "payload": payload,
            "size": size,
            "cookies": json.dumps(cookies),
            "disconnect_category": disconnect_category,
            "context": context,
            "contacted_party": "first-party" if self.extension_name.lower() in request_domain else "third-party"
        }

        for header in self.headers_list:
            if "req_header_" in header:
                row[header] = request_headers.get(header.replace("req_header_", ""), "")
            elif "res_header_" in header:
                row[header] = response_headers.get(header.replace("res_header_", ""), "")

        self.output_rows.append(row)

    def determine_response_body(self, request_url, response_headers):
        content_type = response_headers.get("content-type", "").lower()
        if content_type.startswith("text/html"):
            return "[HTML File/Code]"
        elif "javascript" in content_type or request_url.endswith(".js"):
            return "[Javascript File/Code]"
        elif "css" in content_type or request_url.endswith(".css"):
            return "[CSS File/Code]"
        elif content_type.startswith("image/"):
            return "[Media/Image]"
        elif content_type.startswith("video/"):
            return "[Media/Video]"
        else:
            return ""

    def handle_websocket_payloads(self, flow, payload):
        websocket_payloads = []
        if hasattr(flow, "websocket") and flow.websocket is not None:
            for message in flow.websocket.messages:
                if isinstance(message, WebSocketMessage):
                    websocket_payloads.append(message.content.decode("utf-8", errors="ignore"))

        websocket_combined = "\n".join(websocket_payloads)
        if websocket_combined and not payload:
            return websocket_combined
        elif websocket_combined and payload:
            return f"{payload}\n{websocket_combined}"
        return payload

    def get_dataframe(self):
        fieldnames = [
            "extension", "filename", "timestamp", "context", "disconnect_category",
            "contacted_party", "request_domain", "request_url", "method", "status",
            "response", "payload", "size", "cookies"
        ] + self.headers_list

        return pd.DataFrame(self.output_rows, columns=fieldnames)

    def write_to_csv(self):
        fieldnames = [
            "extension", "filename", "timestamp", "context", "disconnect_category",
            "contacted_party", "request_domain", "request_url", "method", "status",
            "response", "payload", "size", "cookies"
        ] + self.headers_list

        with open(self.output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.output_rows)

    def process_flows(self, file_path):
        self.parse_flow_file(file_path)
        if self.output_csv is not None:
            self.write_to_csv()
        return self.get_dataframe()

if __name__ == "__main__":
    processor = FlowProcessor(
        extension_name="maxai",
        output_csv=None,
    )
    df = processor.process_flows('working.flow')
    print(df[['request_domain', 'contacted_party']])
    # df.to_csv('max_test.csv')
