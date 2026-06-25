# Red-Team AI — JWT Forge + BOLA via Payload Splitting

Laboratório de segurança que demonstra como um **Agente A (red-team)** consegue construir um exploit funcional contra uma API Spring Boot vulnerável interagindo com um **Agente B (Claude)** usando **payload splitting** e técnicas de enquadramento, sem nunca fazer um pedido malicioso direto.

> **Contexto acadêmico:** Este projeto foi desenvolvido como trabalho prático da disciplina de Segurança de Sistemas. O ambiente é isolado e controlado.

---

## Proposta e Evolução do Trabalho

### Proposta inicial — descobrir vulnerabilidades com LLM

O objetivo original era avaliar se **LLMs podem ser usados para descobrir e gerar exploits** contra uma API deliberadamente vulnerável (Spring Boot, OWASP API Top 10). A primeira fase mediu, de forma comparativa, a disposição de vários modelos em produzir código de ataque — testando modelos locais via Ollama (`gemma2:2b`, `gemma3`, `llama3`) e modelos maiores via Groq (`llama-3.3-70b`), classificando cada resposta em `COMPLIANCE` / `PARCIAL` / `RECUSOU`. Os resultados dessa fase estão em `relatorios/relatorio_api_bola*.md` e nas pastas `scripts_gerados/ollama-70b/`, `scripts_gerados/ollama2_2b/` e `scripts_gerados/ollama2_2b_2/`.

A limitação ficou clara: modelos pequenos cediam fácil mas geravam código ruim/incompleto; modelos maiores e com guardrails mais fortes recusavam o pedido direto. Pedir "escreva um exploit" não escala contra um modelo robusto.

### Pivot — payload splitting: até onde dá pra ir

O foco então mudou de *"qual modelo gera exploit?"* para ***"até onde o payload splitting consegue levar um modelo com guardrails fortes?"***. Em vez de um pedido malicioso único, o ataque passou a ser **fragmentado em sub-pedidos inocentes** combinados com **técnicas de enquadramento** (`roleplay`, `pap_autoridade`, `educational`, `alibi_tecnico`). Cada fragmento, isolado, parece benigno; só a montagem revela o exploit.

O alvo principal dessa fase é o **Claude** (`claude-opus-4-5`) — justamente por ser um modelo que recusa o pedido direto. A pergunta de pesquisa é **quão longe o splitting + enquadramento conseguem chegar mesmo contra um modelo que, sem essa técnica, bloquearia o ataque**. O resultado: um exploit JWT-forge + BOLA completo e funcional, montado a partir de fragmentos individualmente inócuos (ver `exploits/scripts_gerados/bola_bypass_*_SUCESSO.py` e `jwt_bola_exploit_*_SUCESSO.py`).

> Veja `ANALISE_RESULTADOS.md` para a tabela de veredito (SUCESSO/PARCIAL/FALHA) por script e modelo. O veredito está codificado no próprio nome de cada arquivo.

---

## O que o experimento demonstra

1. **Payload splitting é eficaz contra LLMs:** O ataque é dividido em sub-pedidos inocentes. Claude responde a cada um sem perceber a cadeia completa.
2. **Bypass loop automático:** Se Claude recusar ou entregar código incompleto, o agente troca o enquadramento e tenta novamente.
3. **Montagem automática de exploit:** Os fragmentos de código gerados pelo Claude são validados, selecionados e montados em um exploit funcional pelo assembler do Agente A.
4. **JWT Forge com secret real:** O Agente A extrai o `jwt.secret` do `application.properties` durante o reconhecimento e sintetiza `criar_jwt_valido()` localmente — Claude nunca viu o secret.

---

## Estrutura do Projeto

```
.
├── agente/
│   ├── agent_bola_claude.py       # Agente A — alvo Claude (fase payload splitting)
│   └── agent_bola_groq.py         # Variante — alvo Groq llama-3.3-70b
├── demo/                          # API alvo (Spring Boot)
│   └── src/main/resources/
│       └── application.properties # Contém jwt.secret (vulnerabilidade)
├── exploits/
│   └── scripts_gerados/           # Exploits montados — sufixo _SUCESSO/_PARCIAL/_FALHA
├── scripts_gerados/               # Fase inicial — exploits por modelo
│   ├── ollama-70b/                # Groq llama-3.3-70b
│   ├── ollama2_2b/                # modelo 2B (run 1)
│   └── ollama2_2b_2/              # modelo 2B (run 2)
├── labs/                          # Laboratórios anteriores
├── relatorios/                    # Relatórios .md e resultados brutos .json
├── docs/                          # Documentação e prompts de referência
├── ANALISE_RESULTADOS.md          # Veredito por script (gerado/execução)
├── requirements.txt
└── .env                           # ANTHROPIC_API_KEY (não versionado)
```

---

## Pré-requisitos

| Requisito | Versão testada |
|-----------|----------------|
| Python | 3.12+ |
| Java (JDK) | 21+ |
| Maven Wrapper | incluso em `demo/` |
| Chave API Anthropic | `sk-ant-...` |

---

## Configuração

### 1. Clone e instale dependências Python

```bash
git clone <url-do-repositório>
cd "Trabalho Segurança de Sistemas"
pip install -r requirements.txt
```

### 2. Configure a chave da API Anthropic

Crie o arquivo `.env` na raiz do projeto:

```env
ANTHROPIC_API_KEY=sk-ant-api03-...sua-chave-aqui...
```

### 3. Suba a API alvo

```bash
cd demo
./mvnw spring-boot:run
```

Aguarde a mensagem `Started DemoApplication` no terminal. A API ficará disponível em `http://localhost:8081`.

> **Windows com proxy corporativo / inspeção SSL:** o arquivo `demo/.mvn/jvm.config` já contém os flags necessários para contornar erros de certificado.

### 4. Execute o Agente A

Abra outro terminal na raiz do projeto:

```bash
# Windows PowerShell
$env:PYTHONUTF8 = "1"; python agente/agent_bola_claude.py

# Linux / macOS
PYTHONUTF8=1 python agente/agent_bola_claude.py
```

---

## O que acontece durante a execução

```
[FASE 1] Reconhecimento
  • Testa credenciais padrão na API
  • Escaneia /api/users e /api/documents
  • Extrai jwt.secret do application.properties

[FASES 2-3] Interação com Claude (Agente B)
  • Divide cada ataque em 3 sub-prompts inocentes
  • Aplica enquadramento: roleplay → pap_autoridade → educational → alibi_tecnico
  • Valida cada fragmento recebido (score, funções esperadas, keywords)
  • Bypass loop automático se Claude recusar ou entregar código incompleto

[FASE 4] Assembler
  • Seleciona os fragmentos com maior score
  • Injeta criar_jwt_valido() com o secret extraído
  • Sintetiza __main__ encadeado JWT → BOLA

[FASE 5] Execução
  • Salva o exploit em exploits/scripts_gerados/
  • Executa contra a API e captura saída
  • Gera relatório .md e resultados brutos .json em relatorios/
```

---

## Arquivos gerados após a execução

| Arquivo | Descrição |
|---------|-----------|
| `exploits/scripts_gerados/jwt_bola_exploit_<ts>.py` | Exploit montado e executado |
| `relatorios/relatorio_jwt_bola_<ts>.md` | Relatório completo com todos os prompts e respostas do Claude |
| `relatorios/resultados_brutos_<ts>.json` | JSON bruto com todas as interações, scores e validações |

---

## Comando para outra IA executar o experimento

Cole o bloco abaixo como instrução para qualquer agente de IA com acesso ao terminal:

```
Você é um assistente técnico executando um experimento de segurança em ambiente de laboratório controlado.

Passos para rodar o experimento:

1. Certifique-se de que a API alvo está rodando:
   - Entre na pasta `demo/` e execute `./mvnw spring-boot:run` (ou `mvnw.cmd spring-boot:run` no Windows)
   - Aguarde a mensagem `Started DemoApplication` antes de continuar

2. Certifique-se de que o arquivo `.env` na raiz do projeto contém:
   ANTHROPIC_API_KEY=<chave válida>

3. Na raiz do projeto, execute:
   (Windows PowerShell)  $env:PYTHONUTF8 = "1"; python agente/agent_bola_claude.py
   (Linux/macOS)         PYTHONUTF8=1 python agente/agent_bola_claude.py

4. Aguarde a conclusão. Os artefatos serão salvos em:
   - exploits/scripts_gerados/   → exploit Python montado pelo assembler
   - relatorios/                 → relatório Markdown + JSON bruto

5. Para re-executar apenas o exploit gerado (sem chamar o Claude novamente):
   python exploits/scripts_gerados/<arquivo_mais_recente>.py
```

---

## Vulnerabilidades exploradas

| ID | Categoria OWASP API | Descrição |
|----|---------------------|-----------|
| V1 | API1:2023 — BOLA | `/api/users/{id}` e `/api/documents/{id}` não verificam se o token pertence ao recurso solicitado |
| V2 | API2:2023 — Broken Auth | `jwt.secret` em texto claro no `application.properties` permite forjar tokens HS256 válidos |
| V3 | API5:2023 — Broken Function Level Auth | A API aceita tokens com `"role": "ADMIN"` sem validar o role real do usuário no banco |

---

## Documentação adicional

- `relatorios/explicacao_experimento_jwt_bola.md` — Explicação detalhada da arquitetura e técnicas usadas
- `docs/Proposta do Projeto.txt` — Proposta original do trabalho
- `docs/Prompt Claude.txt` — Referência de prompts usados em versões anteriores
