# markdown-scrolly

This package have two purposes:

* Organize the `html` output of the markdown parser in classes that can be styled with css.

* Add a markdown syntax for including scroll driven animations in the output. 

The [Project Webpage](https://gitlab.com/wpregliasco/markdown-scrolly) includes some demonstration files and better program description.

## Description

There are available multiple parsers for translating markdown content to html. 
We used the [`markdown`](https://pypi.org/project/Markdown/) package to include some class syntax in the output, and a 
cascade stylesheet that can be modified to style the output. 

Some features included are automatic numbering of sections and a signature at the end. 

Ispired by the beautiful animations made by The New Yorker (see for example [this article](https://www.newyorker.com/magazine/2021/12/06/the-secretive-libyan-prisons-that-keep-migrants-out-of-europe)) I wanted to include them in my reports but without doing more than a markdown file as input. 

The html generated is standalone and you share the images and some light text files, and the heavy task of render the animations is done in the destination browser. 

## Quickstart

* Installation: 
  
  ```bash
  $ pip install markdown-scrolly
  ```

* Make your markdown file `mymarkdown.md`. Use one per directory.

* Run the system command:
  
  ```
  $ scrolly mymarkdown.md -s '<myname>'
  ```

The output is a file named `mymarkdown.html` and some .css and .js files in a subdirectory `resources`.

As a demo of the features, with [this markdown file](https://gitlab.com/wpregliasco/markdown-scrolly/-/raw/main/demo/test.md?ref_type=heads) the output is [this webpage](https://markdown-scrolly-1730e5.gitlab.io/test.html)

## Workflow

The markdown syntax is as usual. 

* You can include html blocks but be careful with the closing syntax (use `<br/>` instead of `<br>`).
* Latex not implemented yet

After the compilation you will have two .css files that defines the style of the document:

* `md.css`  standard formatting (including tables and figures)
* `anima_base.css` document-independent part of the animation styling
  If theese files exists they are not overwritten by the command, so you can play with them
  preserving the results on succesive runs. 

The only new flavour in markdown syntax is in the image insertion.   
The syntax is:

> `![source_info | caption](img_filename){style}`

* if there is not `|` separator, the whole `[]` field is caption
* the `{style}` is optional and applies to the `img` element.

If there are multiple images not separated by blank lines or other elements, they are grouped together.

The size of the images is indicated as percentage in height of the viewport.   
The default is 30% but it can be changed anywhere in the document inserting a line with the directive.

```markdown
[graph: 40]
```

This sets the size of all future graphs in the document or up to the next directive. 

## Animations

There is a whole syntax to include scroll-animations in the output. 

Animations are composed by:

* background images that can fade in and out and support transformations
* markdown texts that traverses the screen with the scroll. 

The animation syntax have three blocks delimited:

* `[animation: texts]` with a numbered list of the texts in the animation.   
  The texts can be either:
  * one line of text 
  * multiline structured text enclosed in a `markdown block`
* `[animation: images]` is a numbered list of the images to use in the background.  
  Path are relatives to the source .md file. 
* `[animation: script]` is a table with the animation schedule. 
  As the animation runs on the scroll action, the animation time is measured in pages scrolled.  
  The title of the columns is irrelevant, but the order is meaningful.
  * __text animation:__   
    The first three columns indicate in what page will appear the texts.  
    The thirth column indicates the with, the left margin and the top position in percentages of viewport width.   
    The format fields are interpreted in this order and can be ommited each of them.  
    A not number information in any place is interpreted as a color.    
    Colors can be specified by name or in `#12f587` format
  * __background animation:__  
    Each additional column refers to the animation of every image.  
    The content are css transformations with the addition of four verbs: `in, on, out off`  
    Each image must enter in stage with `in` (scrolling input) or `on` (a glowing entrance) and go out with `out` (scrolling) or `off` (fading).
    Every style property can be animated. The geometric animations are listed in [mdn web docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API)
* `[animation: end]` closes the animation declaration block.

Here is a complete example included in de demo, that renders [in this page](https://markdown-scrolly-1730e5.gitlab.io/test.html) (is the first animation).

```markdown
  [animation: texts]

  1. __Southern Patagonian Ice Field__ 
  2. ```markdown
    Is the world's second largest contiguous extrapolar ice field. 
    It is the bigger of two remnant parts of the Patagonian Ice Sheet, 
    which covered all of southern Chile during the last glacial period, 
    locally called the Llanquihue glaciation. 
    ```
  3. ```markdown
    __Perito Moreno Glacier__  
    ![](imgs/640px-Perito_Moreno_Glacier_Patagonia_Argentina_Luca_Galuzzi_2005.jpeg)
    ```

  [animation: images]

  1. imgs/south_america.jpg
  2. imgs/south_field.png
  3. imgs/south_field_gm.jpg
  4. imgs/perito.png

  [animation: script]

  | page | text | widthLeftTop     | 1.SAmerica | 2.SF_remark | 3.S_Field | 4.Glacier_remark |
  | ---- | ---- | ----------       | ------     | ------      | ------    | ------           |
  | 0    |      |                  | in         |             |           |                  |
  | 1    | 1    | 20 10 darkblue   |            |             |           |                  |
  | 1.3  |      |                  |            |  on         |           |                  |
  | 2    |      |                  |            |             |           |                  |
  | 2.2  |      |                  |            |             | on;scale:.05;transform: translate(-30%,90%);|  |
  | 2.4  |      |                  | off        |  off        |           |                  |
  | 3    | 2    | 35 54 70 #000055 |            |             | scale:1;transform: translate(0%,0%); |   |
  | 4    | 3    | 36 54  #000055   |            |             |           | on               |
  | 5    |      |                  |            |             | out       | out              |

  [animation: end]
```

## Viewing and distributing the output

As the output is an html file with some relative path files (css, images and javascript code)
the only browser that renders correctly relative paths is Firefox.   
Other browsers blocks relative references for security reasons. 

This can be solved using a local temporary server. It is easier than it sounds. 
In a terminal, go to the directory of the html file and run:

```bash
$ python -m http.server
```

And you can visualize the file from the browser in the address

```
localhost:8000/myfile.html
```

But for distribution purposes and to allow others to see the result without any configuration, 
all the external information can be packaged in one file. So in one file are all the images, codes and styling.   
That is why we included the command `html-package` with the syntax:

```
$ html-package myfile.html
```

and outputs a file `myfile_pkg.html` that is standalone with all the information needed inside. 

## Documentation

* Features:
  
  * section numbering
  * signature
  * post edition css
  * html packaging
  * one file per directory

* [HTML Structure](./docs/md_css.md)

* [Animation HTML Structure](./docs/anima_css.md)

* [Markdown Animation Syntax](./docs/anima_syntax.md)

## Author

This project is made by Willy Pregliasco from Bariloche, Argentina.   
It is an earlier working version and every recommendation, objection and collaboration is welcomed.   
You can add an [issue to the Project](https://gitlab.com/wpregliasco/markdown-scrolly/-/issues).

Licensed under the MIT License - see the LICENSE file for details.

---

_Willy Pregliasco, 10/2024_