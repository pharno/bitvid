from fractions import Fraction
import json
import subprocess
import traceback
from shared import sentry

class Media:

    def __init__(self, source_file):
        self.source_file = source_file

    def get_info_as_dict(self):
        cmd = [
            'avprobe',
            '-v',
            'quiet',
            '-of',
            'json',
            '-show_format',
            '-show_streams',
            self.source_file]

        print " ".join(cmd)
        try:
            raw_data = json.loads(subprocess.check_output(" ".join(cmd),shell=True))
            if "streams" not in raw_data:
                raise ValueError("Not a Video")
        except subprocess.CalledProcessError as ex:
            traceback.print_exc()
            sentry.captureException()

            raise ValueError("Not a Video")

        return raw_data

    def is_video(self):
        data = self.get_info_video()
        return data and "duration" in self.get_info_video().keys()

    def get_info_audio(self):
        info = self.get_info_as_dict()
        stream = None
        for item in info['streams']:
            if item['codec_type'] == 'audio':
                stream = item
                break
        if not stream:
            return None
        duration = round(stream['duration'])
        file_size = int(info['format']['size'])
        sample_rate = int(stream['sample_rate'])
        bit_depth = int(stream['bits_per_sample'])
        channels = int(stream['channels'])
        return {'duration': duration,
                'file_size': file_size,
                'sample_rate': sample_rate,
                'bit_depth': bit_depth,
                'channels': channels}

    def get_info_video(self):
        info = self.get_info_as_dict()
        stream = None
        for item in info['streams']:
            if item['codec_type'] == 'video' and "bit_rate" in item.keys():
                stream = item
                break
        if not stream:
            raise ValueError("Not a Video")

        duration = float(stream['duration'])
        file_size = float(info['format']['size'])
        width = int(stream['width'])
        height = int(stream['height'])
        codec = stream['codec_name']
        aspect_ratio = str(width / height)
        # framerate = float(Fraction(stream['r_frame_rate']))
        return {'duration': duration,
                'file_size': file_size,
                'width': width,
                'height': height,
                'codec': codec,
                'aspect_ratio': aspect_ratio}  # ,
        #        'framerate': framerate}
