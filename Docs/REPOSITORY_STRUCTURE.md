# Repository Structure

```
dynasty-politics-india/
│
├── .env                                    # Environment variables (API keys)
├── .gitignore                              # Git ignore rules
├── readme.md                               # Project documentation
│
├── ACPC_json_dumps/                        # API Response Storage
│   ├── outputAC_jsonl_batch/               # AC elections API responses (31 AC elections)
│   │   ├── sync_output_AndhraPradesh.jsonl
│   │   ├── sync_output_ArunachalPradesh.jsonl
│   │   └── ... (31 state files)
│   ├── outputPC_jsonl_batch/               # PC elections API responses (18 PC elections)
│   │   ├── sync_output_LokSabha1952.jsonl
│   │   ├── sync_output_LokSabha1957.jsonl
│   │   └── ... (18 election files)
│   └── test run for jsonl/                 # Test runs
│       ├── PromptAC_output_test001.jsonl
│       └── promptPC_output__test001.jsonl
│
├── Batch api calls/                        # Batch API Management
│   ├── Azure openAI endpoint/              # Azure-specific batch operations
│   │   ├── createbatch.py
│   │   ├── retrieve batch.py
│   │   ├── trackbatch.py
│   │   └── uploadbatch.py
│   └── OpenAI endpoint/                    # OpenAI-specific batch operations
│       ├── createbatch1.py
│       ├── retrievebatch1.py
│       ├── trackbatch1.py
│       ├── uploadbatch1.py
│       ├── cancelbatch1.py
│       ├── listbatches1.py
│       └── error_for_batch1.py
│
├── Creating and Parsing Files/             # Data Transformation Scripts
│   ├── create5000_prompts_json_file.py     # Generate batch prompts
│   ├── createCSV.py                        # CSV generation utilities
│   ├── createJSONL.py                      # JSONL format conversion
│   ├── createTXT.py                        # Text file generation
│   ├── CSVcombiner.py                      # Combine multiple CSVs
│   ├── jsondumpsCOMBINED.py                # Parse combined JSON dumps
│   └── jsondumpsSINGLE_parser.py           # Parse individual JSON responses
│
├── Data/                                   # Processed Datasets
│   ├── Final parsed tables/
│   │   ├── family tables(AC recent)/       # AC dynasty data (30 states)
│   │   │   ├── AndhraPradeshAC_family_recent.csv
│   │   │   ├── ArunachalPradeshAC_family_recent.csv
│   │   │   └── ... (28 more state files)
│   │   ├── Family tables(PC ALL)/          # PC dynasty data (18 elections)
│   │   │   ├── LokSabha1952family_recent.csv
│   │   │   ├── LokSabha1957family_recent.csv
│   │   │   └── ... (16 more election files)
│   │   ├── Sources tables(AC recent)/      # AC source verification (30 files)
│   │   │   ├── AndhraPradeshAC_sources_recent.csv
│   │   │   └── ...
│   │   └── Sources tables(PC ALL)/         # PC source verification 
│   │       ├── LokSabha1952sources_recent.csv
│   │       └── ...
│   ├── log tables data/                    # Processing Logs
│   │   ├── AC recent logs/                 # AC logs 
│   │   │   ├── AndhraPradeshAC_logs_recent.txt
│   │   │   └── ...
│   │   └── PC recent logs/                 # PC logs 
│   │       ├── LokSabha1952logs.txt
│   │       └── ...
│   └── prompt errors/                      # API Error Tracking
│       ├── AC recent errors/               # AC errors (30 files)
│       │   ├── AndhraPradeshAC_errors_recent.jsonl
│       │   └── ...
│       └── PC all errors/                  # PC errors (18 files)
│           ├── LokSabha1952errors.jsonl
│           └── ...
│
├── ENV endpoints/                          # Environment Configuration
│   └── all_codes.py                        # Endpoint configuration utilities
│
├── Multithreading Azure OpenAI/            # Multi-threaded AI Processing
│   ├── batch_promptsAC_template.py         # AC prompt template
│   ├── batch_promptsPC_template.py         # PC prompt template
│   ├── multiAC_split.py                    # Multi-key AC processing
│   ├── multiPC_combined.py                 # Multi-key PC processing
│   ├── multiPC_combined_StateNameFromFolder_test.py
│   ├── Multitreader Azure endpoint.py      # Multi-key utilities
│   ├── StructuredOutputSyncAC.py           # Pydantic output for AC
│   ├── StructuredOutputSyncPC.py           # Pydantic output for PC
│   └── __pycache__/                        # Python cache
│
├── SINGLE PROMPT API key/                  # Single-prompt API Testing
│   ├── AzureLLMprompt.py                   # Azure OpenAI single prompt
│   ├── OpenAiLLMprompt.py                  # OpenAI single prompt
│   ├── StructuredOutputFinal.py            # Final structured output model
│   ├── StructuredOutputRelatives.py        # Relatives Pydantic output model
│   ├── StructuredOutputSources.py          # Sources Pydantic output model
│   ├── jsonformat.py                       # JSON formatting utilities
│   ├── jsonformat1.py                      # Alternative JSON formatter
│   ├── prompt_test_iterations.py           # Prompt testing iterations
│   └── __pycache__/                        # Python cache
│
├── Tables and UID keys/                    # UID Generation & Table Creation
│   ├── CreatorSingleTable.py               # Single table creator
│   ├── UIDcreatorCombinedPC.py             # PC combined UID generator
│   ├── UIDcreatorSplitAC.py                # AC split UID generator
│   └── UIDcreatorSplitPC.py                # PC split UID generator
│
├── Test files/                             # Testing Resources
│   ├── input_jsonl_batch/                  # Test input files
│   │   └── batch_input_test001.jsonl
│   ├── output_jsonl_batch/                 # Test output files
│   │   └── batch_output_test001.jsonl
│   └── Prompt trials/                      # Prompt testing
│       └── prompt_dry_run.py
│
└── Web scraping code/                      # Data Collection Scripts
    ├── normalized_scraping_ACPC/           # Unified scraping for AC and PC
    │   ├── main.py                         # Main scraper orchestrator
    │   ├── normalizing_columns.py          # Column normalization
    │   ├── normalizing_rows.py             # Row normalization
    │   ├── scraping_single_page.py         # Single page scraper
    │   ├── table_scraping.py               # Table extraction
    │   └── webdriver_code.py               # Selenium WebDriver setup
    ├── Web scraping for AC elections/      # AC-specific scraping
    │   ├── main.py
    │   ├── scraping_code.py
    │   └── WebDriver_code.py
    ├── Web scraping for PC elections/      # PC-specific scraping
    │   ├── main.py
    │   ├── scraping_code.py
    │   └── webdriver_code.py
    └── Web scraping for deets/             # Detailed candidate information
        ├── ipworkchecker.py
        ├── nullValue_fatherName_scrapper.py
        └── original_fatherNAME_scrapper.py
```
