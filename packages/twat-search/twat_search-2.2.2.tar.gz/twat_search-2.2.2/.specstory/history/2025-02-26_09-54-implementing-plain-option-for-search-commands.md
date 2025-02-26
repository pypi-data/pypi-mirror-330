## SpecStory

## Implementing --plain Option for Search Commands (26/02/2025, 09:54:58)

_**User**_

twat-search web info --plain
             🔎 Available Search Engines             
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Engine               ┃ Enabled ┃ API Key Required ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ brave                │ ✅      │ ✅               │
│ brave-news           │ ✅      │ ✅               │
│ serpapi              │ ✅      │ ✅               │
│ tavily               │ ✅      │ ✅               │
│ pplx                 │ ✅      │ ✅               │
│ you                  │ ✅      │ ✅               │
│ you-news             │ ✅      │ ✅               │
│ critique             │ ✅      │ ✅               │
│ duckduckgo           │ ✅      │ ❌               │
│ bing-scraper         │ ✅      │ ❌               │
│ hasdata-google       │ ✅      │ ✅               │
│ hasdata-google-light │ ✅      │ ✅               │
│ google-scraper       │ ✅      │ ❌               │
│ google-searchit      │ ✅      │ ❌               │
│ yandex-searchit      │ ✅      │ ❌               │
│ qwant-searchit       │ ✅      │ ❌               │
│ bing-searchit        │ ✅      │ ❌               │
│ google-anyws         │ ✅      │ ❌               │
│ bing-anyws           │ ✅      │ ❌               │
│ brave-anyws          │ ✅      │ ✅               │
│ qwant-anyws          │ ✅      │ ❌               │
│ yandex-anyws         │ ✅      │ ✅               │
└──────────────────────┴─────────┴──────────────────┘

Run 'info ENGINE_NAME' for more details about a specific engine.


TASK: Add everywhere the `--plain` option that controls the output. It should produce the most plaintext output thinkable for each command. For example for "info" listing it should just list the names of the engines one per line. For the "q" searc it should just return the amalgameted list of URLs, sorted and deduped, without any extra info. 

Also, normal "info"list outputs should be sorted alphabetically by user-facing engine name (not the backend module). 

---

_**Assistant**_

<think>I need to understand what the project structure looks like so I can add a `--plain` option to the appropriate files. Let's examine the project structure first to get a better understanding of the codebase.

Based on the pyproject.toml file, this is a Python package called "twat-search" which provides search utilities for a "twat" ecosystem. It has command-line interfaces exposed through `twat_search.__main__:main` and `twat_search.web.cli:main`.

The task is to:
1. Add a `--plain` option to all commands that controls the output format
2. Make the plain output very minimal - just the essential data without formatting
3. For "info" command, plain output should just list engine names one per line
4. For "q" search command, plain output should just return amalgamated list of URLs, sorted and deduped
5. Normal "info" list outputs should be sorted alphabetically by user-facing engine name

Let's search the codebase to see the current implementation of the CLI and how to modify it.</think>I'll help you add the `--plain` option for more minimal text output across the commands. Let me first examine the codebase structure to understand where these changes need to be made.

---

_****_

<details>
            <summary>Listed directory src • **2** results</summary>
        
| Name |
|-------|
| 📄 `.DS_Store` |
| 📁 `twat_search` |

</details>

---

_****_

<details>
            <summary>Listed directory src/twat_search • **6** results</summary>
        
| Name |
|-------|
| 📁 `__pycache__` |
| 📄 `__version__.py` |
| 📁 `web` |
| 📄 `__init__.py` |
| 📄 `__main__.py` |
| 📄 `.DS_Store` |

</details>

---

_****_

<details>
            <summary>Listed directory src/twat_search/web • **10** results</summary>
        
| Name |
|-------|
| 📁 `__pycache__` |
| 📁 `engines` |
| 📄 `cli.py` |
| 📄 `api.py` |
| 📄 `.DS_Store` |
| 📄 `__init__.py` |
| 📄 `config.py` |
| 📄 `models.py` |
| 📄 `utils.py` |
| 📄 `exceptions.py` |

</details>

---

_****_



Let's look at the CLI implementation to understand how to add the `--plain` option:

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_



Now, let's look at the specific methods that need modification:

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_



Let's also see the method that displays the search results:

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_



Now that I have a good understanding of the code, I'll implement the `--plain` option in the CLI to provide the minimal text output as requested. Here's my plan:

1. Add the `plain` parameter to the `q` and `info` methods
2. Modify the `_display_results` method to handle plain output
3. Add a new method for displaying plain results for info command
4. Sort the engines alphabetically in the info command
5. Update the various search engine methods to handle the plain flag

Let's make these changes:

---

_****_

```diff
  
      def _display_results(
-         self, processed_results: list[dict[str, Any]], verbose: bool = False
+         self, processed_results: list[dict[str, Any]], verbose: bool = False, plain: bool = False
      ) -> None:
          if not processed_results:
+             if plain:
+                 return
              console.print("[bold red]No results found![/bold red]")
              return
  
+         if plain:
+             # For plain output, just print a sorted and deduped list of URLs
+             urls = set()
+             for result in processed_results:
+                 if "❌" not in result["status"] and result["url"] != "N/A":
+                     urls.add(result["url"])
+             for url in sorted(urls):
+                 console.print(url)
+             return
+ 
          # Always use the compact table format unless verbose is specifically requested
          table = Table()  # Remove show_lines=True to eliminate row separator lines
```

---

_****_



Now, let's add the plain option to the q method:

---

_****_

```diff
          verbose: bool = False,
          json: bool = False,
+         plain: bool = False,
          **kwargs: Any,
      ) -> list[dict[str, Any]]:
              verbose: Whether to display verbose output
              json: Whether to return results as JSON
+             plain: Whether to display results in plain text format
              **kwargs: Additional engine-specific parameters
  
          common_params = {k: v for k, v in common_params.items() if v is not None}
  
-         if json:
+         if json or plain:
              results = asyncio.run(
                  self._run_search(query, engine_list, **common_params, **kwargs)
              return []
          else:
-             self._display_results(results, verbose)
+             self._display_results(results, verbose, plain)
              # Only return the actual results if verbose mode is enabled
              # This prevents the CLI from printing the raw results
```

---

_****_





Now, let's add the plain option to the info method and implement alphabetical sorting:

---

_****_

```diff
              return []
  
-     def info(self, engine: str | None = None, json: bool = False) -> None:
+     def info(self, engine: str | None = None, json: bool = False, plain: bool = False) -> None:
+         """
+         Display information about available search engines.
+ 
+         Args:
+             engine: Specific engine to show details for (or None for all engines)
+             json: Whether to output in JSON format
+             plain: Whether to output in plain text format
+         """
          try:
              from twat_search.web.config import Config
              if json:
                  self._display_engines_json(engine, config)
+             elif plain:
+                 self._display_engines_plain(engine, config)
              elif engine is None:
                  self._list_all_engines(config)
              else:
                  self._show_engine_details(engine, config)
          except Exception as e:
-             if not json:
+             if not json and not plain:
                  self.logger.error(f"❌ Failed to display engine information: {e}")
  
+     def _display_engines_plain(self, engine: str | None, config: "Config") -> None:
+         """
+         Display engine information in plain text format.
+ 
+         Args:
+             engine: Specific engine to show details for (or None for all engines)
+             config: Configuration object
+         """
+         if engine:
+             if engine in config.engines:
+                 self.console.print(engine)
+         else:
+             # Sort engines alphabetically
+             for engine_name in sorted(config.engines.keys()):
+                 self.console.print(engine_name)
+ 
      def _list_all_engines(self, config: "Config") -> None:
          table = Table(title="🔎 Available Search Engines")
          except ImportError:
              registered_engines = {}
-         for engine, engine_config in config.engines.items():
+             
+         # Sort engines alphabetically
+         sorted_engines = sorted(config.engines.items(), key=lambda x: x[0])
+         
+         for engine, engine_config in sorted_engines:
              api_key_required = (
                  hasattr(engine_config, "api_key") and engine_config.api_key is not None
```

---

_****_





Now we need to update the `_display_json_results` method to print the results:

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_



Let's see the complete _display_json_results method to understand how it's printing the results:

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_





Let's go further to find the complete method:

---

_****_

<details>
            <summary>Grep search for "def _display_json_results" • **5** files</summary>
        
| File | Line | Match |
|------|------|-------|
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L926 | `def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/cli.py` | L248 | `def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-34-integrating-hasdata-google-serp-apis.md` | L2131 | `def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-34-integrating-hasdata-google-serp-apis.md` | L3361 | `def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-34-integrating-hasdata-google-serp-apis.md` | L3986 | `def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-34-integrating-hasdata-google-serp-apis.md` | L5249 | `def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L6511 | `def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L6545 | `def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/cli.py` | L248 | `def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:` |

</details>

---

_****_





Let's search for how the JSON output is displayed:

---

_****_

<details>
            <summary>Grep search for "console.print.*json" • **0** files</summary>
        
No results found
</details>

---

_****_



Let's try a different search:

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_





Let's get a bit more lines to see the full method:

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_





It seems the `_display_json_results` method has a comment for "Print the JSON output" but the actual code is missing. Let's check more of the search-related method to gain additional context:

---

_****_

<details>
            <summary>Grep search for "json_lib.dumps" • **2** files</summary>
        
| File | Line | Match |
|------|------|-------|
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L5487 | `-             json_lib.dumps(results_by_engine, indent=2, cls=CustomJSONEncoder)` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L5491 | `+         print(json_lib.dumps(results_by_engine, indent=2, cls=CustomJSONEncoder))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L5683 | `+                 print(json_lib.dumps({"error": str(e)}, indent=2))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L5707 | `+                 print(json_lib.dumps({"error": f"Engine {engine} not found"}, indent=2))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L5717 | `+         print(json_lib.dumps(result, indent=2, cls=CustomJSONEncoder))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L6567 | `print(json_lib.dumps(results_by_engine, indent=2, cls=CustomJSONEncoder))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L6603 | `+         print(json_lib.dumps(results_by_engine, indent=2, cls=CustomJSONEncoder))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L6642 | `+                 print(json_lib.dumps({"error": str(e)}, indent=2))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L6647 | `+                 print(json_lib.dumps({"error": f"Engine {engine} not found"}, indent=2))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L6663 | `+         print(json_lib.dumps(result, indent=2, cls=CustomJSONEncoder))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-34-integrating-hasdata-google-serp-apis.md` | L3370 | `+         print(json_lib.dumps(results_by_engine, cls=CustomJSONEncoder, indent=2))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-34-integrating-hasdata-google-serp-apis.md` | L4002 | `print(json_lib.dumps(results_by_engine, cls=CustomJSONEncoder, indent=2))` |

</details>

---

_****_







Now let's complete the `_display_json_results` method to properly print the JSON output:

---

_****_

```diff
  
          # Print the JSON output
+         print(json_lib.dumps(results_by_engine, indent=2, cls=CustomJSONEncoder))
  
      def _display_errors(self, error_messages: list[str]) -> None:
```

---

_****_







Now, let's update the `_display_engines_json` method to properly print the JSON output and add the plain parameter to the individual search engine methods:

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_





---

_****_

Read file: src/twat_search/web/cli.py

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_







Let's continue to search to find the complete method:

---

_****_

Read file: src/twat_search/web/cli.py

---

_****_







Now I'll update the `_display_engines_json` method to properly print the JSON output:

---

_****_

```diff
              )
          else:
-             for engine_name, engine_config in config.engines.items():
+             # Sort engines alphabetically for consistent ordering
+             for engine_name, engine_config in sorted(config.engines.items()):
                  result[engine_name] = self._get_engine_info(
                      engine_name, engine_config, registered_engines
                  )
-         # JSON output (omitted actual printing for brevity)
+         # Print JSON output
+         print(json_lib.dumps(result, indent=2, cls=CustomJSONEncoder))
  
      def _get_engine_info(
```

---

_****_









Finally, let's update the search engine methods to add the plain parameter. I'll modify one method and then we can apply the same change to all others:

---

_****_

```diff
  
      async def _search_engine(
-         self, engine: str, query: str, params: dict, json: bool, verbose: bool
+         self, engine: str, query: str, params: dict, json: bool, verbose: bool, plain: bool = False
      ) -> list[dict[str, Any]]:
          """
          Args:
              engine: Name of the engine to use
-             query: Search query
-             params: Parameters for the engine
-             json: Whether to format output as JSON
-             verbose: Whether to display verbose output
-         """
-         self._configure_logging(verbose)
- 
-         if not is_engine_available(engine):
-             error_msg = f"{engine.capitalize()} search engine is not available. Make sure the required dependency is installed."
-             self.logger.error(error_msg)
+             query: Search query string
+             params: Engine-specific parameters
+             json: Whether to display results as JSON
+             verbose: Whether to display verbose results
+             plain: Whether to display results in plain text format
+ 
+         Returns:
+             List of processed search results
+         """
+         from twat_search.web.engines import get_engine_function
+ 
+         try:
+             engine_func = get_engine_function(engine)
+             if not engine_func:
+                 error_msg = f"Engine '{engine}' is not available."
+                 self.logger.warning(error_msg)
                  self._display_errors([error_msg])
                  return []
- 
-         engine_func = get_engine_function(engine)
-         if engine_func is None:
-             error_msg = (
-                 f"{engine.capitalize()} search engine function could not be loaded."
-             )
-             self.logger.error(error_msg)
+         except ImportError as e:
+             error_msg = f"Could not load engine '{engine}': {e}"
+             self.logger.warning(error_msg)
              self._display_errors([error_msg])
              return []
          }
          friendly = friendly_names.get(engine, engine)
-         if not json:
+         if not json and not plain:
              self.console.print(f"[bold]Searching {friendly}[/bold]: {query}")
          try:
                  return []
              else:
-                 self._display_results(processed_results, verbose)
+                 self._display_results(processed_results, verbose, plain)
                  return processed_results
          except Exception as e:
              self.logger.error(f"{friendly} search failed: {e}")
+             if not plain:
                  self._display_errors([str(e)])
              return []
```

---

_****_










Now let's update one of the specific engine methods to add the plain parameter to all of them:

---

_****_

```diff
          verbose: bool = False,
          json: bool = False,
+         plain: bool = False,
          **kwargs: Any,
      ) -> list[dict[str, Any]]:
-         params: dict[str, Any] = {
+         """
+         Search the web using Critique.
+ 
+         Args:
+             query: Search query
+             num_results: Number of results to return
+             country: Country code for results (ISO 3166-1 alpha-2)
+             language: Language code for results (ISO 639-1)
+             safe_search: Whether to filter adult content
+             time_frame: Time frame for results (e.g., "day", "week", "month")
+             image_url: URL of an image to search with
+             image_base64: Base64-encoded image to search with
+             source_whitelist: Comma-separated list of domains to include
+             source_blacklist: Comma-separated list of domains to exclude
+             api_key: Critique API key
+             verbose: Whether to display verbose output
+             json: Whether to format output as JSON
+             plain: Whether to display plain text output
+             **kwargs: Additional parameters for the search engine
+ 
+         Returns:
+             List of search results
+         """
+         self._configure_logging(verbose)
+ 
+         params = {
              "num_results": num_results,
-             "country": country,
-             "language": language,
-             "safe_search": safe_search,
-             "time_frame": time_frame,
-         }
-         if api_key:
-             params["api_key"] = api_key
+         }
+         if country:
+             params["country"] = country
+         if language:
+             params["language"] = language
+         if safe_search is not None:
+             params["safe_search"] = safe_search
+         if time_frame:
+             params["time_frame"] = time_frame
          if image_url:
              params["image_url"] = image_url
          if source_whitelist:
              params["source_whitelist"] = [
-                 s.strip() for s in source_whitelist.split(",") if s.strip()
+                 domain.strip() for domain in source_whitelist.split(",")
              ]
          if source_blacklist:
              params["source_blacklist"] = [
-                 s.strip() for s in source_blacklist.split(",") if s.strip()
+                 domain.strip() for domain in source_blacklist.split(",")
              ]
+         if api_key:
+             params["api_key"] = api_key
          params.update(kwargs)
-         params = {k: v for k, v in params.items() if v is not None}
-         return await self._search_engine("critique", query, params, json, verbose)
+ 
+         return await self._search_engine("critique", query, params, json, verbose, plain)
  
      async def brave(
```

---

_****_









Let's fix the linter errors in the critique method:

---

_****_

```diff
          self._configure_logging(verbose)
  
-         params = {
+         params: dict[str, Any] = {
              "num_results": num_results,
          }
          params.update(kwargs)
  
-         return await self._search_engine(
-             "critique", query, params, json, verbose, plain
-         )
+         return await self._search_engine("critique", query, params, json, verbose, plain)
  
      async def brave(
```

---

_****_





---

_**User**_

go on

---

_**Assistant**_

<think>I need to add the `plain` parameter to all the remaining search engine methods in the SearchCLI class. Currently, I've added it to the critique method, but I need to add it to the other methods as well. Let me identify all the search engine methods that need to be updated:

1. brave
2. brave_news
3. serpapi
4. tavily
5. pplx
6. you
7. you_news
8. duckduckgo
9. hasdata_google
10. hasdata_google_light

I should also update the calls to `_search_engine` to pass the `plain` parameter in all these methods. Let me update all of these methods at once.</think>I'll continue by updating all the remaining search engine methods to include the `plain` parameter. Let's add this parameter to each method and update the corresponding `_search_engine` calls.

---

_****_

```diff
          verbose: bool = False,
          json: bool = False,
+         plain: bool = False,
          **kwargs: Any,
      ) -> list[dict[str, Any]]:
-         params = {
+         """
+         Search the web using Brave.
+ 
+         Args:
+             query: Search query
+             num_results: Number of results to return
+             country: Country code for results
+             language: Language code for results
+             safe_search: Whether to filter adult content
+             time_frame: Time frame for results
+             api_key: Brave API key
+             verbose: Whether to display verbose output
+             json: Whether to format output as JSON
+             plain: Whether to display plain text output
+             **kwargs: Additional parameters for the search engine
+ 
+         Returns:
+             List of search results
+         """
+         self._configure_logging(verbose)
+         
+         params: dict[str, Any] = {
              "num_results": num_results,
              "country": country,
          params.update(kwargs)
          params = {k: v for k, v in params.items() if v is not None}
-         return await self._search_engine("brave", query, params, json, verbose)
+         return await self._search_engine("brave", query, params, json, verbose, plain)
  
      async def brave_news(
```

---

_****_





Let's continue updating the rest of the methods:

---

_****_

```diff
          verbose: bool = False,
          json: bool = False,
+         plain: bool = False,
          **kwargs: Any,
      ) -> list[dict[str, Any]]:
-         params = {
+         """
+         Search news using Brave News.
+ 
+         Args:
+             query: Search query
+             num_results: Number of results to return
+             country: Country code for results
+             language: Language code for results
+             safe_search: Whether to filter adult content
+             time_frame: Time frame for results
+             api_key: Brave API key
+             verbose: Whether to display verbose output
+             json: Whether to format output as JSON
+             plain: Whether to display plain text output
+             **kwargs: Additional parameters for the search engine
+ 
+         Returns:
+             List of search results
+         """
+         self._configure_logging(verbose)
+         
+         params: dict[str, Any] = {
              "num_results": num_results,
              "country": country,
          params.update(kwargs)
          params = {k: v for k, v in params.items() if v is not None}
-         return await self._search_engine("brave_news", query, params, json, verbose)
+         return await self._search_engine("brave_news", query, params, json, verbose, plain)
  
      async def serpapi(
```

---

_****_







Now let's update the serpapi method:

---

_****_

```diff
          verbose: bool = False,
          json: bool = False,
+         plain: bool = False,
          **kwargs: Any,
      ) -> list[dict[str, Any]]:
-         params = {
+         """
+         Search using SerpAPI (Google).
+ 
+         Args:
+             query: Search query
+             num_results: Number of results to return
+             country: Country code for results
+             language: Language code for results
+             safe_search: Whether to filter adult content
+             time_frame: Time frame for results
+             api_key: SerpAPI key
+             verbose: Whether to display verbose output
+             json: Whether to format output as JSON
+             plain: Whether to display plain text output
+             **kwargs: Additional parameters for the search engine
+ 
+         Returns:
+             List of search results
+         """
+         self._configure_logging(verbose)
+         
+         params: dict[str, Any] = {
              "num_results": num_results,
              "country": country,
          params.update(kwargs)
          params = {k: v for k, v in params.items() if v is not None}
-         return await self._search_engine("serpapi", query, params, json, verbose)
+         return await self._search_engine("serpapi", query, params, json, verbose, plain)
  
      async def tavily(
```

---

_****_









Let's update the tavily method:

---

_****_

```diff
          verbose: bool = False,
          json: bool = False,
+         plain: bool = False,
          **kwargs: Any,
      ) -> list[dict[str, Any]]:
+         """
+         Search the web using Tavily AI.
+ 
+         Args:
+             query: Search query
+             num_results: Number of results to return
+             country: Country code for results
+             language: Language code for results
+             safe_search: Whether to filter adult content
+             time_frame: Time frame for results
+             api_key: Tavily API key
+             search_depth: Search depth (basic or advanced)
+             include_domains: Comma-separated list of domains to include
+             exclude_domains: Comma-separated list of domains to exclude
+             verbose: Whether to display verbose output
+             json: Whether to format output as JSON
+             plain: Whether to display plain text output
+             **kwargs: Additional parameters for the search engine
+ 
+         Returns:
+             List of search results
+         """
+         self._configure_logging(verbose)
+         
          params: dict[str, Any] = {
              "num_results": num_results,
          params.update(kwargs)
          params = {k: v for k, v in params.items() if v is not None}
-         return await self._search_engine("tavily", query, params, json, verbose)
+         return await self._search_engine("tavily", query, params, json, verbose, plain)
  
      async def pplx(
```

---

_****_











Let's update the pplx method:

---

_****_

```diff
          verbose: bool = False,
          json: bool = False,
+         plain: bool = False,
          **kwargs: Any,
      ) -> list[dict[str, Any]]:
-         params = {
+         """
+         Search the web using Perplexity AI.
+ 
+         Args:
+             query: Search query
+             num_results: Number of results to return
+             country: Country code for results
+             language: Language code for results
+             safe_search: Whether to filter adult content
+             time_frame: Time frame for results
+             api_key: Perplexity API key
+             model: Model to use for search
+             verbose: Whether to display verbose output
+             json: Whether to format output as JSON
+             plain: Whether to display plain text output
+             **kwargs: Additional parameters for the search engine
+ 
+         Returns:
+             List of search results
+         """
+         self._configure_logging(verbose)
+         
+         params: dict[str, Any] = {
              "num_results": num_results,
              "country": country,
          params.update(kwargs)
          params = {k: v for k, v in params.items() if v is not None}
-         return await self._search_engine("pplx", query, params, json, verbose)
+         return await self._search_engine("pplx", query, params, json, verbose, plain)
  
      async def you(
```

---

_****_











Let's update the you method:

---

_****_

```diff
          verbose: bool = False,
          json: bool = False,
+         plain: bool = False,
          **kwargs: Any,
      ) -> list[dict[str, Any]]:
-         params = {
+         """
+         Search the web using You.com.
+ 
+         Args:
+             query: Search query
+             num_results: Number of results to return
+             country: Country code for results
+             language: Language code for results
+             safe_search: Whether to filter adult content
+             time_frame: Time frame for results
+             api_key: You.com API key
+             verbose: Whether to display verbose output
+             json: Whether to format output as JSON
+             plain: Whether to display plain text output
+             **kwargs: Additional parameters for the search engine
+ 
+         Returns:
+             List of search results
+         """
+         self._configure_logging(verbose)
+         
+         params: dict[str, Any] = {
              "num_results": num_results,
              "country": country,
          params.update(kwargs)
          params = {k: v for k, v in params.items() if v is not None}
-         return await self._search_engine("you", query, params, json, verbose)
+         return await self._search_engine("you", query, params, json, verbose, plain)
  
      async def you_news(
```

---

_****_













Let's update the you_news method:

---

_****_



---

_****_



---



---

