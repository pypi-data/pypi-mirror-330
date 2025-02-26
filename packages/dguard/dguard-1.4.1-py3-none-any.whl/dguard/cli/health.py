import os
import time

import torch
import torchaudio

# Try to import rich, if not available, define a fallback
try:
    from rich.console import Console
    from rich.progress import Progress
    from rich.table import Table

    rich_available = True
    console = Console()
except ImportError:
    rich_available = False


test_audio = {
    "ASR_zh": "/home/zhaosheng/Documents/dguard_project/dguard_home/aliasr/example/zh.mp3",
    "ASR_en": "/home/zhaosheng/Documents/dguard_project/dguard_home/aliasr/example/en.mp3",
    "DIA_zh_1c2p": "/home/zhaosheng/Documents/dguard_project/test/data/1channel2person.wav",
    "DIA_zh_2c2p": "/home/zhaosheng/Documents/dguard_project/test/data/2channel2person.wav",
    "SPK_zh": "/home/zhaosheng/Documents/dguard_project/test/data/test.wav",
    "ASV_zh": "/home/zhaosheng/Documents/dguard_project/dguard_home/aliasr/example/zh.mp3",
}


def print_step(message, status="Success", style="bold green"):
    global step
    step += 1
    if rich_available:
        console.print(f"Step {step}: {message}", style=style)
    else:
        print(f"Step {step}: {message} - {status}")


def print_results_table(results):
    # 如果result中的第一个元素（name)是字符串重复了，则只取第一个
    all_results = results
    results = []
    for item in all_results:
        if item[0] not in [x[0] for x in results]:
            results.append(item)
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Test")
    table.add_column("Time (s)")
    table.add_column("Device")
    table.add_column("Status")
    table.add_column("Additional Info")

    for result in results:
        # Format the output
        test, time, device, status, additional_info = result
        status_symbol = "✔" if status == "Success" else "×"
        additional_info = "/" if additional_info is None else additional_info
        table.add_row(test, str(time), device, status_symbol, additional_info)
    console.print(table)


# Helper function to load audio and get its length
def get_audio_length(file_path):
    data, sr = torchaudio.load(file_path)
    return data.size(1) / sr


# Initialize global variables
step = 0
result = []
audio_lengths = {key: get_audio_length(val) for key, val in test_audio.items()}

# Rest of the code...

# Load Modules
start_time = time.time()
from dguard import DguardASR, DguardASV, DguardClient, DguardModel, DguardMos

if rich_available:
    console.print("Importing Modules", style="bold")
else:
    print("Importing Modules")
print_step(f"Import Time: {time.time()-start_time:.2f}s", status="Success")

# Check DGUARD_MODEL_PATH
DGUARD_MODEL_PATH = os.getenv("DGUARD_MODEL_PATH", None)
result.append(
    [
        "DGUARD_MODEL_PATH",
        "/",
        "/",
        "Failed" if DGUARD_MODEL_PATH is None else "Success",
        "/" if DGUARD_MODEL_PATH is None else DGUARD_MODEL_PATH,
    ]
)

# ASR Health Check
for device in ["cpu", "cuda"]:
    asr = None
    try:
        asr_start = time.time()
        asr = DguardASR(device=device)
        asr_time = time.time() - asr_start
        print_step(f"ASR Init Time: {asr_time:.2f}s on {device}", status="Success")
        result.append([f"ASR_{device}_init", f"{asr_time:.2f}", device, "Success", "/"])
    except Exception as e:
        print_step(f"ASR Init on {device} failed", status="Failed", style="bold red")
        result.append([f"ASR_{device}_init", "/", device, "Failed", str(e)])

    if asr:
        for language, audio_file in test_audio.items():
            if "ASR" in language:
                try:
                    asr_start = time.time()
                    text = asr.infer(audio_file, language=language.split("_")[1])
                    asr_time = time.time() - asr_start
                    asr_rtf = asr_time / audio_lengths[language]
                    print_step(
                        f"ASR Infer Time: {asr_time:.2f}s on {device}", status="Success"
                    )
                    result.append(
                        [
                            f"ASR_{device}_infer_{language}",
                            f"{asr_time:.2f}",
                            device,
                            "Success",
                            f"RTF: {asr_rtf:.4f}",
                        ]
                    )
                except Exception as e:
                    print_step(
                        f"ASR Infer on {device} failed",
                        status="Failed",
                        style="bold red",
                    )
                    result.append(
                        [
                            f"ASR_{device}_infer_{language}",
                            "/",
                            device,
                            "Failed",
                            str(e),
                        ]
                    )

# Model Health Check
for dguard_device in ["cpu", "cuda"]:
    try:
        start_time = time.time()
        model = DguardModel(
            embedding_model_names=[
                "dguard_sv_r101_cjsd8000_split_lm",
                "dguard_sv_r152_cjsd8000_split_lm",
                "dguard_sv_r293_cjsd8000_split_lm",
            ],
            device=dguard_device,
            length=-1,  # 每个片段10秒
            channel=0,  # 选择第一个通道
            max_split_num=5,  # 最多分割5个片段
            start_time=0,  # 每个音频从0秒开始处理
            mean=False,  # 返回所有片段特征的平均值
            verbose=False,  # 输出详细日志,默认在DGUARD_MODEL_PATH/logs/%Y%m%d-%H%M%S.log
            apply_vad=False,  # 声纹编码前自动应用VAD
            vad_smooth_threshold=0.25,  # VAD处理的平滑阈值,两个语音段之间的间隔小于该值时合并
            vad_min_duration=0.3,  # VAD处理的最小语音段持续时间,平滑后的语音段小于该值时被丢弃
            save_vad_path=None,  # 不自动保存VAD结果
            diar_num_spks=5,
            diar_min_num_spks=1,
            diar_max_num_spks=10,
            diar_min_duration=0.3,
            diar_window_secs=1.5,
            diar_period_secs=0.75,
            diar_frame_shift=10,
            diar_batch_size=4,  # 聚类时进行子片段声纹编码的批处理大小
            diar_subseg_cmn=True,
        )
        end_time = time.time()
        dguard_time = end_time - start_time
        print_step(
            f"Dguard Model Init Time: {dguard_time:.2f}s on {dguard_device}",
        )
        result.append(
            [
                f"Dguard_{dguard_device}_init",
                f"{dguard_time:.2f}",
                dguard_device,
                "Success",
                "/",
            ]
        )
    except Exception as e:
        print_step("Dguard Model Init failed", status="Failed", style="bold red")
        result.append(["Dguard_init", "/", "cuda", "Failed", str(e)])

    try:
        start_time = time.time()
        r = model.encode(test_audio["SPK_zh"])
        end_time = time.time()
        print_step(f"Dguard Model Encode Time: {end_time-start_time:.2f}s")
        rtf_encode = (end_time - start_time) / audio_lengths["SPK_zh"]
        result.append(
            [
                f"Dguard_{dguard_device}_encode",
                f"{end_time - start_time:.2f}",
                dguard_device,
                "Success",
                f"RTF: {rtf_encode:.4f}",
            ]
        )
    except Exception as e:
        print_step("Dguard Model Encode failed", status="Failed", style="bold red")
        result.append(["Dguard_{device}_encode", "/", dguard_device, "Failed", str(e)])

    try:
        start_time = time.time()
        r = model.diarize(test_audio["DIA_zh_1c2p"])
        end_time = time.time()
        print_step(f"Dguard Model Diarize Time: {end_time-start_time:.2f}s")
        rtf_diarize = (end_time - start_time) / audio_lengths["DIA_zh_1c2p"]
        result.append(
            [
                f"Dguard_{dguard_device}_diarize",
                f"{end_time - start_time:.2f}",
                dguard_device,
                "Success",
                f"RTF: {rtf_diarize:.4f}",
            ]
        )
    except Exception as e:
        print_step("Dguard Model Diarize failed", status="Failed", style="bold red")
        result.append(["Dguard_{device}_diarize", "/", dguard_device, "Failed", str(e)])

    try:
        start_time = time.time()
        r = model.file_similarity(test_audio["DIA_zh_1c2p"], test_audio["DIA_zh_2c2p"])
        end_time = time.time()
        print_step(f"Dguard Model File Similarity Time: {end_time-start_time:.2f}s")
        rtf_similarity = (end_time - start_time) / (
            audio_lengths["DIA_zh_1c2p"] + audio_lengths["DIA_zh_2c2p"]
        )
        result.append(
            [
                f"Dguard_{dguard_device}_file_similarity",
                f"{end_time - start_time:.2f}",
                dguard_device,
                "Success",
                f"RTF: {rtf_similarity:.4f}",
            ]
        )
    except Exception as e:
        print_step(
            "Dguard Model File Similarity failed", status="Failed", style="bold red"
        )
        result.append(
            ["Dguard_{device}_file_similarity", "/", dguard_device, "Failed", str(e)]
        )

# Mos Health Check
for mos_device in ["cpu", "cuda"]:
    try:
        start_time = time.time()
        mos_model = DguardMos()
        end_time = time.time()
        mos_time = end_time - start_time
        print_step(f"Dguard Mos Init Time: {mos_time:.2f}s on {mos_device}")
        result.append(
            [
                f"Mos_{mos_device}_init",
                f"{mos_time:.2f}",
                mos_device,
                "Success",
                "/",
            ]
        )
    except Exception as e:
        print_step("Mos Init failed", status="Failed", style="bold red")
        result.append(["Mos_init", "/", mos_device, "Failed", str(e)])

    try:
        start_time = time.time()
        r = mos_model.dnsmos(test_audio["SPK_zh"])
        end_time = time.time()
        print_step(f"Dguard Mos Time: {end_time-start_time:.2f}s")
        mos_rtf = (end_time - start_time) / audio_lengths["SPK_zh"]
        result.append(
            [
                f"Mos_{mos_device}_infer",
                f"{end_time - start_time:.2f}",
                mos_device,
                "Success",
                f"RTF: {mos_rtf:.4f}",
            ]
        )
    except Exception as e:
        print_step("Mos Infer failed", status="Failed", style="bold red")
        result.append(["Mos_infer", "/", mos_device, "Failed", str(e)])

# ASV Health Check
for device in ["cpu", "cuda"]:
    asv = DguardASV(device=device)
    for language, audio_file in test_audio.items():
        if "ASV" in language:
            try:
                asv_start = time.time()
                DF_result = asv.infer(audio_file)
                asv_time = time.time() - asv_start
                asv_rtf = asv_time / audio_lengths[language]
                print_step(f"ASV Infer Time: {asv_time:.2f}s on {device}")
                result.append(
                    [
                        f"ASV_{device}_infer_{language}",
                        f"{asv_time:.2f}",
                        device,
                        "Success",
                        f"RTF: {asv_rtf:.4f}",
                    ]
                )
            except Exception as e:
                print_step(
                    f"ASV Infer on {device} failed", status="Failed", style="bold red"
                )
                result.append(
                    [
                        f"ASV_{device}_infer_{language}",
                        "/",
                        device,
                        "Failed",
                        str(e),
                    ]
                )


# Print results in a table
print_results_table(result)

# Additional tests can be added here following the same pattern
# ...
