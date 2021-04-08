import re

queries = []
sentences = []
constant = []
verbal = False

def read_file(filename):
    queries.clear()
    sentences.clear()
    constant.clear()
    with open(filename, 'r') as f:
        N = int(f.readline().strip())
        for i in range(N):
            queries.append(f.readline().strip())

        K = int(f.readline().strip())
        for i in range(K):
            cnf = to_cnf(f.readline().strip())
            if "|" in cnf:
                sentences.append(cnf)
            else:
                constant.append(cnf)
            # kbs.append(f.readline().strip())


def solve():
    ans = []
    resolved_sentence = []
    resolved = []
    asked = set()

    def ask(pred):
        for s in resolved_sentence:
            if has_neg_predicate(s, pred):
                res = resolve(s, pred)
                if res:
                    if "|" in res:
                        if res not in resolved_sentence:
                            resolved_sentence.append(res)
                            resolved.extend(list(asked))
                            if verbal:
                                print(f"New Sentence: {res}")
                    else:
                        if negate(res) in asked:
                            if verbal:
                                print(f"Conflict found: {res}, {negate(res)}")
                            return True
                        else:
                            if res not in asked:
                                if verbal:
                                    print(f"New Resolved: {res}")
                                resolved.append(res)
        return False

    for q in queries:
        nq = negate(q)
        if verbal:
            print(f"Solving for {q} by adding {nq}")
        resolved_sentence = [s for s in sentences]
        resolved = [c for c in constant]
        resolved.insert(0, nq)
        asked = set()
        solved = False
        while len(resolved) > 0:
            r = resolved.pop()
            if ask(r):
                solved = True
                break
            asked.add(r)
        if verbal:
            print(f"TELL: {solved}")
        ans.append(solved)
    print(ans)


def has_neg_predicate(sentence, pred):
    name = ("~" if "~" in pred else "") + get_pred_name(pred)
    neg_name = negate(name)

    if "~" in neg_name:
        return neg_name in sentence
    else:
        return neg_name in sentence and name not in sentence


def resolve(sentence, pred):
    # return None if it is not resolvable
    args = {}
    name = ("~" if "~" in pred else "") + get_pred_name(pred)
    neg_name = negate(name)
    sentence_split = sentence.split("|")
    for p in sentence_split:
        if neg_name in p:

            for p1, p2 in zip(get_arg(p), get_arg(pred)):
                p1 = p1.strip()
                p2 = p2.strip()
                if is_variable(p1) & is_variable(p2):
                    return None
                elif is_variable(p1) | is_variable(p2):
                    if is_variable(p1):
                        args[p1] = p2
                    else:
                        args[p2] = p1
                else:
                    if p1 != p2:
                        return None
            sentence_split.remove(p)
            break

    for i, p in enumerate(sentence_split):
        p_args = get_arg(p)
        for arg in p_args:
            if arg in args:
                sentence_split[i] = replace_param(p, arg, args[arg])

    return "|".join(sentence_split)


def to_cnf(implication):
    # convert an implication to CNF and return the CNF

    # implication needs to have "=>"
    if "=>" not in implication:
        return implication

    cnf = []
    left, right = implication.split("=>")[0], implication.split("=>")[1]
    for pred in left.split("&"):
        cnf.append(negate(pred.strip()))
    cnf.append(right.strip())
    return "|".join(cnf)


def negate(pred):
    if "~" in pred:
        return pred.replace("~", "")
    else:
        return "~"+pred


def get_arg(pred):
    pattern = r"\(([^)]+)\)"
    p = re.search(pattern, pred)

    return p.group().strip(")").strip("(").split(",")


def get_pred_name(pred):
    return pred.replace("~", "").split("(")[0]


def is_variable(param):
    cap = r"^[A-Z]"
    # if the parameter starts with a capitalized letter, then it's not a variable
    return not re.search(cap, param)


def replace_param(pred, param, new_value):
    split = pred.split("(")
    params = split[1].strip(")")
    args = params.split(",")
    for i, arg in enumerate(args):
        args[i] = arg.strip()
        if arg.strip() == param:
            args[i] = new_value
    return split[0] + "(" + ",".join(args) + ")"


read_file("input3.txt")
solve()