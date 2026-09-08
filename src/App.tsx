import { useState } from 'react'

type Tab = 'overview' | 'endpoints' | 'structure' | 'setup' | 'models'

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('overview')
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)

  const copyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text)
    setCopiedIndex(index)
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  const tabs: { id: Tab; label: string; icon: string }[] = [
    { id: 'overview', label: 'Обзор', icon: '🏠' },
    { id: 'endpoints', label: 'API Endpoints', icon: '🔌' },
    { id: 'models', label: 'Модели', icon: '🗄️' },
    { id: 'structure', label: 'Структура', icon: '📁' },
    { id: 'setup', label: 'Запуск', icon: '🚀' },
  ]

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-400 to-cyan-500 flex items-center justify-center text-xl font-bold">
                ⚔️
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">SQL Battle Backend</h1>
                <p className="text-xs text-gray-400">FastAPI + SQLAlchemy + WebSocket</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-1 text-xs rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                v1.0.0
              </span>
              <span className="px-2 py-1 text-xs rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                Python 3.10+
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="border-b border-gray-800 bg-gray-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex gap-1 overflow-x-auto py-2">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
                  activeTab === tab.id
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'
                }`}
              >
                <span className="mr-1.5">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && <OverviewTab />}
        {activeTab === 'endpoints' && <EndpointsTab copiedIndex={copiedIndex} copyToClipboard={copyToClipboard} />}
        {activeTab === 'models' && <ModelsTab />}
        {activeTab === 'structure' && <StructureTab />}
        {activeTab === 'setup' && <SetupTab copiedIndex={copiedIndex} copyToClipboard={copyToClipboard} />}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-6 text-center text-gray-500 text-sm">
        <p>SQL Battle Backend — для платформы SQL-соревнований cdek_digital</p>
      </footer>
    </div>
  )
}

function OverviewTab() {
  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="rounded-2xl bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-700 p-8">
        <h2 className="text-3xl font-bold text-white mb-4">
          🐍 Backend для SQL Battle
        </h2>
        <p className="text-gray-300 text-lg mb-6">
          Полный REST API + WebSocket бэкенд для платформы интерактивных SQL-соревнований.
          Написан на FastAPI с асинхронной базой данных.
        </p>
        <div className="flex flex-wrap gap-3">
          <TechBadge name="FastAPI" color="emerald" />
          <TechBadge name="SQLAlchemy 2.0" color="blue" />
          <TechBadge name="SQLite/PostgreSQL" color="purple" />
          <TechBadge name="JWT Auth" color="amber" />
          <TechBadge name="WebSocket" color="cyan" />
          <TechBadge name="Pydantic v2" color="pink" />
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <FeatureCard
          icon="🔐"
          title="Аутентификация"
          description="JWT токены, регистрация, вход. Роли: participant и admin."
        />
        <FeatureCard
          icon="🎮"
          title="Задачи"
          description="CRUD задач, выполнение SQL в sandbox, автоматическая проверка решений."
        />
        <FeatureCard
          icon="🏆"
          title="Лидерборд"
          description="Рейтинг участников в реальном времени через WebSocket."
        />
        <FeatureCard
          icon="🛡️"
          title="SQL Sandbox"
          description="Изолированное выполнение запросов. Только SELECT, таймаут 3 сек."
        />
        <FeatureCard
          icon="👥"
          title="Админка"
          description="Управление пользователями, назначение задач, создание задач."
        />
        <FeatureCard
          icon="⚡"
          title="Realtime"
          description="WebSocket для мгновенных обновлений лидерборда."
        />
      </div>

      {/* Architecture */}
      <div className="rounded-xl bg-gray-900 border border-gray-700 p-6">
        <h3 className="text-xl font-bold text-white mb-4">🏗 Архитектура</h3>
        <div className="bg-gray-950 rounded-lg p-4 font-mono text-sm overflow-x-auto">
          <pre className="text-gray-300">{`┌─────────────────────┐
│     Frontend        │  Next.js 16 + React + TypeScript
│  (отдельный репо)   │  Tailwind CSS + shadcn/ui
└──────────┬──────────┘
           │ HTTP + WebSocket
           ▼
┌─────────────────────┐
│     Backend         │  Python + FastAPI
│  (этот репо)        │  SQLAlchemy + SQLite/PostgreSQL
│                     │  WebSocket для реалтайма
└─────────────────────┘`}</pre>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard value="16" label="API Endpoints" />
        <StatCard value="4" label="DB Модели" />
        <StatCard value="1" label="WebSocket" />
        <StatCard value="~500" label="Строк кода" />
      </div>
    </div>
  )
}

function EndpointsTab({ copiedIndex, copyToClipboard }: { copiedIndex: number | null; copyToClipboard: (text: string, index: number) => void }) {
  const endpoints = [
    {
      group: '🔐 Аутентификация',
      items: [
        { method: 'POST', path: '/api/auth/register', desc: 'Регистрация нового пользователя', body: '{"username": "ivan", "email": "ivan@mail.ru", "password": "pass123"}', response: '{"token": "eyJ...", "user": {...}}' },
        { method: 'POST', path: '/api/auth/login', desc: 'Вход в систему', body: '{"username": "ivan", "password": "pass123"}', response: '{"token": "eyJ...", "user": {...}}' },
      ]
    },
    {
      group: '👤 Профиль',
      items: [
        { method: 'GET', path: '/api/profile', desc: 'Получить данные текущего пользователя', body: '', response: '{"id": 1, "username": "...", "rating": 1250, "total_points": 450, "rank": 3, "solved_tasks": [1,2,5]}' },
      ]
    },
    {
      group: '🎮 Задачи',
      items: [
        { method: 'GET', path: '/api/tasks', desc: 'Список всех задач', body: '', response: '[{"id": 1, "title": "...", "difficulty": "easy", "points": 100, "status": "unsolved"}]' },
        { method: 'GET', path: '/api/tasks/{id}', desc: 'Детали задачи', body: '', response: '{"id": 1, "title": "...", "description": "...", "schema": "...", "tables": [...], "expectedResult": [...]}' },
        { method: 'POST', path: '/api/tasks/{id}/execute', desc: 'Выполнить SQL (Run)', body: '{"query": "SELECT * FROM users"}', response: '{"status": "success", "data": [...], "execution_time": 0.045}' },
        { method: 'POST', path: '/api/tasks/{id}/submit', desc: 'Отправить решение', body: '{"query": "SELECT name, COUNT(*) ..."}', response: '{"is_correct": true, "points_earned": 100, "new_total_points": 550, "expected_result": [...]}' },
      ]
    },
    {
      group: '🏆 Лидерборд',
      items: [
        { method: 'GET', path: '/api/leaderboard', desc: 'Таблица лидеров', body: '', response: '[{"rank": 1, "username": "...", "total_points": 1250, "solved_tasks": 8, "avg_time": 0.45, "avatar": "АС"}]' },
        { method: 'WS', path: '/ws/leaderboard', desc: 'Реалтайм обновления', body: '', response: '{"type": "leaderboard_update", "data": [...]}' },
      ]
    },
    {
      group: '👥 Админка',
      items: [
        { method: 'GET', path: '/api/admin/users', desc: 'Все пользователи', body: '', response: '[{"id": 1, "username": "...", "total_points": 450, "assigned_task_id": 3}]' },
        { method: 'POST', path: '/api/admin/users/{id}/assign', desc: 'Назначить задачу', body: '{"taskId": 3}', response: '{"success": true, "message": "Задача назначена"}' },
        { method: 'POST', path: '/api/admin/users/{id}/clear', desc: 'Снять назначение', body: '', response: '{"success": true, "message": "Назначение снято"}' },
        { method: 'GET', path: '/api/admin/tasks', desc: 'Все задачи (полные)', body: '', response: '[{"id": 1, "title": "...", "schema": "...", "tables": [...], "expected_result": [...]}]' },
        { method: 'POST', path: '/api/admin/tasks', desc: 'Создать задачу', body: '{"title": "...", "description": "...", "difficulty": "medium", "points": 250, "schema": "...", "tables": [...], "expected_result": [...]}', response: '{"id": 10, "title": "...", "success": true}' },
        { method: 'GET', path: '/api/admin/settings', desc: 'Настройки баттла', body: '', response: '{"battle_start": "2026-09-15T10:00:00Z", "round_duration_minutes": 120}' },
        { method: 'PUT', path: '/api/admin/settings', desc: 'Обновить настройки', body: '{"battle_start": "...", "round_duration_minutes": 120}', response: '{"battle_start": "...", "round_duration_minutes": 120}' },
      ]
    },
    {
      group: '🎮 Пользователь',
      items: [
        { method: 'GET', path: '/api/user/assigned-task', desc: 'Назначенная задача', body: '', response: '{"id": 3, "title": "...", "difficulty": "hard", "points": 500}' },
      ]
    },
  ]

  let globalIndex = 0

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-3 mb-6">
        <h2 className="text-2xl font-bold text-white">API Endpoints</h2>
        <span className="text-sm text-gray-400">Базовый URL: <code className="text-emerald-400">http://localhost:8000</code></span>
      </div>

      {/* Auth notice */}
      <div className="rounded-lg bg-amber-500/5 border border-amber-500/20 p-4">
        <p className="text-amber-300 text-sm">
          🔑 Все endpoints (кроме <code>/api/auth/*</code>, <code>/api/leaderboard</code>) требуют заголовок:
          <code className="ml-2 bg-gray-800 px-2 py-0.5 rounded">Authorization: Bearer &lt;jwt_token&gt;</code>
        </p>
      </div>

      {endpoints.map((group, gi) => (
        <div key={gi} className="space-y-3">
          <h3 className="text-lg font-semibold text-white">{group.group}</h3>
          <div className="space-y-2">
            {group.items.map((item, ii) => {
              const idx = globalIndex++
              return (
                <div key={ii} className="rounded-lg bg-gray-900 border border-gray-700 overflow-hidden">
                  <div className="flex items-center gap-3 px-4 py-3">
                    <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                      item.method === 'GET' ? 'bg-blue-500/20 text-blue-400' :
                      item.method === 'POST' ? 'bg-emerald-500/20 text-emerald-400' :
                      item.method === 'PUT' ? 'bg-amber-500/20 text-amber-400' :
                      'bg-purple-500/20 text-purple-400'
                    }`}>
                      {item.method}
                    </span>
                    <code className="text-sm text-gray-200 font-mono">{item.path}</code>
                    <span className="text-sm text-gray-400 ml-auto">{item.desc}</span>
                  </div>
                  {(item.body || item.response) && (
                    <div className="border-t border-gray-800 px-4 py-3 space-y-2">
                      {item.body && (
                        <div className="flex items-start gap-2">
                          <span className="text-xs text-gray-500 mt-1 w-16 shrink-0">Request:</span>
                          <code className="text-xs text-gray-300 bg-gray-950 px-2 py-1 rounded flex-1 overflow-x-auto">
                            {item.body}
                          </code>
                          <button
                            onClick={() => copyToClipboard(item.body, idx * 2)}
                            className="text-xs text-gray-500 hover:text-gray-300 shrink-0"
                          >
                            {copiedIndex === idx * 2 ? '✅' : '📋'}
                          </button>
                        </div>
                      )}
                      {item.response && (
                        <div className="flex items-start gap-2">
                          <span className="text-xs text-gray-500 mt-1 w-16 shrink-0">Response:</span>
                          <code className="text-xs text-gray-300 bg-gray-950 px-2 py-1 rounded flex-1 overflow-x-auto">
                            {item.response}
                          </code>
                          <button
                            onClick={() => copyToClipboard(item.response, idx * 2 + 1)}
                            className="text-xs text-gray-500 hover:text-gray-300 shrink-0"
                          >
                            {copiedIndex === idx * 2 + 1 ? '✅' : '📋'}
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}

function ModelsTab() {
  const models = [
    {
      name: 'User',
      table: 'users',
      fields: [
        { name: 'id', type: 'Integer', desc: 'Primary Key' },
        { name: 'username', type: 'String(50)', desc: 'Unique, Not Null' },
        { name: 'email', type: 'String(100)', desc: 'Unique, Nullable' },
        { name: 'password_hash', type: 'String(255)', desc: 'Not Null (bcrypt)' },
        { name: 'rating', type: 'Integer', desc: 'Default: 0' },
        { name: 'total_points', type: 'Integer', desc: 'Default: 0' },
        { name: 'role', type: 'String(20)', desc: "'participant' | 'admin'" },
        { name: 'created_at', type: 'DateTime', desc: 'Default: NOW()' },
      ]
    },
    {
      name: 'Task',
      table: 'tasks',
      fields: [
        { name: 'id', type: 'Integer', desc: 'Primary Key' },
        { name: 'title', type: 'String(200)', desc: 'Not Null' },
        { name: 'description', type: 'Text', desc: 'Not Null' },
        { name: 'difficulty', type: 'String(20)', desc: "'easy' | 'medium' | 'hard'" },
        { name: 'points', type: 'Integer', desc: 'Not Null' },
        { name: 'schema', type: 'Text', desc: 'DDL для создания таблиц' },
        { name: 'tables', type: 'JSON', desc: 'Структура таблиц с данными' },
        { name: 'expected_result', type: 'JSON', desc: 'Эталонный результат' },
        { name: 'created_at', type: 'DateTime', desc: 'Default: NOW()' },
      ]
    },
    {
      name: 'Submission',
      table: 'submissions',
      fields: [
        { name: 'id', type: 'Integer', desc: 'Primary Key' },
        { name: 'user_id', type: 'Integer', desc: 'FK → users.id' },
        { name: 'task_id', type: 'Integer', desc: 'FK → tasks.id' },
        { name: 'query', type: 'Text', desc: 'SQL запрос' },
        { name: 'is_correct', type: 'Boolean', desc: 'Результат проверки' },
        { name: 'points_earned', type: 'Integer', desc: 'Default: 0' },
        { name: 'execution_time_ms', type: 'Integer', desc: 'Nullable' },
        { name: 'created_at', type: 'DateTime', desc: 'Default: NOW()' },
      ]
    },
    {
      name: 'TaskAssignment',
      table: 'task_assignments',
      fields: [
        { name: 'id', type: 'Integer', desc: 'Primary Key' },
        { name: 'user_id', type: 'Integer', desc: 'FK → users.id, Unique' },
        { name: 'task_id', type: 'Integer', desc: 'FK → tasks.id' },
        { name: 'assigned_at', type: 'DateTime', desc: 'Default: NOW()' },
        { name: 'started_at', type: 'DateTime', desc: 'Nullable' },
        { name: 'completed_at', type: 'DateTime', desc: 'Nullable' },
      ]
    },
  ]

  return (
    <div className="space-y-8">
      <h2 className="text-2xl font-bold text-white">Модели базы данных</h2>

      <div className="rounded-lg bg-blue-500/5 border border-blue-500/20 p-4">
        <p className="text-blue-300 text-sm">
          💾 По умолчанию используется SQLite (aiosqlite). Для переключения на PostgreSQL замените DATABASE_URL в .env
        </p>
      </div>

      {models.map(model => (
        <div key={model.name} className="rounded-xl bg-gray-900 border border-gray-700 overflow-hidden">
          <div className="px-5 py-3 border-b border-gray-700 bg-gray-800/50">
            <div className="flex items-center gap-3">
              <span className="text-lg">📋</span>
              <h3 className="font-bold text-white">{model.name}</h3>
              <code className="text-xs text-gray-400 bg-gray-950 px-2 py-0.5 rounded">
                {model.table}
              </code>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-800">
                  <th className="text-left px-5 py-2 text-gray-400 font-medium">Поле</th>
                  <th className="text-left px-5 py-2 text-gray-400 font-medium">Тип</th>
                  <th className="text-left px-5 py-2 text-gray-400 font-medium">Описание</th>
                </tr>
              </thead>
              <tbody>
                {model.fields.map((field, i) => (
                  <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-800/30">
                    <td className="px-5 py-2 font-mono text-emerald-400">{field.name}</td>
                    <td className="px-5 py-2 font-mono text-blue-300">{field.type}</td>
                    <td className="px-5 py-2 text-gray-400">{field.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  )
}

function StructureTab() {
  return (
    <div className="space-y-8">
      <h2 className="text-2xl font-bold text-white">Структура проекта</h2>

      <div className="rounded-xl bg-gray-900 border border-gray-700 p-6">
        <pre className="text-sm font-mono text-gray-300 overflow-x-auto">{`backend/
├── main.py                 # Точка входа FastAPI приложения
├── config.py               # Конфигурация (Pydantic Settings)
├── database.py             # Async SQLAlchemy engine & session
├── models.py               # ORM модели (User, Task, Submission, TaskAssignment)
├── schemas.py              # Pydantic схемы для валидации
├── auth.py                 # JWT аутентификация, password hashing
├── seed.py                 # Скрипт заполнения БД тестовыми данными
├── requirements.txt        # Python зависимости
├── .env.example            # Пример конфигурации
├── README.md               # Документация
│
├── routers/
│   ├── __init__.py
│   ├── auth.py             # POST /api/auth/register, /api/auth/login
│   ├── profile.py          # GET /api/profile
│   ├── tasks.py            # GET /api/tasks, POST execute/submit
│   ├── leaderboard.py      # GET /api/leaderboard
│   ├── admin.py            # Admin endpoints + /api/user/assigned-task
│   └── websocket.py        # WS /ws/leaderboard + periodic broadcast
│
└── services/
    └── __init__.py         # SQL sandbox execution + result comparison`}</pre>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <FileCard
          filename="main.py"
          description="Создаёт FastAPI app, настраивает CORS, подключает роутеры, запускает периодический broadcast лидерборда"
        />
        <FileCard
          filename="database.py"
          description="Async engine, session factory, init_db() для создания таблиц"
        />
        <FileCard
          filename="auth.py"
          description="bcrypt password hashing, JWT create/verify, зависимости get_current_user и get_current_admin"
        />
        <FileCard
          filename="services/__init__.py"
          description="SQL sandbox: временная SQLite БД, валидация запросов, сравнение результатов"
        />
        <FileCard
          filename="routers/websocket.py"
          description="ConnectionManager, broadcast каждые 5 сек, отправка обновлений при submit"
        />
        <FileCard
          filename="schemas.py"
          description="Все Pydantic модели: запросы, ответы, вложенные структуры"
        />
      </div>
    </div>
  )
}

function SetupTab({ copiedIndex, copyToClipboard }: { copiedIndex: number | null; copyToClipboard: (text: string, index: number) => void }) {
  const steps = [
    {
      title: '1. Клонировать и перейти в директорию',
      code: `git clone https://github.com/your-username/sql-battle-backend.git
cd sql-battle-backend`,
    },
    {
      title: '2. Создать виртуальное окружение',
      code: `python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\\Scripts\\activate   # Windows`,
    },
    {
      title: '3. Установить зависимости',
      code: 'pip install -r requirements.txt',
    },
    {
      title: '4. Настроить окружение',
      code: `cp .env.example .env
# Отредактировать .env при необходимости`,
    },
    {
      title: '5. Заполнить базу тестовыми данными',
      code: 'python seed.py',
    },
    {
      title: '6. Запустить сервер',
      code: 'uvicorn main:app --reload --host 0.0.0.0 --port 8000',
    },
    {
      title: '7. Проверить',
      code: `# Открыть http://localhost:8000/docs
# Swagger UI с полным API

# Тестовый admin: admin / admin123
# 3 задачи уже в базе`,
    },
  ]

  return (
    <div className="space-y-8">
      <h2 className="text-2xl font-bold text-white">Инструкция по запуску</h2>

      <div className="space-y-4">
        {steps.map((step, i) => (
          <div key={i} className="rounded-xl bg-gray-900 border border-gray-700 overflow-hidden">
            <div className="px-5 py-3 border-b border-gray-700 flex items-center justify-between">
              <h3 className="font-semibold text-white">{step.title}</h3>
              <button
                onClick={() => copyToClipboard(step.code, i + 100)}
                className="text-xs text-gray-400 hover:text-gray-200 px-2 py-1 rounded bg-gray-800 hover:bg-gray-700 transition"
              >
                {copiedIndex === i + 100 ? '✅ Скопировано' : '📋 Копировать'}
              </button>
            </div>
            <div className="p-4 bg-gray-950">
              <pre className="text-sm font-mono text-emerald-300 overflow-x-auto whitespace-pre-wrap">{step.code}</pre>
            </div>
          </div>
        ))}
      </div>

      {/* Switch to PostgreSQL */}
      <div className="rounded-xl bg-gray-900 border border-gray-700 p-6">
        <h3 className="text-lg font-bold text-white mb-3">🔄 Переключение на PostgreSQL</h3>
        <div className="space-y-3">
          <p className="text-gray-400 text-sm">Для продакшена рекомендуется PostgreSQL:</p>
          <div className="bg-gray-950 rounded-lg p-3">
            <pre className="text-sm font-mono text-emerald-300">{`# .env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/sql_battle

# Установить драйвер
pip install asyncpg`}</pre>
          </div>
        </div>
      </div>

      {/* Frontend connection */}
      <div className="rounded-xl bg-gray-900 border border-gray-700 p-6">
        <h3 className="text-lg font-bold text-white mb-3">🔗 Подключение фронтенда</h3>
        <div className="space-y-3">
          <p className="text-gray-400 text-sm">В фронтенде (Next.js) установить переменную окружения:</p>
          <div className="bg-gray-950 rounded-lg p-3">
            <pre className="text-sm font-mono text-emerald-300">{`# .env.local (в репозитории фронтенда)
NEXT_PUBLIC_API_URL=http://localhost:8000/api`}</pre>
          </div>
          <p className="text-gray-400 text-sm">И переключить режим моков:</p>
          <div className="bg-gray-950 rounded-lg p-3">
            <pre className="text-sm font-mono text-emerald-300">{`// lib/api.ts
const USE_MOCKS = false;  // Было: true`}</pre>
          </div>
        </div>
      </div>
    </div>
  )
}

// ============ Components ============

function TechBadge({ name, color }: { name: string; color: string }) {
  const colorClasses: Record<string, string> = {
    emerald: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    amber: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    cyan: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
    pink: 'bg-pink-500/10 text-pink-400 border-pink-500/20',
  }
  return (
    <span className={`px-3 py-1 text-sm rounded-full border ${colorClasses[color]}`}>
      {name}
    </span>
  )
}

function FeatureCard({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <div className="rounded-xl bg-gray-900 border border-gray-700 p-5 hover:border-gray-600 transition">
      <div className="text-2xl mb-2">{icon}</div>
      <h3 className="font-semibold text-white mb-1">{title}</h3>
      <p className="text-sm text-gray-400">{description}</p>
    </div>
  )
}

function StatCard({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-xl bg-gray-900 border border-gray-700 p-4 text-center">
      <div className="text-2xl font-bold text-emerald-400">{value}</div>
      <div className="text-sm text-gray-400">{label}</div>
    </div>
  )
}

function FileCard({ filename, description }: { filename: string; description: string }) {
  return (
    <div className="rounded-lg bg-gray-900 border border-gray-700 p-4">
      <code className="text-emerald-400 text-sm font-mono">{filename}</code>
      <p className="text-sm text-gray-400 mt-1">{description}</p>
    </div>
  )
}

export default App
