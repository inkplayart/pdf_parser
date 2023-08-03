import os

def find_substring_indices(string, substring):
    indices = []
    index = -1  # Starting index for the find() method

    while True:
        index = string.find(substring, index + 1)
        if index == -1:
            break
        indices.append(index)

    return indices

def get_whole_section_indices(string,startString):
    startHeaders = find_substring_indices(string,"<h1>")
    endHeaders = find_substring_indices(string,"</h1>")

    startIndex = len(string)
    endIndex = 0
    
    for i in range(0,len(startHeaders)):
        header = string[startHeaders[i]+4:endHeaders[i]].strip()
        if header.startswith(startString):
            if startIndex > startHeaders[i]:
                startIndex = startHeaders[i]
            nextHeader = string[startHeaders[i+1]+4:endHeaders[i+1]].strip()
            if not nextHeader.startswith(startString):
                endIndex = startHeaders[i+1]
                break
    return [startIndex,endIndex]

def remove_html_tags(string):
    stringLines = string.split("\n")
    outString = ""
    for ln in stringLines:
        if not ln.strip().startswith("<"):
            outString = outString + " " + ln
    return outString

for file in os.listdir("clean"):
    lines = ""
    user = file.split("_")[0].strip()
    with open(os.path.join("clean",file),'r') as reader:
        lines = reader.read().lower()
        
    indc = get_whole_section_indices(lines,"discussion")

    section = lines[indc[0]:] #we don't care about the ending tags, we just want the discussion part
    with open(os.path.join("clean",user+"_discussion.txt"),"w") as writer:
        writer.write(section)