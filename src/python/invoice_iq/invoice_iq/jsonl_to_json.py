import json

def jsonl_to_json(jsonl):
    '''
    #Comment add 
    #TODO: HarshK 
    '''
    json_obj = list()
    with open(jsonl,'r',encoding='utf-8') as f:
        jsonl_content = f.read()
        json_obj = [json.loads(lines) for lines in jsonl_content.splitlines()]
        f.close()
    return json.dumps(json_obj)



    
    
    