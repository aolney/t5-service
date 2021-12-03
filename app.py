from flask import Flask, request, jsonify

app = Flask(__name__)

# Service set up

import torch
from transformers import T5ForConditionalGeneration,T5Config,T5Tokenizer

def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

set_seed(42)

t5_version = 't5-large'

config = T5Config.from_pretrained(t5_version)
tokenizer = T5Tokenizer.from_pretrained(t5_version)
model = T5ForConditionalGeneration.from_pretrained(t5_version,config=config)

# DEBUG
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = "cpu"
print ("device ",device)
model = model.to(device)

#=======================================================================================
# Service functions
# Fill in <extra_id_0> token
def getFillIn(text, fillLength, responseCount):

    text = text + "  </s>"

    # encode text
    encoding = tokenizer.encode_plus(text, add_special_tokens=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)

    # set top_k = 50 and set top_p = 0.95 and num_return_sequences = 3
    outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        do_sample=True,
        max_length=fillLength,
        top_k=120,
        top_p=0.98,
        early_stopping=True,
        num_return_sequences=responseCount
    )

    _0_index = text.index('<extra_id_0>')
    _result_prefix = text[:_0_index]
    _result_suffix = text[_0_index+12:]  # 12 is the length of <extra_id_0>

    def _filter(output, end_token='<extra_id_1>'):
        # The first token is <unk> (inidex at 0) and the second token is <extra_id_0> (indexed at 32099)
        _txt = tokenizer.decode(output[2:], skip_special_tokens=False, clean_up_tokenization_spaces=False)
        if end_token in _txt:
            _end_token_index = _txt.index(end_token)
            return _result_prefix + _txt[:_end_token_index] + _result_suffix
        else:
            return _result_prefix + _txt + _result_suffix

    results = list(map(_filter, outputs))

    #remove dups
    final_outputs =[]
    for r in results:
        if r not in final_outputs:
            final_outputs.append(r)
    
    return final_outputs

#=======================================================================================
# Instructions/help
@app.route('/')
def api_help():
    return 'API for t5-service, see https://github.com/aolney/t5-service'

# getFillIn(text,fillLength)
@app.route('/api/getFillIn', methods=['GET', 'POST'])
def api_getFillIn():
    content = request.get_json()
    result = getFillIn( content['text'], int(content['fillLength']), int(content['responseCount']) )
    return jsonify(result)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST') #GET,PUT,POST,DELETE')
    return response
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')