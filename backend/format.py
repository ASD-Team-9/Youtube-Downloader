def update_video_args(format: str, quality: str, other_args=[]) -> list[str]:
    "Update video arguements for ytdlp"
    args = []
    match format:
        case 'best video':
            args = ["-f", "bv+ba/b"]
        case 'best audio':
            args = ["-x"]
        case "webm":
            args = ["-f"]
            match quality:
                case "highest":
                    args += ["webm"]
                case "lowest":
                    args += ["wv*[ext=webm]+wa/w"]
        case "mp4":
            args = ["-f"]
            match quality:
                case "highest":
                    args += ["bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]", "/", "bv*+ba/b"]
                case "medium":
                    args += ["bv*[ext=mp4]+[height<=480]+ba/b[height<=480]", "/" , "wv*+ba/w"]
                case "low":
                    args += ["bv*[ext=mp4]+[height<=360]+ba/b[height<=360]",  "/", "wv*+ba/w"]
                case "lowest":
                #   args.append("bv*[ext=mp4]+[height<=144]+ba/b[height<=144] / wv*+ba/w")
                    args += ["wv*[ext=mp4]+wa/w"]
        case "m4a":
            # args.append("140" if quality == "highest" else "139")
            args += ['-x', '--audio-format', 'm4a']
            args += get_audio_quality(quality)
        case "mp3":
            args += ['-x', '--audio-format', 'mp3']
            args += get_audio_quality(quality)
    return other_args + args

def get_audio_quality(quality: str):
    "Get audio quality arguements"
    match quality:
        case "highest":
            args += ['--audio-quality', '0']
        case "medium":
            args += ['--audio-quality', '5']
        case "low":
            args += ['--audio-quality', '8']
        case "lowest":
            args += ['--audio-quality', '10']