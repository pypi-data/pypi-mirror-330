`python3 main.py` 

```
usage: examples:
        # 初始化配置信息 
        ylz_langchain reset 

        # 启动大语言模型对话
        ylz_langchain start --mode chat
        
        # 测试neo4j
        ylz_langchain neo4j start
       [-h] --mode {llm,chat,prompt,loader,runnable,tools,rag,outputParser,graph,agent,info} [--llm_key LLM_KEY] [--embedding_key EMBEDDING_KEY]
       [--llm_model LLM_MODEL] [--embedding_model EMBEDDING_MODEL] [--message MESSAGE] [--user_id USER_ID] [--conversation_id CONVERSATION_ID] [--url URL]
       [--depth DEPTH] [--rag_indexname RAG_INDEXNAME] [--chat_dbname CHAT_DBNAME] [--query_dbname QUERY_DBNAME] [--docx DOCX] [--pptx PPTX] [--pdf PDF]
       [--glob GLOB] [--websearch {tavily,duckduckgo,serpapi}] [--size SIZE] [--graph {stand,life,engineer,db,selfrag,test,stock}] [--fake_size FAKE_SIZE]
       [--batch BATCH]

options:
  -h, --help            show this help message and exit
  --mode {llm,chat,prompt,loader,runnable,tools,rag,outputParser,graph,agent,info}
                        测试内容
  --llm_key LLM_KEY     语言模型标识，例如：LLM.DEEPSEEK
  --embedding_key EMBEDDING_KEY
                        嵌入模型标识，例如：EMBEDDING.TOGETHER
  --llm_model LLM_MODEL
                        语言模型model
  --embedding_model EMBEDDING_MODEL
                        嵌入模型model
  --message MESSAGE     input message
  --user_id USER_ID     user_id,example: alice
  --conversation_id CONVERSATION_ID
                        conversation_id,example: 123
  --url URL             仅rag,loader使用,下载的URL地址
  --depth DEPTH         仅rag使用,下载的深度，默认为1
  --rag_indexname RAG_INDEXNAME
                        保存的向量索引表,格式为<es|faiss|chroma>:<indexname>
  --chat_dbname CHAT_DBNAME
                        保存的对话数据库
  --query_dbname QUERY_DBNAME
                        测试查询的数据库，默认Chinook.db
  --docx DOCX           docx文档文件名
  --pptx PPTX           pptx文档文件名
  --pdf PDF             pdf文档文件名
  --glob GLOB           当前目录下的glob匹配的文件
  --websearch {tavily,duckduckgo,serpapi}
                        websearch的工具
  --size SIZE           文档分隔的size
  --graph {stand,life,engineer,db,selfrag,test,stock}
                        内置graph的类型
  --fake_size FAKE_SIZE
                        使用fake embeding的size，当fake_size>0是使用fake embeding，并且维度为fake_size
  --batch BATCH         使用生成embeding时的以batch为度量显示进度，默认分隔为10批

  ```