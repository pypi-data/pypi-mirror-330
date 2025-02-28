#!/usr/bin/python3
#MIT License
#
#Copyright (c) 2024 Rodolfo Guillermo Pregliasco

import sys
import markdown
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
import datetime as dt
import re
from pathlib import Path
import shutil
from importlib import resources
from .animation import Animation

SIGNATURE = "Willy Pregliasco, 10/2024."
PATH_CWD  = Path.cwd()
OUT_DIR = PATH_CWD / "resources"
CSS_OUT = OUT_DIR  / "anima_build.css"

def copy_files():
        
        # directory
        OUT_DIR.mkdir(parents=True, exist_ok=True)

        # clean css
        if CSS_OUT.exists():
            CSS_OUT.unlink()
        # populate if not exists
        if not (OUT_DIR / 'md.css').exists():
            md_css = resources.files('markdown_scrolly') / 'resources/md.css'
            shutil.copy(md_css, OUT_DIR)

        if not (OUT_DIR / 'anima_base.css').exists():    
            anima_base_css = resources.files('markdown_scrolly') / 'resources/anima_base.css'
            shutil.copy(anima_base_css, OUT_DIR)

        if not (OUT_DIR / 'anima.js').exists():
            anima_js = resources.files('markdown_scrolly') / 'resources/anima.js'
            shutil.copy(anima_js, OUT_DIR)

def append_css_build(txt):
    with open(CSS_OUT, 'a') as f:
            f.write(txt)

class AnimationBlockExtractor(Preprocessor):
    def run(self, lines):
        inside_animation_block = False
        animation_block = []
        new_lines = []
        animation_block_index = 1

        #output directory
        copy_files()

        # Loop through each line and check for markers
        for line in lines:
            # Start capturing when we encounter [animation: texts]
            match = re.match(r'^\s*\[animation:\s*texts\]', line)
            if match and not inside_animation_block:
                inside_animation_block = True
                continue

            # Stop capturing when we encounter [animation: end]
            if re.match(r'^\s*\[animation:\s*end\]', line):
                inside_animation_block = False

                # Process the captured animation block into HTML
                animation = Animation(animation_block, animation_block_index) 
                processed_block = self.process_animation_block(animation)

                new_lines.append(processed_block)
                animation_block = []  # Clear the animation block after processing
                animation_block_index += 1
                continue

            # If we are inside the animation block, store the line
            if inside_animation_block:
                animation_block.append(line)
            else:
                new_lines.append(line)

        return new_lines
    
    def process_animation_block(self, animation):
        """
        This function generates HTML from the extracted animation block.
        Modify it to fit your custom HTML output needs based on the block_type.
        """

        append_css_build(animation.css)

        return animation.html

class AnimationExtractorExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(AnimationBlockExtractor(md), 'animation_extractor', 45)

class SectionTreeprocessor(Treeprocessor):
    def run(self, root):
        new_elements = []     # To store the results
        section_content = []  # Track content of the current section
        i_section = 0
        i_subsection = 1

        for elem in root:
            if elem.tag in ['h2']:  # New section begins
                # Numerate section
                i_section+=1
                i_subsection = 1
                elem.text = f"{i_section}. {elem.text}"
                
                # If there's a previous section, process it
                if section_content != []:
                    #print('section_content:\n', section_content, end = '\n'+'-'*70+'\n')
                    ID = f"section_{i_section-1:02d}"
                    if i_section == 1:
                        ID='header'
                    self.process_section(section_content, new_elements, id=ID)
                # Reset for new section
                section_content = [elem]

            elif elem.tag in ['h3']:  # Numerate subsection
                elem.text = f"{i_section}.{i_subsection} {elem.text}"
                i_subsection+=1
                section_content.append(elem)
            else:
                # Add elements to the current section content
                section_content.append(elem)

        # Process the last section
        if section_content != []:
            self.process_section(section_content, new_elements, id=f"section_{i_section:02d}")

        # Add signature
        sign = Element('p', {'class': 'signature'})
        sign.text = SIGNATURE
        new_elements[-1].append(self.enclose_item(sign))
        
        # Clear the root and insert the new elements
        root.clear()
        root.extend(new_elements)

    def enclose_item(self, item, wbox_only=False):
        wbox = Element('div', {'class':'wbox'})
        tbox = Element('div', {'class':'tbox'})
        if wbox_only:
            tbox = item
        else:
            tbox.append(item)
        wbox.append(tbox)
        return wbox


    def process_section(self, section_content, new_elements, id=''):
        """Process a section's content 
                * handle adding/replacing <hr>
                * head section
        """

        #### header handler
        if section_content[0].tag == 'h1':
            for item in section_content[1:]:
                item.set('class', 'header')

        #### hr handler
        has_hr = False
        # Check if the last element in the section is an <hr>
        if len(section_content) > 0 and section_content[-1].tag == 'hr':
            # Replace the existing <hr> with the custom one
            section_content[-1] = Element('hr', {'class': 'sectionrule'})
            has_hr = True
        
        # If no <hr> was found, add a custom <hr> at the end
        if not has_hr and section_content[0].tag != 'h1':
            section_content.append(Element('hr', {'class': 'sectionrule'}))

        # Add all section elements to the new_elements list
        # Enclose root elements in div class="tbox"
        # Enclose section in div class="section" id="section_0x"
        root_elements = ['h1','h2','h3','h4','h5','h6',
                         'hr', 'p', 'blockquote', 'ul', 'ol' ]
        enclosed_elements = Element('div', {'class':'section','id':id})

        for item in section_content:
            if item.tag in root_elements:
                enclosed_elements.append(self.enclose_item(item))
            elif item.tag in ['table']:
                enclosed_elements.append(self.enclose_item(item, wbox_only=True))
            else:
                enclosed_elements.append(item)
                
        new_elements.append(enclosed_elements)
        
class SectionExtension(Extension):
    def extendMarkdown(self, md):
        # Register the treeprocessor with the markdown parser
        md.treeprocessors.register(SectionTreeprocessor(md), 'section', 35)

class imgExtractor(Preprocessor):
    def run(self, lines):
        new_lines = []
        graph_block = []
        inside_graph_block = False
        graph_type = '30'
        i_graph = 1
        i_subgraph = 1

        # Loop through each line and check for images & styles
        pattern_style = r"\[\s*graph:\s*(?P<content>.*?)\]"
        pattern_graph = r'!\[(?P<alt_text>.*?)\]\((?P<filename>.*?)\)(?:\{(?P<optional>.*?)\})?'

        for line in lines:
            # If the line have a graph_style, capture it
            match_style = re.match(pattern_style, line)
            if match_style:
                graph_type = match_style.group("content").strip()
                continue
            
            # Start capturing when we encounter an image
            match = re.match(pattern_graph, line)
            if match:
                if not inside_graph_block:
                    inside_graph_block = True

                try: 
                    style = match.group("optional").strip()
                except:
                    style = None
                fdata = {'i'      : int(i_graph),
                         'j'      : int(i_subgraph),
                         'type'   : graph_type,
                         'caption': match.group("alt_text").strip(),
                         'fname'  : match.group("filename").strip(),
                         'style'  : style,
                        }
                i_subgraph +=1

                graph_block.append(fdata)

            else:
                if inside_graph_block:
                    # end block
                    graph = self.process_graph_block(graph_block)
                    new_lines.append(graph)
                    i_graph   += 1
                    i_subgraph = 1
                    inside_graph_block = False
                    graph_block = []
                else:
                    new_lines.append(line)

        return new_lines
    
    def process_graph_block(self, gblock):
        out = Element('div', {'class':'graph'})
        for fig in gblock:

            caption = fig['caption']
            fname   = fig['fname']
            style   = fig['style']

            try:
                h = int(fig['type'])
            except: 
                h = None
            if h is not None:
                if style is not None and not style.endswith(';'):
                    style += ';'
                elif style is None:
                    style = ''
                style += f'height:{h}vh;' 

            f = Element('figure')
            if style is None:
                f.append(Element('img', {'src':fname}))
            else:
                f.append(Element('img', {'src':fname, 'style':style}))

            if caption !='':
                tx = Element('figcaption', {'class':'caption'})
                sr = SubElement(tx, 'span', {'class':'source'})
                sr.text = ' '
                br = SubElement(tx, 'br')

                if '|' in caption:
                    source, fcaption = caption.split('|')
                    source, fcaption = source.strip(), fcaption.strip()    
                    if source != '':
                        sr.text = source
                    if fcaption != '':
                        br.tail = fcaption
                else:
                    br.tail = caption

                f.append(tx)

            out.append(f)

        return ET.tostring(out, encoding='unicode')
        
class ImgExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(imgExtractor(md), 'img_extractor', 35)

# Function to remove wbox and tbox while preserving animation content
def unwrap_animation_containers(root):
    # Find all wbox elements that contain animations
    for wbox in root.findall(".//div[@class='wbox']"):
        # Check if this wbox contains an animation div at any depth
        animation = wbox.find(".//div[@class='animation']")
        if animation is not None:
            # Get the direct parent of the animation div
            parent = None
            for elem in wbox.iter():
                for child in elem:
                    if child is animation:
                        parent = elem
                        break
                if parent:
                    break
            
            if parent and parent != wbox:
                # Remove the animation from its current parent
                parent.remove(animation)
            
            # Replace wbox content with animation content
            wbox.clear()  # Clear the wbox element
            wbox.tag = "div"  # Keep it a div
            wbox.attrib = animation.attrib  # Copy animation's attributes
            wbox.text = animation.text  # Copy animation's text
            wbox.extend(animation)  # Move over animation's children

# Function to remove tbox while preserving graph content
def unwrap_graph_containers(root):
    # Find all <div class="wbox"> elements
    for wbox in root.findall(".//div[@class='wbox']"):
        # Locate <div class="tbox"> inside <div class="wbox">
        tbox = wbox.find(".//div[@class='tbox']")
        if tbox is not None:
            # Locate <div class="graph"> inside <div class="tbox">
            graph = tbox.find(".//div[@class='graph']")
            if graph is not None:
                # Replace wbox content with graph content
                tbox.clear()  # Clear the wbox element
                tbox.tag = "div"  # Keep it a div
                tbox.attrib = graph.attrib  # Copy graph's attributes
                tbox.text = graph.text  # Copy graph's text
                tbox.extend(graph)  # Move over graph's children

# Function to convert Markdown to HTML
def convert_markdown(md_text, extensions=[]):
    out_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{}</title>
    <link rel="stylesheet" href="resources/md.css">
    <link rel="stylesheet" href="resources/anima_base.css">
    <link rel="stylesheet" href="resources/anima_build.css">
</head>
'''

    out_post = '''
</html>
'''

    md = markdown.Markdown(extensions=[SectionExtension(), 
                                       AnimationExtractorExtension(), 
                                       ImgExtension(), 
                                       'extra'] + extensions)

    out_body = '<body>\n' + \
                md.convert(md_text) +\
                '\n<script src="resources/anima.js"></script>' +\
                '\n</body>\n'
    
    body_et = ET.fromstring(out_body)
    
    unwrap_animation_containers(body_et)
    unwrap_graph_containers(body_et)
    for h1 in body_et.iter('h1'):
        break
    title = h1.text.strip()
    body_str = ET.tostring(body_et, encoding='unicode')
    # explicit closing of tags    
    body_str = re.sub(r"<(?!br\b)(\w+)([^>]*)\s*/>", r"<\1\2></\1>", body_str)


    out = out_head.format(title) + body_str + out_post

    return out

def convert_file_markdown(fname, signature='', date='today', extensions=[]):
    global SIGNATURE

    if date == 'today':
        date = f'{dt.datetime.now().month:02d}/{dt.datetime.now().year}'
    if signature.strip() != '':
        SIGNATURE = f"{signature.strip()}, {date}."
    else:
        SIGNATURE = f"{date}."

    # read input                    
    with open(fname, 'rt') as f:
        text_md = f.read()
    # convert
    out = convert_markdown(text_md, extensions=extensions)
    # write output
    fout = '.'.join(fname.split('.')[:-1]) + '.html'
    with open(fout, 'wt') as f:
        f.write(out)

    print('Done.')

if __name__ == "__main__":
  fname = sys.argv[1]
  convert_file_markdown(fname)