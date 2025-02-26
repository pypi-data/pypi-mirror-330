# coding = utf-8
# @Time    : 2025-02-10  10:47:41
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: ASVSpoof Interface

import torch
import torchaudio
import torch.nn.functional as F
from torchaudio.compliance import kaldi
from dguard.speaker.utils.checkpoint import load_checkpoint
from dguard.speaker.models.speaker_model import get_speaker_model
# from silero_vad import load_silero_vad, read_audio, get_speech_timestamps

def extract_speech_waveform(wav, vad_model):
    """Extract speech segments using VAD"""
    speech_timestamps = get_speech_timestamps(wav, vad_model)
    
    if not speech_timestamps:  # 如果没有检测到语音
        return wav  # 返回原始音频
        
    speech_waveform = []
    for segment in speech_timestamps:
        start_sample = segment['start']
        end_sample = segment['end']
        speech_waveform.append(wav[start_sample:end_sample])

    speech_waveform = np.concatenate(speech_waveform)
    return speech_waveform

DEFAULT_CONFIG = {
    'model': 'ResNet34_classify',
    'data_type': 'raw',
    'seed': 42,
    'gpus': '[0]',
    'use_vad': False,  ##根据实际情况修改（主要做VAD的）
    'model_args': {
        'feat_dim': 80,
        'embed_dim': 256,
        'pooling_func': 'TSTP',
        'two_emb_layer': False
    },
    'dataloader_args': {
        'batch_size': 1,
        'num_workers': 2,
        'pin_memory': False,
        'prefetch_factor': 8,
        'drop_last': True
    },
    
    'dataset_args': {
        'sample_num_per_epoch': 0,
        'shuffle': True,
        'shuffle_args': {
            'shuffle_size': 2500
        },
        'filter': True,
        'filter_args': {
            'min_num_frames': 100,
            'max_num_frames': 800
        },
        'resample_rate': 16000,
        'speed_perturb': True,
        'num_frms': 200,
        'aug_prob': 0.6,
        'vad': True,
        'vad_args': {
            'vad_threshold': 0.5
        },
        'fbank_args': {
            'num_mel_bins': 80,
            'frame_shift': 10,
            'frame_length': 25,
            'dither': 1.0
        },
        'spec_aug': False,
        'spec_aug_args': {
            'num_t_mask': 1,
            'num_f_mask': 1,
            'max_t': 10,
            'max_f': 8,
            'prob': 0.6
        }
    }
}

def load_trained_model(configs, checkpoint_path, device="cuda"):
    model = get_speaker_model(configs['model'])(**configs['model_args'])
    load_checkpoint(model, checkpoint_path)
    model.to(device)
    model.eval()
    return model

def process_audio(audio_path, use_vad=False, resample_rate=16000):
    waveform, sample_rate = torchaudio.load(audio_path)
    if sample_rate != resample_rate:
        waveform = torchaudio.transforms.Resample(
            orig_freq=sample_rate, new_freq=resample_rate)(waveform)
    return waveform
# def process_audio(audio_path, vad_model, use_vad=False, resample_rate=16000):
#     """Process a single audio file"""
#     if use_vad:
#         wav = read_audio(audio_path)
#         waveform = extract_speech_waveform(wav, vad_model)
#         if isinstance(waveform, np.ndarray):
#             waveform = torch.tensor(waveform, dtype=torch.float32)
#         if waveform.ndimension() == 1:
#             waveform = waveform.unsqueeze(0)
#     else:
#         waveform, sample_rate = torchaudio.load(audio_path)
#         # print("sample_rate",sample_rate)
#         if sample_rate != resample_rate:
#             waveform = torchaudio.transforms.Resample(
#                 orig_freq=sample_rate, new_freq=resample_rate)(waveform)
#     return waveform

def compute_fbank(waveform, configs):
    """Compute Fbank features"""
    fbank_args = configs['dataset_args']['fbank_args']
    waveform = waveform * (1 << 15)
    mat = kaldi.fbank(
        waveform,
        num_mel_bins=fbank_args['num_mel_bins'],
        frame_length=fbank_args['frame_length'],
        frame_shift=fbank_args['frame_shift'],
        dither=fbank_args['dither'],
        sample_frequency=configs['dataset_args']['resample_rate'],
        window_type='hamming',
        use_energy=False
    )
    # Apply CMVN
    mat = mat - torch.mean(mat, dim=0)
    return mat

def predict_single_audio(audio_path, model, configs, device="cuda"):
    """Predict for a single audio file"""
    model.eval()
    with torch.no_grad():
        try:
            # Process audio
            waveform = process_audio(
                audio_path,
                configs['use_vad'], 
                configs['dataset_args']['resample_rate']
            )
            
            # Compute features
            features = compute_fbank(waveform, configs)
            
            # Prepare features for model
            features = features.unsqueeze(0).float().to(device)
            
            # Forward pass
            outputs = model(features)

            # Handle different output types
            if isinstance(outputs, tuple):
                logits = outputs[1]
            else:
                logits = outputs
            # from IPython import embed; embed()
            # Get prediction
            if logits.size(-1) > 1:
                probs = F.softmax(logits, dim=-1)
                pred = torch.argmax(probs, dim=-1)
                confidence = probs[0][pred.item()].item()
            else:
                prob = torch.sigmoid(logits)
                pred = (prob > 0.5).long()
                confidence = prob.item() if pred.item() == 1 else 1 - prob.item()
                
            return {
                "prediction": pred.item(),
                "confidence": confidence,
                "raw_output": logits.cpu().numpy(),
                "status": "success"
            }
        
        except Exception as e:
            print(f"Error in ASV prediction: {e}")
            return {
                "status": "error",
                "error_message": str(e)
            }