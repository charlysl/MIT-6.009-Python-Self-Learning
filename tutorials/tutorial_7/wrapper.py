import lab, json, traceback
from importlib import reload
reload(lab) # this forces the student code to be reloaded when page is refreshed

def run_test(input_data):
    try:
        return ('ok', select_candidates(input_data))
    except:
        return ('error', traceback.format_exc())

def select_candidates(input_data):
    print("wrapper.select_candidates: input_data = ", input_data, flush=True)
    num_candidates = input_data["num_candidates"]
    num_talents = input_data["num_talents"]
    candidate_to_talents = input_data["candidate_to_talents"]
    talent_to_candidates = input_data["talent_to_candidates"]
    matrix = input_data["matrix"] #only needed for ui
    r = lab.select_candidates(num_candidates, num_talents,
                              candidate_to_talents, talent_to_candidates)
    print("wrapper.select_candidates returning", r, flush=True)
    return r

def init():
    return None

