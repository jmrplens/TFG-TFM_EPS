2026-02-08T12:43:14.3820468Z ##[group]Run gaurav-nelson/github-action-markdown-link-check@v1
2026-02-08T12:43:14.3820851Z with:
2026-02-08T12:43:14.3821028Z   use-quiet-mode: yes
2026-02-08T12:43:14.3821235Z   config-file: .github/mlc_config.json
2026-02-08T12:43:14.3821481Z   use-verbose-mode: no
2026-02-08T12:43:14.3821668Z   folder-path: .
2026-02-08T12:43:14.3821867Z   max-depth: -1
2026-02-08T12:43:14.3822054Z   check-modified-files-only: no
2026-02-08T12:43:14.3822276Z   base-branch: master
2026-02-08T12:43:14.3822455Z   file-extension: .md
2026-02-08T12:43:14.3822634Z env:
2026-02-08T12:43:14.3822790Z   TEXLIVE_VERSION: 2025
2026-02-08T12:43:14.3822975Z ##[endgroup]
2026-02-08T12:43:14.3931339Z ##[command]/usr/bin/docker run --name c6072e19f0887e7404fdb9de6f48d80ab9660_a7d80f --label 5c6072 --workdir /github/workspace --rm -e "TEXLIVE_VERSION" -e "INPUT_USE-QUIET-MODE" -e "INPUT_CONFIG-FILE" -e "INPUT_USE-VERBOSE-MODE" -e "INPUT_FOLDER-PATH" -e "INPUT_MAX-DEPTH" -e "INPUT_CHECK-MODIFIED-FILES-ONLY" -e "INPUT_BASE-BRANCH" -e "INPUT_FILE-EXTENSION" -e "INPUT_FILE-PATH" -e "HOME" -e "GITHUB_JOB" -e "GITHUB_REF" -e "GITHUB_SHA" -e "GITHUB_REPOSITORY" -e "GITHUB_REPOSITORY_OWNER" -e "GITHUB_REPOSITORY_OWNER_ID" -e "GITHUB_RUN_ID" -e "GITHUB_RUN_NUMBER" -e "GITHUB_RETENTION_DAYS" -e "GITHUB_RUN_ATTEMPT" -e "GITHUB_ACTOR_ID" -e "GITHUB_ACTOR" -e "GITHUB_WORKFLOW" -e "GITHUB_HEAD_REF" -e "GITHUB_BASE_REF" -e "GITHUB_EVENT_NAME" -e "GITHUB_SERVER_URL" -e "GITHUB_API_URL" -e "GITHUB_GRAPHQL_URL" -e "GITHUB_REF_NAME" -e "GITHUB_REF_PROTECTED" -e "GITHUB_REF_TYPE" -e "GITHUB_WORKFLOW_REF" -e "GITHUB_WORKFLOW_SHA" -e "GITHUB_REPOSITORY_ID" -e "GITHUB_TRIGGERING_ACTOR" -e "GITHUB_WORKSPACE" -e "GITHUB_ACTION" -e "GITHUB_EVENT_PATH" -e "GITHUB_ACTION_REPOSITORY" -e "GITHUB_ACTION_REF" -e "GITHUB_PATH" -e "GITHUB_ENV" -e "GITHUB_STEP_SUMMARY" -e "GITHUB_STATE" -e "GITHUB_OUTPUT" -e "RUNNER_OS" -e "RUNNER_ARCH" -e "RUNNER_NAME" -e "RUNNER_ENVIRONMENT" -e "RUNNER_TOOL_CACHE" -e "RUNNER_TEMP" -e "RUNNER_WORKSPACE" -e "ACTIONS_RUNTIME_URL" -e "ACTIONS_RUNTIME_TOKEN" -e "ACTIONS_CACHE_URL" -e "ACTIONS_RESULTS_URL" -e "ACTIONS_ORCHESTRATION_ID" -e GITHUB_ACTIONS=true -e CI=true -v "/var/run/docker.sock":"/var/run/docker.sock" -v "/home/runner/work/_temp":"/github/runner_temp" -v "/home/runner/work/_temp/_github_home":"/github/home" -v "/home/runner/work/_temp/_github_workflow":"/github/workflow" -v "/home/runner/work/_temp/_runner_file_commands":"/github/file_commands" -v "/home/runner/work/TFG-TFM_EPS/TFG-TFM_EPS":"/github/workspace" 5c6072:e19f0887e7404fdb9de6f48d80ab9660  "yes" "no" ".github/mlc_config.json" "." "-1" "no" "master" ".md" ""
2026-02-08T12:43:16.4248154Z npm warn deprecated har-validator@5.1.5: this library is no longer supported
2026-02-08T12:43:16.4940188Z npm warn deprecated uuid@3.4.0: Please upgrade  to version 7 or higher.  Older versions may use Math.random() in certain circumstances, which is known to be problematic.  See https://v8.dev/blog/math-random for details.
2026-02-08T12:43:16.5054476Z npm warn deprecated request@2.88.2: request has been deprecated, see https://github.com/request/request/issues/3142
2026-02-08T12:43:16.7444681Z 
2026-02-08T12:43:16.7447250Z added 65 packages in 2s
2026-02-08T12:43:16.7448845Z 
2026-02-08T12:43:16.7449017Z 5 packages are looking for funding
2026-02-08T12:43:16.7450551Z   run `npm fund` for details
2026-02-08T12:43:16.8158526Z [0;34mCannot find [0;33m.github/mlc_config.json[0m
2026-02-08T12:43:16.8159615Z [0;33mNOTE: See https://github.com/tcort/markdown-link-check#config-file-format to know more about
2026-02-08T12:43:16.8160691Z customizing markdown-link-check by using a configuration file.[0m
2026-02-08T12:43:16.8161379Z [0;34mUSE_QUIET_MODE: yes[0m
2026-02-08T12:43:16.8161914Z [0;34mUSE_VERBOSE_MODE: no[0m
2026-02-08T12:43:16.8163840Z [0;34mFOLDER_PATH: .[0m
2026-02-08T12:43:16.8164556Z [0;34mMAX_DEPTH: -1[0m
2026-02-08T12:43:16.8165348Z [0;34mCHECK_MODIFIED_FILES: no[0m
2026-02-08T12:43:16.8170046Z [0;34mFILE_EXTENSION: .md[0m
2026-02-08T12:43:16.8177804Z + find . -name '*.md' -not -path './node_modules/*' -exec markdown-link-check '{}' -q ';'
2026-02-08T12:43:16.8179979Z [0;34mFILE_PATH: [0m
2026-02-08T12:44:15.2296982Z + set +x
2026-02-08T12:44:15.2306159Z [0;33m=========================> MARKDOWN LINK CHECK <=========================[0m
2026-02-08T12:44:15.2315375Z 
2026-02-08T12:44:15.2316292Z FILE: ./CHANGELOG.md
2026-02-08T12:44:15.2318723Z 
2026-02-08T12:44:15.2318880Z 2 links checked.
2026-02-08T12:44:15.2319091Z 
2026-02-08T12:44:15.2319206Z FILE: ./sty/README.md
2026-02-08T12:44:15.2319407Z 
2026-02-08T12:44:15.2319523Z 4 links checked.
2026-02-08T12:44:15.2319713Z 
2026-02-08T12:44:15.2319842Z FILE: ./CONTRIBUTING.md
2026-02-08T12:44:15.2324078Z (node:41) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2325010Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2325469Z 
2026-02-08T12:44:15.2325757Z 10 links checked.
2026-02-08T12:44:15.2325932Z 
2026-02-08T12:44:15.2326087Z FILE: ./.herramientas/README.md
2026-02-08T12:44:15.2326625Z 
2026-02-08T12:44:15.2326727Z 0 links checked.
2026-02-08T12:44:15.2326894Z 
2026-02-08T12:44:15.2327057Z FILE: ./.github/copilot-instructions.md
2026-02-08T12:44:15.2327372Z 
2026-02-08T12:44:15.2327474Z 0 links checked.
2026-02-08T12:44:15.2327659Z 
2026-02-08T12:44:15.2327840Z FILE: ./.github/PULL_REQUEST_TEMPLATE.md
2026-02-08T12:44:15.2328145Z 
2026-02-08T12:44:15.2328246Z 0 links checked.
2026-02-08T12:44:15.2328416Z 
2026-02-08T12:44:15.2328540Z FILE: ./recursos/figuras/README.md
2026-02-08T12:44:15.2328787Z 
2026-02-08T12:44:15.2328891Z 0 links checked.
2026-02-08T12:44:15.2329065Z 
2026-02-08T12:44:15.2329170Z FILE: ./AGENTS.md
2026-02-08T12:44:15.2329352Z 
2026-02-08T12:44:15.2329467Z 0 links checked.
2026-02-08T12:44:15.2329635Z 
2026-02-08T12:44:15.2329742Z FILE: ./README.md
2026-02-08T12:44:15.2330354Z (node:107) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2331256Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2332109Z [✖] https://www.gnu.org/licenses/gpl-3.0
2026-02-08T12:44:15.2332697Z [✖] https://tex.stackexchange.com/
2026-02-08T12:44:15.2333259Z [✖] https://pgfplots.sourceforge.io/
2026-02-08T12:44:15.2333567Z 
2026-02-08T12:44:15.2333682Z 43 links checked.
2026-02-08T12:44:15.2333861Z 
2026-02-08T12:44:15.2333987Z ERROR: 3 dead links found!
2026-02-08T12:44:15.2334559Z [✖] https://www.gnu.org/licenses/gpl-3.0 → Status: 403
2026-02-08T12:44:15.2335200Z [✖] https://tex.stackexchange.com/ → Status: 403
2026-02-08T12:44:15.2336127Z [✖] https://pgfplots.sourceforge.io/ → Status: 403
2026-02-08T12:44:15.2336476Z 
2026-02-08T12:44:15.2336619Z FILE: ./docs/BIBLIOGRAFIA.md
2026-02-08T12:44:15.2337299Z (node:118) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2338224Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2338964Z [✖] https://scholar.google.com/
2026-02-08T12:44:15.2339271Z 
2026-02-08T12:44:15.2339398Z 87 links checked.
2026-02-08T12:44:15.2339592Z 
2026-02-08T12:44:15.2339733Z ERROR: 1 dead links found!
2026-02-08T12:44:15.2340233Z [✖] https://scholar.google.com/ → Status: 403
2026-02-08T12:44:15.2340578Z 
2026-02-08T12:44:15.2340705Z FILE: ./docs/AUDIT_2025.md
2026-02-08T12:44:15.2340933Z 
2026-02-08T12:44:15.2341045Z 0 links checked.
2026-02-08T12:44:15.2341221Z 
2026-02-08T12:44:15.2341381Z FILE: ./docs/IMAGENES_SUBFIGURAS.md
2026-02-08T12:44:15.2342085Z (node:140) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2343024Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2343507Z 
2026-02-08T12:44:15.2343618Z 77 links checked.
2026-02-08T12:44:15.2343812Z 
2026-02-08T12:44:15.2343952Z FILE: ./docs/ACCESIBILIDAD.md
2026-02-08T12:44:15.2344521Z (node:151) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2345545Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2346530Z [✖] https://www.adobe.com/acrobat
2026-02-08T12:44:15.2347129Z [✖] https://www.overleaf.com/learn/latex/Accessibility
2026-02-08T12:44:15.2348135Z [✖] https://esail.tamu.edu/faculty-tutorials/accessible-latex-pdf-ua-2-overleaf-2025/
2026-02-08T12:44:15.2348758Z 
2026-02-08T12:44:15.2348890Z 21 links checked.
2026-02-08T12:44:15.2349098Z 
2026-02-08T12:44:15.2349216Z ERROR: 3 dead links found!
2026-02-08T12:44:15.2349705Z [✖] https://www.adobe.com/acrobat → Status: 0
2026-02-08T12:44:15.2350422Z [✖] https://www.overleaf.com/learn/latex/Accessibility → Status: 404
2026-02-08T12:44:15.2351448Z [✖] https://esail.tamu.edu/faculty-tutorials/accessible-latex-pdf-ua-2-overleaf-2025/ → Status: 403
2026-02-08T12:44:15.2352111Z 
2026-02-08T12:44:15.2352263Z FILE: ./docs/REFERENCIAS_CRUZADAS.md
2026-02-08T12:44:15.2352977Z (node:162) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2354124Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2354611Z 
2026-02-08T12:44:15.2354736Z 69 links checked.
2026-02-08T12:44:15.2354933Z 
2026-02-08T12:44:15.2355084Z FILE: ./docs/README.md
2026-02-08T12:44:15.2355961Z (node:173) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2356643Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2357041Z 
2026-02-08T12:44:15.2357115Z 13 links checked.
2026-02-08T12:44:15.2357304Z 
2026-02-08T12:44:15.2357434Z FILE: ./docs/TABLAS.md
2026-02-08T12:44:15.2358096Z (node:184) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2359055Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2359563Z 
2026-02-08T12:44:15.2359693Z 89 links checked.
2026-02-08T12:44:15.2359899Z 
2026-02-08T12:44:15.2360067Z FILE: ./docs/TEXTO_LISTAS.md
2026-02-08T12:44:15.2360731Z (node:195) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2361657Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2362195Z 
2026-02-08T12:44:15.2362340Z 94 links checked.
2026-02-08T12:44:15.2362551Z 
2026-02-08T12:44:15.2362687Z FILE: ./docs/CODIGO_FUENTE.md
2026-02-08T12:44:15.2363236Z (node:206) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2364236Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2364611Z 
2026-02-08T12:44:15.2364750Z 72 links checked.
2026-02-08T12:44:15.2364936Z 
2026-02-08T12:44:15.2365083Z FILE: ./docs/FIGURAS_GRAFICAS.md
2026-02-08T12:44:15.2365936Z (node:217) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2366888Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2367450Z 
2026-02-08T12:44:15.2367575Z 94 links checked.
2026-02-08T12:44:15.2367768Z 
2026-02-08T12:44:15.2367929Z FILE: ./docs/COMPONENTES.md
2026-02-08T12:44:15.2368525Z (node:228) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2369149Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2369432Z 
2026-02-08T12:44:15.2369502Z 118 links checked.
2026-02-08T12:44:15.2369640Z 
2026-02-08T12:44:15.2369780Z FILE: ./docs/AI_CONTEXT.md
2026-02-08T12:44:15.2370254Z (node:239) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2371119Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2371402Z 
2026-02-08T12:44:15.2371477Z 60 links checked.
2026-02-08T12:44:15.2371655Z 
2026-02-08T12:44:15.2371782Z FILE: ./docs/GLOSARIOS_ACRONIMOS.md
2026-02-08T12:44:15.2372452Z (node:250) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2373117Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2373491Z 
2026-02-08T12:44:15.2373560Z 73 links checked.
2026-02-08T12:44:15.2373668Z 
2026-02-08T12:44:15.2373751Z FILE: ./docs/ECUACIONES.md
2026-02-08T12:44:15.2374117Z (node:261) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2374618Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2375135Z [✖] https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols
2026-02-08T12:44:15.2375375Z 
2026-02-08T12:44:15.2375443Z 125 links checked.
2026-02-08T12:44:15.2375707Z 
2026-02-08T12:44:15.2375841Z ERROR: 1 dead links found!
2026-02-08T12:44:15.2376487Z [✖] https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols → Status: 403
2026-02-08T12:44:15.2376972Z 
2026-02-08T12:44:15.2377125Z FILE: ./docs/GUIA_PRINCIPIANTES.md
2026-02-08T12:44:15.2378070Z (node:272) [DEP0176] DeprecationWarning: fs.R_OK is deprecated, use fs.constants.R_OK instead
2026-02-08T12:44:15.2379033Z (Use `node --trace-deprecation ...` to show where the warning was created)
2026-02-08T12:44:15.2380007Z [✖] https://tecdigital.tec.ac.cr/revistamatematica/Libros/LATEX/LaTeX_2014.pdf
2026-02-08T12:44:15.2380567Z [✖] https://www.youtube.com/c/Overleaf
2026-02-08T12:44:15.2380863Z 
2026-02-08T12:44:15.2380943Z 72 links checked.
2026-02-08T12:44:15.2381053Z 
2026-02-08T12:44:15.2381128Z ERROR: 2 dead links found!
2026-02-08T12:44:15.2381588Z [✖] https://tecdigital.tec.ac.cr/revistamatematica/Libros/LATEX/LaTeX_2014.pdf → Status: 404
2026-02-08T12:44:15.2382088Z [✖] https://www.youtube.com/c/Overleaf → Status: 404
2026-02-08T12:44:15.2382313Z 
2026-02-08T12:44:15.2382380Z FILE: ./CLAUDE.md
2026-02-08T12:44:15.2382492Z 
2026-02-08T12:44:15.2382558Z 0 links checked.
2026-02-08T12:44:15.2382673Z 
2026-02-08T12:44:15.2382744Z FILE: ./cls/README.md
2026-02-08T12:44:15.2383016Z [✖] https://ctan.org/pkg/interface3
2026-02-08T12:44:15.2383193Z 
2026-02-08T12:44:15.2383259Z 4 links checked.
2026-02-08T12:44:15.2383361Z 
2026-02-08T12:44:15.2383444Z ERROR: 1 dead links found!
2026-02-08T12:44:15.2383723Z [✖] https://ctan.org/pkg/interface3 → Status: 404
2026-02-08T12:44:15.2383930Z 
2026-02-08T12:44:15.2384111Z [0;33m=========================================================================[0m
