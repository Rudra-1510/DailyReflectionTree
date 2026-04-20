import csv

def load_tree(file_path):
    tree = {}
    
    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        
        for row in reader:
            tree[row["id"]] = row
    
    return tree


def find_children(tree, parent_id):
    return [node for node in tree.values() if node["parentId"] == parent_id]


def run_agent():

    tree = load_tree("../tree/reflection-tree.tsv")
    
    state = {
        "answers": {},
        "axis1": {"internal": 0, "external": 0},
        "axis2": {"contribution": 0, "entitlement": 0},
        "axis3": {"self": 0, "others": 0}
    }

    current_id = "START"

    while True:

        node = tree[current_id]
        node_type = node["type"]
        
        print("\n", node["text"])

        # question node
        if node_type == "question":
            
            options = node["options"].split("|")
            
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            
            choice = int(input("Select option: ")) - 1
            
            answer = options[choice]
            
            state["answers"][current_id] = answer
        
        # record signal
        if node["signal"]:
            
            axis, value = node["signal"].split(":")
            
            state[axis][value] += 1
        
        # find next node
        children = find_children(tree, current_id)

        if node["type"] == "decision":
            
            rules = node["options"].split(";")
            
            previous_answer = list(state["answers"].values())[-1]
            
            for rule in rules:
                
                cond, target = rule.split(":")
                
                valid_answers = cond.replace("answer=", "").split("|")
                
                if previous_answer in valid_answers:
                    current_id = target
                    break
        
        elif node["target"]:
            current_id = node["target"]
        
        elif children:
            current_id = children[0]["id"]
        
        else:
            break

        if node_type == "end":
            break


if __name__ == "__main__":
    run_agent()
