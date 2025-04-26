### Gennadiy Kharatyan (Геннадий Харатьян)

Тестовое задание для Frontend-разработчика

[Visit Demo Site](https://bogoda-tz.vercel.app/)

### Примечание к проекту на тему оптимизации:

Так как Demo версия опубликована в vercel хосте , а не на собственном сервере , где проект можно засунуть в докер контейнер , то передеча json данных через next js api зависит от внешних факторов (интернет , скорость серверов Vercel и тд. )

в Vercel получения json приходят со скоростью 210-220 мс

в localhost (внутри контейнера) же все работает гораздо быстрее (7-10 мс)


## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

The `pages/api` directory is mapped to `/api/*`. Files in this directory are treated as [API routes](https://nextjs.org/docs/api-routes/introduction) instead of React pages.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.
