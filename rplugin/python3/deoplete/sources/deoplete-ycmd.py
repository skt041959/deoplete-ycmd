
# encoding: utf-8

import os
import time
import logging
from .base import Base
from deoplete.util import load_external_module

load_external_module(__file__, "YouCompleteMe/third_party/ycmd")
from ycmd import server_utils as su
su.AddNearestThirdPartyFoldersToSysPath( su.__file__ )

load_external_module(__file__, "YouCompleteMe/python")
from ycm import base, vimsupport, youcompleteme
su.AddNearestThirdPartyFoldersToSysPath(os.path.dirname(youcompleteme.__file__))

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'ycmd'
        self.mark = '[ycmd]'
        self.filetypes = ['c', 'cpp']
        self.rank = 500

        self.input_pattern = (r'[^. \t0-9]\.\w*|'
                r'[^. \t0-9]->\w*|'
                r'[a-zA-Z_]\w*::\w*|'
                r'\[.*\]*\s')

    def on_init(self, context):
        if not self.is_debug_enabled:
            root_log = logging.getLogger('deoplete')
            child_log = root_log.getChild('ycmd')
            child_log.propagate = False

        import sys; self.vim.err_write('\n'.join(sys.path))
        self.ycm_client = youcompleteme.YouCompleteMe(self.vim, child_log)

    def gather_candidates(self, context):
        self.ycm_client.SendCompletionRequest( True )

        while not self.ycm_client.CompletionRequestReady():
            time.sleep(1)

        response = self.ycm_client.GetCompletionResponse()

        out = response['completions']

        return out


