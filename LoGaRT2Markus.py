import os
import sys
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='ArgParser')
    parser.add_argument("--file", dest="input_file", required=True,
                        help="path to a LoGaRT file")
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    return args

def generate_ramdon_html_color_code():
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_number = '#' + hex_number[2:]
    return hex_number

def LoGaRT2Markus(args):
    input_file = args.input_file
    filename = "markus-" + os.path.splitext(os.path.basename(input_file))[0]+".html"

    with open('tags.txt', encoding="utf-8") as fi:
        tags = fi.readlines()

    tag_def_string_list = []
    for tag in tags:
        tag = tag.strip()
        hex_number = generate_ramdon_html_color_code()
        per_tag_string = f'''&quot;{tag}&quot;:{{&quot;color&quot;:&quot;{hex_number}&quot;,&quot;buttonName&quot;:&quot;{tag}&quot;,&quot;visible&quot;:true,&quot;status&quot;:&quot;bordered&quot;}}'''
        tag_def_string_list.append(per_tag_string)
    tag_def_string = ",".join(tag_def_string_list)

    header=f'''<div class="doc" markupfullname="false" markuppartialname="false" markupnianhao="false" markupofficaltitle="false" markupplacename="false" filename="{filename}" tag="{{{tag_def_string}}}"><pre contenteditable="false" dir="ltr">'''
    end = "</pre></div>"
    content = ""
    content += header

    line_count = 0
    with open(input_file, encoding="utf-8") as fi:
        lines = fi.readlines()
        for line in lines:
            new_line = ""
            line_start =f'''<span class="passage" type="passage" id="passage{line_count}"><span class="commentContainer" value="[]"><span class="glyphicon glyphicon-comment" type="commentIcon" style="display:none" aria-hidden="true" data-markus-passageid="passage{line_count}"></span></span>'''
            line_end = f'''</span>'''
            for tag in tags:
                tag = tag.strip()
                line = line.replace(f"<{tag}>", f'''<span class="markup manual unsolved {tag}" type="{tag}" {tag}_id="">''')
                line = line.replace(f"</{tag}>", "</span>")
            new_line += line_start + line + line_end
            line_count += 1
            content += new_line + "\n"

    content += end

    with open(filename, "w+", encoding="utf-8") as f:
        f.write(content)
    print(f"Finished writing Markus result to:{filename}")

def main():
    args = parse_args()
    LoGaRT2Markus(args)

if __name__ == '__main__':
    main()