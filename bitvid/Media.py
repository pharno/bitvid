from fractions import Fraction
import json
import subprocess


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
        raw_data = subprocess.check_output(cmd)
        return json.loads(raw_data.decode())

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
            if item['codec_type'] == 'video':
                stream = item
                break
        if not stream:
            return None
        duration = float(stream['duration'])
        file_size = float(info['format']['size'])
        width = int(stream['width'])
        height = int(stream['height'])
        codec = stream['codec_name']
        aspect_ratio = str(width / height)
        #framerate = float(Fraction(stream['r_frame_rate']))
        return {'duration': duration,
                'file_size': file_size,
                'width': width,
                'height': height,
                'codec': codec,
                'aspect_ratio': aspect_ratio}  # ,
        #        'framerate': framerate}
