# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>

import threading


class ThreadTool(threading.Thread):
    def __init__(self, target, args=()):
        super(ThreadTool, self).__init__()
        self.target = target
        self.args = args
        self.result = None

    def run(self):
        self.result = self.target(*self.args)

    def get_result(self):
        return self.result
