import re

queries = []
sentences = []
resolved = set()


def read_file(filename):
    queries.clear()
    sentences.clear()
    resolved.clear()
    with open(filename, 'r') as f:
        N = int(f.readline().strip())
        for i in range(N):
            queries.append(f.readline().strip())

        K = int(f.readline().strip())
        for i in range(K):
            cnf = to_cnf(f.readline().strip())
            if "|" in cnf:
                sentences.append(cnf)
                q = negate(queries[0])
                # if has_predicate(cnf, q):
                #     resolve(cnf, q)
            else:
                resolved.add(cnf)
            # kbs.append(f.readline().strip())


def has_predicate(sentence, pred):
    name = ("~" if "~" in pred else "") + get_pred_name(pred)
    neg_name = negate(name)

    if "~" in pred:
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
            # TODO: What are the invalid cases?
            for p1, p2 in zip(get_arg(p), get_arg(pred)):
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
            break


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




read_file("input1.txt")
print(replace_param("Play(x, y)", "y", "Teddy"))