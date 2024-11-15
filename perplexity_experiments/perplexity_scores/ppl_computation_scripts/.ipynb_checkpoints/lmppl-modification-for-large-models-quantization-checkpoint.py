# requirement
#pip install bitsandbytes


# set quantization configuration to load large model with less GPU memory
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)


# add "quantization_config" in the params dictionary for the class you call : EncoderDecoderLM, LM or MaskedLM
params = {"local_files_only": not internet_connection(), "use_auth_token": use_auth_token,
           "trust_remote_code": trust_remote_code,"quantization_config": bnb_config}
 
 
