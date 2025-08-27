# 📦 AGENT CURSOR — Повний бриф на створення QuanticX

Коротко: чіткий технічний бриф для реалізації QuanticX — монорепо з Bot, WebApp, Backend, Admin та P0-модулями відповідно до ТЗ.

Мета
- Синхронізувати Bot ↔ WebApp ↔ Backend ↔ Admin як єдину екосистему.
- Забезпечити продуктивність (avg ≤ 500 ms, p95 ≤ 800 ms), безпеку (RBAC, audit, rate-limit), i18n ua/ru/en та аналітику.

Обсяг (Scope)
- Монорепо: /bot, /backend, /webapp, /admin, /common, /infra.
- P0-модулі: авторизація, баланс/VIP, магазин, Escrow, рефералька, базова казино, OSINT (мінімум), групові інструменти, AI routing (4 провайдера), WebSocket, базова адмінка з 21 вкладкою (інтерфейс та API).
- CI/CD, міграції, Docker, Swagger, README модулів, e2e тести.

Ключові результати (Deliverables)
- Структура монорепо з шаблонами/README для кожного модуля.
- Реалізовані API P0 (повний swagger).
- Telegram Bot (aiogram v3) з WebApp entry.
- WebApp + Admin (React + Vite + TS) з i18n.
- Backend (FastAPI, PostgreSQL, Redis, Celery/RQ) з RBAC, JWT, audit, rate-limit.
- Моніторинг: JSON-логи з trace_id, Prometheus/Grafana, Sentry інтеграції.
- Тести: unit + e2e, покриття ≥ 70%.
- Звіт: список змін, метрики продуктивності, тест-результати, скріни ключових потоків.

Пріоритети (P0)
- Коректна аутентифікація/профілі, баланс/VIP, оплати (top-up/withdraw), магазин, Escrow create/release/dispute, базовий казино play/history, OSINT query/report, AI routing, basic admin panels і WebSocket канали.
- Безпека: RBAC, rate-limit, audit-trails, базовий антифрод.

Нефункціональні вимоги
- Локалі: ua (дефолт) / ru / en (всі тексти через i18n).
- Продуктивність: avg ≤ 500 ms, p95 ≤ 800 ms.
- Логи та телеметрія, error-tracing.
- CI: lint, автотести, контейнерні збірки.
- Документація: README, архітектурна діаграма (mermaid), Swagger, Postman-колекція.

Критерії прийняття
- Усі P0 завдання реалізовані і покриті тестами.
- Метрики відповідають SLO.
- Повна i18n для P0-флоу.
- Наявний звіт з тестами, метриками та скрінами.

Додаткові вказівки
- Дотримуватися дизайн-гайду QuanticX (тема, кольори, типографіка).
- Адмінські приховані ключі/журнали доступні тільки для ролей admin/support/analyst.
- При реалізації CLI/скриптів використовувати середовище dev container (Ubuntu 24.04.2 LTS). Для відкриття сторінок у хості використовувати "$BROWSER" <url>.

Контакт/розміщення
- Перший коміт у /workspaces/QuantumX. Докладний roadmap та спринт-план у кореневому README.

(Цей бриф використовується як керівний документ — всі подальші модулі та таски повинні узгоджуватися з ним.)

Привіт 👋
Будь ласка, візьми це технічне завдання і створи повний проєкт QuanticX.
Це унікальна екосистема від SHADOW & COMPANY: Telegram Bot + WebApp 6.0+ + Backend з модулями (AI, OSINT, економіка/магазин, казино/ігри, знайомства, escrow «Гарант», інструменти для груп, CRM/аналітика) та потужною адмінкою.
Нижче — повний розгорнутий опис із усіма деталями. Орієнтуйся на нього як на єдине джерело правди.

⸻

0) Цілі проєкту
	•	🧩 Узгодити всі модулі в єдиній екосистемі: Bot ↔ WebApp ↔ Backend ↔ Admin.
	•	⚡️ Швидкодія: avg ≤ 500 мс, p95 ≤ 800 мс.
	•	🔐 Безпека: RBAC, audit, rate limit, fraud-контроль.
	•	💰 Монетизація: VIP, магазин, escrow-комісії, ігри, підписки, рефералка.
	•	🌍 Локалі: ua (дефолт) / ru / en (всі тексти через i18n).
	•	📈 Аналітика: події, retention, когортний аналіз.

⸻

1) Архітектура і стек

Монорепо:

/bot         (Telegram Bot; aiogram v3; WebApp entry)
/backend     (FastAPI, PostgreSQL, Redis, Celery/RQ, WebSocket)
/webapp      (React + Vite + TS, i18n, Bottom Nav, Theme Sync)
/admin       (React + Vite + TS; 21 вкладка керування)
/common      (DTO, валідатори, i18n-ключі, UI-kit)
/infra       (docker-compose, env, CI/CD, міграції)

Технології:
	•	Python 3.11+, FastAPI, SQLAlchemy, Alembic, Redis, Celery/RQ
	•	aiogram v3, Telegram WebApp API 6.0+
	•	React + Vite + TypeScript, Zustand/Redux, i18n
	•	Auth: JWT (access/refresh), RBAC (user/vip/moderator/support/analyst/admin)
	•	Логи: JSON з trace_id, Prometheus+Grafana, Sentry
	•	CI/CD: Docker, lint, авто-тести, деплой

⸻

2) Ролі і права (RBAC)
	•	user — базові можливості
	•	vip — розширені ліміти, знижки, пріоритети
	•	moderator — модерація чатів і відгуків
	•	support — підтримка, escrow disputes
	•	analyst — доступ до логів/аналітики
	•	admin — повний контроль, emergency-дії

⸻

3) 21 вкладка Admin Panel
	1.	Dashboard — KPIs (DAU/MAU, ARPPU, LTV, конверсії, інциденти)
	2.	User Management — пошук, блок/розблок, VIP, баланси, історії
	3.	Module Control — запуск/рестарт модулів, health-check
	4.	AI Services — GPT-4, Claude, Gemini, Groq (ключі, маршрутизація, ліміти)
	5.	Economy System — Shadow Talks валюта, кешбек, VIP-перки
	6.	OSINT Tools — джерела, тарифи, журнали доступів
	7.	Dating Engine — анкети, матчінг, модерація
	8.	Guarantor (Escrow) — угоди, спори, арбітраж
	9.	Casino Games — каталог, RTP, ліміти, історія
	10.	Shop Integration — каталог, кошик, знижки, промо
	11.	Telegram Bot — меню, deep links, WebApp
	12.	WebSocket Server — канали, статуси
	13.	Security System — fraud-аналіз, алерти
	14.	Real-time Monitoring — черги, latency, помилки
	15.	Optimization Engine — кеш, prefetch, warm-up
	16.	Integrations — CRM, PSP, зовнішні API
	17.	Configuration — feature flags, env
	18.	System Monitoring — CPU/RAM/Disk, uptime
	19.	Logs Management — пошук, trace_id, експорт
	20.	Analytics — retention, воронки, когортний аналіз
	21.	Emergency Controls — Shutdown, Lockdown, Tx Freeze, Optimization

⸻

4) Модулі (16 штук, розгорнуто)

4.1 Лобі / Навігація
	•	Public: головне меню, CTA, швидкі дії (Top-up, VIP, Shop, Games, OSINT, Escrow)
	•	Internal: приховані CTA для адмінів (логи, advanced OSINT, Hermes)

4.2 Авторизація / Профіль
	•	Public: профіль (id, нік, VIP, баланс, історія дій)
	•	Internal: логувати IP/UA, країну входу, ризик-скор (видно тільки в адмінці)

4.3 Баланс / VIP
	•	Public: гаманець, поповнення/вивід, VIP-плани, кешбек, знижки
	•	Internal: “admin-VIP” рівень, прихований режим freeze транзакцій

4.4 Магазин
	•	Каталог, кошик, оплата, політика повернень
	•	P1: разом купують, P2: відгуки

4.5 Реферальна система
	•	Public: реф-посилання, % винагороди
	•	Internal: антифрод на країну/IP/девайс

4.6 Казино
	•	Public: RTP, демо, історія, proof-of-fairness
	•	Internal: повні журнали ігор з метаданими, VIP-бонуси

4.7 OSINT-система
	•	Public: уніфікований інтерфейс, шаблони (email, username, домен, номер), логи доступів, кеш, PDF/CSV експорт
	•	Internal: підключення до “сірих” баз, витоки, IP, телефони, акаунти. Логи тримати приховано; доступ тільки для адмінів

4.8 Escrow («Гарант»)
	•	Створення угод, депонування, реліз, спори
	•	Internal: приховані журнали, арбітражні інструменти для адмінів

4.9 Інструменти для груп (Hermes)
	•	Public: антиспам, антирейд, аналіз нового учасника (мінімум даних)
	•	Internal: Hermes IDS: ризик-скор сесії (гео, час, патерни), приховані сигнали

4.10 Глобальний чат
	•	Рівні, репутація, модерація, інтеграція з економікою

4.11 AI-асистенти
	•	Public: 4 провайдера, fallback
	•	Internal: “психолог”, “аналітик”, custom моделі

4.12 Dating Engine
	•	Анкети, матчінг, модерація контенту

4.13 Крипто-утиліти
	•	Public: довідники, курси
	•	Internal: інтеграція з PSP (KYC/AML)

4.14 Аналітика / Логи / Сповіщення
	•	Public: події, email/push
	•	Internal: внутрішні фрод-сигнали, алерти

4.15 Адмінка (UI)
	•	Таблиці, фільтри, масові дії

4.16 Локалізація / Тексти
	•	Public: i18n ua/ru/en
	•	Internal: приховані ключі для адмін-функцій

⸻

5) API (≈50+ endpointів)
	•	Auth: /api/auth/login, /api/auth/refresh, /api/profile
	•	Wallet: /api/wallet/topup, /api/wallet/withdraw, /api/vip/purchase
	•	Shop: /api/shop/catalog, /api/shop/cart, /api/shop/checkout
	•	Referral: /api/referral/link, /api/referral/stats
	•	Games: /api/games/list, /api/games/play, /api/games/history
	•	OSINT: /api/osint/query, /api/osint/report/:id
	•	Escrow: /api/escrow/create, /api/escrow/release, /api/escrow/dispute
	•	Groups: /api/groups/onboard, /api/groups/rules
	•	AI: /api/ai/route, /api/ai/session/:id
	•	Admin: /api/admin/stats, /api/admin/users, /api/admin/security/lockdown, /api/admin/emergency-shutdown

⸻

6) Acceptance
	•	Усі P0 реалізовані, критичних багів немає
	•	avg ≤ 500 мс, p95 ≤ 800 мс
	•	i18n ua/ru/en повний набір
	•	Події аналітики доступні у дашборді
	•	e2e тести проходять:
	•	“Topup → Buy VIP → Discount in Shop”
	•	“Create Escrow → Release/Dispute”

⸻

7) План спринтів
	•	Sprint 1: Лобі, Профіль, Баланс/VIP, Магазин, Аналітика, i18n
	•	Sprint 2: Рефералка, Escrow, Казино, Групи, Admin мінімум
	•	Sprint 3: OSINT, промо, лідерборди, глобальний чат, експорт звітів

⸻

8) Документація
	•	README на кожен модуль
	•	Архітектурна діаграма (mermaid)
	•	Swagger для /api/*
	•	Postman-колекція

⸻

19) Дизайн-гайд QuanticX

	•	Загальний стиль: сучасний, технологічний, не дитячий. Атмосфера "кіберпанк + корпоратив". Строгість + динаміка.
	•	Темна тема за замовчуванням + неонові акценти (фіолетовий → рожевий → синій).
	•	Палітра кольорів:
		- #FF1CC0 (яскравий акцент, неон-рожевий)
		- #B131FA (фіолетовий акцент)
		- #4A0074 (темний фіолетовий фон)
		- #1C3AFF (електро-синій акцент)
		- #0E0E10 (базовий чорний фон)
	•	Типографіка: строгий, читабельний sans-serif (Poppins, Inter, системні шрифти).
	•	UI патерни:
		- Темний фон + яскраві неонові лінії/блискавки.
		- Кнопки з глайсами (градієнтами), ефекти наведення.
		- Картки з неонними рамками.
		- Спливаючі тости для нотифікацій.
	•	Анімації: легкі, технологічні (не мультяшні). Ефекти блискавки, сяйва, плавних градієнтів.
	•	Іконки/графіка: 3D-сфери, глайси, неонові патерни, без дитячих ілюстрацій.
	•	Лендінг / WebApp / Admin:
		- Лендінг — динамічні блоки з неоном, блискавками, градієнтними текстами.
		- WebApp — мінімалістична нижня навігація, великі CTA-кнопки.
		- Admin — строгі таблиці/графіки, але теж з акцентними кольорами для станів (успіх/ризик/критика).

⸻

🔚 Фінальна задача для агента:

Створи проєкт QuanticX за цим ТЗ. Реалізуй Telegram Bot + WebApp + Backend з P0-модулями, 21 вкладкою адмінки, AI (4 провайдера), економікою (Shadow Talks + VIP + Shop), казино, OSINT, escrow, рефералкою, груповими інструментами (Hermes), аналітикою подій, i18n (ua/ru/en), RBAC, audit, rate-limit, WebSocket. Забезпеч avg ≤ 500 мс, p95 ≤ 800 мс, покриття тестами ≥70%. Надати звіт: список змін, метрики, тести, скріни ключових потоків.
