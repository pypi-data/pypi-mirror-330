model_info = {
    "dguard_sv_r101_cjsd8000_split_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "dguard_sv_r152_cjsd8000_split_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "dguard_sv_r221_cjsd8000_split_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "dguard_sv_r293_cjsd8000_split_lm": {
        "embedding_size": "256",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "cjsd",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
    },
    "dguard_sv_e_cjsd8000_split_lm": {
        "embedding_size": "192",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
        "wavform_normalize": True,
    },
    "dguard_sv_c_cjsd8000_split_lm": {
        "embedding_size": "192",
        "sample_rate": "16000",
        "mode": "wespeaker",
        "subdir": "wespeaker",
        "add_time": "2024-05-01",
        "author": "zhaosheng",
        "wavform_normalize": True,
    },
}

if __name__ == "__main__":
    # print all pt and yaml path
    for _model in model_info.keys():
        # print(f"# {_model}")
        pt = model_info[_model]["pt"]
        print(f'wget "{pt}" -O encrypted_{_model}.pt')
        yaml = model_info[_model]["yaml"]
        print(f'wget "{yaml}" -O encrypted_{_model}.yaml')
        # print(model_info[_model]['yaml'])
        # print('# -------------------')
