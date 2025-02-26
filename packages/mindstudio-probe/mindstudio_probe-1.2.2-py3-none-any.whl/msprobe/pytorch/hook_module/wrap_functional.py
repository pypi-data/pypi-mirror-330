# Copyright (c) 2024-2024, Huawei Technologies Co., Ltd.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0  (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import torch

from msprobe.pytorch.hook_module.hook_module import HOOKModule
from msprobe.pytorch.common.utils import torch_device_guard
from msprobe.core.common.const import Const
from msprobe.pytorch.common.log import logger
from msprobe.core.common.file_utils import load_yaml


cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path, "support_wrap_ops.yaml")


def get_functional_ops():
    yaml_data = load_yaml(yaml_path)
    wrap_functional_ops = yaml_data.get('functional')
    _all_functional_ops = dir(torch.nn.functional)
    return set(wrap_functional_ops) & set(_all_functional_ops)


TorchFunctions = {func: getattr(torch.nn.functional, func) for func in get_functional_ops()}


class HOOKFunctionalOP(object):
    pass


class FunctionalOPTemplate(HOOKModule):
    def __init__(self, op_name, hook, need_hook=True):
        self.op_name_ = op_name
        self.prefix_op_name_ = "Functional" + Const.SEP + str(op_name) + Const.SEP
        if need_hook:
            super().__init__(hook)

    @torch_device_guard
    def forward(self, *args, **kwargs):
        return TorchFunctions[str(self.op_name_)](*args, **kwargs)


def wrap_functional_op(op_name, hook):
    def functional_op_template(*args, **kwargs):
        return FunctionalOPTemplate(op_name, hook)(*args, **kwargs)

    return functional_op_template


def wrap_functional_ops_and_bind(hook):
    _functional_ops = get_functional_ops()
    for op_name in _functional_ops:
        setattr(HOOKFunctionalOP, "wrap_" + op_name, wrap_functional_op(op_name, hook))
