import os
import re


def start_conversion(srt_path, vtt_path):
    try:
        srt_file = open(srt_path, 'r')
        vtt_file = open(vtt_path, 'w')
        srt_lines = srt_file.readlines()

        vtt_file.write('WEBVTT\n\n')
        for line in srt_lines:
            if line in ['\n', '\r\n']:
                vtt_file.write('\n')
            else:
                # print(h)
                match = re.match(r'[\d]{2}:[\d]{2}:[\d]{2},[\d]{3}', line)
                if match:
                    new_line_for_vtt = line.replace(',', '.').replace('\n', ' ').rstrip()
                    full = new_line_for_vtt + ' align:middle line:84%\n'
                    vtt_file.write(full)
                else:
                    vtt_file.write(line)
    except UnicodeDecodeError as e:
        print('Unable to read srt file.')
        print(e)
        vtt_file.close()
        os.remove(vtt_path)
    finally:
        srt_file.close()
        if os.path.isfile(vtt_path):
            vtt_file.close()

    return vtt_file


if __name__ == '__main__':
    start_conversion()
