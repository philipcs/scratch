from dns import resolver, reversename, exception
import argparse

class Engine:
    def __init__(self, nameservers=[]):
        self.res = resolver.Resolver()
        if len(nameservers) > 0:
            self.res.nameservers = nameservers

    def lookup(self, ip: str) -> str:
        try:
            rev_name = reversename.from_address(ip)
            answers = self.res.query(rev_name, "PTR")
            return str(answers[0])[:-1]
        except resolver.NXDOMAIN:
            return "NOT FOUND"
        except exception.SyntaxError:
            return "MALFORMED IP"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", nargs="+", required=True, help="File to read list of IPs to do lookup from")
    parser.add_argument("-s", "--server", nargs="+", required=False, help="Server(s) to query")
    args = parser.parse_args()
    if args.server:
        e = Engine(nameservers=args.server)
    else:
        e = Engine()
    for filename in args.file:
        print("ip,reverse_lookup")
        with open(filename) as f:
            for line in f:
                query = line.strip()
                print("%s,%s" %(query, e.lookup(query)))

