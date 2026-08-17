# Third-Party Notices

Every skill in this repository is released under the MIT License in `LICENSE`. Most are
entirely ALYA Labs' own work. Where a skill incorporates or builds on someone else's, it is
credited here and inline, and the upstream licence is reproduced below.

## idea-validation

The Phase 0 nine-dimension pre-screen is adapted from the `business-brainstorm` skill in
[coreyhaines31/makerskills](https://github.com/coreyhaines31/makerskills), MIT License,
Copyright (c) Corey Haines. The seven adversarial stress-test personas, the scoring model,
and the pivot-conversion step are ALYA Labs' own.

## deepdive

Three distinct kinds of debt here, listed separately because they are not equivalent.

**Research citation (no code).** The recursive decomposition approach is informed by the
Recursive Language Models line of research (Zhang, Kraska and Khattab, MIT CSAIL,
arXiv:2512.24601v2). deepdive is a practical approximation for Claude Code's tool
architecture, not an implementation of the paper's Algorithm 1.

**Adapted code: brainqub3/RLM.** `scripts/rlm_repl.py` (persistent pickle REPL, buffer and
chunking helpers) and the sub-agent pattern in `agents/deepdive-subcall.md` are adapted from
[brainqub3/RLM](https://github.com/brainqub3/RLM), published at the time as
`brainqub3/claude_code_RLM`, MIT License, Copyright (c) 2026 john-adeojo. Full licence text
below.

**Adapted code: avilum/minrlm.** The compression-ratio entropy profiling in
`scripts/entropy_probe.py`, including the text output format, is adapted from
[avilum/minrlm](https://github.com/avilum/minrlm), MIT License,
Copyright (c) 2026 Avi Lumelsky. Full licence text below.

`scripts/rce_engine.py` and `scripts/concept_auditor.py` are ALYA Labs' own, as are the
task modes, the PRD mode, and the coverage-audit loop.

### MIT License, Copyright (c) 2026 john-adeojo (brainqub3/RLM)

```
MIT License

Copyright (c) 2026 john-adeojo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### MIT License, Copyright (c) 2026 Avi Lumelsky (avilum/minrlm)

```
MIT License

Copyright (c) 2026 Avi Lumelsky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## premium-web-design

Cites two public bodies of work as references rather than reproducing them:

- Jakob Nielsen's 10 Usability Heuristics (Nielsen Norman Group), used as a named scoring
  rubric in audit mode.
- Refactoring UI (Adam Wathan and Steve Schoger), listed as a recommended external resource.

## What is deliberately absent

Material that ALYA Labs uses internally but cannot or should not relicense was excluded from
this repository rather than shipped with a disclaimer. That includes anything derived from
paid commercial training products, anything derived from share-alike sources, and upstream
skills that their original authors already publish themselves.
