import sys
import json
from client import VRFSimulator

vrf = VRFSimulator("vrf_server_key_8819")

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "vrf_evaluate_or_verify",
                        "description": "Evaluate VRF on input or verify proof against output",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["evaluate", "verify"]},
                                "input_val": {"type": "string"},
                                "output": {"type": "string"},
                                "proof": {"type": "string"}
                            },
                            "required": ["action", "input_val"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "vrf_evaluate_or_verify":
            act = args["action"]
            inp = args["input_val"]
            if act == "evaluate":
                out, prf = vrf.evaluate(inp)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"output": out, "proof": prf, "public_key": vrf.pk})}]}}
            elif act == "verify":
                ok = VRFSimulator.verify(vrf.pk, inp, args.get("output", ""), args.get("proof", ""))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"valid_proof": ok})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
