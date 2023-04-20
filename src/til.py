from devrev import DevrevAPI
from transcribe import YoutubeTranscribe
import sys

def main():
    if len(sys.argv) > 3:
        print("Too many inputs. Please provide id and feature name")
        return
    elif len(sys.argv) < 2:
        print("video id not provided")
        return
    elif len(sys.argv) == 3 :
        feat = str(sys.argv[2])
    else:
        print("Feature not provided, setting default Uncategorized")
        feat = "Uncategorized"
    vid = str(sys.argv[1])
    yt = YoutubeTranscribe(vid)    
    til = yt.prepare_til()
    dr_api = DevrevAPI(feat)
    dr_api.print_work_id()
    #dr_api.setup()
    dr_api.create_comment(til)

if __name__ == "__main__":
    main()

