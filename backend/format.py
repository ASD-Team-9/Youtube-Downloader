def update_video_args(format: str, quality: str, other_args=[]) -> list[str]:
      args = ["-f"]
      match format:
          case "mp4":
              match quality:
                  case "highest":
                      args.append("-bestvideo")
                  case "medium":
                      args.append("136")
                  case "low":
                      args.append("135")
                  case "lowest":
                      args.append("160")
          case "m4a":
              args.append("140" if quality == "highest" else "139")
          case "mp3":
              match quality:
                  case "highest" | "medium":
                      args += ['ba' , '-x' ,'--audio-format', 'mp3']
                  case "low" | "lowest":
                      args += ['wa', '-x', '--audio-format', 'mp3']
      return other_args + args