import markdown
import sys



if len(sys.argv)!=3:
    print("Usage: python md_collapse_sections.py INPUT.md OUTPUT.html")
    sys.exit(-1)





def chop_sections(inp):
    """ 
    Given an input markdown string, chop this up into sections (simply take the
    highest header level and return the markdown for each section individually. 

    Arguments
    inp : list of strings where each element is a line from the Markdown file.

    Returns a string containing the HTML for the input Markdown.
    """

    inps = [ l.strip() for l in inp ]

    # Build a structure where each line is turned into a tuple (h,c)
    # where h is the header level (0 if this is not a header), c is the
    # contents (i.e. the header label itself or the contents of the line if not a header).
    headers = []
    for l in inps:
        # Determine the header level by looking at how many
        # string-initial pound characters we find
        lvl = 0
        while lvl<len(l)-1 and l[lvl]=="#": lvl+=1
        headers.append( (lvl,l[lvl:].strip()) )

    
    def chop(lines):
        """ 
        Turns markdown (with (header,content) structure) into html. This function is called recursively.
        
        Arguments
        lines : a list of (header,content) tuples (see above).

        Returns
        A string corresponding to the HTML output.
        """
        # Find the highest header level (i.e. the lowest nonzero number of pounds)
        hlvls = [ h for (h,_) in lines if h!=0 ]
        if len(hlvls)==0:
            # This doesn't have any header subsections, so nothing to do...
            src = "\n".join([ l for (_,l) in lines ])
            html = markdown.markdown(src)+"\n" #, ['outline'])
            return html
        maxhdr = min(hlvls)

        sections    = []   # we put all the contents per section
        buff        = []   # all the lines contained in the section we are currently building
        curr_header = ""   # the header of the section we are currently building
        for (h,c) in lines:
            if h==maxhdr: # if this is the level of header we are currently chopping at, chop!
                if len(buff)>0:
                    sections.append( (h,curr_header,chop(buff)) )
                curr_header = c
                buff        = []
            else:
                buff.append((h,c))
        if len(buff)>0:
            sections.append( (maxhdr,curr_header,chop(buff)) )

        # Now let's build the output, i.e. each header can be turned into a details-summary
        # tag structure.
        outp = ""
        for (hlvl,h,contents) in sections:
            if h!="":
                thissect =  "<details>"
                thissect += "<summary><span class=\"h%i\">%s</span></summary>\n"%(hlvl,h)
                thissect += contents+"\n"
                thissect += "</details>\n"
            else:
                thissect = contents+"\n"
                
            outp+=thissect
        return outp
        
    return chop(headers)
        
        
    

    

# Open the source file (regular markdown)
src = open(sys.argv[1],'r').readlines()

# Now go through the input file line by line
outp = chop_sections(src)

# Determine the output file
outfname = sys.argv[2]

# Write the output file
fout = open(outfname,'w')
fout.write("<html>\n")
fout.write("<head><meta charset=\"UTF-8\" /><style>\n")
fout.write("""
.h1 { font-size: 2em; color: blue}
.h2 { font-size: 1.5em; color: red }
.h3 { font-size: 1.17em; color: green }
.h4 { font-size: 1.12em; }
.h5 { font-size: .83em; }
.h6 { font-size: .75em; }
""")
fout.write("</style></head>\n")
fout.write("<body>%s</body>\n"%outp)
fout.write("</html>\n")
fout.close()

