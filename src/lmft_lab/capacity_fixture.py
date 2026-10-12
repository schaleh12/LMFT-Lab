"""Frozen capacity task. Only evidence verifier / post-prediction evaluator executes it."""
PROCEDURE = "capacity-transmit-1"
SOURCE = "registered-capacity-1"
TRAIN = dict(zip(("t"+str(i) for i in range(1,7)), ((1,3),(2,4),(3,3),(4,2),(3,1),(2,1))))
VALIDATION = dict(zip(("v"+str(i) for i in range(1,5)), ((1,1),(4,4),(1,2),(4,3))))
SEEN = dict(zip(("s"+str(i) for i in range(1,5)), ((1,3),(3,3),(4,2),(2,1))))
UNSEEN = dict(zip(("h"+str(i) for i in range(1,7)), ((1,4),(2,2),(2,3),(3,2),(3,4),(4,1))))
SHIFT = dict(zip(("r"+str(i) for i in range(1,7)), ((5,6),(6,5),(6,6),(8,5),(5,8),(8,8))))
HELD = {**SEEN, **UNSEEN, **SHIFT, "x1":(9,8)}


def execute(length, capacity):
    """Noiseless empty buffer, no draining; writes are the independent task definition."""
    buffer = [None] * capacity
    for index in range(length):
        if index == len(buffer):
            return False
        buffer[index] = index
    return True


def case(identifier):
    length,capacity = {**TRAIN, **VALIDATION, **HELD}[identifier]
    return {"case_id":identifier,"procedure":PROCEDURE,"length":length,"capacity":capacity}


def outcome(identifier, split):
    table = {"train":TRAIN,"validation":VALIDATION}[split]
    length,capacity = table[identifier]
    return {"evidence_id":identifier,"split":split,"procedure":PROCEDURE,"length":length,
            "capacity":capacity,"success":execute(length,capacity)}


def verify(record):
    if set(record)!={"evidence_id","split","procedure","length","capacity","success"}:
        return False
    split=record["split"];identifier=record["evidence_id"]
    if not isinstance(split,str) or not isinstance(identifier,str):return False
    table={"train":TRAIN,"validation":VALIDATION}.get(split,{})
    if identifier not in table or record["procedure"]!=PROCEDURE:return False
    if type(record["success"]) is not bool or any(type(record[k]) is not int for k in ("length","capacity")):return False
    if (record["length"],record["capacity"])!=table[identifier]:return False
    return record["success"]==execute(record["length"],record["capacity"])
