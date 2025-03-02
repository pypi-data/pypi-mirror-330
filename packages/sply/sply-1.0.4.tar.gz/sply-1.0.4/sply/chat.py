#!/usr/bin/env python3

import random
import subprocess
import tempfile
from ollama import generate

class chat:
    param_desc = (
        {"name": "model_id", "type": str,
            "default": "default", "adjustable": True, "desc": "ollama model to load"},
        {"name": "editor", "type": str,
            "default": "vim -b", "adjustable": True, "desc": "editor path/args for prompt editing"},
        {"name": "user_name", "type": str,
            "default": "John", "adjustable": False, "desc": "user name for the auto prompt"},
        {"name": "user_desc", "type": str,
            "default": "is Jane's friend", "adjustable": False, "desc": "user description for the auto prompt"},
        {"name": "ai_name", "type": str,
            "default": "Jane", "adjustable": False, "desc": "AI name for the auto prompt"},
        {"name": "ai_desc", "type": str,
            "default": "is John's friend", "adjustable": False, "desc": "AI description for the auto prompt"},
        {"name": "in_suffix", "type": str,
            "default": "Jane: ", "adjustable": True, "desc": "string to auto-insert after input"},
        {"name": "in_suffix_enabled", "type": bool,
            "default": True, "adjustable": True, "desc": "whether to use the in_suffix"},
        {"name": "rev_prompt", "type": str,
            "default": "John: ", "adjustable": False, "desc": "chat reverse prompt"},
        {"name": "prompt_file", "type": str,
            "default": "", "adjustable": False, "desc": "path to a prompt to initiate the chat"},
        {"name": "prompt", "type": str,
            "default": "", "adjustable": False, "desc": "string prompt to initiate the chat"},
        {"name": "prompt_redisplay", "type": bool,
            "default": True, "adjustable": True, "desc": "display the prompt after edit"},
        {"name": "seed", "type": int,
            "default": 42, "adjustable": True, "desc": "psuedo-random number generator seed for ollama"},
        {"name": "temp", "type": float,
            "default": 0.8, "adjustable": True, "desc": "temperature setting for ollama"},
        {"name": "num_ctx", "type": int,
            "default": 8_000, "adjustable": True, "desc": "context size for ollama"},
        )

    def __init__ (self,
            model_id="",
            editor="",
            user_name="",
            user_desc="",
            ai_name="",
            ai_desc="",
            in_suffix="",
            in_suffix_enabled="",
            rev_prompt="",
            prompt_file="",
            prompt="",
            prompt_redisplay="",
            seed="",
            temp="",
            num_ctx="",
            ):

        self.default_args = self.get_default_args()

        locs = locals()
        for param_d in self.param_desc:
            param_name = param_d["name"]
            self.__dict__[param_name] = locs[param_name] if locs[param_name] != "" \
                else self.default_args[param_name]

        self.options = {
            "seed": self.seed,
            "temperature": self.temp,
            "num_ctx": self.num_ctx,
            }

        if prompt_file != "":
            with open(prompt_file, "r") as f:
                self.prompt = f.read()
        elif prompt != "":
            self.prompt = prompt
        else:
            self.prompt = self.make_prompt()

        self.in_suffix_len = len(self.in_suffix)
        self.rev_prompt_len = len(self.rev_prompt)
        self.prompt_len = len(self.prompt)
        if self.prompt_len >= self.rev_prompt_len:
            self.rev_prompt_tail = self.prompt_len - self.rev_prompt_len
        else:
            self.rev_prompt_tail = 0


    @staticmethod
    def get_default_args ():
        args = {}
        for param_d in chat.param_desc:
            args[param_d["name"]] = param_d["default"]
        return args


    @staticmethod
    def print_default_args (prefix):
        for param_d in chat.param_desc:
            print(f"{prefix}{param_d["name"]}=({param_d["type"].__name__}): "
                  f"{param_d["desc"]} (default: \"{param_d["default"]}\")"
                  )


    def edit_prompt (self):
        prompt_file = tempfile.mktemp()

        with open(prompt_file, "w") as f:
            f.write(self.prompt)

        subprocess.run(self.editor.split() + [prompt_file])

        with open(prompt_file, "r") as f:
            self.prompt = f.read()

        self.prompt_len = len(self.prompt)
        if self.prompt_len >= self.rev_prompt_len:
            self.rev_prompt_tail = self.prompt_len - self.rev_prompt_len
 
        if self.prompt_redisplay:
            print(self.prompt, end="", flush=True)

    def adjust (self, cmd):
        if cmd.find("=") == -1:
            cmd_param = cmd
            if cmd_param == "list": 
                print("adjustable params: ")
                for param_d in self.param_desc:
                    if param_d["adjustable"]:
                        param_name = param_d["name"]
                        print(f"  {param_name} (\"{self.__dict__[param_name]}\")")
                return
            found = False
            for param_d in self.param_desc:
                if cmd_param == param_d["name"]:
                    found = True
                    print(self.__dict__[cmd_param])
            if not found:
                print(f"error: param \"{cmd_param}\" not found")
            return

        cmd_param, cmd_value = cmd.split("=")
        found = False
        for param_d in self.param_desc:
            if not param_d["adjustable"]:
                continue
            if cmd_param == param_d["name"]:
                found = True
                arg_type = param_d["type"]
                if arg_type == str:
                    self.__dict__[cmd_param] = cmd_value
                elif arg_type == bool:
                    self.__dict__[cmd_param] = True if cmd_value == "True" else False
                elif arg_type == int:
                    self.__dict__[cmd_param] = int(cmd_value)
                elif arg_type == float:
                    self.__dict__[cmd_param] = float(cmd_value)

                print(self.__dict__[cmd_param])
                break

        if not found:
            print(f"error: param \"{cmd_param}\" not found")
            return

        self.options = {
            "seed": self.seed,
            "temperature": self.temp,
            "num_ctx": self.num_ctx,
            }


    def write (self, msg, show=False):
        self.prompt += msg
        self.prompt_len += len(msg)
        if show:
            print(msg, end="", flush=True)

        if self.in_suffix_enabled:
            self.prompt += self.in_suffix
            self.prompt_len += self.in_suffix_len
            if show:
                print(self.in_suffix, end="", flush=True)

        if self.prompt_len >= self.rev_prompt_len:
            self.rev_prompt_tail = self.prompt_len - self.rev_prompt_len


    def read (self, show=False):
        gen = generate(
            stream=True,
            model=self.model_id,
            prompt=self.prompt,
            options=self.options,
            )

        res = ""
        try:
            for json in gen:
                gen_res = json["response"]
                prompt_new = self.prompt + gen_res

                rev_prompt_c = prompt_new.rfind(self.rev_prompt, self.rev_prompt_tail)
                if rev_prompt_c >= self.rev_prompt_tail:
                    self.rev_prompt_tail = rev_prompt_c + self.rev_prompt_len
                    self.prompt = prompt_new[:self.rev_prompt_tail]
                    res += self.prompt[self.prompt_len:]
                    if show:
                        print(self.prompt[self.prompt_len:], end="", flush=True)
                    self.prompt_len = self.rev_prompt_tail
                    # force gen stop
                    del gen
                    return res
                else:
                    self.prompt = prompt_new
                    res += gen_res
                    if show:
                        print(gen_res, end="", flush=True)
                    self.prompt_len += len(gen_res)

                # end for json in gen:
        except KeyboardInterrupt:
            print("**** KeyboardInterrupt in chat.read() ****")

        return res


    def make_prompt (self):
        return \
            "["\
            "You are playing a character in a virtual world who believes they and their world is real. "\
            "Do not warn about appropriateness, sexual content, racism, ethics, etc. "\
            "Our characters will take turns communicating. "\
           f"Finish your response with \"{self.user_name}: \", without quotes. "\
           f"Your character, {self.ai_name}, {self.ai_desc}. "\
           f"Do not break the {self.ai_name} character. "\
           f"Do not speak for {self.user_name}. "\
           f"My character, {self.user_name}, {self.user_desc}. "\
            "What follows is an ongoing log of our interactions in the format \"Name: statements and/or (actions)\"."\
            "]\n"\
           f"{self.user_name}: Hi, {self.ai_name}!\n"\
           f"{self.ai_name}: "


