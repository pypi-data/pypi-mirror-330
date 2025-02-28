# 
import re
import markdown
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from PIL import Image as PILImage

class Animation():

    texts = None
    index = None

    def __init__(self, block, index):
        ''' block: list of lines as strings
            index: index of animation (start=1)
        '''
        self.index = index
        # separate blocks
        blocks = self.separate_blocks(block)

        # load
        self.texts  = Texts (blocks['texts' ])
        self.images = Images(blocks['images'])
        self.script = Script(blocks['script'])

    def separate_blocks(self, block):
        """
        Returns the three blocks separated in dict
        with keys: 'texts', 'images', 'script'
        """
        out = {}
        i=0
 
        # texts
        for i,line in enumerate(block):
            if re.match(r'^\s*\[animation:\s*images\]', line):
                break
        itext = i
        out['texts'] = block[:itext]
        
        # images
        for i,line in enumerate(block[itext+1:]):
            if re.match(r'^\s*\[animation:\s*script\]', line):
                break
        iimage = i+itext+1
        out['images'] = block[itext+1:iimage]

        # script
        out['script'] = block[iimage+1:]
        return out
    
    def get_text_scripts(self):
        '''return text scripts with texts replaced by html string'''
        out = self.script.get_texts()
        
        for item in out:
            text_id = item['text']
            item['text'] = self.texts.texts[text_id-1]
        return out


    @property
    def html(self):
        '''output to html string'''

        animation_id = f'{self.index:02d}'
        # spacer def
        spacer = Element('div', {'class':'spacer'})

        # container ET
        out = Element('div', {'class': 'animation', 'id': f'animation_{animation_id}'})
        wrap= Element('div', {'class': 'back-wrapper'})

        # images
        back_container = Element('div', {'class': 'back_container'})
        for i, img in enumerate(self.images.images, start=1):
            file_id = f'{i:02d}'
            back_container.append(Element('div', {'class':'back', 'id':f'bg_{animation_id}_{file_id}'}))
        out.append(back_container)

        #if self.script.startsin:
        out.append(spacer)
            
        # sorted text blocks
        i_script = 0
        scripts = self.get_text_scripts()
        pages_txt = [int(s['page']) for s in scripts]

        for page in range(1, self.script.lastpage+1):
            if page in pages_txt:
                i_text = [i  for i,s in enumerate(scripts) if int(s['page'])==page][0]
                script = scripts[i_text]
                page_container = Element('div', {'class':'page_container'})

                txt_html = f'<div class="text_container" style="{script["text_props"]}">' + \
                           script['text'] + \
                           '</div>'
                
                txt_et = ET.fromstring(txt_html)              
                page_container.append(txt_et)
                outpage = page_container
                i_script += 1
            else:
                outpage = spacer

            out.append(outpage)

        return ET.tostring(out, encoding='unicode')

    @property    
    def css(self):
        out = ''
        animations = ''
        animation_id = f'{self.index:02d}'

        scripts = self.script.get_imgs()

        
        for i, img in enumerate(self.images.images):
            pimg = PILImage.open(img[3:])
            width, height = pimg.size
            file_id = f'{i+1:02d}'
            script = scripts[i]

            # image css
            img_css = f'''#bg_{animation_id}_{file_id} {{
    background-image: url('{img}');
    width: {width}px;
    height: {height}px;
    animation: animation_{animation_id}_{file_id} 100s linear;
    animation-delay: calc(var(--scroll_{animation_id}) * -1s);
    animation-iteration-count: 1;
    animation-fill-mode: both;
    animation-play-state: paused;
}}       

'''
            out += img_css[:]

            # animation css
            kframes_css = f'@keyframes animation_{animation_id}_{file_id}{{\n' 

            for kframe in script: 
                kframes_css += f'\t{kframe["percent"]} {{\n'
                for item in kframe["transform"].split(';'):
                    kframes_css += f'\t\t{item};\n'
                kframes_css += '\t}\n'
            kframes_css += '}\n\n'

            animations += kframes_css

        return out + animations

##########################################################
class Texts():

    texts = []

    def __init__(self, textblock):
        self.texts = self.load(textblock)
        self.texts = self.to_html()

    def load(self, texts):
        '''Loads a textblock (list of line strings)
           Returns a list of texts
        '''
        out = []
        buffer = []
        loading_buffer = False

        for line in texts:
            match = re.match(r'^\d{1,2}\.\s*(.+)', line)
            if match:
                txt = match.group(1).strip()
                if not txt.strip().startswith("```"):
                    out.append(txt)
                else:
                    loading_buffer = True
            else:
                if loading_buffer:
                    if not line.strip().startswith("```"):
                        buffer.append(line)
                    else:
                        if buffer != []:
                            out.append('\n'.join(buffer))
                            buffer=[]
                            loading_buffer = False

        return out
    
    def to_html(self):
        '''convert texts md strings to html strings
           without container
        '''
        out = []
        for txt in self.texts:
            txt_html = markdown.markdown(txt, extensions=['extra'])
            out.append(txt_html)

        return out

##########################################################
class Images():

    images = []

    def __init__(self, imageblock):
        
        self.images = self.load(imageblock)

    def load(self, images):
        '''Loads a imageblock (list of line strings)
            Returns a list of images paths
        '''

        out = []

        for line in images:
            match = re.match(r'^\d{1,2}\.\s*(.+)', line)
            if match:
                img = match.group(1).strip()
                # set to root directory
                if img.startswith('./'):
                    img = img[2:]
                elif img.startswith(('.','/')):
                    img = img[1:]
                
                out.append(f"../{img}")

        return out

##########################################################    
class Script():

    script = []
    lastpage = 0
    endpage  = 0
    startsin = False
    pars = {'delta': 0.15,
            'page_factor': 1.2}

    def __init__(self, scriptblock):
        
        self.script = self.load(scriptblock)
        self.lastpage = self.set_lastpage()

        self.load_text_props()
        self.set_startsin()

    def load(self, script):
        '''Loads a script (list of line strings with a table)
            Returns a list of script dictionaries
                keys: page(float), text(int), text_props(str), transform(str)
        '''

        out = []
        itable = 0
        for line in script:
            line = line.strip()
            if line.startswith('|'):
                if itable < 2:
                    itable += 1
                else:
                    line = line[1:-1].split('|')
                    dic = {
                        'page': float(line[0].strip()),
                        'text': line[1].strip(),
                        'text_props': line[2].strip(),
                        'transform' : [item.strip() for item in line[3:]]
                    }
                    
                    if dic['text'] == '':
                        dic['text'] = 0
                    else:
                        dic['text'] = int(dic['text'])
                    
                    out.append(dic)

        return out
    
    def set_lastpage(self):
        return int(max([item['page'] for item in self.script]))
    
    def set_startsin(self):
        self.startsin = self.script[0]['transform'][0].strip().startswith('in')
    
    def load_text_props(self):
        '''reads the text in text_props
           outputs a string with style declaration
        '''
        out = []
        for item in self.script:
            if item['text'] == 0:
                item['text_props'] = None
            else:
                # separate fields
                text_props = item['text_props']
                text_props = [item.strip() for item in text_props.split()]
                # check if blank or ends in %
                tmp = []
                color = None
                for p in text_props:
                    if p == '':
                        continue
                    
                    if p.endswith('%'):
                        p = p[:-1]

                    if p.isnumeric():
                        tmp.append(int(p))
                    else:
                        color = p
                    
                if len(tmp) != 0:
                    if len(tmp) == 1:
                        width, left, top = tmp[0], 10, 0 
                    elif len(tmp) == 2:
                        width, left, top = tmp[0], tmp[1], 0
                    elif len(tmp) == 3:
                        width, left, top = tmp

                    page_float = item['page']
                    top += round((page_float % 1) * 100)
                    text_props = f'width:{width}%; margin: {top}vh auto auto {left}%;'
                else:
                    text_props = 'width:  800px; max-width: 90%; margin: 0 auto;'
                
                if color is not None:
                    text_props += f' background-color: {color};'    

                item['text_props'] = text_props

    def get_texts(self):
        out = []
        for item in self.script:
            if item['text'] > 0:
                out.append({'page': int(item['page']),
                            'text': item['text'],
                            'text_props': item['text_props']})

        if out != []:        
            out.sort(key= lambda x: x['page'])

        return out

    def get_imgs(self):
        '''return images scripts [script_img1, script_img2,...]'''
        script = self.script
        n_imgs = len(script[0]['transform'])
        out = []
        for i in range(n_imgs):
            out.append([])

        for key in script:
            for i in range(n_imgs):
                t = key['transform'][i].strip()
                if t.startswith(';'):
                    t = t[1:]
                if t.endswith(';'):
                    t = t[:-1]
                if t != '':
                    t_list = t.split(';')
                    t_list = [item.strip() for item in t_list if item.strip()!='']
                    out[i].append({'page':key['page'],
                                   'transform': t_list})
                    
        # process directives & percent animation            
        for i, outimg in enumerate(out):
            out[i] = self.process_transforms(outimg)
        return out
    
    def process_transforms(self, imagescript):
        '''loads: imagescript in the form script_img1
           returns: processed script with field 'percent'
        '''

        delta = self.pars['delta']
        page_factor = self.pars['page_factor']
        lastpage = self.lastpage
        total_vh = lastpage * page_factor + 1
        endpage  = lastpage + 1/page_factor
        self.endpage = endpage

        tmp = []

        ## verb transcription
        for kframe in imagescript:
            pg = kframe['page']
            tr = kframe['transform']
                
            ## Entradas in/on
            if 'in' in tr:
                tmp += self.verb_in(imagescript, kframe)
                continue

            if 'on' in tr:
                tmp += self.verb_on(imagescript, kframe)
                continue

            ## Salidas out/off
            if 'out' in tr:
                tmp += self.verb_out(imagescript, kframe)
                continue    

            if 'off' in tr:
                tmp += self.verb_off(imagescript, kframe)
                continue
            
            tmp.append([pg, tr])

        pairs =  sorted(tmp, key = lambda x: x[0])
    
        # output dicts
        out = []

        for pg, tlist in pairs:
            tout = ';'.join(tlist)
            percent =f'{round((((pg)*page_factor)/total_vh)*100, 1)}%'
            if percent == '0.0%':
                percent = 'from'
            if percent == '100.0%':
                percent = 'to'    
            if tout =='':
                continue
            out.append({'page':pg, 
                        'percent': percent,
                        'transform': tout})

        return out

    def verb_in(self, imagescript, kframe):

        out = []
        pg = kframe['page']
        tr = kframe['transform']        
        tr.remove('in')
        
        # dictionary of previous transforms
        tprev = self.tr_cumulative(imagescript, pg)
        
        if 'transform' not in tprev:
            tprev['transform'] = ''
            
        tout = tprev.copy()
        tout['opacity'] = 1
        tout['transform'] = 'translateY(100%) ' + tprev['transform']

        out.append([pg, self.to_list(tout)])

        nex = pg + 1/self.pars['page_factor']
        if nex > self.endpage: 
            nex = self.endpage

        tout = tprev.copy()
        tout['transform'] = 'translateY(0%) ' + tprev['transform']
        out.append([nex, self.to_list(tout)])

        return out

    def verb_on(self, imagescript, kframe):

        out = []
        pg = kframe['page']
        tr = kframe['transform']        
        tr.remove('on')

        # residual transform
        if tr != []:
            out.append([pg, tr])
        
        # dictionary of previous transforms
        tprev = self.tr_cumulative(imagescript, pg)
        
        # cumulated
        tout = tprev.copy()
        tout['opacity'] = 0
        out.append([0, self.to_list(tout)])

        # start
        prev = pg - self.pars['delta']
        if prev < 0: 
            prev = 0
        out.append([prev, ['opacity: 0']])

        # end
        nex = pg + self.pars['delta']
        if nex > self.endpage: 
            nex = self.endpage
        out.append([nex, ['opacity: 1']])

        return out

    def verb_out(self, imagescript, kframe):

        out = []
        pg = kframe['page']
        tr = kframe['transform']        
        tr.remove('out')
        
        # dictionary of previous transforms
        tprev = self.tr_cumulative(imagescript, pg)
        
        # out start
        tout = tprev.copy()
        if 'transform' not in tprev:
            tprev['transform'] = ''
        tout['transform'] = 'translateY(0%) ' + tprev['transform']
        tout['opacity'] = 1
        out.append([pg, self.to_list(tout)])

        # out
        tout = tprev.copy()
        if 'transform' not in tprev:
            tprev['transform'] = ''
        tout['transform'] = 'translateY(-100%) ' + tprev['transform']
        

        nex = pg + 1/self.pars['page_factor']
        if nex > self.endpage: 
            nex = self.endpage
        out.append([nex, self.to_list(tout)])

        return out

    def verb_off(self, imagescript, kframe):

        out = []
        pg = kframe['page']
        tr = kframe['transform']        
        tr.remove('off')
        
        # dictionary of previous transforms
        tprev = self.tr_cumulative(imagescript, pg)
        
        # cumulated
        tout = tprev.copy()
        if not 'opacity' in tout:
            tout['opacity'] = 1

        # start
        prev = pg - self.pars['delta']
        if prev < 0: 
            prev = 0
        out.append([prev, self.to_list(tout)])

        # end
        nex = pg + self.pars['delta']
        if nex > self.endpage: 
            nex = self.endpage
        tout['opacity'] = 0
        out.append([nex, self.to_list(tout)])
        out.append([self.endpage, self.to_list(tout)])


        return out    

    def tr_cumulative(self, script, page):
        
        # cumulative
        out = []
             
        for kf in script:     
            if kf['page'] <= page:
                out += kf['transform']
        
        return self.to_dict(out)
               
        
    def to_dict(self, props):
        out = {}
        for p in props:
            if ':' in p:
                l = p.split(':')
                k,v = [l[0].strip(), l[1].strip()]
                out[k] = v
        
        return out

    def to_list(self, d):
        return [f'{k}: {d[k]}' for k in d]
##########################################################