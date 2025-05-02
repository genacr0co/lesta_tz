/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        NEXT_PUBLIC_DOMAIN: process.env.NEXT_PUBLIC_DOMAIN,
      },
      
    reactStrictMode: true,
    output: 'standalone',
    compiler: {
        styledComponents: true,
    },
    i18n: {
        locales: ['ru', 'en'],
        defaultLocale: 'ru',
        localeDetection: false,
    },
}

module.exports = nextConfig
