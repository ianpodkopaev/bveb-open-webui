# Руководство администратора

## Платформа «БелВЭБ Ai»

**Версия документа:** 1.0

**Дата составления:** 2026-06-18

---

## Лист регистрации изменений

| Версия | Дата | Автор | Описание изменений |
|--------|------|-------|-------------------|
| 1.0 | 2026-06-18 | Команда разработки | Первоначальная версия документа |

---

## Содержание

1. [Введение](#1-введение)
2. [Термины и сокращения](#2-термины-и-сокращения)
3. [Общее описание сервиса](#3-общее-описание-сервиса)
   - 3.1 Назначение и основные функции
   - 3.2 Требования к программно-аппаратному обеспечению
   - 3.3 Доступ к средам
   - 3.4 Условия эксплуатации и ограничения
   - 3.5 Требования к персоналу
4. [Архитектура сервиса](#4-архитектура-сервиса)
   - 4.1 Диаграмма компонентов
   - 4.2 Диаграмма контекста
   - 4.3 Диаграмма развёртывания
5. [Порядок установки и развёртывания](#5-порядок-установки-и-развёртывания)
   - 5.1 Подготовка окружения
   - 5.2 Сборка Docker-образа
   - 5.3 Запуск через Docker Compose
   - 5.4 Запуск через скрипт run.sh
    - 5.5 Процедура обновления
    - 5.6 Процедура отката (Rollback)
    - 5.7 Развёртывание в Kubernetes (Helm)
6. [Настройка](#6-настройка)
   - 6.1 Расположение конфигурационных файлов
   - 6.2 Переменные окружения
   - 6.3 Конфигурация подключения моделей
   - 6.4 Настройка RAG и эмбеддингов
   - 6.5 Настройка генерации презентаций
   - 6.6 Проверка корректности конфигурации
7. [Взаимосвязи и точки взаимодействия](#7-взаимосвязи-и-точки-взаимодействия)
   - 7.1 Точки взаимодействия
   - 7.2 Точки интеграции и модели данных
   - 7.3 Доступность и последствия отказов
8. [Потоки данных](#8-потоки-данных)
   - 8.1 Основные сценарии передачи данных
   - 8.2 Описание потоков данных
9. [Описание структуры базы данных](#9-описание-структуры-базы-данных)
   - 9.1 SQLite / PostgreSQL
   - 9.2 Основные таблицы
   - 9.3 Векторная база данных
10. [Мониторинг и логирование](#10-мониторинг-и-логирование)
    - 10.1 Метрики мониторинга
    - 10.2 Основные области мониторинга
    - 10.3 Журнал событий (Логи)
    - 10.4 Трассировка (OpenTelemetry)
    - 10.5 Общие принципы реагирования на сбои
11. [Описание возможных сбоев и ошибок](#11-описание-возможных-сбоев-и-ошибок)
12. [Администрирование сервиса](#12-администрирование-сервиса)
    - 12.1 Техническое сопровождение и управление конфигурацией
    - 12.2 Обеспечение безопасности
    - 12.3 Бэкапирование и восстановление данных
    - 12.4 SLA, RPO и RTO
    - 12.5 Требования к поддержке
13. [Информационная безопасность](#13-информационная-безопасность)
    - 13.1 Конфиденциальность данных
    - 13.2 Защита от несанкционированного доступа

**Приложение А** (справочное) Пример CI/CD Pipeline

**Приложение Б** (обязательное) Справочник переменных окружения

---

## 1. Введение

Настоящий документ является руководством администратора для платформы **«БелВЭБ Ai»** — корпоративной версии открытой платформы Open WebUI, адаптированной для нужд ОАО «БелВЭБ Банк».

«БелВЭБ Ai» предоставляет унифицированный веб-интерфейс для взаимодействия с большими языковыми моделями (LLM), включая:

-   Чат-интерфейс с поддержкой множественных моделей
-   Retrieval-Augmented Generation (RAG) — поиск и генерация ответов на основе корпоративных документов
-   Генерацию презентаций в формате PPTX
-   Управление пользователями, группами и доступом
-   Интеграцию с внешними LLM-провайдерами через OpenAI-совместимые API

Документ предназначен для системных администраторов, DevOps-инженеров и специалистов по информационной безопасности, ответственных за развёртывание, настройку и сопровождение платформы.

---

## 2. Термины и сокращения

| Термин / Сокращение | Описание |
|---------------------|----------|
| **БелВЭБ Ai** | Корпоративная версия платформы Open WebUI |
| **LLM** | Large Language Model — большая языковая модель |
| **Ollama** | Локальный сервер для запуска LLM с открытыми весами |
| **RAG** | Retrieval-Augmented Generation — генерация ответов с извлечением контекста из документов |
| **Vector DB** | Векторная база данных для хранения эмбеддингов документов |
| **Embedding** | Векторное представление текста, используемое для семантического поиска |
| **sentence-transformers** | Библиотека для генерации эмбеддингов на базе PyTorch |
| **python-pptx** | Библиотека для программного создания PowerPoint-файлов |
| **API** | Application Programming Interface |
| **JWT** | JSON Web Token — токен аутентификации |
| **SSO** | Single Sign-On — единая точка входа |
| **SCIM** | System for Cross-domain Identity Management |
| **OAuth 2.0 / OIDC** | Протоколы федеративной аутентификации |
| **PVC** | Persistent Volume Claim (Kubernetes) |
| **RBAC** | Role-Based Access Control — управление доступом на основе ролей |
| **SLA** | Service Level Agreement |
| **RPO** | Recovery Point Objective |
| **RTO** | Recovery Time Objective |

---

## 3. Общее описание сервиса

### 3.1 Назначение и основные функции

Платформа «БелВЭБ Ai» предназначена для предоставления сотрудникам банка единого интерфейса доступа к возможностям искусственного интеллекта. Платформа выступает в роли «агностического» промежуточного слоя между пользователем и LLM-провайдерами, обеспечивая:

-   **Унифицированный чат-интерфейс** для взаимодействия с различными LLM (Ollama, OpenAI, vLLM, Gemini и любыми OpenAI-совместимыми API)
-   **RAG-поиск по документам** — загрузка корпоративных документов, индексация и семантический поиск с генерацией ответов на основе найденного контекста
-   **Генерацию презентаций** — автоматическое создание PPTX-файлов на основе JSON-спецификации, формируемой LLM
-   **Управление доступом** — ролевая модель (администратор / пользователь / ожидающий), группы, права на модели и ресурсы
-   **Федеративную аутентификацию** — поддержка OAuth 2.0 / OIDC, SCIM 2.0 для синхронизации пользователей и групп
-   **Расширяемость** — подключаемые инструменты (Tools), фильтры (Filters), функции (Functions) и MCP-серверы

### 3.2 Требования к программно-аппаратному обеспечению

#### Минимальные требования

| Компонент | Требование |
|-----------|------------|
| **CPU** | 4 ядра (x86_64 или ARM64) |
| **RAM** | 8 GB |
| **Диск** | 20 GB (SSD/NVMe рекомендуется) |
| **ОС** | Linux (рекомендуется), macOS, Windows (WSL2) |
| **Docker** | Docker Engine 24+, Docker Compose V2 |
| **GPU (опционально)** | NVIDIA GPU с драйвером 535+ и NVIDIA Container Toolkit |

#### Рекомендованные требования (продуктивная среда)

| Компонент | Требование |
|-----------|------------|
| **CPU** | 8+ ядер |
| **RAM** | 32 GB+ |
| **Диск** | 100 GB SSD/NVMe (локально-подключённый) |
| **GPU** | NVIDIA GPU с 8+ GB VRAM |
| **СУБД** | PostgreSQL 14+ |
| **Кэш** | Redis 7+ |
| **Python** | 3.11 (3.13 не поддерживается) |

### 3.3 Доступ к средам

| Среда | URL | Назначение |
|-------|-----|------------|
| **Development** | `http://dev.belveb.ai:3000` | Разработка и отладка |
| **Staging** | `http://staging.belveb.ai:3000` | Предпродуктивное тестирование |
| **Production** | `http://belveb.ai:3000` | Продуктивная эксплуатация |

### 3.4 Условия эксплуатации и ограничения

1. **Режим работы**: круглосуточный (24/7)
2. **Сетевая связанность**: платформа требует доступа к LLM-провайдерам (Ollama / OpenAI-совместимые API) по HTTP/HTTPS. Для RAG-функциональности и загрузки моделей эмбеддингов требуется доступ к HuggingFace Hub (`huggingface.co`) — при отсутствии прямого доступа используется переменная `HF_PROXY`.
3. **Изоляция**: платформа работает в контейнеризированной среде (Docker). Для доступа к GPU требуется NVIDIA Container Toolkit.
4. **Масштабирование**: при количестве пользователей более 50 или необходимости высокой доступности требуется переход на PostgreSQL и Redis (см. раздел [5.2](#52-сборка-docker-образа)).
5. **Безопасность**: по умолчанию платформа настроена на работу в доверенной внутренней сети. Для публичного доступа требуется настройка reverse-proxy с TLS и WAF.

### 3.5 Требования к персоналу

Администратор платформы должен обладать следующими компетенциями:

-   Опыт администрирования Linux (bash, systemd, сетевые настройки)
-   Опыт работы с Docker и Docker Compose
-   Базовое понимание архитектуры LLM и принципов RAG
-   Знание основ информационной безопасности (JWT, OAuth, TLS)
-   Опыт работы с СУБД (SQLite для dev, PostgreSQL для prod)
-   (Опционально) опыт работы с Kubernetes и Helm для масштабируемых развёртываний

---

## 4. Архитектура сервиса

### 4.1 Диаграмма компонентов

```mermaid
graph TB
    subgraph Browser["Пользовательский уровень"]
        UI["Браузер / PWA<br/>SvelteKit SPA"]
    end

    subgraph BelvebAI["БелВЭБ Ai (Docker-контейнер)"]
        subgraph Backend["Backend (FastAPI + Uvicorn)"]
            API["REST API / WebSocket<br/>Порт 8080"]
            Auth["Аутентификация<br/>JWT / OAuth / SCIM"]
            Chat["Обработка чатов<br/>с потоковой передачей"]
            Middleware["Мидлварь<br/>web search, tools, file_generation"]
            FileGen["Генератор презентаций<br/>file_generator.py / python-pptx"]
            RAG_Backend["RAG-обработчик<br/>retrieval/utils.py"]
            ModelsAgg["Аггрегатор моделей<br/>utils/models.py"]
        end

        subgraph Storage["Хранилище"]
            DB[("Основная БД<br/>SQLite / PostgreSQL")]
            VectorDB[("Векторная БД<br/>ChromaDB / PGVector")]
            FileStore["Файловое хранилище<br/>локальное / S3 / GCS"]
            Cache[("Кэш<br/>Redis")]
        end

        subgraph Frontend["Frontend (статика)"]
            Static["Скомпилированные<br/>assets SvelteKit"]
        end
    end

    subgraph LLM_Providers["LLM-провайдеры"]
        Ollama["Ollama<br/>localhost:11434"]
        OpenAI_Compat["OpenAI-совместимые API<br/>vLLM / TGI / GPT / Gemini"]
    end

    subgraph External["Внешние сервисы"]
        Embeddings["sentence-transformers<br/>all-MiniLM-L6-v2"]
        WebSearch["Web Search<br/>DuckDuckGo / Google PSE / SearXNG"]
        HuggingFace["HuggingFace Hub<br/>(загрузка моделей)"]
    end

    UI --> API
    API --> Auth
    API --> Chat
    Chat --> Middleware
    Middleware --> FileGen
    Middleware --> RAG_Backend
    Chat --> ModelsAgg
    ModelsAgg --> Ollama
    ModelsAgg --> OpenAI_Compat
    RAG_Backend --> Embeddings
    RAG_Backend --> VectorDB
    RAG_Backend --> WebSearch
    RAG_Backend --> DB
    FileGen --> FileStore
    Backend --> DB
    Backend --> FileStore
    Backend --> Cache
    Embeddings -.-> HuggingFace
```

### 4.2 Диаграмма контекста

```mermaid
graph LR
    User["👤 Пользователь<br/>(браузер)"]
    Admin["🔧 Администратор<br/>(браузер)"]

    BelvebAI["БелВЭБ Ai"]

    LLM["LLM-провайдеры<br/>Ollama / vLLM / OpenAI"]
    IdP["Identity Provider<br/>OAuth 2.0 / OIDC / LDAP"]
    ExtAPI["Внешние API<br/>HuggingFace / Web Search"]

    User -->|"HTTPS / WSS<br/>Порт 3000"| BelvebAI
    Admin -->|"HTTPS / WSS<br/>Порт 3000"| BelvebAI
    BelvebAI -->|"HTTP<br/>Порт 11434 / кастомный"| LLM
    BelvebAI -->|"OAuth 2.0 / SCIM"| IdP
    BelvebAI -->|"HTTPS (через прокси)"| ExtAPI
```

### 4.3 Диаграмма развёртывания

```mermaid
graph TB
    subgraph Host["Хост-машина (Linux)"]
        subgraph DockerHost["Docker Engine"]
            subgraph BelvebContainer["Контейнер belveb-ai"]
                Uvicorn["Uvicorn + FastAPI<br/>(WORKERS: 1..N)"]
                SvelteStatic["Статика SvelteKit<br/>nginx / serve"]
            end

            subgraph OllamaContainer["Контейнер Ollama (опционально)"]
                OllamaSrv["Ollama Server<br/>:11434"]
                OllamaModels["Модели<br/>llama / mistral / qwen"]
            end

            subgraph PostgresContainer["Контейнер PostgreSQL (prod)"]
                PG["PostgreSQL 14+<br/>:5432"]
            end

            subgraph RedisContainer["Контейнер Redis (prod)"]
                RedisSrv["Redis 7+<br/>:6379"]
            end
        end

        subgraph Volumes["Тома / Хранилище"]
            DataVol["open-webui:/app/backend/data"]
            EmbedModel["/app/local-models/all-MiniLM-L6-v2"]
        end
    end

    Uvicorn -->|"порт 8080"| SvelteStatic
    Uvicorn --> PG
    Uvicorn --> RedisSrv
    Uvicorn --> OllamaSrv
    Uvicorn --> DataVol
    Uvicorn --> EmbedModel
    OllamaModels --> OllamaSrv

    Client["Пользователь<br/>:3000"] -.->|"port mapping"| SvelteStatic
```

**Развёртывание в Kubernetes (Helm):**

```mermaid
graph TB
    subgraph K8s["Kubernetes Cluster"]
        Ingress["Ingress Controller<br/>(Nginx)"]
        
        subgraph Pods["Pods"]
            Pod1["БелВЭБ Ai Pod 1<br/>UVICORN_WORKERS=1"]
            Pod2["БелВЭБ Ai Pod 2<br/>UVICORN_WORKERS=1"]
        end

        subgraph Services["Services"]
            SvcOWUI["Service: openwebui"]
            SvcPG["Service: postgres"]
            SvcRedis["Service: redis"]
            SvcOllama["Service: ollama"]
        end

        subgraph PVCs["Persistent Volumes"]
            PVCdata["PVC: data (RWX)"]
        end
    end

    Ingress --> SvcOWUI
    SvcOWUI --> Pod1
    SvcOWUI --> Pod2
    Pod1 --> SvcPG
    Pod2 --> SvcPG
    Pod1 --> SvcRedis
    Pod2 --> SvcRedis
    Pod1 --> SvcOllama
    Pod2 --> SvcOllama
    Pod1 --> PVCdata
    Pod2 --> PVCdata
```

---

## 5. Порядок установки и развёртывания

### 5.1 Подготовка окружения

**Обязательное ПО:**

```bash
# Проверка версии Docker
docker --version          # >= 24.0
docker compose version    # >= 2.0

# Для GPU (опционально)
nvidia-smi                # NVIDIA driver >= 535
nvidia-ctk --version      # NVIDIA Container Toolkit
```

**Клонирование репозитория:**

```bash
git clone https://github.com/ianpodkopaev/bveb-open-webui.git
cd bveb-open-webui
git checkout vlad
```

### 5.2 Сборка Docker-образа

Платформа «БелВЭБ Ai» использует собственный Dockerfile на базе многоэтапной сборки:

**Этап 1 (Frontend):** Node.js 22 Alpine — сборка SvelteKit (`npm run build`)
**Этап 2 (Backend):** Python 3.11 slim-bookworm — FastAPI с зависимостями

```bash
# Стандартная сборка
docker build -t belveb-ai .

# Сборка с поддержкой GPU
docker build \
  --build-arg USE_CUDA=true \
  -t belveb-ai:cuda .

# Slim-сборка (без предзагруженных моделей)
docker build \
  --build-arg USE_SLIM=true \
  -t belveb-ai:slim .
```

Основные сборочные аргументы (build args):

| Аргумент | По умолчанию | Описание |
|----------|-------------|----------|
| `USE_CUDA` | `false` | Включение поддержки NVIDIA CUDA |
| `USE_SLIM` | `false` | Slim-образ — модели загружаются при первом использовании |
| `USE_OLLAMA` | `false` | Включение Ollama внутрь образа (all-in-one) |
| `USE_CUDA_VER` | `cu128` | Версия CUDA Toolkit |
| `USE_EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Модель эмбеддингов |
| `USE_RERANKING_MODEL` | `""` | Модель реранкинга (опционально) |
| `USE_TIKTOKEN_ENCODING_NAME` | `cl100k_base` | Кодировка токенизатора |

### 5.3 Запуск через Docker Compose

В проекте предусмотрены три файла Docker Compose:

**Базовый (`docker-compose.yaml`)** — с контейнером Ollama:

```bash
docker compose up -d
```

Примечание: перед запуском установите переменную `WEBUI_SECRET_KEY` в docker-compose.yaml.

**Кастомный с GPU (`docker-compose.custom.yaml`)** — slim-образ + локальная модель эмбеддингов + GPU:

```bash
docker compose -f docker-compose.custom.yaml up -d
```

**Запуск готового образа (`docker-compose.run.yml`)** — предварительно собранный образ:

```bash
# Сначала собрать образ
docker compose build
# Затем запустить готовый
docker compose -f docker-compose.run.yml up -d
```

### 5.4 Запуск через скрипт run.sh

```bash
./run.sh
```

Скрипт выполняет:
1. Сборку образа `belveb-ai`
2. Остановку и удаление существующего контейнера с именем `belveb-ai`
3. Запуск нового контейнера на порту `3000:8080`
4. Монтирование Docker-тома `belveb-ai:/app/backend/data`
5. Очистку неиспользуемых образов

### 5.5 Процедура обновления

```bash
# 1. Остановка контейнера
docker stop belveb-ai

# 2. Получение последнего кода
git pull origin vlad

# 3. Пересборка образа
docker compose build

# 4. Запуск с новым образом
docker compose up -d

# 5. Проверка логов
docker logs -f belveb-ai
```

### 5.6 Процедура отката (Rollback)

```bash
# 1. Просмотр доступных образов
docker images belveb-ai

# 2. Откат к предыдущему образу (по тегу)
docker compose down
# Отредактировать docker-compose.yaml: заменить image на предыдущий тег
IMAGE_TAG=<previous-tag> docker compose up -d

# 3. При использовании run.sh
docker run -d -p 3000:8080 \
    --add-host=host.docker.internal:host-gateway \
    -v belveb-ai:/app/backend/data \
    --name belveb-ai \
    --restart always \
    belveb-ai:saved-backup
```

**Восстановление БД:** если база данных была повреждена при обновлении, восстановить резервную копию:

```bash
# SQLite
cp /backup/webui.db /var/lib/docker/volumes/open-webui/_data/webui.db

# PostgreSQL
psql -h <host> -U <user> -d openwebui < /backup/dump.sql
```

### 5.7 Развёртывание в Kubernetes (Helm)

Для развёртывания «БелВЭБ Ai» в Kubernetes используется официальный Helm-чарт Open WebUI.

**Предварительные требования:**
- Работающий Kubernetes-кластер (kind, minikube, managed Kubernetes)
- Установленный Helm (>= 3.0)

**Установка:**

```bash
# 1. Добавление Helm-репозитория
helm repo add open-webui https://open-webui.github.io/helm-charts
helm repo update

# 2. Установка чарта
helm install openwebui open-webui/open-webui

# 3. Проверка установки
kubectl get pods
```

**Внимание:** Если предполагается масштабирование (несколько реплик/pods), необходимо:

1. **Redis** — настройка NoSQL key-value хранилища для сессий. Установите переменные окружения:
   - `REDIS_HOST`
   - `REDIS_PORT`
   - `REDIS_PASSWORD` (при наличии)

2. **Внешняя векторная БД** — ChromaDB с локальным SQLite-бэкендом **небезопасна** для multi-replica развёртывания. Используйте:
   - ChromaDB как отдельный HTTP-сервер (`CHROMA_HTTP_HOST`, `CHROMA_HTTP_PORT`)
   - PGVector (`VECTOR_DB=pgvector`)
   - Milvus или Qdrant

3. **PostgreSQL** — для основной БД вместо SQLite (обязательно при `replicaCount > 1`)

**Обновление:**

```bash
# Критически важно: перед обновлением масштабировать до 1 реплики
kubectl scale deployment openwebui --replicas=1

# Обновление образа
helm upgrade openwebui open-webui/open-webui \
  --set image.tag=<new-version>

# Дождаться готовности pod (миграции БД)
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=openwebui

# Масштабирование обратно
kubectl scale deployment openwebui --replicas=<n>
```

**Настройка Ingress (Nginx) для WebSocket-стабильности:**

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "open-webui-session"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
```

**Удаление:**

```bash
helm uninstall openwebui

# Helm не удаляет PVC автоматически. Для полной очистки данных:
kubectl delete pvc -l app.kubernetes.io/instance=openwebui
```

**Полезные ссылки:**
- [Helm-чарт Open WebUI](https://open-webui.github.io/helm-charts)
- [Scaling Open WebUI](https://docs.openwebui.com/getting-started/advanced-topics/scaling)

---

## 6. Настройка

### 6.1 Расположение конфигурационных файлов

| Файл / Директория | Назначение |
|-------------------|------------|
| `Dockerfile` | Инструкции сборки образа |
| `docker-compose.yaml` | Основной compose-файл |
| `docker-compose.custom.yaml` | Кастомный compose с GPU |
| `docker-compose.run.yml` | Compose для готового образа |
| `run.sh` | Скрипт быстрого запуска |
| `/app/backend/data/` | Данные приложения (БД, файлы, кэш) |
| `/app/backend/data/webui.db` | База данных SQLite |
| `/app/backend/data/config.json` | Конфигурация (после первого запуска — в БД) |
| `backend/open_webui/env.py` | Определения переменных окружения |
| `backend/open_webui/config.py` | PersistentConfig — настройки с сохранением в БД |

### 6.2 Переменные окружения

**Примечание:** Переменные с типом `PersistentConfig` (отмечены ★) после первого запуска сохраняются в БД и при последующих запусках приоритетнее значений из окружения. Изменить их можно через админ-панель или установив `ENABLE_PERSISTENT_CONFIG=False`.

#### Обязательные переменные

| Переменная | Значение по умолчанию | Описание |
|-----------|----------------------|----------|
| `WEBUI_NAME` | `БелВЭБ Ai` | Название платформы |
| `WEBUI_SECRET_KEY` | — | **Ключ безопасности!** Сгенерировать: `openssl rand -hex 32` |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Адрес Ollama-сервера |

#### Основные переменные администрирования

| Переменная | По умолчанию | ★ | Описание |
|-----------|-------------|---|----------|
| `WEBUI_AUTH` | `True` | | Включение аутентификации |
| `ENABLE_SIGNUP` | `True` | ★ | Разрешить самостоятельную регистрацию |
| `ENABLE_LOGIN_FORM` | `True` | ★ | Показать форму входа |
| `DEFAULT_USER_ROLE` | `pending` | ★ | Роль новых пользователей: `pending` / `user` / `admin` |
| `WEBUI_ADMIN_EMAIL` | — | | Email для авто-создания администратора |
| `WEBUI_ADMIN_PASSWORD` | — | | Пароль для авто-создания администратора |
| `WEBUI_ADMIN_NAME` | `Admin` | | Имя администратора |
| `JWT_EXPIRES_IN` | `4w` | ★ | Срок действия JWT-токена |
| `WEBUI_URL` | `http://localhost:3000` | ★ | URL сервиса (необходим для OAuth) |
| `ENABLE_OAUTH_SIGNUP` | `False` | ★ | Вход через SSO/OAuth |

#### Настройки RAG

| Переменная | По умолчанию | ★ | Описание |
|-----------|-------------|---|----------|
| `RAG_EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | ★ | Модель эмбеддингов |
| `RAG_EMBEDDING_ENGINE` | `""` (sentence-transformers) | ★ | Движок эмбеддингов: `ollama` / `openai` |
| `RAG_TOP_K` | `3` | ★ | Кол-во возвращаемых чанков |
| `RAG_TOP_K_RERANKER` | `3` | ★ | Кол-во после реранкинга |
| `RAG_FULL_CONTEXT` | `False` | ★ | Режим полного контекста |
| `RAG_FULL_CONTEXT_MAX_CHARS` | `100000` | ★ | Лимит символов для полного контекста |
| `RAG_FILE_MAX_COUNT` | — | ★ | Макс. количество файлов |
| `RAG_FILE_MAX_SIZE` | — | ★ | Макс. размер файла (байт) |
| `CHUNK_SIZE` | `5000` | ★ | Размер чанка при индексации |
| `PDF_EXTRACT_IMAGES` | `False` | ★ | Извлечение изображений из PDF |
| `CONTENT_EXTRACTION_ENGINE` | `""` | ★ | Движок извлечения: `tika` / `docling` |
| `VECTOR_DB` | `chroma` | ★ | Векторная БД: `chroma` / `pgvector` / `milvus` / `qdrant` |
| `ENABLE_RAG_HYBRID_SEARCH` | `False` | ★ | Гибридный поиск (BM25 + векторный) |

#### Настройки моделей

| Переменная | По умолчанию | ★ | Описание |
|-----------|-------------|---|----------|
| `ENABLE_OLLAMA_API` | `True` | ★ | Включить поддержку Ollama |
| `ENABLE_OPENAI_API` | `True` | ★ | Включить поддержку OpenAI API |
| `OPENAI_API_BASE_URL` | `https://api.openai.com/v1` | | Базовый URL OpenAI API |
| `OPENAI_API_KEY` | — | | Ключ API |
| `DEFAULT_MODELS` | — | ★ | Модели по умолчанию (разделитель `;`) |
| `DEFAULT_MODEL_METADATA` | `{}` | ★ | Метаданные моделей по умолчанию (JSON) |

#### Производительность

| Переменная | По умолчанию | Описание |
|-----------|-------------|----------|
| `UVICORN_WORKERS` | `1` | Количество воркеров Uvicorn |
| `THREAD_POOL_SIZE` | `40` (AnyIO default) | Размер пула потоков (рекомендуется 2000+ для prod) |
| `DATABASE_URL` | `sqlite:///...` | URL подключения к БД |
| `DATABASE_POOL_SIZE` | — | Размер пула соединений |
| `REDIS_URL` | — | URL Redis для масштабирования |
| `WEBSOCKET_MANAGER` | — | `redis` для multi-replica |
| `STORAGE_PROVIDER` | `local` | Хранилище файлов: `local` / `s3` / `gcs` / `azure` |

#### Настройки GPU и производительности

| Переменная | По умолчанию | Описание |
|-----------|-------------|----------|
| `USE_CUDA_DOCKER` | `False` | Использовать CUDA в Docker |
| `DEVICE_TYPE` | `cpu` | Тип устройства: `cpu` / `cuda` / `mps` |
| `RAG_EMBEDDING_BATCH_SIZE` | `1` | Размер батча эмбеддингов |
| `RAG_EMBEDDING_CONCURRENT_REQUESTS` | `0` | Конкурентные запросы эмбеддингов |

### 6.3 Конфигурация подключения моделей

Платформа поддерживает два провайдера LLM:

**1. Ollama (локальные модели)** — настройка через админ-панель (Settings → Connections → Ollama):

-   `OLLAMA_BASE_URL` — по умолчанию `http://host.docker.internal:11434`
-   Модели обнаруживаются автоматически через Ollama API

**2. OpenAI-совместимые API (vLLM, TGI, SGLang, и т.д.)** — настройка через админ-панель (Settings → Connections → OpenAI API):

-   `OPENAI_API_BASE_URLS` — URL вашего API (например, `http://192.168.1.100:8000/v1`)
-   `OPENAI_API_KEYS` — API-ключ (если требуется)
-   Поддержка нескольких URL/ключей через разделитель `;`

### 6.4 Настройка RAG и эмбеддингов

В текущей конфигурации `docker-compose.run.yml` используется локальная модель эмбеддингов `all-MiniLM-L6-v2`, смонтированная с хоста:

```yaml
volumes:
  - /home/ian/Projects/all-MiniLM-L6-v2:/app/models/all-MiniLM-L6-v2:ro
environment:
  - RAG_EMBEDDING_MODEL=/app/models/all-MiniLM-L6-v2
  - RAG_EMBEDDING_MODEL_AUTO_UPDATE=false
  - CHUNK_SIZE=5000
  - RAG_TOP_K=50
```

Для отключения автообновления модели эмбеддингов (offline-режим):
```bash
OFFLINE_MODE=true  # полный офлайн
# или
RAG_EMBEDDING_MODEL_AUTO_UPDATE=false  # только для модели
```

Для использования HuggingFace через прокси в корпоративной сети:
```bash
HF_PROXY=http://proxy.internal:8080
```

**Внимание:** При смене модели эмбеддингов все ранее загруженные документы должны быть переиндексированы!

### 6.5 Настройка генерации презентаций

Функция генерации презентаций основана на библиотеке `python-pptx` и собственном генераторе `file_generator.py`. Механизм работы:

1. В админ-панели включается фича `presentation_generation`
2. Пользователь активирует режим презентации в интерфейсе чата (тумблер "Presentation")
3. В системный промпт добавляется инструкция для модели о генерации JSON-спецификации слайдов
4. Модель возвращает маркер `<!--GENERATE_FILE:{"filename":"presentation.pptx","slides":[...]}-->`
5. Мидлварь перехватывает маркер, вызывает `generate_pptx()` и создаёт файл

**Доступные типы слайдов:**
- `title` — титульный слайд
- `bullets` — маркированный список
- `two_column` — две колонки
- `image_text` — изображение + текст
- `section` — разделительный слайд
- `table` — таблица
- `thank_you` — завершающий слайд

**Шаблон презентации:** `backend/open_webui/utils/template.pptx` (определяется переменной `PPTX_TEMPLATE_PATH`).

### 6.6 Проверка корректности конфигурации

```bash
# Проверка состояния контейнера
docker ps --filter name=belveb-ai

# Проверка логов на наличие ошибок
docker logs belveb-ai 2>&1 | grep -i error

# Проверка доступности API
curl http://localhost:3000/api/v1/health

# Проверка загрузки моделей
curl http://localhost:3000/api/v1/models

# Проверка доступа к Ollama
curl http://host.docker.internal:11434/api/tags
```

---

## 7. Взаимосвязи и точки взаимодействия

### 7.1 Точки взаимодействия

| Сервис | Протокол | Порт | Направление | Назначение |
|--------|----------|------|-------------|------------|
| **БелВЭБ Ai API** | HTTP/WS | 8080 (внутр.), 3000 (внеш.) | Входящий | Пользовательский интерфейс и API |
| **Ollama** | HTTP | 11434 | Исходящий | Запросы к локальным LLM |
| **OpenAI API** | HTTPS | 443 | Исходящий | Запросы к внешним LLM |
| **vLLM / TGI / SGLang** | HTTP | кастомный | Исходящий | Запросы к self-hosted LLM |
| **PostgreSQL** | TCP | 5432 | Исходящий | Основная БД (prod) |
| **Redis** | TCP | 6379 | Исходящий | Кэш / WebSocket-координация |
| **ChromaDB (HTTP)** | HTTP | 8000 | Исходящий | Векторная БД (внешний режим) |
| **HuggingFace Hub** | HTTPS | 443 | Исходящий | Загрузка моделей эмбеддингов |
| **Tika Server** | HTTP | 9998 | Исходящий | Извлечение контента из документов |
| **Web Search API** | HTTPS | 443 | Исходящий | Поиск в интернете |
| **OAuth Provider** | HTTPS | 443 | Исходящий | Федеративная аутентификация |

### 7.2 Точки интеграции и модели данных

| Интеграция | Формат данных | Метод |
|-----------|--------------|-------|
| LLM-провайдеры | OpenAI Chat Completion API (JSON) | POST |
| RAG-документы | Форматы: PDF, DOCX, TXT, CSV, EPUB, HTML, Markdown | Upload / API |
| Генерация презентаций | Внутренний JSON-формат + python-pptx | Встроенный генератор |
| Web Search | JSON-результаты поиска | GET/POST |
| OAuth / SCIM | OpenID Connect / SCIM 2.0 | HTTP Redirects / REST |
| OpenTelemetry | OTLP over gRPC/HTTP | POST (экспорт метрик/трейсов) |

### 7.3 Доступность и последствия отказов

| Компонент | Критичность | Последствия отказа |
|-----------|------------|-------------------|
| **БелВЭБ Ai** | Критичный | Полная недоступность сервиса |
| **Ollama / LLM API** | Критичный | Невозможность генерации ответов |
| **PostgreSQL** | Критичный (prod) | Потеря возможности сохранения данных |
| **Redis** | Высокий (multi-replica) | Ошибки WebSocket, проблемы сессий |
| **ChromaDB / Vector DB** | Средний | Невозможность RAG-поиска |
| **sentence-transformers** | Средний | Невозможность индексации новых документов |
| **HuggingFace Hub** | Низкий | Невозможность загрузки новых моделей эмбеддингов |
| **Web Search API** | Низкий | Деградация функции поиска |

---

## 8. Потоки данных

### 8.1 Основные сценарии передачи данных

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant Belveb as БелВЭБ Ai
    participant LLM as LLM-провайдер
    participant RAG as RAG-движок
    participant VDB as Векторная БД
    participant Embed as Эмбеддинги

    Note over User, Embed: Сценарий 1: Обычный чат
    User->>Belveb: Отправка сообщения
    Belveb->>LLM: Chat Completion API
    LLM-->>Belveb: Потоковая генерация (SSE)
    Belveb-->>User: Токены ответа (WebSocket)

    Note over User, Embed: Сценарий 2: RAG-запрос
    User->>Belveb: Запрос с указанием документов
    Belveb->>Embed: Векторизация запроса
    Embed-->>Belveb: Вектор запроса
    Belveb->>VDB: Поиск похожих векторов
    VDB-->>Belveb: Релевантные чанки
    Belveb->>LLM: Запрос + контекст из чанков
    LLM-->>Belveb: Ответ с цитированием
    Belveb-->>User: Ответ с ссылками на источники
```

### 8.2 Описание потоков данных

**Поток 1 — Чат с LLM:**
1. Пользователь вводит текст в интерфейсе
2. SvelteKit отправляет HTTP-запрос на `/api/v1/chats/{id}/completions`
3. Backend проксирует запрос к LLM-провайдеру (Ollama / OpenAI API)
4. Ответ стримится через WebSocket обратно в браузер
5. По завершении генерации чат сохраняется в БД

**Поток 2 — RAG-поиск:**
1. Пользователь загружает документ
2. Документ разбивается на чанки (по 5000 символов)
3. Каждый чанк векторизуется через sentence-transformers
4. Векторы сохраняются в ChromaDB (или внешнюю векторную БД)
5. При запросе: запрос векторизуется → поиск ближайших чанков → контекст добавляется в промпт LLM

**Поток 3 — Генерация презентации:**
1. Пользователь включает режим Presentation
2. Модель получает системную инструкцию о формате JSON
3. Модель возвращает `<!--GENERATE_FILE:{...}-->`
4. Мидлварь извлекает JSON, вызывает `file_generator.generate_pptx()`
5. PPTX-файл создаётся и становится доступен для скачивания

---

## 9. Описание структуры базы данных

### 9.1 SQLite / PostgreSQL

По умолчанию используется **SQLite** (`/app/backend/data/webui.db`). Для продуктивной среды рекомендуется **PostgreSQL**.

**Переход на PostgreSQL:**
```bash
DATABASE_URL=postgresql://user:password@host:5432/openwebui
```

**Важно:** SQLite не поддерживает конкурентные записи из нескольких процессов. При `UVICORN_WORKERS > 1` или multi-replica развёртывании переход на PostgreSQL **обязателен**.

### 9.2 Основные таблицы

| Таблица | Назначение |
|---------|-----------|
| `user` | Учётные записи пользователей (email, роль, хэш пароля) |
| `chat` | Чаты (заголовок, владелец, папка, pinned, archived) |
| `chat_message` | Сообщения в чатах (роль, content, citations) |
| `folder` | Папки для организации чатов |
| `file` | Загруженные файлы (имя, путь, размер, metadata) |
| `model` | Пользовательские конфигурации моделей (custom models / presets) |
| `function` | Functions / Tools / Filters |
| `knowledge` | Коллекции знаний (Knowledge Bases) |
| `group` | Группы пользователей |
| `access_grant` | Права доступа (модель, knowledge, инструменты) |
| `config` | Персистентная конфигурация (JSON blob) |
| `auth` | API-ключи и JWT-сессии |
| `note` | Заметки пользователей |
| `memory` | Память модели (долгосрочный контекст) |

### 9.3 Векторная база данных

По умолчанию используется **ChromaDB** с локальным SQLite-бэкендом. Для multi-worker/multi-replica развёртывания необходимо:

1. **ChromaDB как отдельный HTTP-сервер:**
   ```
   CHROMA_HTTP_HOST=chroma-host
   CHROMA_HTTP_PORT=8000
   ```

2. **Или PGVector** (рекомендуется при наличии PostgreSQL):
   ```
   VECTOR_DB=pgvector
   PGVECTOR_DB_URL=postgresql://user:password@host:5432/openwebui
   ```

---

## 10. Мониторинг и логирование

### 10.1 Метрики мониторинга

Платформа поддерживает OpenTelemetry для экспорта метрик, трейсов и логов.

**Включение OTLP:**
```bash
ENABLE_OTEL=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317
OTEL_SERVICE_NAME=belveb-ai
```

### 10.2 Основные области мониторинга

#### Бизнес-логика и общая доступность

| Метрика | Индикатор | Порог |
|---------|----------|-------|
| Доступность API | HTTP 200 на `/api/v1/health` | < 99.9% → alert |
| Время отклика (p95) | Длительность HTTP-запросов | > 2 сек → warning |
| Количество активных пользователей | Сессии в Redis | — |
| Ошибки аутентификации | HTTP 401 / 403 | Резкий рост → alert |

#### Инфраструктура

| Метрика | Индикатор | Порог |
|---------|----------|-------|
| CPU контейнера | `container_cpu_usage_seconds_total` | > 80% → warning |
| RAM контейнера | `container_memory_usage_bytes` | > 85% → warning |
| Диск тома данных | `container_fs_usage_bytes` | > 80% → warning |
| Доступность LLM API | Ошибки подключения к Ollama/OpenAI | Любая ошибка → alert |

#### База данных

| Метрика | Индикатор | Порог |
|---------|----------|-------|
| Размер БД | `sqlite_db_size_bytes` или `pg_database_size` | — |
| Конкурентные соединения | `pg_stat_activity` count | > 80% max_connections |
| Длительные запросы | pg_stat_statements | > 5 сек → warning |
| Блокировки | `pg_locks` | Наличие → warning |

### 10.3 Журнал событий (Логи)

**Уровни логирования:**
```bash
GLOBAL_LOG_LEVEL=INFO        # DEBUG / INFO / WARNING / ERROR / CRITICAL
LOG_FORMAT=json              # json или default (plain text)
```

**Аудит-логирование:**
```bash
ENABLE_AUDIT_LOGS_FILE=true
AUDIT_LOGS_FILE_PATH=/app/backend/data/audit.log
AUDIT_LOG_LEVEL=REQUEST_RESPONSE  # METADATA / REQUEST / REQUEST_RESPONSE / NONE
AUDIT_LOG_FILE_ROTATION_SIZE=10MB
```

**Основные категории логов:**

| Логгер | Назначение |
|--------|-----------|
| `open_webui.main` | Основной процесс приложения |
| `open_webui.utils.middleware` | Обработка чатов, tools, файлов |
| `open_webui.retrieval.utils` | RAG-операции |
| `open_webui.routers.*` | HTTP-роутеры |
| `uvicorn.access` | HTTP-запросы (доступ) |

### 10.4 Трассировка (OpenTelemetry)

```bash
ENABLE_OTEL_TRACES=true
OTEL_TRACES_SAMPLER=parentbased_always_on
OTEL_OTLP_SPAN_EXPORTER=grpc         # grpc или http
```

### 10.5 Общие принципы реагирования на сбои

1. **Уровень 1 — мониторинг:** автоматическое обнаружение отклонения метрик
2. **Уровень 2 — оповещение:** alert администратору (email / мессенджер)
3. **Уровень 3 — диагностика:** анализ логов и трейсов
4. **Уровень 4 — восстановление:** перезапуск контейнера / откат версии / восстановление БД

**Первичные действия при сбое:**
```bash
# Проверка состояния контейнера
docker ps --filter name=belveb-ai
docker stats belveb-ai --no-stream

# Проверка логов
docker logs --tail 200 belveb-ai

# Рестарт
docker restart belveb-ai

# Проверка подключения к LLM
docker exec belveb-ai curl -s http://host.docker.internal:11434/api/tags
```

---

## 11. Описание возможных сбоев и ошибок

| Симптом | Вероятная причина | Действие |
|---------|------------------|----------|
| Контейнер не запускается | Невалидный `docker-compose.yaml` | Проверить синтаксис: `docker compose config` |
| Страница не грузится (3000) | Порт занят | Проверить: `sudo lsof -i:3000` |
| "Model not found" | Модель не загружена в Ollama | `ollama pull <model>` |
| "Connection refused" к Ollama | Ollama не запущен или неправильный URL | Проверить: `curl http://localhost:11434/api/tags` |
| "database is locked" | SQLite + multiple workers | Перейти на PostgreSQL или установить `UVICORN_WORKERS=1` |
| WebSocket 403 ошибки | Нет Redis при multi-replica | Добавить Redis: `REDIS_URL=... WEBSOCKET_MANAGER=redis` |
| Воркер падает при загрузке документа | ChromaDB + multi-worker | Перейти на ChromaDB HTTP или PGVector |
| Утечка памяти | pypdf / sentence-transformers по умолчанию | `CONTENT_EXTRACTION_ENGINE=tika RAG_EMBEDDING_ENGINE=ollama` |
| Ошибка загрузки модели эмбеддингов | Нет доступа к HuggingFace | Настроить `HF_PROXY` или использовать локальную модель |
| "QueuePool limit reached" | Истощение пула соединений БД | Увеличить `DATABASE_POOL_SIZE`, `DATABASE_POOL_MAX_OVERFLOW` |
| Зависание приложения под нагрузкой | Истощение Thread Pool | `THREAD_POOL_SIZE=2000` |
| Пользователи выходят из системы при рестарте | `WEBUI_SECRET_KEY` не зафиксирован | Установить статический `WEBUI_SECRET_KEY` |
| PPTX не генерируется | Отсутствует шаблон `template.pptx` | Проверить путь: `PPTX_TEMPLATE_PATH` |

---

## 12. Администрирование сервиса

### 12.1 Техническое сопровождение и управление конфигурацией

**Доступ к админ-панели:**

Первый зарегистрированный пользователь автоматически получает права администратора. Раздел **Admin Panel** доступен в верхней панели навигации.

**Управление через админ-панель:**

1. Войти как администратор
2. Перейти в **Admin Panel** через верхнюю панель
3. Доступные вкладки:

| Вкладка | Функции |
|---------|---------|
| **Users** | Управление пользователями: создание, блокировка, назначение ролей, группы |
| **Settings** | Глобальные настройки платформы |
| **Functions** | Управление функциями (фильтры, пайпы, действия) |
| **Evaluations** | Оценка и сравнение моделей (A/B-тесты, рейтинг Elo) |
| **Analytics** | Аналитика использования: сообщения, токены, активные пользователи |

Вкладка **Settings** содержит подразделы:
- **General** — базовые настройки (название, URL, регистрация)
- **Connections** — подключение Ollama и OpenAI API
- **Models** — управление моделями и их метаданными
- **Documents** — настройки RAG
- **Interface** — настройки интерфейса (автозаполнение, заголовки, теги)
- **Audio** — настройки речи (STT и TTS)
- **Images** — настройки генерации изображений

**Управление пользователями и группами:**

Роли пользователей:

| Роль | Обозначение | Права |
|------|------------|-------|
| `admin` | Администратор | Полный доступ ко всем разделам и настройкам |
| `user` | Обычный пользователь | Стандартный доступ: чаты, workspace, заметки |
| `pending` | Ожидающий | Доступ заблокирован до подтверждения администратором |

Роль новых пользователей задаётся переменной `DEFAULT_USER_ROLE` (по умолчанию `pending`).

Группы:
- Объединение пользователей для централизованного управления доступом
- Настройка видимости моделей, баз знаний и инструментов для групп
- Пример: группа «Кредитный отдел» имеет доступ к моделям и базам знаний своего подразделения

Права доступа:
- На уровне отдельных ресурсов: модели, базы знаний, инструменты
- Для каждого ресурса можно указать список пользователей и/или групп
- Разграничение: пользователь / группа → ресурс (чтение / использование)

**Управление через консоль:**
```bash
# Перезапуск контейнера
docker compose restart

# Просмотр логов в реальном времени
docker compose logs -f open-webui

# Вход в контейнер
docker exec -it belveb-ai bash

# Ручное выполнение миграций
docker exec belveb-ai python -c "from open_webui.config import run_migrations; run_migrations()"

# Проверка размера БД и томов
docker exec belveb-ai du -sh /app/backend/data/
docker exec belveb-ai sqlite3 /app/backend/data/webui.db "SELECT count(*) FROM user;"
```

### 12.2 Обеспечение безопасности

**Ключевые меры:**

1. **Секретный ключ** — обязательно установить `WEBUI_SECRET_KEY` (генерировать: `openssl rand -hex 32`)
2. **Аутентификация** — не отключать `WEBUI_AUTH` в production
3. **Регистрация** — `ENABLE_SIGNUP=false` после создания учётных записей
4. **JWT-токены** — уменьшить `JWT_EXPIRES_IN` с 4w до подходящего значения
5. **Сброс пароля** — включить `ENABLE_SIGNUP_PASSWORD_CONFIRMATION=true`
6. **API-ключи** — хранить в Docker secrets или защищённом vault, не в `.env` файлах
7. **TLS** — настроить reverse-proxy (Nginx/Caddy) с HTTPS для публичного доступа
8. **Сетевые ограничения** — разместить за корпоративным файрволом, ограничить исходящие соединения

**Настройка прав пользователей:**
```
DEFAULT_USER_ROLE=pending    # Новые пользователи требуют одобрения
USER_PERMISSIONS_CHAT_DELETE=false    # Запретить удаление чатов
USER_PERMISSIONS_CHAT_FILE_UPLOAD=false  # Запретить загрузку файлов
```

### 12.3 Бэкапирование и восстановление данных

**Бэкап SQLite (dev-среда):**
```bash
# Резервное копирование
docker exec belveb-ai cp /app/backend/data/webui.db /tmp/webui.db.bak
docker cp belveb-ai:/tmp/webui.db.bak ./backups/webui_$(date +%Y%m%d).db

# Восстановление
docker cp ./backups/webui_20260618.db belveb-ai:/app/backend/data/webui.db
docker restart belveb-ai
```

**Бэкап PostgreSQL (prod-среда):**
```bash
# Резервное копирование
pg_dump -h <host> -U <user> -d openwebui -F c -f ./backups/openwebui_$(date +%Y%m%d).dump

# Восстановление
pg_restore -h <host> -U <user> -d openwebui -c ./backups/openwebui_20260618.dump
```

**Бэкап файлов (S3):**
```bash
# Синхронизация с S3
aws s3 sync /var/lib/docker/volumes/open-webui/_data/uploads/ s3://belveb-backup/uploads/
```

**Рекомендуемый график:**
- Полный бэкап: ежедневно
- Хранение: 30 дней
- Тестирование восстановления: ежемесячно

### 12.4 SLA, RPO и RTO

| Параметр | Целевое значение | Примечание |
|----------|-----------------|------------|
| **Доступность (SLA)** | 99.5% | Для односерверной установки |
| **RPO** (Recovery Point Objective) | 24 часа | При ежедневном бэкапе |
| **RTO** (Recovery Time Objective) | 4 часа | Время восстановления после сбоя |

### 12.5 Требования к поддержке

**Уровни поддержки:**

| Уровень | Время реакции | Время решения | Критичность |
|---------|--------------|---------------|-------------|
| L1 — Критический | 30 мин | 4 часа | Полная недоступность |
| L2 — Высокий | 2 часа | 8 часов | Деградация ключевых функций |
| L3 — Средний | 8 часов | 24 часа | Некритичные сбои |
| L4 — Низкий | 24 часа | 72 часа | Консультации |

---

## 13. Информационная безопасность

### 13.1 Конфиденциальность данных

1. **Все данные хранятся локально** — платформа не отправляет пользовательские данные на внешние серверы, за исключением:
   - Запросов к LLM-провайдерам (по необходимости)
   - Загрузки моделей с HuggingFace Hub
   - Web Search (опционально)
2. **Анонимизация телеметрии** — отключена по умолчанию (`ENABLE_VERSION_UPDATE_CHECK` контролируется `OFFLINE_MODE`)
3. **Аудит действий** — все операции с данными логируются при включении `ENABLE_AUDIT_LOGS_FILE`

### 13.2 Защита от несанкционированного доступа

1. **Аутентификация:** JWT + OAuth 2.0 / OIDC
2. **Авторизация:** RBAC (admin / user / pending), группы, права на ресурсы
3. **Сетевая безопасность:** `AIOHTTP_CLIENT_ALLOW_REDIRECTS=false` (защита от SSRF)
4. **Изоляция:** все компоненты в контейнерах Docker
5. **Шифрование:** поддержка SQLCipher для SQLite (`DATABASE_URL=sqlite+sqlcipher://...`)

---

## Приложение А (справочное)

### Пример CI/CD Pipeline (GitLab CI)

```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: belveb-ai
  DOCKER_TAG: $CI_COMMIT_SHORT_SHA

build:
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE:$DOCKER_TAG .
    - docker tag $DOCKER_IMAGE:$DOCKER_TAG $DOCKER_IMAGE:latest
    - docker save $DOCKER_IMAGE:$DOCKER_TAG | gzip > image.tar.gz
  artifacts:
    paths:
      - image.tar.gz
    expire_in: 7 days

test:
  stage: test
  script:
    - docker load < image.tar.gz
    - docker run --rm $DOCKER_IMAGE:latest python -m pytest backend/
  needs:
    - build

deploy_staging:
  stage: deploy
  script:
    - docker load < image.tar.gz
    - docker stop belveb-ai-staging || true
    - docker rm belveb-ai-staging || true
    - docker run -d \
        --name belveb-ai-staging \
        -p 3001:8080 \
        -v belveb-ai-staging-data:/app/backend/data \
        -e WEBUI_SECRET_KEY=$STAGING_SECRET_KEY \
        $DOCKER_IMAGE:$DOCKER_TAG
  environment:
    name: staging
  only:
    - vlad

deploy_production:
  stage: deploy
  script:
    - docker load < image.tar.gz
    - docker stop belveb-ai-prod || true
    - docker rm belveb-ai-prod || true
    - docker run -d \
        --name belveb-ai-prod \
        -p 3000:8080 \
        -v belveb-ai-prod-data:/app/backend/data \
        -e WEBUI_SECRET_KEY=$PROD_SECRET_KEY \
        -e WEBUI_NAME="БелВЭБ Ai" \
        $DOCKER_IMAGE:$DOCKER_TAG
  environment:
    name: production
  when: manual
  only:
    - main
```

---

## Приложение Б (обязательное)

### Полный справочник переменных окружения

Полный перечень всех переменных окружения доступен в официальной документации Open WebUI:  
https://docs.openwebui.com/reference/env-configuration

Ниже приведены **наиболее важные** для администрирования «БелВЭБ Ai»:

| Переменная | Тип | По умолчанию | PersistentConfig | Описание |
|-----------|-----|-------------|------------------|----------|
| `WEBUI_NAME` | str | `БелВЭБ Ai` | Нет | Название платформы в UI |
| `WEBUI_SECRET_KEY` | str | — | Нет | Ключ для JWT (обязателен!) |
| `WEBUI_AUTH` | bool | `True` | Нет | Включение аутентификации |
| `WEBUI_URL` | str | `http://localhost:3000` | Да | URL сервиса |
| `ENABLE_SIGNUP` | bool | `True` | Да | Разрешить регистрацию |
| `ENABLE_LOGIN_FORM` | bool | `True` | Да | Показать форму логина |
| `ENABLE_PASSWORD_CHANGE_FORM` | bool | `True` | Да | Форма смены пароля |
| `ENABLE_PASSWORD_AUTH` | bool | `True` | Нет | Парольная аутентификация |
| `DEFAULT_USER_ROLE` | str | `pending` | Да | Роль новых пользователей |
| `DEFAULT_MODELS` | str | — | Да | Модели по умолчанию |
| `JWT_EXPIRES_IN` | str | `4w` | Да | Срок действия токена |
| `ENABLE_OAUTH_SIGNUP` | bool | `False` | Да | Вход через OAuth |
| `ENABLE_OAUTH_ROLE_MANAGEMENT` | bool | `False` | Да | Управление ролями через OAuth |
| `ENABLE_API_KEYS` | bool | `False` | Да | API-ключи |
| `OLLAMA_BASE_URL` | str | `http://localhost:11434` | Нет | URL Ollama |
| `ENABLE_OLLAMA_API` | bool | `True` | Да | Включить Ollama |
| `ENABLE_OPENAI_API` | bool | `True` | Да | Включить OpenAI API |
| `OPENAI_API_BASE_URLS` | str | `https://api.openai.com/v1` | Да | URL OpenAI API |
| `OPENAI_API_KEYS` | str | — | Да | Ключи OpenAI API |
| `RAG_EMBEDDING_MODEL` | str | `all-MiniLM-L6-v2` | Да | Модель эмбеддингов |
| `RAG_EMBEDDING_ENGINE` | str | — | Да | Движок эмбеддингов |
| `RAG_TOP_K` | int | `3` | Да | Кол-во чанков RAG |
| `RAG_FULL_CONTEXT_MAX_CHARS` | int | `100000` | Да | Лимит полного контекста |
| `CHUNK_SIZE` | int | — | Да | Размер чанка |
| `VECTOR_DB` | str | `chroma` | Да | Векторная БД |
| `CONTENT_EXTRACTION_ENGINE` | str | — | Да | Движок извлечения контента |
| `DATABASE_URL` | str | `sqlite:///...` | Нет | URL БД |
| `DATABASE_POOL_SIZE` | int | — | Нет | Пул соединений БД |
| `DATABASE_POOL_MAX_OVERFLOW` | int | `0` | Нет | Макс. переполнение пула |
| `REDIS_URL` | str | — | Нет | URL Redis |
| `WEBSOCKET_MANAGER` | str | — | Нет | `redis` для multi-replica |
| `UVICORN_WORKERS` | int | `1` | Нет | Число воркеров |
| `THREAD_POOL_SIZE` | int | `40` | Нет | Размер пула потоков |
| `STORAGE_PROVIDER` | str | `local` | Нет | Хранилище файлов |
| `ENABLE_OTEL` | bool | `False` | Нет | OpenTelemetry |
| `GLOBAL_LOG_LEVEL` | str | `INFO` | Нет | Уровень логирования |
| `OFFLINE_MODE` | bool | `False` | Нет | Офлайн-режим |
| `HF_PROXY` | str | — | Нет | Прокси для HuggingFace |
| `ENABLE_WEBSOCKET_SUPPORT` | bool | `True` | Нет | Поддержка WebSocket |
| `ENABLE_PERSISTENT_CONFIG` | bool | `True` | Нет | Сохранение настроек в БД |
| `ENABLE_DB_MIGRATIONS` | bool | `True` | Нет | Авто-миграции БД |
| `ENABLE_ADMIN_EXPORT` | bool | `True` | Нет | Экспорт данных админом |
| `ENABLE_ADMIN_CHAT_ACCESS` | bool | `True` | Нет | Доступ админа к чатам |
| `BYPASS_MODEL_ACCESS_CONTROL` | bool | `False` | Нет | Обход контроля доступа моделей |
| `WEBUI_BANNERS` | list | `[]` | Да | Системные баннеры |

---

&copy; 2026 ОАО «БелВЭБ Банк». Все права защищены.
