2026-02-08T13:49:55.7146517Z ##[group]Run gaurav-nelson/github-action-markdown-link-check@v1
2026-02-08T13:49:55.7146894Z with:
2026-02-08T13:49:55.7147080Z   use-quiet-mode: yes
2026-02-08T13:49:55.7147300Z   config-file: .github/mlc_config.json
2026-02-08T13:49:55.7147565Z   use-verbose-mode: no
2026-02-08T13:49:55.7147764Z   folder-path: .
2026-02-08T13:49:55.7147966Z   max-depth: -1
2026-02-08T13:49:55.7148158Z   check-modified-files-only: no
2026-02-08T13:49:55.7148389Z   base-branch: master
2026-02-08T13:49:55.7148571Z   file-extension: .md
2026-02-08T13:49:55.7148751Z env:
2026-02-08T13:49:55.7148905Z   TEXLIVE_VERSION: 2025
2026-02-08T13:49:55.7149097Z ##[endgroup]
2026-02-08T13:49:55.7258702Z ##[command]/usr/bin/docker run --name d2489c74c5a34332c047f08d6daf78c2edba59_5af5b7 --label d2489c --workdir /github/workspace --rm -e "TEXLIVE_VERSION" -e "INPUT_USE-QUIET-MODE" -e "INPUT_CONFIG-FILE" -e "INPUT_USE-VERBOSE-MODE" -e "INPUT_FOLDER-PATH" -e "INPUT_MAX-DEPTH" -e "INPUT_CHECK-MODIFIED-FILES-ONLY" -e "INPUT_BASE-BRANCH" -e "INPUT_FILE-EXTENSION" -e "INPUT_FILE-PATH" -e "HOME" -e "GITHUB_JOB" -e "GITHUB_REF" -e "GITHUB_SHA" -e "GITHUB_REPOSITORY" -e "GITHUB_REPOSITORY_OWNER" -e "GITHUB_REPOSITORY_OWNER_ID" -e "GITHUB_RUN_ID" -e "GITHUB_RUN_NUMBER" -e "GITHUB_RETENTION_DAYS" -e "GITHUB_RUN_ATTEMPT" -e "GITHUB_ACTOR_ID" -e "GITHUB_ACTOR" -e "GITHUB_WORKFLOW" -e "GITHUB_HEAD_REF" -e "GITHUB_BASE_REF" -e "GITHUB_EVENT_NAME" -e "GITHUB_SERVER_URL" -e "GITHUB_API_URL" -e "GITHUB_GRAPHQL_URL" -e "GITHUB_REF_NAME" -e "GITHUB_REF_PROTECTED" -e "GITHUB_REF_TYPE" -e "GITHUB_WORKFLOW_REF" -e "GITHUB_WORKFLOW_SHA" -e "GITHUB_REPOSITORY_ID" -e "GITHUB_TRIGGERING_ACTOR" -e "GITHUB_WORKSPACE" -e "GITHUB_ACTION" -e "GITHUB_EVENT_PATH" -e "GITHUB_ACTION_REPOSITORY" -e "GITHUB_ACTION_REF" -e "GITHUB_PATH" -e "GITHUB_ENV" -e "GITHUB_STEP_SUMMARY" -e "GITHUB_STATE" -e "GITHUB_OUTPUT" -e "RUNNER_OS" -e "RUNNER_ARCH" -e "RUNNER_NAME" -e "RUNNER_ENVIRONMENT" -e "RUNNER_TOOL_CACHE" -e "RUNNER_TEMP" -e "RUNNER_WORKSPACE" -e "ACTIONS_RUNTIME_URL" -e "ACTIONS_RUNTIME_TOKEN" -e "ACTIONS_CACHE_URL" -e "ACTIONS_RESULTS_URL" -e "ACTIONS_ORCHESTRATION_ID" -e GITHUB_ACTIONS=true -e CI=true -v "/var/run/docker.sock":"/var/run/docker.sock" -v "/home/runner/work/_temp":"/github/runner_temp" -v "/home/runner/work/_temp/_github_home":"/github/home" -v "/home/runner/work/_temp/_github_workflow":"/github/workflow" -v "/home/runner/work/_temp/_runner_file_commands":"/github/file_commands" -v "/home/runner/work/TFG-TFM_EPS/TFG-TFM_EPS":"/github/workspace" d2489c:74c5a34332c047f08d6daf78c2edba59  "yes" "no" ".github/mlc_config.json" "." "-1" "no" "master" ".md" ""
2026-02-08T13:49:57.7566263Z npm warn deprecated har-validator@5.1.5: this library is no longer supported
2026-02-08T13:49:57.8263394Z npm warn deprecated uuid@3.4.0: Please upgrade  to version 7 or higher.  Older versions may use Math.random() in certain circumstances, which is known to be problematic.  See https://v8.dev/blog/math-random for details.
2026-02-08T13:49:57.8496852Z npm warn deprecated request@2.88.2: request has been deprecated, see https://github.com/request/request/issues/3142
2026-02-08T13:49:58.0659364Z 
2026-02-08T13:49:58.0660035Z added 65 packages in 2s
2026-02-08T13:49:58.0660369Z 
2026-02-08T13:49:58.0663879Z 5 packages are looking for funding
2026-02-08T13:49:58.0668024Z   run `npm fund` for details
2026-02-08T13:49:58.1370175Z [0;34mCannot find [0;33m.github/mlc_config.json[0m
2026-02-08T13:49:58.1371411Z [0;33mNOTE: See https://github.com/tcort/markdown-link-check#config-file-format to know more about
2026-02-08T13:49:58.1372582Z customizing markdown-link-check by using a configuration file.[0m
2026-02-08T13:49:58.1373324Z [0;34mUSE_QUIET_MODE: yes[0m
2026-02-08T13:49:58.1373807Z [0;34mUSE_VERBOSE_MODE: no[0m
2026-02-08T13:49:58.1374256Z [0;34mFOLDER_PATH: .[0m
2026-02-08T13:49:58.1374531Z [0;34mMAX_DEPTH: -1[0m
2026-02-08T13:49:58.1374844Z [0;34mCHECK_MODIFIED_FILES: no[0m
2026-02-08T13:49:58.1376398Z [0;34mFILE_EXTENSION: .md[0m
2026-02-08T13:49:58.1376738Z [0;34mFILE_PATH: [0m
2026-02-08T13:49:58.1384283Z + find . -name '*.md' -not -path './node_modules/*' -exec markdown-link-check '{}' -q ';'
2026-02-08T13:50:47.7200617Z + set +x
2026-02-08T13:50:47.7210179Z [0;33m=========================> MARKDOWN LINK CHECK <=========================[0m
2026-02-08T13:50:47.7216233Z 
2026-02-08T13:50:47.7216687Z FILE: ./CHANGELOG.md
2026-02-08T13:50:47.7216935Z 
2026-02-08T13:50:47.7219429Z 2 links checked.
2026-02-08T13:50:47.7219696Z 
2026-02-08T13:50:47.7220007Z FILE: ./sty/README.md
2026-02-08T13:50:47.7220216Z 
2026-02-08T13:50:47.7220327Z 4 links checked.
2026-02-08T13:50:47.7220524Z 
2026-02-08T13:50:47.7220653Z FILE: ./CONTRIBUTING.md
2026-02-08T13:50:47.7221297Z (node:41) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7222256Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7222802Z 
2026-02-08T13:50:47.7222912Z 10 links checked.
2026-02-08T13:50:47.7223095Z 
2026-02-08T13:50:47.7223247Z FILE: ./.herramientas/README.md
2026-02-08T13:50:47.7223510Z 
2026-02-08T13:50:47.7223614Z 0 links checked.
2026-02-08T13:50:47.7223788Z 
2026-02-08T13:50:47.7223957Z FILE: ./.github/copilot-instructions.md
2026-02-08T13:50:47.7224241Z 
2026-02-08T13:50:47.7224349Z 0 links checked.
2026-02-08T13:50:47.7224527Z 
2026-02-08T13:50:47.7224695Z FILE: ./.github/PULL_REQUEST_TEMPLATE.md
2026-02-08T13:50:47.7224992Z 
2026-02-08T13:50:47.7225100Z 0 links checked.
2026-02-08T13:50:47.7225279Z 
2026-02-08T13:50:47.7225439Z FILE: ./recursos/figuras/README.md
2026-02-08T13:50:47.7225708Z 
2026-02-08T13:50:47.7225819Z 0 links checked.
2026-02-08T13:50:47.7225995Z 
2026-02-08T13:50:47.7226105Z FILE: ./AGENTS.md
2026-02-08T13:50:47.7226280Z 
2026-02-08T13:50:47.7226392Z 0 links checked.
2026-02-08T13:50:47.7226559Z 
2026-02-08T13:50:47.7226667Z FILE: ./README.md
2026-02-08T13:50:47.7227265Z (node:107) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7228497Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7229340Z [✖] https://www.gnu.org/licenses/gpl-3.0
2026-02-08T13:50:47.7230098Z [✖] https://tex.stackexchange.com/
2026-02-08T13:50:47.7230628Z [✖] https://pgfplots.sourceforge.io/
2026-02-08T13:50:47.7230905Z 
2026-02-08T13:50:47.7231015Z 43 links checked.
2026-02-08T13:50:47.7231181Z 
2026-02-08T13:50:47.7231319Z ERROR: 3 dead links found!
2026-02-08T13:50:47.7231795Z [✖] https://www.gnu.org/licenses/gpl-3.0 → Status: 0
2026-02-08T13:50:47.7232373Z [✖] https://tex.stackexchange.com/ → Status: 403
2026-02-08T13:50:47.7233007Z [✖] https://pgfplots.sourceforge.io/ → Status: 403
2026-02-08T13:50:47.7233361Z 
2026-02-08T13:50:47.7233506Z FILE: ./docs/BIBLIOGRAFIA.md
2026-02-08T13:50:47.7234195Z (node:118) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7235122Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7235861Z [✖] https://scholar.google.com/
2026-02-08T13:50:47.7236158Z 
2026-02-08T13:50:47.7236277Z 87 links checked.
2026-02-08T13:50:47.7236443Z 
2026-02-08T13:50:47.7236566Z ERROR: 1 dead links found!
2026-02-08T13:50:47.7237096Z [✖] https://scholar.google.com/ → Status: 403
2026-02-08T13:50:47.7237433Z 
2026-02-08T13:50:47.7237565Z FILE: ./docs/AUDIT_2025.md
2026-02-08T13:50:47.7237820Z 
2026-02-08T13:50:47.7237942Z 0 links checked.
2026-02-08T13:50:47.7238131Z 
2026-02-08T13:50:47.7238288Z FILE: ./docs/IMAGENES_SUBFIGURAS.md
2026-02-08T13:50:47.7239031Z (node:140) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7241197Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7241712Z 
2026-02-08T13:50:47.7241849Z 77 links checked.
2026-02-08T13:50:47.7242056Z 
2026-02-08T13:50:47.7242200Z FILE: ./docs/ACCESIBILIDAD.md
2026-02-08T13:50:47.7242909Z (node:151) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7244154Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7244928Z [✖] https://www.adobe.com/acrobat
2026-02-08T13:50:47.7245528Z [✖] https://www.overleaf.com/learn/latex/Accessibility
2026-02-08T13:50:47.7246470Z [✖] https://esail.tamu.edu/faculty-tutorials/accessible-latex-pdf-ua-2-overleaf-2025/
2026-02-08T13:50:47.7247084Z 
2026-02-08T13:50:47.7247200Z 21 links checked.
2026-02-08T13:50:47.7247392Z 
2026-02-08T13:50:47.7247525Z ERROR: 3 dead links found!
2026-02-08T13:50:47.7248018Z [✖] https://www.adobe.com/acrobat → Status: 0
2026-02-08T13:50:47.7248888Z [✖] https://www.overleaf.com/learn/latex/Accessibility → Status: 404
2026-02-08T13:50:47.7250317Z [✖] https://esail.tamu.edu/faculty-tutorials/accessible-latex-pdf-ua-2-overleaf-2025/ → Status: 403
2026-02-08T13:50:47.7251149Z 
2026-02-08T13:50:47.7251255Z FILE: ./docs/REFERENCIAS_CRUZADAS.md
2026-02-08T13:50:47.7251844Z (node:162) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7252733Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7253216Z 
2026-02-08T13:50:47.7253346Z 69 links checked.
2026-02-08T13:50:47.7253544Z 
2026-02-08T13:50:47.7253670Z FILE: ./docs/README.md
2026-02-08T13:50:47.7254260Z (node:173) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7255106Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7255590Z 
2026-02-08T13:50:47.7255702Z 13 links checked.
2026-02-08T13:50:47.7255871Z 
2026-02-08T13:50:47.7255979Z FILE: ./docs/TABLAS.md
2026-02-08T13:50:47.7256567Z (node:184) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7257493Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7258225Z 
2026-02-08T13:50:47.7258360Z 89 links checked.
2026-02-08T13:50:47.7258552Z 
2026-02-08T13:50:47.7258712Z FILE: ./docs/TEXTO_LISTAS.md
2026-02-08T13:50:47.7259192Z (node:195) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7260208Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7260676Z 
2026-02-08T13:50:47.7260784Z 94 links checked.
2026-02-08T13:50:47.7260964Z 
2026-02-08T13:50:47.7261090Z FILE: ./docs/CODIGO_FUENTE.md
2026-02-08T13:50:47.7261714Z (node:206) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7262585Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7263053Z 
2026-02-08T13:50:47.7263187Z 72 links checked.
2026-02-08T13:50:47.7263372Z 
2026-02-08T13:50:47.7263520Z FILE: ./docs/FIGURAS_GRAFICAS.md
2026-02-08T13:50:47.7264208Z (node:217) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7265144Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7265653Z 
2026-02-08T13:50:47.7265777Z 94 links checked.
2026-02-08T13:50:47.7265973Z 
2026-02-08T13:50:47.7266109Z FILE: ./docs/COMPONENTES.md
2026-02-08T13:50:47.7266775Z (node:228) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7267693Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7268204Z 
2026-02-08T13:50:47.7268340Z 118 links checked.
2026-02-08T13:50:47.7268554Z 
2026-02-08T13:50:47.7268698Z FILE: ./docs/AI_CONTEXT.md
2026-02-08T13:50:47.7269375Z (node:239) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7270348Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7270730Z 
2026-02-08T13:50:47.7270866Z 60 links checked.
2026-02-08T13:50:47.7271078Z 
2026-02-08T13:50:47.7271232Z FILE: ./docs/GLOSARIOS_ACRONIMOS.md
2026-02-08T13:50:47.7272213Z (node:250) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7273183Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7273481Z 
2026-02-08T13:50:47.7273550Z 73 links checked.
2026-02-08T13:50:47.7273656Z 
2026-02-08T13:50:47.7273745Z FILE: ./docs/ECUACIONES.md
2026-02-08T13:50:47.7274115Z (node:261) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7274772Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7275463Z [✖] https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols
2026-02-08T13:50:47.7348305Z 
2026-02-08T13:50:47.7348472Z 125 links checked.
2026-02-08T13:50:47.7348684Z 
2026-02-08T13:50:47.7348824Z ERROR: 1 dead links found!
2026-02-08T13:50:47.7349570Z [✖] https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols → Status: 403
2026-02-08T13:50:47.7350613Z 
2026-02-08T13:50:47.7350791Z FILE: ./docs/GUIA_PRINCIPIANTES.md
2026-02-08T13:50:47.7351605Z (node:272) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T13:50:47.7352573Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T13:50:47.7353603Z [✖] https://tecdigital.tec.ac.cr/revistamatematica/Libros/LATEX/LaTeX_2014.pdf
2026-02-08T13:50:47.7354406Z [✖] https://www.youtube.com/c/Overleaf
2026-02-08T13:50:47.7354720Z 
2026-02-08T13:50:47.7354899Z 72 links checked.
2026-02-08T13:50:47.7355089Z 
2026-02-08T13:50:47.7355219Z ERROR: 2 dead links found!
2026-02-08T13:50:47.7356064Z [✖] https://tecdigital.tec.ac.cr/revistamatematica/Libros/LATEX/LaTeX_2014.pdf → Status: 404
2026-02-08T13:50:47.7356931Z [✖] https://www.youtube.com/c/Overleaf → Status: 404
2026-02-08T13:50:47.7357297Z 
2026-02-08T13:50:47.7357420Z FILE: ./CLAUDE.md
2026-02-08T13:50:47.7357579Z 
2026-02-08T13:50:47.7357989Z 0 links checked.
2026-02-08T13:50:47.7358175Z 
2026-02-08T13:50:47.7358252Z FILE: ./cls/README.md
2026-02-08T13:50:47.7358738Z [✖] https://ctan.org/pkg/interface3
2026-02-08T13:50:47.7359234Z 
2026-02-08T13:50:47.7359365Z 4 links checked.
2026-02-08T13:50:47.7359563Z 
2026-02-08T13:50:47.7359696Z ERROR: 1 dead links found!
2026-02-08T13:50:47.7360405Z [✖] https://ctan.org/pkg/interface3 → Status: 404
2026-02-08T13:50:47.7360784Z 
2026-02-08T13:50:47.7361147Z [0;33m=========================================================================[0m
