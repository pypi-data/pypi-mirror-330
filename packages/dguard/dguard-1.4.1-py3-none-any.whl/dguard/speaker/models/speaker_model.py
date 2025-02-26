# Copyright (c) 2022 Hongji Wang (jijijiang77@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import dguard.speaker.models.campplus as campplus
import dguard.speaker.models.eres2net as eres2net
import dguard.speaker.models.resnet as resnet
import dguard.speaker.models.resnet_classify as resnet_classify


def get_speaker_model(model_name: str):
    if model_name.startswith("ResNet") or "_sv_r" in model_name:
        if "101" in model_name:
            return getattr(resnet, "ResNet101")
        elif "152" in model_name:
            return getattr(resnet, "ResNet152")
        elif "221" in model_name:
            return getattr(resnet, "ResNet221")
        elif "293" in model_name:
            return getattr(resnet, "ResNet293")
        elif "34_classify" in model_name:
            return getattr(resnet_classify, "ResNet34")
    elif model_name.startswith("CAMPPlus") or "_sv_c_" in model_name:
        return getattr(campplus, "CAMPPlus")
    elif model_name.startswith("ERes2Net") or "_sv_e_" in model_name:
        return getattr(eres2net, "ERes2Net34_aug")
    else:  # model_name error !!!
        print(model_name + " not found !!!")
        exit(1)
