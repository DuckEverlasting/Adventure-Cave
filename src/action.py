class Action:
    def __init__(self, name, grammar, run):
        self.name = name
        self.grammar = grammar
        self.run = run

    def check_grammar(self, command):
        if "adv_required" in self.grammar:
            # Currently hard coded for movement, since that's the only
            # place adverbs are being used.
            if not command["adv"]:
                return {
                    "result": False,
                    "message": f"Where would you like to {command['act']}?"
                }
                
        if "d_obj_prohibited" in self.grammar:
            if command["d_obj"]:
                return {
                    "result": False,
                    "message": f"The word {command['d_obj']} doesn't make sense there.",
                }
        elif "d_obj_required" in self.grammar:
            if not command["d_obj"]:
                return {"result": False, "message": f"What would you like to {command['act']}?"}

        if "i_obj_prohibited" in self.grammar:
            if command["i_obj"]:
                return {
                    "result": False,
                    "message": f"The word {command['d_obj']} doesn't make sense there.",
                }
        elif "i_obj_required" in self.grammar:
            if not command["i_obj"]:
                if command["d_obj"]:
                    return {
                        "result": False,
                        "message": f"What would you like to {command['act']} {command['d_obj']} {self.grammar['preps_accepted'][0]}?",
                    }
                else:
                    return {"result": False, "message": f"What would you like to {command['act']} {command['prep']}?"}

        if command["i_obj"]:
            if command["prep"] not in self.grammar["preps_accepted"]:
                return {
                    "result": False,
                    "message": f"The word {command['prep']} doesn't make sense there.",
                }

        return {"result": True, "message": None}
