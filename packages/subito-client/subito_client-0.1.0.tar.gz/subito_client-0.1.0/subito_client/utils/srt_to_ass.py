import pysubs2

def srt_to_ass_using_template(srt_file_path, template_ass_path, output_ass_path="output.ass"):
    """
    Converts an input SRT file (e.g. translated subtitles) to ASS format using a template ASS file.
    Assumes the number of dialogues in SRT matches the template ASS file.
    
    Parameters:
      srt_file_path (str): Path to input SRT file
      template_ass_path (str): Path to template ASS file (with desired styles and settings)
      output_ass_path (str): Path for output ASS file (default: "output.ass")
      
    Returns:
      str: Path to output ASS file if successful, None otherwise
    """
    try:
        # Load SRT file
        srt_subs = pysubs2.load(srt_file_path, format="srt")
        
        # Load template ASS file
        template_ass = pysubs2.load(template_ass_path)
        
        # Verify dialogue count matches
        if len(srt_subs.events) != len(template_ass.events):
            print("Number of lines in SRT and template ASS files do not match!")
            return None
        
        # Transfer SRT texts to template ASS
        for i, event in enumerate(template_ass.events):
            # Replace ASS dialogue text with corresponding SRT text
            event.text = srt_subs.events[i].text
        
        # Save final ASS file
        template_ass.save(output_ass_path, format="ass")
        return output_ass_path
    except Exception as e:
        print("Error converting SRT to ASS:", e)
        return None

# Usage example:
if __name__ == "__main__":
    srt_file = r"C:\Users\Mohammad ebrahimi\Downloads\Compressed\Solo Leveling_2x07_WEB.AMZN.en\fa - Solo Leveling - 2x07 - The 10th S-rank Hunter.WEB.AMZN.en---.srt"
    template_ass_file = r"C:\Users\Mohammad ebrahimi\Downloads\Compressed\Solo Leveling_2x07_WEB.AMZN.en\Solo Leveling - 2x07 - The 10th S-rank Hunter.WEB.AMZN.en - Copy.ass"
    output_file = srt_to_ass_using_template(srt_file, template_ass_file, "final_output.ass")
    if output_file:
        print("Final ASS file successfully created:", output_file)
