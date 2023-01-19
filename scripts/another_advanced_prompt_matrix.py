import math
from collections import namedtuple
from copy import copy
import random
import re

import modules.scripts as scripts
import gradio as gr

from modules import images
from modules.processing import process_images, Processed
from modules.shared import opts, cmd_opts, state
import modules.sd_samplers

class Script(scripts.Script):
    def title(self):
        return "Another advanced prompt matrix"

    def ui(self, is_img2img):
        # dummy = gr.Checkbox(label="")
        info = gr.Markdown('''
        Usage: `?white|red|glowing|blue|yellow|pink? hair, $headwear@0.3$`   
        `?x|y|z?` - random from a list   
        `$headwear@0.3$` - headwear will appear with a probability of 30%   
        ''')
        checkbox_iterate = gr.Checkbox(label="Iterate seed every line", value=True)
        checkbox_iterate_batch = gr.Checkbox(label="Use same random seed for all lines", value=False)
        counts = gr.Textbox(label="Number of combinations", lines=1, placeholder='1')

        return [info, counts, checkbox_iterate, checkbox_iterate_batch]


    def run(self, p, info, counts, checkbox_iterate, *args, **kargs):
        def chooser(number):
            return number >= random.random()
        modules.processing.fix_seed(p)

        original_prompt = p.prompt[0] if type(p.prompt) == list else p.prompt



        all_prompts = []


        if counts == '':
            counts = '1'
        for _ in range(int(counts)):
            pattern = re.compile(r'[\$\$]+')
            split1 = list(filter(None, pattern.split(original_prompt)))


            new_prompt = ''

            for part in split1:
                if '@' not in part:
                    new_prompt = new_prompt + part
                else:
                    part, number = part.split('@')
                    if chooser(float(number)) == True:
                        new_prompt = new_prompt + part

            pattern = re.compile(r'[\?\?]+')
            split1 = list(filter(None, pattern.split(new_prompt)))


            new_prompt = ''

            for part in split1:
                if '|' not in part:
                    new_prompt = new_prompt + part
                else:
                    variants = part.split('|')
                    part = random.sample(variants, 1)[0]
                    new_prompt = new_prompt + part
            all_prompts.append(new_prompt)


        lines = all_prompts
        p.do_not_save_grid = True

        job_count = 0
        jobs = []

        for line in lines:

            args = {"prompt": line}

            n_iter = args.get("n_iter", 1)
            if n_iter != 1:
                job_count += n_iter
            else:
                job_count += 1

            jobs.append(args)

        print(f"Will process {len(lines)} lines in {job_count} jobs.")
        if (checkbox_iterate or checkbox_iterate_batch) and p.seed == -1:
            p.seed = int(random.randrange(4294967294))

        state.job_count = job_count

        images = []
        all_prompts = []
        infotexts = []
        for n, args in enumerate(jobs):
            state.job = f"{state.job_no + 1} out of {state.job_count}"

            copy_p = copy(p)
            for k, v in args.items():
                setattr(copy_p, k, v)

            proc = process_images(copy_p)
            images += proc.images
            
            if checkbox_iterate:
                p.seed = p.seed + (p.batch_size * p.n_iter)
            all_prompts += proc.all_prompts
            infotexts += proc.infotexts

        return Processed(p, images, p.seed, "", all_prompts=all_prompts, infotexts=infotexts)
