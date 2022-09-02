#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description       : Mask span in the content randomly.
@Date     :2022/08/26 16:28:30
@Author      :Lv Chuancheng
@version      :1.0
'''

import random
import torch
import numpy as np

def random_mask_span(tokens: list, ratio: float, max_span_num: int):
    """
    
    Args:
    
    Returns:
    
    """

    def verify(mask_span_start_id,span_length,masked_positions,seq_len):
        flag = True
        if mask_span_start_id-1 in masked_positions:
            return False
        for i in range(span_length+1):
            if mask_span_start_id+i in masked_positions or mask_span_start_id+i >= seq_len:
                flag = False
        return flag

    seq_len = len(tokens)
    sample_prob = torch.ones(seq_len)
    sample_prob /= torch.sum(sample_prob)
    if not max_span_num:
        span_num = random.randint(1, max(1, round(seq_len*ratio)) if not max_span_num else max_span_num)
    masked_positions = []
    masked_start_positions = []
    masked_span_lengths = []
    total_span_length = 0
    for i in range(span_num):
        span_length = max(1,np.random.poisson(3))
        mask_span_start_id = sample_prob.multinomial(1)
        trials = 0
        while not verify(mask_span_start_id,span_length,masked_positions,seq_len) and trials <= 10:
            mask_span_start_id = sample_prob.multinomial(1)
            trials += 1
        if trials >= 10:
            break
        for i in range(span_length):
            masked_positions.append(mask_span_start_id+i)
        masked_start_positions.append(mask_span_start_id)
        masked_span_lengths.append(span_length)
        total_span_length += span_length
        
    new_tokens = []
    masked_tokens = []
    span_idx = 0
    for idx in range(seq_len):
        if idx in masked_start_positions:
            new_tokens.append('<extra_id_'+str(span_idx)+'>')
            masked_tokens.append(tokens[idx])
            if idx+1 not in masked_positions:
                masked_tokens.append('<extra_id_'+str(span_idx+1)+'>')
            span_idx += 1
        elif idx in masked_positions:
            masked_tokens.append(tokens[idx])
            if idx+1 not in masked_positions:
                masked_tokens.append('<extra_id_'+str(span_idx)+'>')
        else:
            new_tokens.append(tokens[idx])
    return new_tokens, total_span_length, masked_tokens, new_tokens

    