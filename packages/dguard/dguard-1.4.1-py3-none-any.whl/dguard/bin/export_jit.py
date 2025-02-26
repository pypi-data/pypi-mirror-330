from __future__ import print_function

import argparse
import os

import torch
import yaml
import os
import sys

sys.path.append("/VAF/train")
from dguard.utils.config import build_config
from dguard.utils.builder import build


def get_args():
    parser = argparse.ArgumentParser(description="export your script model")
    parser.add_argument(
        "--config", required=True, default="", help="config file"
    )
    parser.add_argument(
        "--checkpoint", required=True, default="", help="checkpoint model"
    )
    parser.add_argument(
        "--output_file", required=True, default="", help="output file"
    )
    parser.add_argument(
        "--output_quant_file", default=None, help="output quantized model file"
    )
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    # No need gpu for model export
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    # check if checkpoint file exists
    if not os.path.exists(args.checkpoint):
        raise FileNotFoundError(
            "checkpoint file ({}) does not exist !!!".format(args.checkpoint)
        )
    # make sure output directory exists
    output_dir = os.path.dirname(args.output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    config = build_config(args.config, overrides, True)
    model = build("embedding_model", config)
    print(model)
    checkpoint = torch.load(args.checkpoint)
    model.load_state_dict(checkpoint["state_dict"])
    script_model = torch.jit.script(model)
    script_model.save(args.output_file)
    print("Export model successfully, see {}".format(args.output_file))
    # Export quantized jit torch script model
    if args.output_quant_file:
        quantized_model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.qint8
        )
        print(quantized_model)
        script_quant_model = torch.jit.script(quantized_model)
        script_quant_model.save(args.output_quant_file)
        print(
            "Export quantized model successfully, "
            "see {}".format(args.output_quant_file)
        )


if __name__ == "__main__":
    main()
