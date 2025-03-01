import pysubs2

def convert_to_srt(input_file_path, output_file_path="output.srt"):
    """
    Converts any subtitle file format supported by pysubs2 to SRT format.
    
    Parameters:
      input_file_path (str): Path to input subtitle file.
      output_file_path (str): Path to output SRT file (default: "output.srt").
    
    Returns:
      str: Path to the saved SRT file.
    """
    try:
        # Load input subtitle file
        subs = pysubs2.load(input_file_path)
        # Save to SRT format
        subs.save(output_file_path, format="srt")
        return output_file_path
    except Exception as e:
        print("Error converting subtitle format:", e)
        return None
