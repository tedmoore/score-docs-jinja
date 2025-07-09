#!/usr/bin/env python3
import jinja2
import os

def render_template(template_file, context):
    loader = jinja2.FileSystemLoader(searchpath=".")
    env = jinja2.Environment(loader=loader)
    template = env.get_template(template_file)
    rendered_text = template.render(context)
    return rendered_text
        
def context_to_pdf(template_file, context, output_file):
    rendered_text = render_template(template_file, context)
    with open("temp.md", "w") as f:
        f.write(rendered_text)
    os.system(f'pandoc --pdf-engine=xelatex -i temp.md -o {output_file}')
    os.system('rm temp.md')
    
def replace_spaces(s):
    return s.replace(" ", "_")

def render_scores(anonymize):
    context_to_pdf("cover.jinja.md", {"redact": anonymize}, "cover.pdf")
    context_to_pdf("front-matter.jinja.md", {"redact": anonymize}, "front-matter.pdf")
    
    titles = ["cylinder lullaby I","acute","bezier","angle","cylinder lullaby II"]
    roman_numerals = ["I","II","III","IV","V"]
    
    for i, title in enumerate(titles):
        context = {
            "movementtitle": title,
            "romannumeral": roman_numerals[i],
            "redact": anonymize
        }
        context_to_pdf("movement-title-page.jinja.md", context, f"movement-title-page-{i+1}.pdf")
        
    system_call = 'cpdf cover.pdf front-matter.pdf '
    for i in range(5):
        system_call += f'movement-title-page-{i+1}.pdf ./../sibelius/mvt-{i+1}.pdf '
        
    if anonymize:
        system_call += '-o rendered-scores-anonymous/0-arco-ANONYMOUS.pdf'
    else:
        system_call += '-o rendered-scores/0-arco-by-Ted-Moore.pdf'
            
    os.system(system_call)
    os.system('rm cover.pdf')
    
    for i in range(5):
        system_call = f'cpdf movement-title-page-{i+1}.pdf front-matter.pdf ./../sibelius/mvt-{i+1}.pdf '
        title_no_spaces = replace_spaces(titles[i])
        if anonymize:
            system_call += f'-o rendered-scores-anonymous/{i+1}-{title_no_spaces}-ANONYMOUS.pdf'
        else:
            system_call += f'-o rendered-scores/{i+1}-{title_no_spaces}-by-Ted-Moore.pdf'
        os.system(system_call)
        os.system(f'rm movement-title-page-{i+1}.pdf')

    os.system('rm front-matter.pdf')
        
if __name__ == "__main__":
    render_scores(False)
    render_scores(True)