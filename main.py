from fastapi import FastAPI
import struct
import json

app = FastAPI(title="Reflexnet-v2", version="2.1 PRO")

class NexusV2_BitPacker:
    FMT = "!I B f"
    SIZE = struct.calcsize(FMT)

    def pack_data(self, msg_id, status_code, value):
        return struct.pack(self.FMT, msg_id, status_code, value)

    def unpack_data(self, binary_packet):
        if len(binary_packet) != self.SIZE:
            raise ValueError(f"Packet corrupt: got {len(binary_packet)}B, need {self.SIZE}B")
        return struct.unpack(self.FMT, binary_packet)

v2 = NexusV2_BitPacker()

@app.get("/")
def home():
    return {"engine": "NexusV2_BitPacker", "version": "2.1 PRO", "size": "9 bytes fixed"}

@app.get("/benchmark")
def benchmark():
    msg_id, status, value = 101, 1, 99.99
    json_data = json.dumps({"id": msg_id, "status": status, "value": value}).encode()
    packed = v2.pack_data(msg_id, status, value)
    return {
        "json_size": f"{len(json_data)}B",
        "binary_size": f"{len(packed)}B",
        "saving": f"{(1-len(packed)/len(json_data))*100:.0f}%",
        "fixed_size": f"{v2.SIZE}B",
        "50k_packets": f"JSON={len(json_data)*50000/1024:.0f}KB vs Binary={v2.SIZE*50000/1024:.0f}KB"
    }
