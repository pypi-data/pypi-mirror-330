import pandas as pd    
from collections import defaultdict
import json
from mitmproxy.io import FlowReader
from mitmproxy.http import HTTPFlow

class NetworkAnalyzer():
    def __init__(
            self,
            df,
            # csv_path,
            flow_file,
            extension
            ) -> None:
        # self.network = pd.read_csv(csv_path)
        self.network = df
        self.res = defaultdict(set)        
        self.extension = extension
        self.flow_file = flow_file

    def get_referer(self, target_domain):
        res = []
        with open(self.flow_file, "rb") as file:
            reader = FlowReader(file)
            
            # Loop through the flows to find requests matching the target domain
            for flow in reader.stream():
                if not hasattr(flow, "request") or not flow.request:
                    continue

                # Check if the request's host matches the target domain
                if target_domain in flow.request.host:
                    referer_header = flow.request.headers.get("Referer")
                    if referer_header:
                        res.append(referer_header)
        return res
        
    def remove_noise(self, domains: set):
        res = []
        for domain in domains:
            if any(self.extension in ref for ref in self.get_referer(domain)):
                res.append(domain)
        return res

    def get_party(self, party):
        df = self.network
        df = df[
            (df['contacted_party'] == f'{party}-party')
        ]
        domains = set(df['request_domain'].tolist())
        if party == 'third':
            return self.remove_noise(domains)
        return domains

    def get_all_payloads(self, endpoint):
        request_payloads = []
        with open(self.flow_file, "rb") as f:
            reader = FlowReader(f)
            
            for flow in reader.stream():
                if not isinstance(flow, HTTPFlow):
                    continue

                if endpoint not in flow.request.url:
                    continue

                try:
                    request_data = json.loads(flow.request.content.decode('utf-8'))
                    request_payloads.append(request_data)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass
        return request_payloads

    @staticmethod
    def combine_payloads(payloads):
        res = {}
        bad = []
        for payload in payloads:
            try:
                for key, val in payload.items():
                    if key not in res:
                        res[key] = val
            except AttributeError:
                bad.append(payload)
        # with open('src/bad_payloads.json', 'w') as f:
        #     json.dump(bad, f, indent=2)
        return res


    def run(self):
        first_parties = self.get_party('first')
        third_parties = self.get_party('third')
        fp_payloads = [self.combine_payloads(self.get_all_payloads(endpoint)) for endpoint in first_parties]
        tp_payloads = [self.combine_payloads(self.get_all_payloads(endpoint)) for endpoint in third_parties]
        return fp_payloads, tp_payloads

def main():
    na = NetworkAnalyzer('max_test.csv', 'working.flow', "maxai")
    fp, tp = na.run()
    print(any(na.network['contacted_party'] == 'third-party'))

if __name__ == "__main__":
   main()

"""
TODO:
1. create a cli tool
2. fill out prompt.txt based on the paper
3. get cookies function
4. represent the output
"""