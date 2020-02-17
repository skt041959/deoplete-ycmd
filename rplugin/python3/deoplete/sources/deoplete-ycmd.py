
# encoding: utf-8

from deoplete.base.source import Base
from deoplete.util import Nvim, UserContext, Candidates

class Source(Base):
    """"""

    def __init__(self, vim: Nvim) -> None:
        """"""
        super().__init__(vim)

        self.name = 'ycmd'
        self.mark = '[Ycm]'
        self.rank = 500
        self.is_bytepos = True
        self.min_pattern_length = 1
        self.filetypes = ['cpp', 'c']
        self.input_pattern = r'(\.|::|->)\w*$'
        self.pyeval = self.vim.funcs.py3eval

    def gather_candidates(self, context: UserContext):
        result = []
        if context['is_async']:
            if self.pyeval('ycm_state.CompletionRequestReady()'):
                context['is_async'] = False
                result = self.pyeval('ycm_state.GetCompletionResponse()')['completions']
        else:
            self.pyeval('ycm_state.SendCompletionRequest( True )')
            if self.pyeval('ycm_state.CompletionRequestReady()'):
                result = self.pyeval('ycm_state.GetCompletionResponse()')['completions']
            else:
                context['is_async'] = True

        return result
