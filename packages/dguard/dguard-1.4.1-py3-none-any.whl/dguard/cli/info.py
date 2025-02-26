# coding = utf-8
# @Time    : 2024-12-16  16:16:35
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Model INFO.
__version__ = '1.4.1'
VERSION = __version__


def main():
    m = f"""
---------------------------------------------------
██████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗
██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
██║  ██║██║  ███╗██║   ██║███████║██████╔╝██║  ██║
██║  ██║██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
██████╔╝╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
---------------------------------------------------
 Author    : LongYuan[Nanjing] VoiceCode[Singapore]
 Version   : {VERSION}
---------------------------------------------------
Usage:

# Example 1.1: Calculate similarity between two audio files by using two models
dguard --task similarity --audio_file test.wav --audio_file2 test.wav \
    --model_name dguard_sv_c,dguard_sv_e

# Example 1.2: Calculate similarity between two scp files by using two models
#             Scp file format: <utt_id1> <wav_path1> <utt_id2> <wav_path2>
dguard --task similarity_list --wav_scp test_sim.scp \
    --model_name dguard_sv_c,dguard_sv_e --output_file output.txt

# example output.txt:
#    test1&test2 dguard_sv_c:1.0000 dguard_sv_e:1.0000 mean_score:1.0000
#    test3&test4 dguard_sv_c:1.0000 dguard_sv_e:1.0000 mean_score:1.0000

# Example 2.1:Extract embedding from audio file by using two models
dguard --task embedding --audio_file test.wav \
    --model_name dguard_sv_c,dguard_sv_e

# Example 2.2:Extract embedding from scp file by using two models
#             Scp file format: <utt_id> <wav_path>
dguard --task embedding_list --wav_scp test.scp \
    --model_name dguard_sv_c,dguard_sv_e --output_file output.txt
# example output.txt:
#    test1 4.00-5.18,6.53-8.29
#    test2 3.00-3.18,7.53-9.29


# Example 3.1:Diarization from audio file by using one model
# (only support one model, Use the first model by default)
dguard --task diarization --audio_file test.wav --model_name dguard_sv_c

Notice:
1. Multiple models are separated by commas.
2. if you just want print result without any other information,\
      you can use `--clean_mode`
3. if you want save the result to a file, \
    you can use `--output_file <file_path>`
4. if you want to see the processing log, \
    you can use `--verbose`

"""
    print(m)
