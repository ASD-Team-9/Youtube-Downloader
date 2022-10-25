"Backend of getting the format"

def update_video_args(video_format: str, quality: str) -> list[str]:
    "Update video arguments for ytdlp (video format, quality)"
    args = []
    match video_format:
        case 'Best Video + Audio':
            args = ["-f", "bestvideo+best+bestaudio", "--video-multistreams", "--audio-multistreams"]
        case 'Best Video':
            args = ["-f", "bv+ba/b"]
        case 'Best Audio':
            args = ["-x"]
        case "webm":
             args = ["-f"]
             match quality:
                 case "Highest" | "Normal":
                     args += ["bv[ext=webm]+ba"]
                 case "Lowest":
                     args += ["wv[ext=webm]+wa"]
        case "mp4":
            args = ["-f"]
            match quality:
                case "Highest":
                    args += ["bv[ext=mp4]+ba[ext=m4a]"]
                case "Normal":
                    args += ["bv[ext=mp4][width=480]+ba[ext=m4a]"]
                case "Lowest":
                    args += ["wv[ext=mp4]+wa[ext=m4a]"]
        case "mp3":
            args += ['-x', '--audio-format', 'mp3']
            match quality:
                case "Highest":
                    args += ['--audio-quality', '0']
                case "Normal":
                    args += ['--audio-quality', '5']
                case "Lowest":
                    args += ['--audio-quality', '10']
        case "m4a":
             args += ['-x', '--audio-format', 'm4a']
             match quality:
                case "Highest":
                    args += ['--audio-quality', '0']
                case "Normal":
                    args += ['--audio-quality', '5']
                case "Lowest":
                    args += ['--audio-quality', '10']
    return args
