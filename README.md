# AI Agent Project

## Overview
This project consists of an AI agent service that interacts with an Ollama-based model server. It is containerized using Docker and managed with Docker Compose.

## Project Structure
```
├── agent_service/           # AI agent service
│   ├── app.py              # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Dockerfile for the agent service
├── ollama_server/          # Ollama model service
│   ├── ollama_server.py    # Server script to run Ollama
│   ├── Dockerfile          # Dockerfile for the Ollama service
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # Project documentation
```

## Prerequisites
- Docker & Docker Compose installed
- Python 3.11

## Installation & Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/ai_agent_project.git
   cd ai_agent_project
   ```

2. **Build & Start the Services**
   ```sh
   docker-compose up --build -d
   ```

3. **Check Running Containers**
   ```sh
   docker ps
   ```

## Usage
- **Test if Ollama is running:**
  ```sh
  curl http://localhost:11434/health
  ```
- **Access the AI Agent API:**
  ```sh
  curl http://localhost:5000
  ```

 - **Access from API URL:**
 ```
 http://localhost:5000/docs#/default/analyze_text_analyze_post

response will be like below.

{
  "classification": "<think>\nOkay, so I need to figure out how to classify this text into one of the given categories: News, Blog, Research, or Other. The text says, \"Student can learn coding from gpt.\" Hmm, let me break this down.\n\nFirst, I should understand what each category means. News is usually about recent events, updates, or information that's current and relevant. A blog would be a website where people write about various topics, often with opinions or analysis. Research might involve academic studies or data collection. Other could be anything not fitting into the above categories.\n\nLooking at the text again: \"Student can learn coding from gpt.\" It seems like it's talking about an educational resource—specifically, GPT (which stands for General-Purpose Computing Team) providing learning materials on coding. So, is this news? Probably not because it's not a recent event or current information.\n\nIs it a blog? Well, blogs are usually more about writing and can cover various topics, but in this case, the text seems like it's promoting something specific—GPT offering coding education. It doesn't sound like a typical blog post; it might be more of an announcement or a recommendation.\n\nResearch could involve academic studies, but here it's not about research findings or data analysis. It's more about providing educational content to students.\n\nSo, putting this together, the text is promoting a service (GPT) that offers learning resources on coding for students. This seems like a news item because it's introducing a new product or service aimed at education. It's not just any general information; it's specifically about an educational resource.\n\nI should make sure I'm not missing anything else. Could it be Other? Well, \"Other\" is usually reserved for things that don't fit into the other categories. Since this isn't news, a blog post, or research, it fits better as News because it's introducing something new in the field of education technology.\n\nI think that makes sense. So, the classification would be News.\n</think>\n\nThe text \"Student can learn coding from gpt.\" is classified as **News**. It introduces an educational resource provided by GPT (General-Purpose Computing Team) aimed at helping students with coding learning.",
  "entities": [
    "<think>\nOkay",
    "so I need to extract all entities from the given text. The text is \"Student can learn coding from gpt.\" Let me break this down step by step.\n\nFirst",
    "I should understand what an entity is in this context. From the previous example",
    "it seems like entities include people",
    "organizations",
    "and locations. So",
    "I'll look for names of people",
    "companies",
    "or places mentioned here.\n\nLooking at the text: \"Student can learn coding from gpt.\" The words are \"student,\" \"coding,\" \"gpt.\" Now",
    "\"student\" is a person",
    "so that's one entity. \"Coding\" could refer to something specific",
    "but in this context",
    "it's likely just an adjective describing what someone does. So maybe I shouldn't consider it as an entity unless it's explicitly mentioned.\n\nNext",
    "\"gpt.\" The \".gpt.\" part might be a typo or code for GPT-3. But the main part is \"gpt,\" which could refer to a company or organization. If I'm following the previous example",
    "entities are person",
    "organization",
    "location. So if \"gpt\" refers to a company",
    "that would count as an entity.\n\nWait",
    "but in the text",
    "it's written as \"gpt.\" without any additional context. It might be safer to assume that \"gpt\" is just a name or identifier for a company. Alternatively",
    "maybe it's a typo and should be \"GPT,\" which could refer to a specific company or technology.\n\nI'm not entirely sure about the meaning of \"gpt.\" If I consider it as an organization",
    "then yes",
    "it would count. But if it's just a name without any context",
    "perhaps it doesn't qualify. However",
    "in the previous example",
    "entities were person",
    "organization",
    "location. So maybe \"gpt\" is considered an entity because it's a company or a brand.\n\nAlternatively",
    "I could consider that \"gpt.\" might be part of a larger phrase like \"GPT-4,\" but without more context",
    "it's hard to tell. Since the text doesn't specify any other information about GPT",
    "I think it's reasonable to include it as an entity if it refers to a company or organization.\n\nSo",
    "putting it all together: entities are \"student\" (person)",
    "and \"gpt.\" (organization). Wait",
    "but in the previous example",
    "there was also \"location,\" but that wasn't present here. So maybe only person and organization.\n\nWait again",
    "let me check the text again. It's just \"Student can learn coding from gpt.\" No other locations mentioned. So perhaps only \"student\" is a person",
    "and \"gpt.\" could be an organization or a brand name.\n\nAlternatively",
    "if \"gpt\" refers to GPT-3",
    "which is a specific model of AI developed by Google",
    "then it would count as an entity. But without more context",
    "I'm not sure. Maybe the safest assumption is that \"gpt\" is just a name and doesn't qualify as an entity.\n\nSo",
    "final entities: person (student) and organization (gpt).\n</think>\n\nentities: student",
    "gpt"
  ],
  "summary": "<think>\nOkay, so I need to summarize the given text into one sentence. The original text says, \"Student can learn coding from gpt.\" Hmm, let me break this down.\n\nFirst, the main idea is about students learning coding. The key term here is \"coding,\" which refers to writing programs or algorithms. Then there's \"from GPT,\" which I think stands for General-Purpose Computing Processing Unit. That's a hardware component used in computers and other devices to perform calculations.\n\nSo putting it together, the sentence should convey that students can learn coding using GPT tools. But wait, is \"GPT\" the correct term? Or should it be \"General-Purpose Processor\"? I think both are acceptable, but maybe \"General-Purpose Computing Processing Unit\" sounds more technical and precise.\n\nLet me check if there's a better way to phrase this without losing meaning. Maybe something like \"students can learn coding using GPT tools.\" That seems straightforward. Alternatively, could it be \"students can learn coding with GPT-based tools\"? Both are fine, but the first one is simpler.\n\nI should make sure that the summary captures both the purpose (learning coding) and the tool used (GPT). So, I think the best way is to say students can learn coding using GPT tools. That's concise and clear.\n</think>\n\nStudents can learn coding using GPT-based tools."
}
```

## Troubleshooting
- If the containers fail to start, check logs:
  ```sh
  docker logs ollama_server
  docker logs agent_service
  ```
- Restart the services:
  ```sh
  docker-compose down --volumes
  docker-compose up -d
  ```

## License
MIT License

