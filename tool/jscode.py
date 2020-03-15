#-*-coding:utf-8-*-
import re
class JsCode:
    def __init__(self, js_code: str):
        self.js_code = "--x_x--0_0--" + js_code + "--x_x--0_0--"

    def replace(self, pattern: str, repl: str):
        self.js_code = re.sub(pattern, repl, self.js_code)
        return self

