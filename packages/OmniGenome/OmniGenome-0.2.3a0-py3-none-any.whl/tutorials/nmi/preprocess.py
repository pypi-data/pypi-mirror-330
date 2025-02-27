import json

import findfile

for f in findfile.find_cwd_files(".txt", exclude_key=[".gz", "json"]):
    print(f)
    lines = open(f, encoding="utf8").readlines()

    newlines = []
    for line in lines:
        data = {"seq": json.loads(line)["rna"], "label": json.loads(line)["structure"]}
        newlines.append(data)

    train_set = newlines[: int(len(newlines) * 0.8)]
    test_set = newlines[int(len(newlines) * 0.8) : int(len(newlines) * 0.9)]
    valid = newlines[int(len(newlines) * 0.9) :]

    with open(f.replace(".txt", "_train.json"), "w", encoding="utf8") as fout:
        for line in train_set:
            fout.write(json.dumps(line) + "\n")

    with open(f.replace(".txt", "_test.json"), "w", encoding="utf8") as fout:
        for line in test_set:
            fout.write(json.dumps(line) + "\n")

    with open(f.replace(".txt", "_valid.json"), "w", encoding="utf8") as fout:
        for line in valid:
            fout.write(json.dumps(line) + "\n")
