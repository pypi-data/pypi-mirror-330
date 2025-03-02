# Copyright (c) 2025 Zhendong Peng (pzd17@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Tuple, Union

import torch
from torch.nn.utils.rnn import pad_sequence


class ChatTokenizer:
    def __init__(
        self,
        tokenizer,
        system_prompt: str = None,
        audio_placeholder: str = "<|audio|>",
        label_placeholder: str = "<|label|>",
    ):
        self.system_prompt = system_prompt
        self.tokenizer = tokenizer
        self.tokenizer.add_special_tokens({"additional_special_tokens": [audio_placeholder, label_placeholder]})
        self.audio_placeholder = audio_placeholder
        self.label_placeholder = label_placeholder
        self.audio_placeholder_id = self.tokenizer.convert_tokens_to_ids(audio_placeholder)
        self.label_placeholder_id = self.tokenizer.convert_tokens_to_ids(label_placeholder)

    def audio_mask(self, input_ids: torch.Tensor, valid: bool = True) -> torch.Tensor:
        if valid:
            return input_ids == self.audio_placeholder_id
        return input_ids != self.audio_placeholder_id

    def label_mask(self, input_ids: torch.Tensor, valid: bool = True) -> torch.Tensor:
        if valid:
            return input_ids == self.label_placeholder_id
        return input_ids != self.label_placeholder_id

    def pad_mask(self, input_ids: torch.Tensor, valid: bool = True) -> torch.Tensor:
        if valid:
            return input_ids == self.tokenizer.pad_token_id
        return input_ids != self.tokenizer.pad_token_id

    def fill_labels(self, label_ids: torch.Tensor, input_ids: torch.Tensor) -> torch.Tensor:
        input_ids[self.label_mask(input_ids)] = label_ids[self.pad_mask(label_ids, False)]
        return input_ids

    def tokenize(
        self,
        audio_lens: Union[int, List[int]],
        labels: Union[str, List[str]],
        task_instruction: str = "",
        tokenize: bool = True,
    ) -> Tuple[List[int], List[int]]:
        if isinstance(audio_lens, int):
            assert isinstance(labels, str)
            audio_lens = [audio_lens]
            labels = [labels]
        assert len(audio_lens) == len(labels)

        chat = []
        label_ids = []
        if self.system_prompt is not None:
            chat.append({"role": "system", "content": self.system_prompt})
        for audio_len, label in zip(audio_lens, labels):
            audio_placeholder = self.audio_placeholder * audio_len
            chat.append({"role": "user", "content": f"{task_instruction} {audio_placeholder}".strip()})
            label_ids.append(self.tokenizer(label)["input_ids"])
            label_placeholder = self.label_placeholder * len(label_ids[-1])
            chat.append({"role": "assistant", "content": label_placeholder})
        input_ids = self.tokenizer.apply_chat_template(chat, tokenize=tokenize, add_generation_prompt=False)
        return sum(label_ids, []), input_ids

    def batch_tokenize(
        self,
        audio_lens: List[Union[int, List[int]]],
        labels: List[Union[str, List[str]]],
        task_instructions: Union[str, List[str]] = "",
        batch_first: bool = True,
        device: torch.device = torch.device("cpu"),
    ):
        assert len(audio_lens) == len(labels)
        if not isinstance(task_instructions, list):
            task_instructions = [task_instructions] * len(audio_lens)
        label_ids, input_ids = zip(*map(self.tokenize, audio_lens, labels, task_instructions))
        label_lens = [len(ids) for ids in label_ids]
        input_lens = [len(ids) for ids in input_ids]
        label_ids = [torch.tensor(ids, device=device, dtype=torch.long) for ids in label_ids]
        input_ids = [torch.tensor(ids, device=device, dtype=torch.long) for ids in input_ids]
        label_ids = pad_sequence(label_ids, padding_value=self.tokenizer.pad_token_id, batch_first=batch_first).long()
        input_ids = pad_sequence(input_ids, padding_value=self.tokenizer.pad_token_id, batch_first=batch_first).long()
        return label_ids, input_ids, label_lens, input_lens
